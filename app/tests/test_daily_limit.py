from app.utils.daily_limit import check_limit_order
from datetime import datetime

def test_check_limit_order_pass():
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    check_limit_order([today, today], 5) 

def test_check_limit_order_exceed():
    from fastapi import HTTPException
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        check_limit_order([today]*10, 5)
        assert False, "Harusnya kena limit"
    except HTTPException as e:
        assert e.status_code == 429
