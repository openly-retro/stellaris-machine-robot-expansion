# How it works

## Version 1

1. Decision on a planetary body with an orbital deposit "primes" the deposit for removal.
1.1. A var is set based on the deposit, and a flag is set
1.2. A special project is created in space at the location
2. Player completes project with construction ship
2.1. On project completion, a transport ship is created and the ship goes to the consolidation dropoff
2.2. Look at what var is set and its value; transfer that amount to the planet and create 1 corresponding deposit per 1 increment of the var


Resources are tracked on the source planet with:
- `oxr_mdlc_consolidator_orbital_resource_type_$RESOURCE$`

When a resource has been marked for extraction, planet flag is set:
- `oxr_mdlc_consolidators_planet_has_available_$RESOURCE$_consolidation`


Resources are tracked on the mover fleet with:
- `oxr_mdlc_consolidator_ship_resource_type_$RESOURCE$`

Mover is doing things: 
planet flag: oxr_mdlc_consolidators_planet_consolidation_in_progress

1. Decision: oxr_mdlc_decision_trigger_orbital_extraction_project
2. Call event `oxr_mdlc_civic_consolidators.3000`
2.1. Player selects an available deposit to extract
2.2. Call planet effect: `oxr_mdlc_planet_select_orbital_energy_deposits_for_processing`
2.3. (planet effect) oxr_mdlc_consolidators_planet_make_orbital_deposits_ready_for_extraction
2.4. Trigger special project
3. Special project finishes
3.1. Trigger planet event `oxr_mdlc_civic_consolidators.3100`
3.2. This summons the ship, copies vars from the planet to the ship, and moves it


Other stuff:

- planet event dialogues won't appear for planets not owned by the initiating country
