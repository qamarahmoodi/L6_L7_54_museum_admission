import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ============================================================================
# Branch Coverage Tests for ticket_price
# ============================================================================

def test_ticket_price_invalid_category_branch():
    """Branch: category not in BASE_PRICE (True)."""
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("vip_member", 30, "tuesday", False)


def test_ticket_price_negative_age_branch():
    """Branch: age < 0 (True)."""
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "wednesday", False)


def test_ticket_price_under_five_free_branch():
    """Branch: age < 5 (True and False boundary)."""
    # Age < 5: True -> returns 0
    assert ticket_price("child", 4, "friday", False) == 0
    assert ticket_price("child", 0, "sunday", True) == 0
    # Age < 5: False (boundary age 5) -> enters pricing logic
    assert ticket_price("child", 5, "wednesday", False) == 100


def test_ticket_price_day_branches():
    """Branches for day: monday (True/False), saturday/sunday (True/False)."""
    # day == "monday" (True)
    # Adult base: 300 // 2 = 150
    assert ticket_price("adult", 30, "monday", False) == 150

    # day == "monday" (False), day in ("saturday", "sunday") (True: saturday)
    # Senior base: 200 + 50 = 250
    assert ticket_price("senior", 65, "saturday", False) == 250

    # day in ("saturday", "sunday") (True: sunday)
    # Child base: 100 + 50 = 150
    assert ticket_price("child", 10, "sunday", False) == 150

    # day in ("saturday", "sunday") (False: regular weekday)
    # Senior base: 200
    assert ticket_price("senior", 70, "thursday", False) == 200


def test_ticket_price_guided_tour_branches():
    """Branches for with_guided_tour (True/False) and category == 'student' (True/False)."""
    # with_guided_tour == False -> skips tour charge
    assert ticket_price("adult", 25, "tuesday", False) == 300

    # with_guided_tour == True, category == "student" (True) -> +50
    # Student base: 150 + 50 = 200
    assert ticket_price("student", 20, "tuesday", True) == 200

    # with_guided_tour == True, category == "student" (False: adult) -> +100
    # Adult base: 300 + 100 = 400
    assert ticket_price("adult", 25, "tuesday", True) == 400

    # with_guided_tour == True, category == "student" on Monday:
    # Student base: (150 // 2) + 50 = 75 + 50 = 125
    assert ticket_price("student", 19, "monday", True) == 125


# ============================================================================
# Branch Coverage Tests for group_discount
# ============================================================================

def test_group_discount_invalid_size_branch():
    """Branch: group_size < 1 (True and False)."""
    # True
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-10, True)


def test_group_discount_school_branches():
    """Branches: is_school (True), group_size >= 20 (True and False)."""
    # group_size >= 20 (True, boundary 20 and above)
    assert group_discount(20, True) == 40
    assert group_discount(35, True) == 40

    # group_size >= 20 (False, boundary 19 and below)
    assert group_discount(19, True) == 25
    assert group_discount(1, True) == 25


def test_group_discount_general_group_branches():
    """Branches: is_school (False), group_size >= 15, >= 8, and < 8."""
    # group_size >= 15 (True, boundary 15 and above)
    assert group_discount(15, False) == 20
    assert group_discount(16, False) == 20

    # group_size >= 15 (False) and group_size >= 8 (True, boundary 8 and 14)
    assert group_discount(14, False) == 10
    assert group_discount(8, False) == 10

    # group_size >= 8 (False, boundary 7 and 1)
    assert group_discount(7, False) == 0
    assert group_discount(1, False) == 0


# ============================================================================
# Branch Coverage Tests for gallery_entry
# ============================================================================

def test_gallery_entry_capacity_reached_branch():
    """Branch: visitors_inside >= capacity (True and False)."""
    # True: at capacity (boundary 100/100)
    assert gallery_entry(100, 100, False) == "wait"
    # True: over capacity (105/100)
    assert gallery_entry(105, 100, True) == "wait"


def test_gallery_entry_queue_branch():
    """Branch: visitors_inside * 10 >= capacity * 9 and not has_timed_slot (Both True)."""
    # 90% full without timed slot (900 >= 900 and not False) -> queue
    assert gallery_entry(90, 100, False) == "queue"
    # 95% full without timed slot -> queue
    assert gallery_entry(95, 100, False) == "queue"


def test_gallery_entry_enter_branches():
    """
    Branches leading to 'enter':
    1. visitors_inside * 10 >= capacity * 9 is True, BUT has_timed_slot is True (short-circuits branch)
    2. visitors_inside * 10 >= capacity * 9 is False (below 90% capacity)
    """
    # Condition: ratio >= 0.9 True, but not has_timed_slot is False (has timed slot) -> enter
    assert gallery_entry(90, 100, True) == "enter"
    assert gallery_entry(99, 100, True) == "enter"

    # Condition: ratio < 0.9 (boundary 89/100), without timed slot -> enter
    assert gallery_entry(89, 100, False) == "enter"

    # Low capacity with timed slot -> enter
    assert gallery_entry(10, 100, True) == "enter"
