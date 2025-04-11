

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
