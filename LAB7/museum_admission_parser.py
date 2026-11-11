import datetime


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    Safely handles None, empty strings, single names, and whitespace.
    """
    if not name or not isinstance(name, str):
        return ""
    parts = name.split()
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0].title()
    return parts[-1].title() + ', ' + ' '.join(parts[:-1]).title()


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of ints.
    Safely handles None, empty strings, non-numeric tokens, and invalid values.
    """
    if not text or not isinstance(text, str):
        return []
    ages = []
    for token in text.split():
        try:
            age = int(token)
            if age >= 0:
                ages.append(age)
        except (ValueError, TypeError):
            continue
    return ages


def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Safely handles None, empty strings, malformed formats, and invalid calendar dates.
    """
    if not text or not isinstance(text, str):
        return None
    parts = text.strip().split('-')
    if len(parts) != 3:
        return None
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        # Validate actual calendar date within valid date range
        datetime.date(year, month, day)
        return (year, month, day)
    except (ValueError, TypeError, OverflowError):
        return None


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))


if __name__ == "__main__":
    main()
