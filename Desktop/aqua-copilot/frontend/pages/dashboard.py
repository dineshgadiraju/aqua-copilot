import streamlit as st
import requests
import pandas as pd


def render_dashboard(api_url):

    st.subheader("Farm Dashboard")

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
            key="dashboard_pond"
        )

        selected_pond = pond_options[selected_pond_name]
        pond_id = selected_pond["id"]

        history_response = requests.get(
            f"{api_url}/ponds/{pond_id}/readings",
            timeout=10
        )

        history = history_response.json()
        readings = history.get("readings", [])

        alerts_response = requests.get(
            f"{api_url}/ponds/{pond_id}/alerts",
            timeout=10
        )

        alerts_data = alerts_response.json()

        pond_alerts = alerts_data.get(
            "alerts",
            []
        )

        # ----------------------------
        # POND INFORMATION
        # ----------------------------

        st.markdown(f"### 🦐 {selected_pond_name}")

        pond1, pond2, pond3 = st.columns(3)

        with pond1:
            st.metric(
                "Location",
                selected_pond.get("location")
                or "Not specified"
            )

        with pond2:
            area = selected_pond.get("area_m2")

            st.metric(
                "Pond Area",
                f"{area:,.0f} m²"
                if area
                else "Not specified"
            )

        with pond3:
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
                "No pond analysis has been recorded yet. "
                "Go to Pond Analysis to create the first reading."
            )
            return

        df = pd.DataFrame(readings)

        df["recorded_at"] = pd.to_datetime(
            df["recorded_at"]
        )

        df = df.sort_values("recorded_at")

        latest = df.iloc[-1]

        probability = latest["risk_probability"]

        health_score = round(
            (1 - probability) * 100
        )

        # ----------------------------
        # HEALTH OVERVIEW
        # ----------------------------

        st.subheader("Pond Health Overview")

        h1, h2, h3 = st.columns(3)

        with h1:
            st.metric(
                "Health Score",
                f"{health_score}/100"
            )

        with h2:
            st.metric(
                "Risk Probability",
                f"{probability * 100:.1f}%"
            )

        with h3:
            st.metric(
                "Risk Level",
                latest["risk_level"]
            )

        risk = latest["risk_level"]

        if risk == "HIGH":
            st.error(
                "🔴 Critical attention required. "
                "Review pond conditions immediately."
            )

        elif risk == "MEDIUM":
            st.warning(
                "🟡 Pond conditions require attention."
            )

        else:
            st.success(
                "🟢 Pond conditions are currently stable."
            )

        st.divider()

        # ----------------------------
        # RECENT ALERTS
        # ----------------------------

        st.subheader("🚨 Recent Pond Alerts")

        if not pond_alerts:
            st.success(
                "No alerts have been recorded for this pond."
            )

        else:
            critical_count = sum(
                1
                for alert in pond_alerts
                if alert["severity"] == "CRITICAL"
            )

            warning_count = sum(
                1
                for alert in pond_alerts
                if alert["severity"] == "WARNING"
            )

            a1, a2, a3 = st.columns(3)

            with a1:
                st.metric(
                    "Total Alerts",
                    len(pond_alerts)
                )

            with a2:
                st.metric(
                    "Critical",
                    critical_count
                )

            with a3:
                st.metric(
                    "Warnings",
                    warning_count
                )

            # Show most recent 5 alerts
            for alert in pond_alerts[:5]:

                severity = alert["severity"]
                parameter = alert["parameter"]

                if severity == "CRITICAL":
                    icon = "🔴"
                else:
                    icon = "🟡"

                with st.expander(
                    f"{icon} {severity} — {parameter}"
                ):
                    st.write(
                        f"**Problem:** {alert['message']}"
                    )

                    st.write(
                        f"**Recommended Action:** "
                        f"{alert['action']}"
                    )

                    if alert.get("created_at"):
                        created_at = pd.to_datetime(
                            alert["created_at"]
                        )

                        st.caption(
                            f"Recorded: {created_at}"
                        )

        st.divider()

        # ----------------------------
        # WATER QUALITY
        # ----------------------------

        st.subheader("Current Water Quality")

        w1, w2, w3 = st.columns(3)

        with w1:
            st.metric(
                "🌡️ Temperature",
                f"{latest['temperature_c']:.1f} °C"
            )

            st.metric(
                "🧪 Ammonia",
                f"{latest['ammonia_mg_l']:.2f} mg/L"
            )

        with w2:
            st.metric(
                "💧 Dissolved Oxygen",
                f"{latest['dissolved_oxygen_mg_l']:.1f} mg/L"
            )

            st.metric(
                "🌊 Salinity",
                f"{latest['salinity_ppt']:.1f} ppt"
            )

        with w3:
            st.metric(
                "⚗️ pH",
                f"{latest['ph']:.1f}"
            )

            st.metric(
                "🍤 Shrimp Age",
                f"{int(latest['shrimp_age_days'])} days"
            )

        st.divider()

        # ----------------------------
        # PRODUCTION
        # ----------------------------

        st.subheader("Production")

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "Daily Feed",
                f"{latest['feed_kg_day']:.1f} kg"
            )

        with p2:
            st.metric(
                "Stocking Density",
                f"{latest['stocking_density_per_m2']:.0f}/m²"
            )

        with p3:
            st.metric(
                "Total Readings",
                len(df)
            )

        st.divider()

        # ----------------------------
        # RISK TREND
        # ----------------------------

        st.subheader("Risk Trend")

        risk_df = df[
            [
                "recorded_at",
                "risk_probability"
            ]
        ].copy()

        risk_df["risk_probability"] *= 100

        risk_df = risk_df.set_index(
            "recorded_at"
        )

        st.line_chart(risk_df)

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Make sure the backend is running."
        )

    except Exception as e:
        st.error(str(e))