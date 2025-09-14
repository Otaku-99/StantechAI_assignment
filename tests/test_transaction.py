import pytest
from app import crud, schemas, models

API_KEY = "StantechAI"

def test_transaction_commit(client, db_override_session):
    """Test that create_item_with_update commits both operations"""
    # Create a first item normally
    item1 = crud.create_item(
        db_override_session,
        schemas.ItemCreate(title="Original", description="desc1", price=5.0),
    )

    # Create new item + update existing item in one transaction
    new_item_in = schemas.ItemCreate(title="Transaction Item", description="desc2", price=12.5)
    new_item = crud.create_item_with_update(
        db_override_session,
        new_item_in,
        new_title_for_existing_id=(item1.id, "Updated Title")
    )

    # Verify new item exists
    fetched = crud.get_item(db_override_session, new_item.id)
    assert fetched is not None
    assert fetched.title == "Transaction Item"

    # Verify existing item was updated
    updated = crud.get_item(db_override_session, item1.id)
    assert updated.title == "Updated Title"


def test_transaction_rollback(client, db_override_session):
    """Test that transaction rolls back on error"""
    # Create an item normally
    item1 = crud.create_item(
        db_override_session,
        schemas.ItemCreate(title="Rollback Item", description="desc", price=8.0),
    )

    # Attempt transaction with invalid update target (non-existent item id)
    bad_item_in = schemas.ItemCreate(title="Should Fail", description="desc", price=15.0)
    with pytest.raises(ValueError):  # our crud raises ValueError
        crud.create_item_with_update(
            db_override_session,
            bad_item_in,
            new_title_for_existing_id=(9999, "Does Not Exist")  # invalid id
        )

    # Verify nothing was committed: "Should Fail" should not exist
    items = crud.get_items(db_override_session, limit=100)
    titles = [i.title for i in items]
    assert "Should Fail" not in titles
