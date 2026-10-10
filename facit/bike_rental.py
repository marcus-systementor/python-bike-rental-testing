"""One simple version with all rental rules in place."""


def is_valid_rental_hours(hours):
    return 0 < hours <= 24


def can_rent_bike(bike):
    return bike["is_available"]


def rent_bike(bike, hours):
    if not is_valid_rental_hours(hours) or not can_rent_bike(bike):
        return False

    bike["is_available"] = False
    return True


def return_bike(bike):
    if bike["is_available"]:
        return False

    bike["is_available"] = True
    return True


def calculate_price(hours, hourly_rate):
    if not is_valid_rental_hours(hours):
        return None

    return hours * hourly_rate
