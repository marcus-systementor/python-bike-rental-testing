from bike_rental import (
    calculate_price,
    can_rent_bike,
    is_valid_rental_hours,
    rent_bike,
    return_bike,
)


def test_calculate_price_for_two_hours():
    # Arrange
    hours = 2
    hourly_rate = 50

    # Act
    result = calculate_price(hours, hourly_rate)

    # Assert
    assert result == 100


# Add your own test_ functions below. Start with one rule at a time.
