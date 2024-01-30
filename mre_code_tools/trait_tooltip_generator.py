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


def convert_stellaris_script_to_standard_yaml(input_string):
    # NOT aren't used in trait description anyway
    convert_tabs_to_spaces = re.sub('\t', '  ', input_string)
    remove_comment_blocks = re.sub('\n#.*', '', convert_tabs_to_spaces)
    comment_nots = re.sub('NOT', '#NOT', remove_comment_blocks)
    convert_blocks = re.sub('(?<!NOT) = \{\n', ':\n', comment_nots)
    convert_sameline_blocks = re.sub('(?<!NOT) = \{', ':', convert_blocks)
    remove_closing_braces = re.sub('\s*\}\n', '\n', convert_sameline_blocks)
    create_key_value_pairs = re.sub(' = ', ': ', remove_closing_braces)
    clean_closing_brace_no_newline = re.sub('\s*\}', '', create_key_value_pairs)
    remove_extralines = re.sub('\n{2,}', '\n', clean_closing_brace_no_newline)
    # One-liners with multiple nested {} don't cleanly replace, so comment those lines
    # since we are doing traits anyway.. dont need those lines
    comment_nested_multiline = re.sub('\n(\s)(?=((.*:){2,4}))', '\n#', remove_extralines)
    # leftover_multiline_comment = re.sub('#{2,}', '', comment_nested_multiline)
    return comment_nested_multiline


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Mostly converts Stellaris script to standard YAML"
    )
    parser.add_argument('-i', '--infile', help='Stellaris traits file to read')
    args = parser.parse_args()
    buffer = ''
    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    with open(args.infile, "r") as infile:
        buffer = convert_stellaris_script_to_standard_yaml(
            infile.read()
        )
    print(buffer)