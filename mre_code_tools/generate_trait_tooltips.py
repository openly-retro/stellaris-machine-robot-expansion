# Given Stellaris leader trait info as YAML, generate Stellaris tooltip game code from it
import logging
import re
import sys
from yaml import safe_load
from json import load as json_load
from os import path as os_path
import argparse

from mre_common_vars import (
    TRAIT_MODIFIER_KEYS,
    BUILD_FOLDER,
    INPUT_FILES_FOR_CODEGEN,
    DEFAULT_UPPERCASE_MODIFIERS_MAP_FILES,
    LEADER_MAKING, CORE_MODIFYING,
    TOOLTIP_LOOKUP_MAP,
    GARBAGE_MODIFIERS,
)

logger = logging.getLogger(__name__)

COLOR_CODES = {
    # https://steamcommunity.com/sharedfiles/filedetails/?id=1955978558
    "orange": "§H",
    "brown": "§L",
    "yellow": "§Y",
    "green": "§G",
    "red": "§R",
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

def make_red_text(some_text):
    return f"{COLOR_CODES['red']}{some_text}{CLOSE_CODE}"

def load_modifier_keys_in_uppercase(json_files_list):
    json_data = {}
    for json_file_name in json_files_list:
        with open(json_file_name, "r") as json_file_object:
            _tmp = json_load(json_file_object)
            json_data.update(_tmp)
    logger.info(
        f"Uppercase keys data is f{sys.getsizeof(json_data)} bytes."
    )
    return json_data

""" Look for a type of modifier, and add some descriptive text before it """
modifier_key_to_tooltip_prefix_var = {
    "army_modifier": "commanding_army_effect",
    "councilor_modifier": "councilor_trait",
    "fleet_modifier": "commanding_navy_effect",
    # "modifier": "",
    "planet_modifier": "governing_planet_effect",
    "sector_modifier": "governing_sector_effect",
    # "self_modifier": "",
    "triggered_army_effect": "commanding_army_effect",
    "triggered_councilor_modifier": "councilor_trait",
    "triggered_fleet_modifier": "commanding_navy_effect",
    "triggered_planet_modifier": "governing_planet_effect",
    "triggered_sector_modifier": "governing_sector_effect",
    "triggered_self_modifier": ""
}

""" This map is to record exceptions to PDX' pattern of naming modifiers. For a good number
of cases, we can correctly guess the localisation key for a modifier by prepending 'mod_' 
to whatever the name of the modifier is, and that will link automatically to a good tooltip.

Of course, nothing is sacred or 100% consistent in the base game data, so there are going to
be numerous exceptions to this naming pattern, and unfortunately, there is no pattern 
to the exceptions. So we have to individual note them all if we are ever to make our way
to the surface here.

The key name is what we thought the tooltip reference should be.
Prepend "mre_" to the key, and that creates a link to a custom copy of the original trait text,
which normally doesn't get shown for various reasons (like dependency on Megacorp DLC, for example)

Logic: if our guess for a modifier localisation key is in the below map,
preprend 'mre_' to the localisation key.
"""
# Dicts are the fastest lookup ( O(1) ) vs searching a list ( O(n) )

# Mappings of modifiers whose tooltips dont match up
# Left side is the modifier, right side is what it actually is in base Stellaris
modifiers_dont_match_tooltip_string = {
    "mod_science_ship_survey_speed": "MOD_SHIP_SCIENCE_SURVEY_SPEED",
    "mod_species_leader_exp_gain": "MOD_LEADER_SPECIES_EXP_GAIN",
    "mod_ship_anomaly_research_speed_mult": "MOD_SHIP_ANOMALY_RESEARCH_SPEED",
}

""" These traits have a tooltip_tt entry in a localisation file """
traits_with_complete_tooltips = {
    "leader_trait_adventurous_spirit_3": "leader_trait_adventurous_spirit_3_tt",
    "leader_trait_bureaucrat_2": "leader_trait_bureaucrat_2_tt"
}

def detect_trait_modifier_permutation(trait_modifier: str,uppercase_key_store: dict) -> str:
    """ run if we couldnt find the localisation key matching the standard word order """
    trait_words = trait_modifier.split('_')
    permutation = f"MOD_{trait_words[1]}_{trait_words[0]}_{'_'.join(trait_words[2:])}".upper()
    match = permutation if uppercase_key_store.get(permutation) else ''
    if match:
        print(f"Found permutation of {trait_modifier} as {permutation}!")
    return match

def create_tooltip_for_leader(
    trait_dict, leader_class, feature="leader_making", uppercase_map_files=None
):
    if uppercase_map_files is None:
        uppercase_map_files = DEFAULT_UPPERCASE_MODIFIERS_MAP_FILES
    
    ALL_REPLACEMENT_MAPS = load_modifier_keys_in_uppercase(uppercase_map_files)
    
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
    tooltip_stem = f"{feature}_tooltip"
    # leader_trait_naturalist_3 will read "Preservation Code III"
    root = trait_dict[trait_name]

    # Displays add'l costs for higher-tier traits
    trait_cost_alt = ""
    # Append only _alt to the trait name if it's vet/paragon, there is no "traitname_alt_2" scripted effect
    # I am WRONG!! append alt ONLY IF THERE IS A SCRIPTED EFFECT BEING ATTACHED TO IT.. see https://github.com/openly-retro/stellaris-machine-robot-expansion/issues/71
    # trait_name_alt = ""
    if root.get("rarity", "") == "veteran":
        trait_cost_alt = "_alt"
        # trait_name_alt = "_alt"
    if root.get("rarity", "") == "paragon":
        trait_cost_alt = "_alt_2"
        # trait_name_alt = "_alt"
    trait_cost_tt = f"$add_xvcv_mdlc_{feature}_traits_costs_desc{trait_cost_alt}$"
    separator_ruler = "--------------"
    # trait_desc_brown_text = make_brown_text(f"${base_trait_name}_machine_desc$")
    trait_desc_brown_text = make_brown_text(f"${base_trait_name}_desc$")

    modifiers_list = []
    for modifier_key in TRAIT_MODIFIER_KEYS:
        if root.get(modifier_key):
            if descriptive_prefix := modifier_key_to_tooltip_prefix_var.get(modifier_key, None):
                modifiers_list.append(f"${descriptive_prefix}$")
            # Remove any garbage modifiers from the trait's modifiers
            modifier_subkeys = root[modifier_key].keys()
            if trait_name == "leader_trait_expertise_new_worlds_3":
                # TODO: Scale to apply to all traits if enough crud is found later
                # TODO: Make this a function
                modifiers_subset = set([ name for name in root[modifier_key].keys() ])
                modifier_subkeys = sorted(list(modifiers_subset.difference(GARBAGE_MODIFIERS)))
            for modifier_name in modifier_subkeys:
                # Check if we have a replacement tooltip for an autogenerated one,
                # and prepend mre_ so it matches with our custom definition
                replacement_check = ''
                uppercase_key_name = f"mod_{modifier_name}".upper()
                if ALL_REPLACEMENT_MAPS.get(uppercase_key_name, False):
                    # make everything lowercase, PDX in this case doesn't care
                    mod_tt_key = f"$mre_mod_{modifier_name}$".lower()
                elif chaos_variation := TOOLTIP_LOOKUP_MAP.get(f"mod_{modifier_name}", None):
                    mod_tt_key = f"${chaos_variation}$"
                # check to see if the first two words have swapped order
                elif permutated_uppercase_key_name := detect_trait_modifier_permutation(
                    uppercase_key_name, uppercase_key_store=ALL_REPLACEMENT_MAPS
                ):
                    mod_tt_key = permutated_uppercase_key_name
                elif f"mod_{modifier_name}" in modifiers_dont_match_tooltip_string:
                    replacement = modifiers_dont_match_tooltip_string[f"mod_{modifier_name}"]
                    mod_tt_key = f"${replacement}$"
                else:
                    mod_tt_key = f"$mod_{modifier_name}$".lower()
                modified_amount = root[modifier_key][modifier_name]
                if "." in str(modified_amount) and str(modified_amount)[-1].isdigit():
                    modified_amount = convert_decimal_to_percent_str(modified_amount)
                number_sign = "+" if "-" not in str(modified_amount) else ""
                # TABBED_NEW_LINE: "\n$t$" but since we already add newlines, just add tab
                indentation = "$t$"
                modifiers_list.append(
                    f"{indentation}{mod_tt_key}: {make_green_text(f"{number_sign}{modified_amount}")}"
                )
    trait_bonuses = '\\n'.join(modifiers_list)
    compiled_tooltip = ''
    remove_trait_tooltip = ''
    if feature == LEADER_MAKING:
        compiled_tooltip = (
            f'{tooltip_base}_{tooltip_stem}_{leader_class}_{trait_name}:0 \"{trait_title}{trait_cost_tt}\\n'
            f'{trait_bonuses}\\n{separator_ruler}\\n{trait_desc_brown_text}\"'
        )
    elif feature == CORE_MODIFYING:
        compiled_tooltip = (
            f'{tooltip_base}_{tooltip_stem}_add_{leader_class}_{trait_name}:0 \"{trait_title}{trait_cost_tt}\\n'
            f'{trait_bonuses}\\n{separator_ruler}\\n{trait_desc_brown_text}\"'
        )
        trait_remove_cost_alt = ""
        if root.get("rarity", "") == "veteran":
            trait_remove_cost_alt = "_alt"
        if root.get("rarity", "") == "paragon":
            trait_remove_cost_alt = "_alt_2"
        trait_remove_cost_tt = f"$remove_xvcv_mdlc_core_modifying_traits_costs_desc{trait_remove_cost_alt}$"
        remove_trait_tooltip = (
            f'{tooltip_base}_{tooltip_stem}_remove_{leader_class}_{trait_name}:0 "'
            f'{make_red_text("Remove")} Trait: {trait_title}{trait_remove_cost_tt}\\n'
            f'{trait_bonuses}\\n{separator_ruler}\\n{trait_desc_brown_text}\"'
        )
    tooltip_with_comment = 'MISSING!'
    if feature == LEADER_MAKING:
        tooltip_with_comment = f"""
  #{feature} #{leader_class} #{trait_name}
  {compiled_tooltip}
"""
    elif feature == CORE_MODIFYING:
        tooltip_with_comment = f"""
  #{feature} #{leader_class} #{trait_name}
  {compiled_tooltip}
  {remove_trait_tooltip}
"""
    return tooltip_with_comment

def convert_decimal_to_percent_str(numeric_amount: float) -> str:
    percent_float = numeric_amount * 100
    return f"{int(percent_float)}%"


if __name__ == "__main__":
    # start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait Tooltip Generator",
        description="Generate localisation tooltips for traits, using files created by mre_mod_trait_organizer.py"
    )
    parser.add_argument(
        '--uppercase_datafile',
        help='Location of a JSON file produced by mre_translation_key_normalizer.',
        required=False,
        nargs="+"
    )
    args = parser.parse_args()