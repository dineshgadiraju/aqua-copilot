def explain(reading):
    factors = []
    actions = []

    # ---------------------------------
    # DISSOLVED OXYGEN
    # ---------------------------------

    if reading.dissolved_oxygen_mg_l < 3.5:
        factors.append(
            "Critical dissolved oxygen level"
        )
        actions.append(
            "Increase aeration immediately, reduce feeding "
            "temporarily, and recheck dissolved oxygen soon."
        )

    elif reading.dissolved_oxygen_mg_l < 5.0:
        factors.append(
            "Dissolved oxygen below preferred range"
        )
        actions.append(
            "Increase aeration and monitor dissolved oxygen "
            "closely."
        )

    # ---------------------------------
    # AMMONIA
    # ---------------------------------

    if reading.ammonia_mg_l > 1.0:
        factors.append(
            "Critically elevated ammonia"
        )
        actions.append(
            "Reduce feeding, increase aeration, inspect feed "
            "waste, and consider partial water exchange."
        )

    elif reading.ammonia_mg_l > 0.25:
        factors.append(
            "Elevated ammonia"
        )
        actions.append(
            "Check feed waste, reduce unnecessary feeding, "
            "and monitor ammonia closely."
        )

    # ---------------------------------
    # pH
    # ---------------------------------

    if reading.ph < 7.0:
        factors.append(
            "Low pond pH"
        )
        actions.append(
            "Check alkalinity and correct pH gradually."
        )

    elif reading.ph > 8.6:
        factors.append(
            "High pond pH"
        )
        actions.append(
            "Monitor algae activity and correct pH gradually."
        )

    # ---------------------------------
    # TEMPERATURE
    # ---------------------------------

    if reading.temperature_c < 26:
        factors.append(
            "Low water temperature"
        )
        actions.append(
            "Monitor shrimp feeding activity and reduce feed "
            "if shrimp activity decreases."
        )

    elif reading.temperature_c > 32:
        factors.append(
            "High water temperature"
        )
        actions.append(
            "Increase aeration and monitor dissolved oxygen "
            "more frequently."
        )

    # ---------------------------------
    # SALINITY
    # ---------------------------------

    if reading.salinity_ppt < 8:
        factors.append(
            "Low salinity"
        )
        actions.append(
            "Avoid sudden salinity changes and monitor shrimp "
            "for signs of stress."
        )

    elif reading.salinity_ppt > 28:
        factors.append(
            "High salinity"
        )
        actions.append(
            "Adjust salinity gradually where farm conditions "
            "allow and monitor shrimp behavior."
        )

    # ---------------------------------
    # STOCKING DENSITY
    # ---------------------------------

    if reading.stocking_density_per_m2 > 65:
        factors.append(
            "High stocking density"
        )
        actions.append(
            "Increase aeration capacity and closely monitor "
            "biomass, dissolved oxygen, and feeding."
        )

    # ---------------------------------
    # NORMAL CONDITIONS
    # ---------------------------------

    if not factors:
        factors.append(
            "No major threshold violations detected"
        )
        actions.append(
            "Pond conditions appear stable. Continue routine "
            "monitoring and normal feeding practices."
        )

    return factors, actions