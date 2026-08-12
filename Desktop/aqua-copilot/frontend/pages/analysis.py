import streamlit as st
import requests

from components.alerts import render_alerts


def render_analysis(api_url):

    st.subheader("Analyze Pond")

    # ----------------------------
    # LOAD PONDS
    # ----------------------------

    try:
        ponds_response = requests.get(
            f"{api_url}/ponds",
            timeout=10
        )

        ponds = ponds_response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot load ponds. "
            "Make sure the FastAPI backend is running."
        )
        return

    except Exception as e:
        st.error(f"Failed to load ponds: {e}")
        return

    if not ponds:
        st.warning(
            "No ponds have been created yet. "
            "Create a pond before running an analysis."
        )
        return

    # ----------------------------
    # SELECT POND
    # ----------------------------

    pond_options = {
        pond["pond_name"]: pond
        for pond in ponds
    }

    selected_pond_name = st.selectbox(
        "Select Pond",
        list(pond_options.keys())
    )

    selected_pond = pond_options[
        selected_pond_name
    ]

    pond_name = selected_pond["pond_name"]

    # ----------------------------
    # POND INFORMATION
    # ----------------------------

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Location",
            selected_pond.get("location")
            or "Not specified"
        )

    with info2:
        area = selected_pond.get("area_m2")

        st.metric(
            "Pond Area",
            f"{area:,.0f} m²"
            if area
            else "Not specified"
        )

    with info3:
        st.metric(
            "Species",
            selected_pond.get(
                "species",
                "Vannamei"
            )
        )

    st.divider()

    # ----------------------------
    # WATER QUALITY INPUTS
    # ----------------------------

    col1, col2 = st.columns(2)

    with col1:

        temperature = st.number_input(
            "Water Temperature (°C)",
            min_value=15.0,
            max_value=45.0,
            value=29.0
        )

        ph = st.number_input(
            "pH",
            min_value=4.0,
            max_value=11.0,
            value=7.8
        )

        dissolved_oxygen = st.number_input(
            "Dissolved Oxygen (mg/L)",
            min_value=0.0,
            max_value=20.0,
            value=5.0
        )

        salinity = st.number_input(
            "Salinity (ppt)",
            min_value=0.0,
            max_value=50.0,
            value=18.0
        )

    with col2:

        ammonia = st.number_input(
            "Ammonia (mg/L)",
            min_value=0.0,
            max_value=5.0,
            value=0.1
        )

        feed = st.number_input(
            "Daily Feed (kg)",
            min_value=0.0,
            max_value=500.0,
            value=40.0
        )

        shrimp_age = st.number_input(
            "Shrimp Age (days)",
            min_value=1,
            max_value=365,
            value=55
        )

        stocking_density = st.number_input(
            "Stocking Density (shrimp/m²)",
            min_value=1.0,
            max_value=300.0,
            value=45.0
        )

    # ----------------------------
    # ANALYZE
    # ----------------------------

    if st.button(
        "Analyze Pond Risk",
        use_container_width=True
    ):

        payload = {
            "pond_name": pond_name,
            "temperature_c": temperature,
            "ph": ph,
            "dissolved_oxygen_mg_l":
                dissolved_oxygen,
            "salinity_ppt": salinity,
            "ammonia_mg_l": ammonia,
            "feed_kg_day": feed,
            "shrimp_age_days": shrimp_age,
            "stocking_density_per_m2":
                stocking_density
        }

        try:
            response = requests.post(
                f"{api_url}/predict-risk",
                json=payload,
                timeout=10
            )

            result = response.json()

            if "error" in result:
                st.error(result["error"])
                return

            render_prediction_result(result)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Make sure the backend is running."
            )

        except Exception as e:
            st.error(str(e))


def render_prediction_result(result):

    risk = result["risk_level"]
    probability = result[
        "risk_probability"
    ]

    health_score = round(
        (1 - probability) * 100
    )

    st.divider()

    st.subheader("Current Pond Status")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Health Score",
            f"{health_score}/100"
        )

    with metric2:
        st.metric(
            "Risk Probability",
            f"{probability * 100:.1f}%"
        )

    with metric3:
        st.metric(
            "Risk Level",
            risk
        )

    # ----------------------------
    # RISK STATUS
    # ----------------------------

    if risk == "HIGH":
        st.error(
            "🔴 High pond risk detected."
        )

    elif risk == "MEDIUM":
        st.warning(
            "🟡 Pond requires attention."
        )

    else:
        st.success(
            "🟢 Pond conditions look healthy."
        )

    # ----------------------------
    # EXPLANATION
    # ----------------------------

    col3, col4 = st.columns(2)

    with col3:

        st.subheader(
            "Detected Risk Factors"
        )

        for factor in result[
            "main_factors"
        ]:
            st.write(f"• {factor}")

    with col4:

        st.subheader(
            "Recommended Actions"
        )

        for action in result[
            "recommended_actions"
        ]:
            st.write(f"• {action}")

    # ----------------------------
    # ALERTS
    # ----------------------------

    alerts = result.get(
        "alerts",
        []
    )

    render_alerts(alerts)