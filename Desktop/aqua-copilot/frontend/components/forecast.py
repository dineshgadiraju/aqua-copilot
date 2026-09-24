import streamlit as st
import requests


def get_forecast(api_url, endpoint, pond_name, hours=6):
    """Fetch forecast data from the backend."""

    try:
        response = requests.get(
            f"{api_url}{endpoint.format(pond_name=pond_name)}",
            params={"hours": hours},
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:
        return None


def render_status(forecast):
    """Render severity message and recommended action."""

    severity = forecast["severity"]
    message = forecast["message"]

    if severity == "CRITICAL":
        st.error(f"🔴 CRITICAL — {message}")

    elif severity == "WARNING":
        st.warning(f"🟡 WARNING — {message}")

    else:
        st.success(f"🟢 NORMAL — {message}")

    st.write(
        f"**Recommended Action:** {forecast['action']}"
    )


def render_parameter_forecast(
    title,
    forecast,
    current_label,
    unit,
):
    """Render one water-quality forecast."""

    st.markdown(f"### {title}")

    if forecast is None:
        st.warning("Unable to load forecast.")
        return

    if forecast.get("status") != "OK":
        st.info(
            forecast.get(
                "message",
                "Forecast is currently unavailable.",
            )
        )
        return

    current = forecast["current_value"]
    predicted = forecast["predicted_value"]
    change = forecast["change_per_hour"]
    hours = forecast["hours_ahead"]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            current_label,
            f"{current:.2f} {unit}",
        )

    with c2:
        st.metric(
            f"{hours}-Hour Forecast",
            f"{predicted:.2f} {unit}",
        )

    with c3:
        st.metric(
            "Change / Hour",
            f"{change:+.4f} {unit}",
        )

    render_status(forecast)


def render_forecast(api_url, pond_name):

    st.subheader("🔮 Predictive Early Warning")

    # ----------------------------
    # DISSOLVED OXYGEN
    # ----------------------------

    do_forecast = get_forecast(
        api_url,
        "/ponds/{pond_name}/forecast",
        pond_name,
    )

    render_parameter_forecast(
        "💧 Dissolved Oxygen",
        do_forecast,
        "Current DO",
        "mg/L",
    )

    st.divider()

    # ----------------------------
    # AMMONIA
    # ----------------------------

    ammonia_forecast = get_forecast(
        api_url,
        "/ponds/{pond_name}/forecast/ammonia",
        pond_name,
    )

    render_parameter_forecast(
        "🧪 Ammonia",
        ammonia_forecast,
        "Current Ammonia",
        "mg/L",
    )