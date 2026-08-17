def calculate_trend(values, higher_is_better=True):
    """
    Determine whether a water-quality parameter
    is improving, stable, or worsening.

    values must be ordered from oldest to newest.
    """

    if len(values) < 2:
        return {
            "trend": "INSUFFICIENT_DATA",
            "change": 0
        }

    first_value = values[0]
    last_value = values[-1]

    change = last_value - first_value

    # Treat very small changes as stable
    tolerance = max(
        abs(first_value) * 0.05,
        0.01
    )

    if abs(change) <= tolerance:
        trend = "STABLE"

    elif higher_is_better:

        if change > 0:
            trend = "IMPROVING"
        else:
            trend = "WORSENING"

    else:

        if change < 0:
            trend = "IMPROVING"
        else:
            trend = "WORSENING"

    return {
        "trend": trend,
        "change": round(change, 3)
    }

def calculate_range_trend(
    values,
    target_min,
    target_max
):
    """
    Determine whether values are moving toward
    or away from a preferred target range.
    """

    if len(values) < 2:
        return {
            "trend": "INSUFFICIENT_DATA",
            "change": 0
        }

    first_value = values[0]
    last_value = values[-1]

    def distance_from_target(value):

        if value < target_min:
            return target_min - value

        if value > target_max:
            return value - target_max

        return 0

    first_distance = distance_from_target(
        first_value
    )

    last_distance = distance_from_target(
        last_value
    )

    distance_change = (
        last_distance - first_distance
    )

    actual_change = (
        last_value - first_value
    )

    tolerance = 0.01

    if (
        first_distance == 0
        and last_distance == 0
    ):
        trend = "STABLE"

    elif abs(distance_change) <= tolerance:
        trend = "STABLE"

    elif last_distance < first_distance:
        trend = "IMPROVING"

    else:
        trend = "WORSENING"

    return {
        "trend": trend,
        "change": round(
            actual_change,
            3
        )
    }


def analyze_pond_trends(readings):
    """
    Analyze historical pond readings.

    readings must be ordered from oldest
    to newest.
    """

    if len(readings) < 2:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": (
                "At least two pond readings are "
                "required for trend analysis."
            ),
            "trends": {}
        }

    dissolved_oxygen = [
        reading.dissolved_oxygen_mg_l
        for reading in readings
    ]

    ammonia = [
        reading.ammonia_mg_l
        for reading in readings
    ]

    temperature = [
        reading.temperature_c
        for reading in readings
    ]

    salinity = [
        reading.salinity_ppt
        for reading in readings
    ]

    ph_values = [
        reading.ph
        for reading in readings
    ]

    trends = {
        "dissolved_oxygen": calculate_trend(
            dissolved_oxygen,
            higher_is_better=True
        ),

        "ammonia": calculate_trend(
            ammonia,
            higher_is_better=False
        ),

        "temperature": calculate_range_trend(
            temperature,
            target_min=26,
            target_max=32
            ),

        "salinity": calculate_range_trend(
            salinity,
            target_min=8,
            target_max=28
        ),

        "ph": calculate_range_trend(
            ph_values,
            target_min=7.0,
            target_max=8.6
        )
    }

    return {
        "status": "OK",
        "readings_analyzed": len(readings),
        "trends": trends
    }