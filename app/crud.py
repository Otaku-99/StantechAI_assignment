from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from app.logger import logger  # ✅ keep your logger

# -----------------------------
# Business logic example
# -----------------------------
def price_with_tax(price: float, tax_pct: float = 0.18) -> float:
    """Return price after applying tax percentage."""
    final_price = round(price * (1 + tax_pct), 2)
    logger.debug(f"Calculated price with tax: base={price}, tax_pct={tax_pct}, result={final_price}")
    return final_price


# -----------------------------
# CRUD: Create
# -----------------------------
def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    logger.info(f"Attempting to create item: {item_in.title}")
    db_item = models.Item(**item_in.model_dump())
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        logger.info(f"✅ Item created successfully with ID={db_item.id}")
        return db_item
    except IntegrityError as e:
        db.rollback()
        logger.error(f"❌ Failed to create item (IntegrityError): {e}")
        raise HTTPException(status_code=400, detail=f"Item creation failed: {str(e)}")


# -----------------------------
# CRUD: Read list (with pagination)
# -----------------------------
def get_items(db: Session, limit: int = 10, offset: int = 0, title: str | None = None):
    logger.info(f"Fetching items: limit={limit}, offset={offset}, title_filter={title}")
    q = db.query(models.Item)
    if title:
        q = q.filter(models.Item.title.ilike(f"%{title}%"))
    items = q.order_by(models.Item.id).offset(offset).limit(limit).all()
    logger.debug(f"Fetched {len(items)} items")
    return items


# -----------------------------
# CRUD: Read single
# -----------------------------
def get_item(db: Session, item_id: int):
    logger.info(f"Fetching single item with ID={item_id}")
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        logger.warning(f"Item with ID={item_id} not found")
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    logger.debug(f"Item found: {item.title}")
    return item


# -----------------------------
# CRUD: Update
# -----------------------------
def update_item(db: Session, item_id: int, updates: schemas.ItemUpdate):
    logger.info(f"Updating item ID={item_id}")
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        logger.warning(f"Item with ID={item_id} not found")
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(item, field, value)
        logger.debug(f" - Field updated: {field} = {value}")
    
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        logger.info(f"✅ Item ID={item.id} updated successfully")
        return item
    except IntegrityError as e:
        db.rollback()
        logger.error(f"❌ Failed to update item (IntegrityError): {e}")
        raise HTTPException(status_code=400, detail=f"Item update failed: {str(e)}")


# -----------------------------
# CRUD: Delete
# -----------------------------
def delete_item(db: Session, item_id: int):
    logger.warning(f"Deleting item ID={item_id}")
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        logger.warning(f"Item with ID={item_id} not found")
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    
    db.delete(item)
    db.commit()
    logger.info(f"✅ Item ID={item_id} deleted")
    return {"detail": f"Item ID {item_id} deleted successfully"}


# -----------------------------
# Custom SQL: Average price
# -----------------------------
def get_average_price(db: Session) -> float:
    logger.info("Calculating average price of items")
    res = db.execute(text("SELECT AVG(price) as avg_price FROM items"))
    row = res.fetchone()
    avg = float(row[0]) if row and row[0] is not None else 0.0
    logger.debug(f"Average price calculated: {avg}")
    return avg


# -----------------------------
# Transaction example
# -----------------------------
def create_item_with_update(
    db: Session,
    item_in: schemas.ItemCreate,
    new_title_for_existing_id: tuple[int, str] | None = None,
):
    """
    Creates a new item and optionally updates another item's title in the same transaction.
    Rolls back on any failure.
    """
    logger.info(f"Starting transaction to create item '{item_in.title}'")
    try:
        new_item = models.Item(**item_in.model_dump())
        db.add(new_item)
        db.flush()  # assign ID

        if new_title_for_existing_id:
            existing_id, new_title = new_title_for_existing_id
            logger.info(f"Updating title of existing item ID={existing_id} -> '{new_title}'")
            existing = db.query(models.Item).filter(models.Item.id == existing_id).first()
            if not existing:
                logger.error(f"❌ Transaction failed: Item ID={existing_id} not found")
                raise HTTPException(status_code=404, detail=f"Existing item ID {existing_id} not found for update")
            existing.title = new_title
            db.add(existing)

        db.commit()
        db.refresh(new_item)
        logger.info(f"✅ Transaction committed successfully, new item ID={new_item.id}")
        return new_item
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Transaction rolled back due to error: {e}")
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")
