"""A small bike rental system with rules still to improve."""


def is_valid_rental_hours(hours):
    return hours >= 0


def can_rent_bike(bike):
    return True


def rent_bike(bike, hours):
    if not can_rent_bike(bike):
        return False

    bike["is_available"] = False
    return True


def return_bike(bike):
    bike["is_available"] = True
    return True


def calculate_price(hours, hourly_rate):
    return hours * hourly_rate
