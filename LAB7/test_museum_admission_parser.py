from hypothesis import given, strategies as st
from museum_admission_parser import format_visitor_name, parse_group_ages, parse_visit_date

@given(st.text() | st.none())
def test_format_visitor_name_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_group_ages_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_visit_date_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass
