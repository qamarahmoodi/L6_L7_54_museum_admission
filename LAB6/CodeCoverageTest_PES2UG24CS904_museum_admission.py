import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ==========================================
# Tests for ticket_price
# ==========================================

def test_ticket_price_invalid_category():
    """Verify that an unknown category raises a ValueError."""
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("foreigner", 25, "monday", False)


def test_ticket_price_negative_age():
    """Verify that a negative age raises a ValueError."""
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "monday", False)


def test_ticket_price_free_admission_under_five():
    """Verify that children under 5 get free admission (0 price)."""
    assert ticket_price("child", 4, "monday", False) == 0
    assert ticket_price("child", 0, "saturday", True) == 0


def test_ticket_price_monday_discount():
    """Verify that Monday offers 50% discount on base price (integer floor division)."""
    # Adult base price = 300; monday = 150
    assert ticket_price("adult", 30, "monday", False) == 150
    # Senior base price = 200; monday = 100
    assert ticket_price("senior", 65, "monday", False) == 100


def test_ticket_price_weekend_surcharge():
    """Verify that Saturday and Sunday include a 50 surcharge."""
    # Child base price = 100; saturday = 150
    assert ticket_price("child", 10, "saturday", False) == 150
    # Adult base price = 300; sunday = 350
    assert ticket_price("adult", 35, "sunday", False) == 350


def test_ticket_price_regular_weekday_no_tour():
    """Verify normal weekday pricing without tour."""
    # Student base price = 150
    assert ticket_price("student", 20, "wednesday", False) == 150


def test_ticket_price_guided_tour_student():
    """Verify student guided tour adds 50."""
    # Student base price = 150; weekday + tour (+50) = 200
    assert ticket_price("student", 21, "thursday", True) == 200


def test_ticket_price_guided_tour_non_student():
    """Verify non-student guided tour adds 100."""
    # Adult base price = 300; weekday + tour (+100) = 400
    assert ticket_price("adult", 40, "friday", True) == 400
    # Weekend + non-student tour: 300 + 50 + 100 = 450
    assert ticket_price("adult", 40, "saturday", True) == 450


# ==========================================
# Tests for group_discount
# ==========================================

def test_group_discount_invalid_size():
    """Verify that group size less than 1 raises a ValueError."""
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-5, True)


def test_group_discount_school_large():
    """Verify school group of 20 or more gets 40% discount."""
    assert group_discount(20, True) == 40
    assert group_discount(30, True) == 40


def test_group_discount_school_small():
    """Verify school group under 20 gets 25% discount."""
    assert group_discount(19, True) == 25
    assert group_discount(5, True) == 25


def test_group_discount_general_tier_15_plus():
    """Verify general group of 15 or more gets 20% discount."""
    assert group_discount(15, False) == 20
    assert group_discount(18, False) == 20


def test_group_discount_general_tier_8_to_14():
    """Verify general group of 8 to 14 gets 10% discount."""
    assert group_discount(8, False) == 10
    assert group_discount(14, False) == 10


def test_group_discount_general_tier_under_8():
    """Verify general group of under 8 gets 0% discount."""
    assert group_discount(7, False) == 0
    assert group_discount(1, False) == 0


# ==========================================
# Tests for gallery_entry
# ==========================================

def test_gallery_entry_capacity_reached():
    """Verify 'wait' is returned when gallery is at or over capacity."""
    assert gallery_entry(100, 100, False) == "wait"
    assert gallery_entry(105, 100, True) == "wait"


def test_gallery_entry_queue_near_capacity_no_slot():
    """Verify 'queue' is returned when gallery is at least 90% full without timed slot."""
    # 90 visitors in 100 capacity: 90 * 10 >= 100 * 9 (900 >= 900)
    assert gallery_entry(90, 100, False) == "queue"
    assert gallery_entry(95, 100, False) == "queue"


def test_gallery_entry_enter():
    """Verify 'enter' is returned when below 90% capacity or when holding timed slot."""
    # Near capacity but has timed slot -> enter
    assert gallery_entry(90, 100, True) == "enter"
    # Below 90% capacity without timed slot -> enter
    assert gallery_entry(89, 100, False) == "enter"
    # Low occupancy -> enter
    assert gallery_entry(20, 100, False) == "enter"
