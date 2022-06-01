from decimal import Decimal, getcontext, ROUND_HALF_UP

from django.conf import settings


def get_dynamic_precision(value: Decimal) -> int:
    engineering_representation = value.to_eng_string()
    try:
        integer_digits, _ = engineering_representation.split(".")
    except ValueError:
        integer_digits = engineering_representation
    return len(integer_digits) + 2


def rounding_up_to_multiplicity(value: Decimal) -> Decimal:
    getcontext().prec = get_dynamic_precision(value)
    pre_rounded_value = value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    ratio = settings.MULTIPLICITY_OF_PRICE_ROUNDING
    if ratio == 1:
        return value
    fraction = pre_rounded_value % 1 * 100
    remainder_of_division = fraction % ratio
    if remainder_of_division >= ratio / 2:
        return Decimal((fraction // ratio * ratio + ratio)) / 100 + Decimal(int(pre_rounded_value))
    else:
        return Decimal(fraction // ratio * ratio / 100) + Decimal(int(pre_rounded_value))
