# Overwritten Vanilla elements

## Economic categories

- pop_category_drones
- pop_category_workers
- pop_category_specialists
- pop_category_rulers

## Game rules

- **can_release_vassal_from_species**: Let Machine empires with a certain AP release vassals
- **can_release_vassal**: Skip checking for Assimilator, Servitor, if the empire has the Distributed Multikernel AP. This overwrite is necessary because there are two checks to see whether vassals can be released
- **can_colonize_planet**: Block colonizing a planet if it's a habitat that's being dismantled, or if it's a ruined World Machine that's being rebooted
- **can_species_be_assembled**: Block Bio-Mech species from being generated via the pop assembly system
- **can_generate_leader_from_species**: Permit Bio-Mech / Mechanical empires to recruit leaders

## Scripted triggers:
- **is_individual_machine**: Triggers yes if empire primary species has machine trait
- **can_add_genetic_traits**: Yes for the Genetic Mastery AP
- **can_remove_beneficial_genetic_traits**: Yes for the Genetic Mastery AP
- **can_add_overclocked_traits**: Yes for the Overclocked origin
- **can_be_leader**: Yes for both Synth origins in this mod

## Species:

- MACHINE: Overwritten to support additional modifiers for World Machine Automatons. There is a known conflict with this mod and any other mod that raises Machine species trait points and picks. There is a sub-mod which I created that raises trait points and picks for Machine species that can be used instead.

## Technology:

Changed weight to consider custom World-Machine blockers

- tech_volcano
- tech_noxious_swamp
- tech_mountain_range
- tech_massive_glacier

## Traits

- trait_mechanical: Add triggered habitability for Mechanical Worlds, and compatibility with Planetary Diversity
