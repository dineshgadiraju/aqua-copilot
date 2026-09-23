import streamlit as st
import requests


def render_forecast(api_url, pond_name):

    st.subheader("🔮 Dissolved Oxygen Early Warning")

    try:
        response = requests.get(
            f"{api_url}/ponds/{pond_name}/forecast",
            params={"hours": 6},
            timeout=10,
        )

        forecast = response.json()

    except requests.exceptions.RequestException:
        st.warning("Unable to load forecast.")
        return

    if forecast.get("status") != "OK":
        st.info(
            forecast.get(
                "message",
                "Forecast is currently unavailable."
            )
        )
        return

    current_do = forecast["current_value"]
    predicted_do = forecast["predicted_value"]
    change = forecast["change_per_hour"]
    severity = forecast["severity"]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Current DO",
            f"{current_do:.2f} mg/L"
        )

    with c2:
        st.metric(
            "6-Hour Forecast",
            f"{predicted_do:.2f} mg/L"
        )

    with c3:
        st.metric(
            "Change / Hour",
            f"{change:+.4f} mg/L"
        )

    message = forecast["message"]

    if severity == "CRITICAL":
        st.error(f"🔴 {message}")

    elif severity == "WARNING":
        st.warning(f"🟡 {message}")

    else:
        st.success(f"🟢 {message}")

    st.write(
        f"**Recommended Action:** {forecast['action']}"
    )