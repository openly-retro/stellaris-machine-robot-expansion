# Given Stellaris leader trait info as YAML, generate Stellaris tooltip game code from it
import re
import sys
from yaml import safe_load
import argparse

from mre_common_vars import TRAIT_MODIFIER_KEYS

COLOR_CODES = {
    # https://steamcommunity.com/sharedfiles/filedetails/?id=1955978558
    "orange": "§H",
    "brown": "§L",
    "yellow": "§Y",
    "green": "§G"
}
CLOSE_CODE = "§!"

DIGIT_TO_LATIN = {
    # How is Latin still alive in the space age?
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
    "7": "VII",
    "8": "VIII",
    "9": "IX",
    "10": "X"
}

def make_orange_text(some_text):
    return f"{COLOR_CODES['orange']}{some_text}{CLOSE_CODE}"

def make_brown_text(some_text):
    return f"{COLOR_CODES['brown']}{some_text}{CLOSE_CODE}"

def make_green_text(some_text):
    return f"{COLOR_CODES['green']}{some_text}{CLOSE_CODE}"

""" Map modifier category name to tooltip """
modifier_key_to_tooltip_prefix_var = {
    "army_modifier": "commanding_army_effect",
    "councilor_modifier": "councilor_trait",
    "fleet_modifier": "commanding_navy_effect",
    "modifier": "",
    "planet_modifier": "governing_planet_effect",
    "sector_modifier": "governing_sector_effect",
    "self_modifier": "",
    "triggered_army_effect": "commanding_army_effect",
    "triggered_councilor_modifier": "councilor_trait",
    "triggered_fleet_modifier": "commanding_navy_effect",
    "triggered_planet_modifier": "governing_planet_effect",
    "triggered_sector_modifier": "governing_sector_effect",
    "triggered_self_modifier": ""
}

""" This map is to record exceptions to PDX' pattern of naming modifiers. For a good number
of cases, we can prepend mod_ to whatever the name of the modifier is, and that will link
automatically to a good tooltip.
Of course, nothing is sacred or 100% consistent in the base game data, so there are going to
be numerous exceptions to this naming pattern, and unfortunately, there is no pattern 
to the exceptions. So we have to individual note them all if we are ever to make our way
to the surface here.

The key name is what we thought the tooltip reference should be.
Prepend "mre_" to the key, and that creates a link to a custom copy of the original trait text,
which normally doesn't get shown for various reasons (like dependency on Megacorp DLC, for example)
"""
kludges_modifier_replacement_map = {
    "galcom_modifier_diplo_weight_desc":1,
    "species_leader_exp_gain":1,
}

megacorp_modifier_replacement_map = {
    "deposit_blockers_cost_mult":1,
    "planet_jobs_food_produces_mult":1,
    "planet_administrators_unity_produces_mult":1,
    "ships_upkeep_mult":1,
    "ship_emergency_ftl_mult":1,
    "planet_farmers_food_produces_mult":1,
    "planet_farmers_food_produces_add":1,
    "planet_jobs_slave_produces_mult":1,
    "planet_miners_minerals_produces_mult":1,
    "planet_miners_minerals_produces_add":1,
    "planet_metallurgists_alloys_produces_mult":1,
    "planet_metallurgists_alloys_produces_add":1,
    "planet_jobs_energy_produces_mult":1,
    "planet_jobs_energy_produces_add":1,
    "s_slot_weapon_damage_mult":1,
    "s_slot_weapon_fire_rate_mult":1,
    "m_slot_weapon_damage_mult":1,
    "m_slot_weapon_fire_rate_mult":1,
    "planet_jobs_minerals_produces_mult":1,
    "planet_jobs_minerals_produces_add":1,
    "weapon_type_explosive_weapon_damage_mult":1,
    "weapon_type_explosive_weapon_fire_rate_mult":1,
    "planet_miners_minerals_produces_add":1,
    "planet_jobs_worker_produces_mult":1,
    "planet_jobs_slave_produces_mult":1,
    "planet_pops_upkeep_mult":1,
    "job_soldier_per_pop":1,
    "planet_technician_physics_research_produces_mult":1,
    "planet_technician_physics_research_produces_add":1,
    "planet_farmers_society_research_produces_add":1,
    "planet_miners_engineering_research_produces_add":1,
    "planet_jobs_energy_produces_mult":1,
}
paragons_modifier_replacement_map = {
    "weapon_role_artillery_weapon_damage_mult":1,
    "weapon_type_strike_craft_weapon_damage_mult":1,
    "planet_soldiers_energy_produces_add":1,
    "planet_soldiers_minerals_produces_add":1,
    "mod_ship_fire_rate_mult":1,
}

# Dicts are the fastest lookup ( O(1) ) vs searching a list ( O(n) )
ALL_REPLACEMENT_MAPS = kludges_modifier_replacement_map | megacorp_modifier_replacement_map | paragons_modifier_replacement_map 

""" Some tooltips have localisation keys only in the yml for that DLC, and arent in 
base stellaris. So they show up empty in the leadermaking UI because the game can't find
them because that DLC is not enabled. And there is no DLC-required flag in the trait itself """
hidden_dlc_requirements = {
    "mod_planet_jobs_food_produces_mult": "Megacorp",  # implement in potential: host_has_dlc = "Megacorp"
    "mod_planet_administrators_unity_produces_mult": "Megacorp",
    "mod_planet_technician_energy_produces_mult": "Megacorp",
    "mod_weapon_archaeotech_weapon_damage_mult": "Ancient Realms",  # has_ancrel
    "mod_weapon_role_artillery_weapon_damage_mult": "Paragons",
    "mod_weapon_type_strike_craft_weapon_damage_mult": "Paragons",
    "mod_ships_upkeep_mult": "Megacorp",
}

""" These traits have a tooltip_tt entry in a localisation file """
traits_with_complete_tooltips = {
    "leader_trait_adventurous_spirit_3": "leader_trait_adventurous_spirit_3_tt",
    "leader_trait_bureaucrat_2": "leader_trait_bureaucrat_2_tt"
}

def create_tooltip_for_leader(
    trait_dict, leader_class, feature="leader_making"
):
    # parsed = safe_load(trait_yaml)
    
    trait_name = list(trait_dict.keys())[0]
    base_trait_name = trait_name
    trait_level = ""
    if trait_name[-1].isdigit():
        base_trait_name = trait_name.rsplit('_',1)[0]
        ending_num = trait_name.rsplit('_',1)[1]
        trait_level = f"{DIGIT_TO_LATIN[ending_num]}"
    # trait_title = make_orange_text(f"${base_trait_name}_machine${trait_level}")
    trait_title = make_orange_text(f"${base_trait_name}$ {trait_level}")
    tooltip_base = "xvcv_mdlc"
    if feature=="leader_making":
        tooltip_stem = "leader_making_tooltip"
    # leader_trait_naturalist_3 will read "Preservation Code III"

    trait_cost_tt = "$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$"
    separator_ruler = "--------------"
    # trait_desc_brown_text = make_brown_text(f"${base_trait_name}_machine_desc$")
    trait_desc_brown_text = make_brown_text(f"${base_trait_name}_desc$")

    root = trait_dict[trait_name]
    modifiers_list = []
    for modifier_key in TRAIT_MODIFIER_KEYS:
        if root.get(modifier_key):
            if descriptive_prefix := modifier_key_to_tooltip_prefix_var[modifier_key]:
                modifiers_list.append(f"${descriptive_prefix}$")

            for modifier_name in root[modifier_key].keys():
                # Check if we have a replacement tooltip for an autogenerated one,
                # and prepend mre_ so it matches with our custom definition
                replacement_check = ''
                if modifier_name in ALL_REPLACEMENT_MAPS:
                    replacement_check = "mre_"
                # make everything lowercase, PDX in this case doesn't care
                mod_tt_key = f"${replacement_check}mod_{modifier_name}$".lower()
                modified_amount = root[modifier_key][modifier_name]
                if "." in str(modified_amount) and str(modified_amount)[-1].isdigit():
                    modified_amount = convert_decimal_to_percent_str(modified_amount)
                number_sign = "+" if "-" not in str(modified_amount) else ""
                modifiers_list.append(
                    f"{mod_tt_key}: {make_green_text(f"{number_sign}{modified_amount}")}"
                )
    trait_bonuses = '\\n'.join(modifiers_list)
    compiled_tooltip = (
        f'{tooltip_base}_{tooltip_stem}_{leader_class}_{trait_name}:0 \"{trait_title}{trait_cost_tt}\\n'
        f'{trait_bonuses}\\n{separator_ruler}\\n{trait_desc_brown_text}\"'
    )
    # breakpoint()
    return f"""
#{feature} #{leader_class} #{trait_name}
{compiled_tooltip}
"""

def convert_decimal_to_percent_str(numeric_amount: float) -> str:
    percent_float = numeric_amount * 100
    return f"{int(percent_float)}%"
