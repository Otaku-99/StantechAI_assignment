from app.crud import price_with_tax

def test_price_with_tax():
    assert price_with_tax(100, 0.1) == 110.0
    assert price_with_tax(0, 0.18) == 0.0
