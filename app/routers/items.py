from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_api_key


router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=schemas.ItemOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
def create_item_endpoint(item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_item(db, item_in)
    except Exception as e:
    # assume uniqueness conflict
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[schemas.ItemOut])
def list_items(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), title: str | None = None, db: Session = Depends(get_db)):
    return crud.get_items(db, limit=limit, offset=offset, title=title)


@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.ItemOut, dependencies=[Depends(get_api_key)])
def update_item(item_id: int, updates: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db, item, updates)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return


@router.get("/meta/average_price")
def average_price(db: Session = Depends(get_db)):
    return {"average_price": crud.get_average_price(db)}