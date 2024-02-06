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
            descriptive_prefix = f"${modifier_key_to_tooltip_prefix_var[modifier_key]}$"
            modifiers_list.append(descriptive_prefix)
            for modifier_name in root[modifier_key].keys():
                mod_tt_key = f"$mod_{modifier_name.lower()}$"
                modified_amount = root[modifier_key][modifier_name]
                if "." in str(modified_amount) and str(modified_amount)[-1].isdigit():
                    modified_amount = convert_decimal_to_percent_str(modified_amount)
                modifiers_list.append(
                    f"{mod_tt_key}: {make_green_text(f"+{modified_amount}")}"
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
