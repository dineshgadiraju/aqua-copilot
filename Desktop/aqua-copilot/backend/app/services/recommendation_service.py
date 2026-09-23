def explain(reading):
    factors = []
    actions = []

    # Temperature
    if reading.temperature_c < 26:
        factors.append(
            f"Water temperature is low at "
            f"{reading.temperature_c}°C."
        )
        actions.append(
            "Monitor temperature closely and avoid sudden "
            "water exchanges that may reduce temperature further."
        )

    elif reading.temperature_c > 32:
        factors.append(
            f"Water temperature is high at "
            f"{reading.temperature_c}°C."
        )
        actions.append(
            "Increase aeration and, if possible, perform a "
            "controlled partial water exchange."
        )

    # pH
    if reading.ph < 7.5:
        factors.append(
            f"pH is low at {reading.ph}."
        )
        actions.append(
            "Check alkalinity and water quality. "
            "Correct pH gradually rather than making sudden changes."
        )

    elif reading.ph > 8.5:
        factors.append(
            f"pH is high at {reading.ph}."
        )
        actions.append(
            "Monitor algae growth and reduce excessive nutrient input. "
            "Check pH again during early morning and afternoon."
        )

    # Dissolved Oxygen
    if reading.dissolved_oxygen_mg_l < 3:
        factors.append(
            f"Dissolved oxygen is critically low at "
            f"{reading.dissolved_oxygen_mg_l} mg/L."
        )
        actions.append(
            "Start aerators immediately and reduce feeding "
            "until dissolved oxygen improves."
        )

    elif reading.dissolved_oxygen_mg_l < 5:
        factors.append(
            f"Dissolved oxygen is below the preferred range at "
            f"{reading.dissolved_oxygen_mg_l} mg/L."
        )
        actions.append(
            "Increase aeration, especially during the night "
            "and early morning."
        )

    # Salinity
    if reading.salinity_ppt < 5:
        factors.append(
            f"Salinity is very low at "
            f"{reading.salinity_ppt} ppt."
        )
        actions.append(
            "Check source-water salinity and adjust gradually "
            "if the cultured shrimp require higher salinity."
        )

    elif reading.salinity_ppt > 30:
        factors.append(
            f"Salinity is high at "
            f"{reading.salinity_ppt} ppt."
        )
        actions.append(
            "Avoid sudden salinity changes. Consider controlled "
            "freshwater addition if appropriate."
        )

    # Ammonia
    if reading.ammonia_mg_l >= 1:
        factors.append(
            f"Ammonia is dangerously high at "
            f"{reading.ammonia_mg_l} mg/L."
        )
        actions.append(
            "Reduce or temporarily stop feeding, increase aeration, "
            "remove organic waste and consider a partial water exchange."
        )

    elif reading.ammonia_mg_l >= 0.5:
        factors.append(
            f"Ammonia is elevated at "
            f"{reading.ammonia_mg_l} mg/L."
        )
        actions.append(
            "Reduce feeding slightly and monitor ammonia again soon. "
            "Check pond waste accumulation."
        )

    # Stocking density
    if reading.stocking_density_per_m2 > 70:
        factors.append(
            f"Stocking density is high at "
            f"{reading.stocking_density_per_m2} shrimp/m²."
        )
        actions.append(
            "Increase aeration capacity and monitor oxygen, "
            "ammonia and feeding response more frequently."
        )

    # Feed
    if (
        reading.feed_kg_day > 40
        and reading.ammonia_mg_l >= 0.5
    ):
        factors.append(
            "High feeding combined with elevated ammonia may "
            "be increasing pond organic waste."
        )
        actions.append(
            "Reduce feed temporarily and check feed trays "
            "for uneaten feed."
        )

    # Combined critical condition
    if (
        reading.dissolved_oxygen_mg_l < 3
        and reading.ammonia_mg_l >= 1
    ):
        factors.insert(
            0,
            "Low dissolved oxygen and high ammonia together "
            "create a serious stress condition."
        )

        actions.insert(
            0,
            "PRIORITY: Increase aeration immediately, reduce feeding "
            "and inspect shrimp behavior for signs of stress."
        )

    # Healthy pond
    if not factors:
        factors.append(
            "All major monitored water-quality parameters "
            "are currently within acceptable ranges."
        )

        actions.append(
            "Continue normal pond management and regular "
            "water-quality monitoring."
        )

    # Avoid duplicate recommendations
    factors = list(dict.fromkeys(factors))
    actions = list(dict.fromkeys(actions))

    return factors, actions