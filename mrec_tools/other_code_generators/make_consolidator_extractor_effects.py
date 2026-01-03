# oxr_mdlc_planet_extract_

orbital_deposit_switch_effect = f"""
d_{game_resource}_{series} = {{
	remove_deposit = d_{game_resource}_1
	space_owner = {{
		oxr_mdlc_country_create_mover_fleet_give_instructions = {{
			RESOURCE = {game_resource}
			AMOUNT = {series}
		}}
	}}
}}
"""

orbital_deposit_switch_effect_wrapper = f"""
oxr_mdlc_planet_extract_orbital_energy_deposits = {{
	switch = {{
		trigger = has_deposit
		{individual_deposit_names_and_switch_effects}
	}}
}}
"""


GAME_RESOURCES_MAXIMUM_DEPOSIT_SIZES = {
	'food': 10,
	'energy': 10,
	'minerals': 10,
	'society_research': 10,
	'physics_research': 10,
	'engineering_research': 10,
	'alloys': 25,
	'sr_living_metal',
	'rare_crystals': 5,
	'exotic_gases': 5,
	'volatile_motes': 5,
	'sr_zro': 5,
	'sr_dark_matter': 5
}