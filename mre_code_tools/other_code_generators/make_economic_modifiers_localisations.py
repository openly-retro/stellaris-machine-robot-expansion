from os.path import exists as os_file_exists
from os.path import join as os_path_join
from typing import List
from yaml import safe_load

"""
Look in xvcv_mdlc_common_categories, and oxr_mdlc_economic_categores
for each object, take the economic category key,
and check for generate_add_modifiers, generate_mult_modifiers

generate loc strings for all create all possible permutations, ex:

from xvcv_mdlc_world_machines_cooling_districts, generate_mult_modifiers, upkeep

mod_xvcv_mdlc_world_machines_cooling_districts_upkeep_mult: "$xvcv_mdlc_world_machines_cooling_districts$ upkeep"
mod_xvcv_mdlc_world_machines_cooling_districts_minerals_upkeep_mult: "$xvcv_mdlc_world_machines_cooling_districts$ £minerals£ upkeep"
etc.
"""

ECONOMIC_CATEGORY_CONFIG_FILES = [
    'mdlc_economic_modifiers.yml'
]
# Why the hell can't I import this from pipeline.mre_common_vars ??
GAME_RESOURCES = [
    "alloys",
    "astral_threads",
    "consumer_goods",
    "energy",
    "engineering_research",
    "exotic_gases",
    "food",
    "minerals",
    "nanites",
    "physics_research",
    "rare_crystals",
    "society_research",
    "trade",
    "unity",
    "volatile_motes",
    "zro"
]
MISSING = 'missing'

def make_subject_mod_loc_with_resource(
        subject_key: str = MISSING,
        game_resource: str = MISSING,
        modification: str = MISSING,
        operation: str = MISSING,
) -> str:
    """
    Produce localisation strings in the form of mod_<econ_category>_<resource>_<produces/cost/upkeep>_<add/mult>

    :param subject_key str: ID of the economic category
    :param game_resource str: Any game resource, like energy, minerals, etc
    :param modification str: produces, cost, upkeep
    :param operation str: what math to apply: add or mult 
    """
    first_half = f"mod_{subject_key}_{game_resource}_{modification}_{operation}: "

    resource_upkeep = f"\"${subject_key}$ £{game_resource}£ $game_resource$ $UPKEEP$\""
    resource_produces = f"\"${subject_key}$ £{game_resource}£ $game_resource$ $OUTPUT$\""
    resource_cost = f"\"${subject_key}$ £{game_resource}£ $game_resource$ $COST$\""
    
    if modification == 'upkeep':
        second_half = resource_upkeep
    elif modification == 'produces':
        second_half = resource_produces
    elif modification == 'cost':
        second_half = resource_cost
    else:
        second_half = MISSING

    complete_loc = first_half + second_half
    if MISSING in complete_loc:
        raise ValueError(
            'There are missing parameters in this loc string: '
            f"{complete_loc}"
        )
    return first_half + second_half

def make_subject_mod_loc_without_resources(
        subject_key: str = MISSING,
        modification: str = MISSING,
        operation: str = MISSING,
) -> str:
    """
    Produce localisation strings in the form of mod_<econ_category>_<produces/cost/upkeep>_<add/mult>
    Note this is the method WITHOUT resources

    :param subject_key str: ID of the economic category
    :param modification str: produces, cost, upkeep
    :param operation str: what math to apply: add or mult 
    """
    first_half = f"mod_{subject_key}_{modification}_{operation}: "
    general_upkeep = f"\"${subject_key}$ $UPKEEP$\""
    general_produces = f"\"${subject_key}$ $OUTPUT$\""
    general_cost = f"\"${subject_key}$ $COST$\""

    if modification == 'upkeep':
        second_half = general_upkeep
    elif modification == 'produces':
        second_half = general_produces
    elif modification == 'cost':
        second_half = general_cost
    else:
        second_half = MISSING

    complete_loc = first_half + second_half
    if MISSING in complete_loc:
        raise ValueError(
            'There are missing parameters in this loc string: '
            f"{complete_loc}"
        )
    return first_half + second_half


def delve_categories(subject_data: dict, collected_strings: list) -> List[str]:
    """ Process a single category """
    # breakpoint()
    subject_key = subject_data['key_id']

    # Not doing anything with this right now, but it will be used to generate loc string for the category
    # so they can be edited right from the config yml file and not have to hunt around elsewhere
    # subject_loc_name = subject_data['name']

    operations_to_iterate = []
    if subject_data.get('add'):
        operations_to_iterate.append('add')
    if subject_data.get('mult'):
        operations_to_iterate.append('mult')

    if len(operations_to_iterate):
        breakpoint()
        for operation_root_key in operations_to_iterate:
            # Go over 'mult' and/or 'add' blocks
            for modification in subject_data.get(operation_root_key):
                for game_resource in GAME_RESOURCES:
                    resource_loc_string = make_subject_mod_loc_with_resource(
                        subject_key=subject_key,
                        game_resource=game_resource,
                        modification=modification,
                        operation=operation_root_key
                    )
                    collected_strings.append(resource_loc_string)
                # mod_<subject_id>_produces_add , for example
                category_loc_string = make_subject_mod_loc_without_resources(
                    subject_key=subject_key,
                    modification=modification,
                    operation=operation_root_key
                )
                collected_strings.append(category_loc_string)
    if subject_data.get('subcategories'):
        print(f"Before processing any subcategories, we re at {len(collected_strings)}")
        for subcategory in subject_data.get('subcategories'):

            subcategory_collected_strings = delve_categories(
                subcategory, collected_strings
            )
            print(f"Got {len(subcategory_collected_strings)} out of f{subcategory}")
            collected_strings = [*subcategory_collected_strings, *collected_strings]
            if len(collected_strings) > 1000000:
                raise ValueError(
                    'Way too many modifiers.. over 1 million'
                )

    return collected_strings

    
if __name__ == "__main__":
    print(
        "0xRetro MREC: Generate zillions of economic category modifier localisation strings. \n"
        "After this is done, manually copy the files to localisation/english. "
        "(Someday that part will be automated)."
    )
    for config_file in ECONOMIC_CATEGORY_CONFIG_FILES:
        list_of_all_loc_strings = []
        buffer = ''
        with open(config_file, 'r') as source_file:
            buffer = safe_load(source_file)

        root_item = list(buffer.keys())[0]
        category_loc_strings = delve_categories(
            subject_data=buffer[root_item], collected_strings=list_of_all_loc_strings
        )
        file_contents_prefix = """
l_english:
"""
        # breakpoint()
        # contents = file_contents_prefix + "\n ".join(list_of_all_loc_strings)
        file_to_write = f"oxr_mdlc_l_english_autogenerated_{config_file}"
        with open(file_to_write) as file_obj:
            file_obj.write(
                file_contents_prefix.encode('utf-8-sig')
            )
            for loc_string in list_of_all_loc_strings:
                file_obj.write(
                    f"\n {loc_string}".encode('utf-8-sig')
                )
            file_obj.write("\n".encode('utf-8-sig'))
        print(
            f"Done processing {config_file}"
        )
    print("... Done with all config files (I hope)!")
