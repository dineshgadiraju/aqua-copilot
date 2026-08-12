def explain(reading):
    factors = []
    actions = []

    if reading.dissolved_oxygen_mg_l < 3.5:
        factors.append(
            "Low dissolved oxygen"
        )
        actions.append(
            "Increase aeration and inspect "
            "aerator performance."
        )

    if reading.ammonia_mg_l > 0.25:
        factors.append(
            "Elevated ammonia"
        )
        actions.append(
            "Check feed waste, improve water exchange, "
            "and monitor ammonia closely."
        )

    if reading.ph < 7.0 or reading.ph > 8.6:
        factors.append(
            "pH outside preferred range"
        )
        actions.append(
            "Recheck alkalinity and correct pH gradually."
        )

    if (
        reading.temperature_c < 26
        or reading.temperature_c > 32
    ):
        factors.append(
            "Temperature stress"
        )
        actions.append(
            "Increase monitoring frequency "
            "and reduce pond stress."
        )

    if (
        reading.salinity_ppt < 8
        or reading.salinity_ppt > 28
    ):
        factors.append(
            "Salinity outside target range"
        )
        actions.append(
            "Adjust salinity gradually where "
            "farm conditions allow."
        )

    if reading.stocking_density_per_m2 > 65:
        factors.append(
            "High stocking density"
        )
        actions.append(
            "Increase aeration and closely monitor "
            "biomass and feeding."
        )

    if not factors:
        factors.append(
            "No major threshold violations detected"
        )
        actions.append(
            "Continue routine monitoring."
        )

    return factors, actions