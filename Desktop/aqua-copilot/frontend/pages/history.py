import streamlit as st
import requests
import pandas as pd


def render_history(api_url):

    st.subheader("Pond History")

    try:
        ponds_response = requests.get(
            f"{api_url}/ponds",
            timeout=10
        )

        ponds = ponds_response.json()

        if not ponds:
            st.info("No ponds have been created yet.")
            return

        pond_options = {
            pond["pond_name"]: pond
            for pond in ponds
        }

        selected_pond_name = st.selectbox(
            "Select Pond",
            list(pond_options.keys()),
            key="history_pond"
        )

        selected_pond = pond_options[selected_pond_name]
        pond_id = selected_pond["id"]

        history_response = requests.get(
            f"{api_url}/ponds/{pond_id}/readings",
            timeout=10
        )

        history = history_response.json()
        readings = history.get("readings", [])

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

        if not readings:
            st.info(
                "No readings have been recorded "
                "for this pond yet."
            )
            return

        df = pd.DataFrame(readings)

        df["recorded_at"] = pd.to_datetime(
            df["recorded_at"]
        )

        df = df.sort_values("recorded_at")

        latest = df.iloc[-1]

        health_score = round(
            (1 - latest["risk_probability"]) * 100
        )

        # ----------------------------
        # LATEST STATUS
        # ----------------------------

        st.subheader("Latest Pond Status")

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Health Score",
                f"{health_score}/100"
            )

        with m2:
            st.metric(
                "Temperature",
                f"{latest['temperature_c']:.1f} °C"
            )

        with m3:
            st.metric(
                "Dissolved Oxygen",
                f"{latest['dissolved_oxygen_mg_l']:.1f} mg/L"
            )

        with m4:
            st.metric(
                "Risk Level",
                latest["risk_level"]
            )

        st.divider()

        # ----------------------------
        # TRENDS
        # ----------------------------

        st.subheader("Water Quality Trends")

        chart_df = df.set_index("recorded_at")

        st.write("Temperature")
        st.line_chart(
            chart_df[["temperature_c"]]
        )

        st.write("pH")
        st.line_chart(
            chart_df[["ph"]]
        )

        st.write("Dissolved Oxygen")
        st.line_chart(
            chart_df[["dissolved_oxygen_mg_l"]]
        )

        st.write("Ammonia")
        st.line_chart(
            chart_df[["ammonia_mg_l"]]
        )

        st.write("Risk Probability")

        risk_chart = chart_df[
            ["risk_probability"]
        ].copy()

        risk_chart["risk_probability"] *= 100

        st.line_chart(risk_chart)

        st.divider()

        # ----------------------------
        # TABLE
        # ----------------------------

        st.subheader("Recent Readings")

        display_df = df[
            [
                "recorded_at",
                "temperature_c",
                "ph",
                "dissolved_oxygen_mg_l",
                "salinity_ppt",
                "ammonia_mg_l",
                "risk_level",
                "risk_probability"
            ]
        ].copy()

        display_df["risk_probability"] = (
            display_df["risk_probability"] * 100
        ).round(1)

        display_df = display_df.rename(
            columns={
                "recorded_at": "Recorded At",
                "temperature_c": "Temperature °C",
                "ph": "pH",
                "dissolved_oxygen_mg_l": "DO mg/L",
                "salinity_ppt": "Salinity ppt",
                "ammonia_mg_l": "Ammonia mg/L",
                "risk_level": "Risk",
                "risk_probability": "Risk %"
            }
        )

        st.dataframe(
            display_df.sort_values(
                "Recorded At",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Make sure the backend is running."
        )

    except Exception as e:
        st.error(str(e))