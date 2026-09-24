import numpy as np


def forecast_parameter(
    readings,
    parameter: str,
    hours_ahead: int = 6,
):
    if len(readings) < 3:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "At least 3 readings are required for forecasting.",
        }

    # Oldest → newest
    readings = sorted(
        readings,
        key=lambda r: r.recorded_at,
    )

    # Use latest 10 readings
    readings = readings[-10:]

    values = [
        getattr(reading, parameter)
        for reading in readings
    ]

    # Convert timestamps into hours
    times = [
        (
            reading.recorded_at
            - readings[0].recorded_at
        ).total_seconds() / 3600
        for reading in readings
    ]

    if len(set(times)) < 2:
        return {
            "status": "INSUFFICIENT_TIME_RANGE",
            "message": "Readings need different timestamps.",
        }

    # Calculate trend
    slope, intercept = np.polyfit(
        times,
        values,
        1,
    )

    future_time = times[-1] + hours_ahead

    predicted_value = (
        slope * future_time
        + intercept
    )

    return {
        "status": "OK",
        "parameter": parameter,
        "current_value": round(float(values[-1]), 3),
        "predicted_value": round(float(predicted_value), 3),
        "hours_ahead": hours_ahead,
        "change_per_hour": round(float(slope), 4),
    }


def dissolved_oxygen_warning(
    readings,
    hours_ahead: int = 6,
):
    forecast = forecast_parameter(
        readings,
        "dissolved_oxygen_mg_l",
        hours_ahead,
    )

    if forecast["status"] != "OK":
        return forecast

    current_do = forecast["current_value"]
    predicted_do = forecast["predicted_value"]
    slope = forecast["change_per_hour"]

    # Current condition takes priority
    if current_do < 3.0:
        severity = "CRITICAL"

        message = (
            f"Dissolved oxygen is currently critically low at "
            f"{current_do} mg/L. It is forecast to reach "
            f"{predicted_do} mg/L within {hours_ahead} hours."
        )

        action = (
            "Increase aeration immediately and monitor "
            "dissolved oxygen closely."
        )

    # Future critical condition
    elif predicted_do < 3.0:
        severity = "CRITICAL"

        message = (
            f"Dissolved oxygen is forecast to fall from "
            f"{current_do} mg/L to {predicted_do} mg/L "
            f"within {hours_ahead} hours."
        )

        action = (
            "Increase aeration and closely monitor "
            "dissolved oxygen."
        )

    # Future warning condition
    elif predicted_do < 4.0:
        severity = "WARNING"

        if slope < 0:
            message = (
                f"Dissolved oxygen is trending downward and may "
                f"fall from {current_do} mg/L to "
                f"{predicted_do} mg/L within {hours_ahead} hours."
            )
        else:
            message = (
                f"Dissolved oxygen is forecast at "
                f"{predicted_do} mg/L within {hours_ahead} hours, "
                f"which remains near the warning range."
            )

        action = (
            "Prepare additional aeration and monitor "
            "dissolved oxygen closely."
        )

    else:
        severity = "NORMAL"

        if slope > 0:
            trend = "improving"
        elif slope < 0:
            trend = "declining"
        else:
            trend = "stable"

        message = (
            f"Dissolved oxygen is {trend}. Current level is "
            f"{current_do} mg/L and the {hours_ahead}-hour "
            f"forecast is {predicted_do} mg/L."
        )

        action = "Continue routine monitoring."

    forecast["severity"] = severity
    forecast["message"] = message
    forecast["action"] = action

    return forecast
def ammonia_warning(
    readings,
    hours_ahead: int = 6,
):
    forecast = forecast_parameter(
        readings,
        "ammonia_mg_l",
        hours_ahead,
    )

    if forecast["status"] != "OK":
        return forecast

    current_ammonia = forecast["current_value"]
    predicted_ammonia = forecast["predicted_value"]
    slope = forecast["change_per_hour"]

    # Current critical condition takes priority
    if current_ammonia > 0.5:
        severity = "CRITICAL"

        message = (
            f"Ammonia is currently critically high at "
            f"{current_ammonia} mg/L. It is forecast to reach "
            f"{predicted_ammonia} mg/L within "
            f"{hours_ahead} hours."
        )

        action = (
            "Reduce feeding, improve aeration, check water "
            "quality, and consider partial water exchange."
        )

    # Future critical condition
    elif predicted_ammonia > 0.5:
        severity = "CRITICAL"

        message = (
            f"Ammonia is forecast to rise from "
            f"{current_ammonia} mg/L to "
            f"{predicted_ammonia} mg/L within "
            f"{hours_ahead} hours."
        )

        action = (
            "Reduce feeding and prepare corrective "
            "water-quality measures."
        )

    # Future warning condition
    elif predicted_ammonia > 0.25:
        severity = "WARNING"

        if slope > 0:
            message = (
                f"Ammonia is trending upward and may rise "
                f"from {current_ammonia} mg/L to "
                f"{predicted_ammonia} mg/L within "
                f"{hours_ahead} hours."
            )
        else:
            message = (
                f"Ammonia is forecast at "
                f"{predicted_ammonia} mg/L within "
                f"{hours_ahead} hours, which remains "
                f"in the warning range."
            )

        action = (
            "Monitor ammonia closely and avoid "
            "overfeeding."
        )

    else:
        severity = "NORMAL"

        if slope < 0:
            trend = "improving"
        elif slope > 0:
            trend = "increasing"
        else:
            trend = "stable"

        message = (
            f"Ammonia is {trend}. Current level is "
            f"{current_ammonia} mg/L and the "
            f"{hours_ahead}-hour forecast is "
            f"{predicted_ammonia} mg/L."
        )

        action = "Continue routine monitoring."

    forecast["severity"] = severity
    forecast["message"] = message
    forecast["action"] = action

    return forecast