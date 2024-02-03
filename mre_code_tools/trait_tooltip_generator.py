# Given Stellaris leader trait info as YAML, generate Stellaris tooltip game code from it
import re
import sys
from yaml import safe_load
import argparse

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
        trait_level = f" {DIGIT_TO_LATIN[ending_num]}"
    trait_title = make_orange_text(f"${base_trait_name}_machine${trait_level}")
    tooltip_base = "xvcv_mdlc"
    if feature=="leader_making":
        tooltip_stem = "leader_making_tooltip"
    # leader_trait_naturalist_3 will read "Preservation Code III"

    trait_cost_tt = "$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$"
    separator_ruler = "--------------"
    trait_desc_brown_text = make_brown_text(f"${base_trait_name}_machine_desc$")

    modifiers_list = []
    if trait_dict[trait_name].get('planet_modifier'):
        modifiers_list.append("$governing_planet_effect$")
        for modifier in trait_dict[trait_name]['planet_modifier'].keys():
            mod_tt_key = f"$mod_{modifier.lower()}$"
            modified_amount = trait_dict[trait_name]['planet_modifier'][modifier]
            modifiers_list.append(
                f"$mod_{modifier.lower()}$: {make_green_text(f"+{modified_amount}")}"
            )
    if trait_dict[trait_name].get('sector_modifier'):
        modifiers_list.append("$governing_sector_effect$")
        for modifier in trait_dict[trait_name]['sector_modifier'].keys():
            mod_tt_key = f"$mod_{modifier.lower()}$"
            modified_amount = trait_dict[trait_name]['sector_modifier'][modifier]
            modifiers_list.append(
                f"$mod_{modifier.lower()}$: "
                f"{make_green_text(f"+{modified_amount}")}"
            )
    trait_bonuses = "\n".join(modifiers_list)
    return (
        f"{tooltip_base}_{tooltip_stem}_{leader_class}_{trait_name}:0 \"{trait_title}{trait_cost_tt}\n"
        f"{trait_bonuses}\n{separator_ruler}\n{trait_desc_brown_text}\"\n"
    )
