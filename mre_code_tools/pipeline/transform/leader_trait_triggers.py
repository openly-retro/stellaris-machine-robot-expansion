from json import load as json_load
import os
from pipeline.transform.sort_and_filter import iterate_traits_create_requirements_triggers
from pipeline.mre_common_vars import (
    COMPILE_FOLDER,
    FILE_NUM_PREFIXES,
    LEADER_CLASSES,
    TRIGGERS_EFFECTS_FOLDER,
)


def iterate_traits_create_requirements_triggers(traits_list) -> str:
    triggers_list = []
    for trait in traits_list:
        trait_name = [*trait][0]
        # Do not create triggers for traits that are tier 2, tier 3 etc
        if not trait_name[-1].isdigit():
            triggers_list.append(
                create_requirements_triggers_for_leader_traits(trait)
            )
    return "\n\n".join(triggers_list)

def write_leader_trait_trigger_files():
    for leader_class in LEADER_CLASSES:
        pipeline_source_file = f"{FILE_NUM_PREFIXES['filtered_traits']}_mre_{leader_class}_traits_for_codegen.json"
        buffer = ''
        input_filename = os.path.join(COMPILE_FOLDER, pipeline_source_file)
        with open(input_filename, "r") as input_file:
            buffer = json_load(input_file)
            # create text
            triggers_for_leader_traits = iterate_traits_create_requirements_triggers(buffer)
            output_file_name = f"{FILE_NUM_PREFIXES["triggers"]}_mre_{leader_class}_leader_trait_triggers.txt"
            output_file_dest = os.path.join(
                TRIGGERS_EFFECTS_FOLDER, output_file_name
            )
            with open(output_file_dest, 'w') as leader_triggers_output_file:
                leader_triggers_output_file.write(triggers_for_leader_traits)
            print(f"+ Wrote {leader_class} trait triggers to {output_file_dest}")


def create_requirements_triggers_for_leader_traits(trait: dict) -> str:
    """
    Take the first leader trait in a series, pick out the requirements,
    and create a trigger for it.
    Also factor in opposites.
    """
    requirements = []
    trait_name = [*trait][0]
    root = trait[trait_name]
    # class
    if root == {}:
        return ''
    requirements.append(
        f"leader_class = {root["leader_class"]}"
    )
    if root.get("required_subclass"):
        requirements.append(
            f"has_trait = {root["required_subclass"]}"
        )
    if root.get("rarity") == "veteran":
        requirements.append(
            f"has_skill >= 4"
        )
    elif root.get("rarity") == "paragon":
        requirements.append(
            f"has_skill >= 8"
        )
    for trigger, value in root.get("leader_potential_add", {}).items():
        if trigger == "has_skill":
            # Deal with my special greater_than_1 thing I forgot I made :psycho_smile:
            skill_level = int(value.split('_')[-1])

            if value.startswith("gt_"):
                operator = ">"
            elif value.startswith("lt_"):
                operator = "<"
            elif value.startswith("gte_"):
                operator = ">="
            elif value.startswith("lte_"):
                operator = "<="
            requirements.append(
                f"has_skill {operator} {skill_level}"
            )
        # Greeting abonimatnion
        elif trigger == "has_subclass_trait" and not root.get("required_subclass"):
            # is it just one?
            if len(value) == 1:
                requirements.append(
                    f"has_trait = {value[0]}"
                )
            else:
                subclasses = [ f"has_trait = {subclass}" for subclass in value ]
                requirements.append(
                    f"OR = {{ {" ".join(subclasses)}   }}"
                )
        elif type(value) is dict and trigger == "owner":
            # too much to deal with..
            # aHAhahAHahhAHAHA let's see what happens with this t(@_o)t
            # requirement = str(value).replace(
            #     ":"," = ").replace("'",'').replace("False","no").replace(
            #         "True",'yes').replace(',','').replace('{')
            # requirements.append(
            #     f"owner = {{ {requirement} }}"
            # )
            # shudder
            abomination = str(value).strip('{').strip('}').replace(':','=').replace("'",' ').replace(',','').replace('True','yes').replace('False','no')
            requirements.append(f"""owner = {{{abomination} }}""")

        # if it's a standard assignment, put in the list
        elif type(value) not in [dict, list]:
            if type(value) != bool:
                requirements.append(
                    f"{trigger} = {value}"
                )
            else:
                requirements.append(
                    f"{trigger} = {'yes' if value else 'no'}"
                )
    # Shroud help us
    return f"""
oxr_mdlc_leader_{root["leader_class"]}_can_add_{trait_name} = {{
    { "\n    ".join(requirements) }
}}
"""
