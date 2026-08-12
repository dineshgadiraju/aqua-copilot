def generate_alerts(reading):
    alerts = []

    # Dissolved Oxygen
    if reading.dissolved_oxygen_mg_l < 3.0:
        alerts.append({
            "parameter": "Dissolved Oxygen",
            "severity": "CRITICAL",
            "message": "Dissolved oxygen is dangerously low.",
            "action": (
                "Start or increase aeration immediately "
                "and inspect aerator performance."
            )
        })

    elif reading.dissolved_oxygen_mg_l < 4.0:
        alerts.append({
            "parameter": "Dissolved Oxygen",
            "severity": "WARNING",
            "message": "Dissolved oxygen is below the preferred range.",
            "action": (
                "Increase aeration and monitor oxygen levels closely."
            )
        })

    # Ammonia
    if reading.ammonia_mg_l > 0.5:
        alerts.append({
            "parameter": "Ammonia",
            "severity": "CRITICAL",
            "message": "Ammonia concentration is dangerously high.",
            "action": (
                "Reduce feeding, inspect waste accumulation, "
                "and consider controlled water exchange."
            )
        })

    elif reading.ammonia_mg_l > 0.25:
        alerts.append({
            "parameter": "Ammonia",
            "severity": "WARNING",
            "message": "Ammonia concentration is elevated.",
            "action": (
                "Check feed waste and monitor ammonia frequently."
            )
        })

    # pH
    if reading.ph < 6.5 or reading.ph > 9.0:
        alerts.append({
            "parameter": "pH",
            "severity": "CRITICAL",
            "message": "Pond pH is outside the safe operating range.",
            "action": (
                "Check alkalinity and water conditions. "
                "Correct pH gradually."
            )
        })

    elif reading.ph < 7.0 or reading.ph > 8.6:
        alerts.append({
            "parameter": "pH",
            "severity": "WARNING",
            "message": "Pond pH is outside the preferred range.",
            "action": (
                "Monitor alkalinity and pH more frequently."
            )
        })

    # Temperature
    if reading.temperature_c < 24 or reading.temperature_c > 34:
        alerts.append({
            "parameter": "Temperature",
            "severity": "CRITICAL",
            "message": "Water temperature indicates severe stress risk.",
            "action": (
                "Increase monitoring and reduce additional pond stress."
            )
        })

    elif reading.temperature_c < 26 or reading.temperature_c > 32:
        alerts.append({
            "parameter": "Temperature",
            "severity": "WARNING",
            "message": "Water temperature is outside the preferred range.",
            "action": (
                "Monitor temperature closely and adjust farm operations."
            )
        })

    # Salinity
    if reading.salinity_ppt < 5 or reading.salinity_ppt > 35:
        alerts.append({
            "parameter": "Salinity",
            "severity": "CRITICAL",
            "message": "Salinity is significantly outside the target range.",
            "action": (
                "Investigate the water source and adjust salinity gradually."
            )
        })

    elif reading.salinity_ppt < 8 or reading.salinity_ppt > 28:
        alerts.append({
            "parameter": "Salinity",
            "severity": "WARNING",
            "message": "Salinity is outside the preferred range.",
            "action": (
                "Monitor salinity and avoid sudden changes."
            )
        })

    # Stocking density
    if reading.stocking_density_per_m2 > 80:
        alerts.append({
            "parameter": "Stocking Density",
            "severity": "WARNING",
            "message": "Stocking density is high.",
            "action": (
                "Increase aeration capacity and closely monitor "
                "oxygen, biomass, and feeding."
            )
        })

    return alerts