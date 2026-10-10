from facit.bike_rental import (
    calculate_price,
    can_rent_bike,
    is_valid_rental_hours,
    rent_bike,
    return_bike,
)


def make_bike():
    return {"id": 101, "is_available": True}


def test_calculate_price_for_two_hours():
    result = calculate_price(2, 50)
    assert result == 100


def test_two_hours_are_valid():
    result = is_valid_rental_hours(2)
    assert result is True


def test_zero_hours_are_invalid():
    result = is_valid_rental_hours(0)
    assert result is False


def test_negative_hours_are_invalid():
    result = is_valid_rental_hours(-1)
    assert result is False


def test_twenty_four_hours_are_valid():
    result = is_valid_rental_hours(24)
    assert result is True


def test_twenty_five_hours_are_invalid():
    result = is_valid_rental_hours(25)
    assert result is False


def test_available_bike_can_be_rented():
    bike = make_bike()
    assert can_rent_bike(bike) is True


def test_unavailable_bike_cannot_be_rented():
    bike = make_bike()
    bike["is_available"] = False
    assert can_rent_bike(bike) is False


def test_successful_rental_changes_state():
    bike = make_bike()
    result = rent_bike(bike, 2)
    assert result is True
    assert bike["is_available"] is False


def test_zero_hour_rental_is_rejected_without_state_change():
    bike = make_bike()
    result = rent_bike(bike, 0)
    assert result is False
    assert bike["is_available"] is True


def test_rental_over_limit_is_rejected_without_state_change():
    bike = make_bike()
    result = rent_bike(bike, 25)
    assert result is False
    assert bike["is_available"] is True


def test_unavailable_bike_stays_unavailable_after_rejected_rental():
    bike = make_bike()
    bike["is_available"] = False
    result = rent_bike(bike, 2)
    assert result is False
    assert bike["is_available"] is False


def test_rented_bike_can_be_returned():
    bike = make_bike()
    bike["is_available"] = False
    result = return_bike(bike)
    assert result is True
    assert bike["is_available"] is True


def test_available_bike_cannot_be_returned_again():
    bike = make_bike()
    result = return_bike(bike)
    assert result is False
    assert bike["is_available"] is True


def test_price_is_not_calculated_for_zero_hours():
    result = calculate_price(0, 50)
    assert result is None


def test_price_is_not_calculated_over_limit():
    result = calculate_price(25, 50)
    assert result is None
