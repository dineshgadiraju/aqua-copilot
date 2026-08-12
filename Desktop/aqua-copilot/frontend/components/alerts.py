import streamlit as st


def render_alerts(alerts):
    st.divider()
    st.subheader("🚨 Pond Alerts")

    if not alerts:
        st.success(
            "No active water-quality alerts detected."
        )
        return

    critical_alerts = [
        alert
        for alert in alerts
        if alert["severity"] == "CRITICAL"
    ]

    warning_alerts = [
        alert
        for alert in alerts
        if alert["severity"] == "WARNING"
    ]

    if critical_alerts:
        st.error(
            f"🔴 {len(critical_alerts)} critical "
            "condition(s) require immediate attention."
        )

        for alert in critical_alerts:
            with st.expander(
                f"🔴 CRITICAL — {alert['parameter']}",
                expanded=True
            ):
                st.write(
                    f"**Problem:** {alert['message']}"
                )

                st.write(
                    f"**Recommended Action:** "
                    f"{alert['action']}"
                )

    if warning_alerts:
        st.warning(
            f"🟡 {len(warning_alerts)} warning "
            "condition(s) detected."
        )

        for alert in warning_alerts:
            with st.expander(
                f"🟡 WARNING — {alert['parameter']}"
            ):
                st.write(
                    f"**Problem:** {alert['message']}"
                )

                st.write(
                    f"**Recommended Action:** "
                    f"{alert['action']}"
                )