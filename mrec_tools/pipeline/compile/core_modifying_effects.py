from json import load as json_load
from pipeline.transform.leader_trait_triggers import create_requirements_triggers_for_leader_traits, process_complex_tech_requirements
from pipeline.mre_common_vars import LEADER_SUBCLASSES, RARITIES, TRAITS_REQUIRING_DLC


def gen_core_modifying_button_effects_code(
    leader_class: str, trait_name: str, trait_data: dict,
    requires_paragon_dlc: bool=False
):
    # This needs to generate two effects: add, and remove
    # xvcv_mdls_button_effects_core_modifying_traits_<LEADER_CLASS>_customgui.txt
    if trait_data['rarity'] not in ['paragon', 'common', 'veteran', 'free_or_veteran']:
        # It pains me to add 'free_or_veteran' .. WHICH IS IT !?
        raise ValueError(
            f"{rarity} rarity must be one of paragon, common, veteran"
        )
    if trait_data['rarity'] == 'free_or_veteran':
        # All the traits that have this foolish schroedinger's rarity ..
        # are veteran traits!
        rarity = 'veteran'
    else:
        rarity = trait_data['rarity']
    trait_ends_in_num = trait_name[-1].isdigit()
    needs_remove_tier_num_trait_effect = True if trait_ends_in_num else False
    if trait_ends_in_num:
        trait_name_no_tier = trait_name.rsplit('_',1)[0]
    else:
        trait_name_no_tier = trait_name

    # commend out skill level trigger if it's not a veteran trait
    trait_comment = f"#{"destiny" if rarity == "paragon" else rarity} trait"

    country_checks = [] # tech, if ever applicable ??
    ruler_checks = []   # leader-specific checks (lvl, points)
    global_checks = []  # DLCs, mainly
    if required_subclass := trait_data.get('required_subclass'):
        ruler_checks.append(
            "xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = "
            f"{{ CLASS = {leader_class} ID = {required_subclass} }}"
        )

    # requires skill level trigger
    if rarity in ['veteran', 'paragon']:
        ruler_checks.append(f"xvcv_mdlc_core_modifying_trait_skill_level_{rarity}_trigger = yes")
    if requires_paragon_dlc:
        global_checks.append("has_paragon_dlc = yes")
    # Get fancy about picking up DLC requirements per trait
    if dlc_dependecy := TRAITS_REQUIRING_DLC.get(trait_name):
        global_checks.append(f"{dlc_dependecy} = yes")

    if tech_prereqs := trait_data.get('prerequisites'):
        # This can have leader-specific checks, and tech checks in the form of:
        # owner = { trigger ... }
        ruler_trigger_block = create_requirements_triggers_for_leader_traits(
            trait=trait_data, generate_for_ruler=True
        )
        ruler_checks.append(ruler_trigger_block)

    hidden_ruler_effects = []
    if needs_remove_tier_num_trait_effect:
        hidden_ruler_effects.append(
            f"xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = {{ ID = {trait_name_no_tier} }}"
        )

    # Select the correct tooltip for showing costs for this trait
    trait_costs_level = ""
    if rarity == 'veteran':
        trait_costs_level = "_alt"
    elif rarity == 'paragon':
        trait_costs_level = "_alt_2"
    
    rendered_country_checks = "\n            ".join(country_checks) if len(country_checks) else ''
    rendered_ruler_checks = "\n            ".join(ruler_checks) if len(ruler_checks) else ''
    rendered_global_checks = "\n        ".join(global_checks) if len(global_checks) else ''

    return f"""
#{trait_name} {trait_comment}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect = {{
    potential = {{
        ruler = {{ NOT = {{ has_trait = {trait_name} }} }}
    }}
    allow = {{
        root.owner = {{
            xvcv_mdlc_core_modifying_check_trait_resources_cost_{rarity} = yes
            {rendered_country_checks}
        }}
        ruler = {{
            xvcv_mdlc_core_modifying_ruler_check_trait_points_cost_{rarity} = yes
            xvcv_mdlc_core_modifying_ruler_check_trait_picks = yes
            {rendered_ruler_checks}
        }}
        {rendered_global_checks}
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_{leader_class}_{trait_name}
    }}
    effect = {{
        custom_tooltip = add_xvcv_mdlc_core_modifying_traits_costs_desc{trait_costs_level}
        hidden_effect = {{
            ruler = {{
                xvcv_mdlc_core_modifying_ruler_deduct_trait_points_{rarity} = yes
                {"\n                ".join(hidden_ruler_effects)}
            }}
            root.owner = {{
                xvcv_mdlc_core_modifying_country_deduct_trait_costs_{rarity} = yes
            }}
        }}
        ruler = {{
            add_trait = {trait_name}       
        }}
    }}
}}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect = {{
    potential = {{
        ruler = {{ has_trait = {trait_name} }}
    }}
    allow = {{ always = yes }}
    effect = {{
        custom_tooltip = remove_xvcv_mdlc_core_modifying_traits_costs_desc{trait_costs_level}
        ruler = {{
            remove_trait = {trait_name}
        }}
        hidden_effect = {{
            ruler = {{
                xvcv_mdlc_core_modifying_ruler_refund_trait_points_picks_{rarity} = yes
            }}
            root.owner = {{
                xvcv_mdlc_core_modifying_country_refund_trait_cost_{rarity} = yes
            }}
        }}
    }}
}}
"""

CORE_MODIFYING_RESET_TRAITS_BUTTON_EFFECT_HEADER = """
xvcv_mdlc_core_modifying_reset_traits_button_effect = {
    potential = { always = yes }
    allow = { xvcv_mdlc_core_modifying_reset_traits_trigger = yes }
    effect = {
        custom_tooltip = xvcv_mdlc_core_modifying_reset_traits_button_effect_tooltip
        if = {
            limit = {
                ruler = {
                    check_variable = { which = xvcv_mdlc_core_modifying_trait_points value = 0 } }
                }
            custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_points_tooltip
            # else = { custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_points_tooltip_alt }
        }
        if = {
            limit = {
                ruler = {
                    check_variable = { which = xvcv_mdlc_core_modifying_trait_picks value = 0 } }
                }
            custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_picks_tooltip
            # else = { custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_picks_tooltip_alt }
        }
        custom_tooltip = xvcv_mdlc_core_modifying_reset_traits_button_effect_tooltip_2
        hidden_effect = {
            ruler = {
"""

# output goes here

CORE_MODIFYING_RESET_TRAITS_BUTTON_EFFECT_FOOTER = """
                xvcv_mdlc_core_modifying_reset_ruler_points_picks_effect = yes
            }
        }
    }
}
"""


def gen_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines(input_files_list):
    """ Print the lines that get pasted in the middle so all the new traits and subclasses get reset
    when players click the brain button in the middle.
        Then these lines get pasted in the effect.
    """
    effect_contents_items = []
    indent = "                "
    ruler_effect_line = (
        "{indent}if = {{ limit = {{ has_trait = {trait_name} }} remove_trait = {trait_name} prev ="
        " {{ xvcv_mdlc_core_modifying_refund_trait_resources_cost_{rarity} = yes }} }}"
    )
    for trait_json_data_path in input_files_list:
        # Iterate through mrec_tools/compile/20_mre_<leader_class>_traits_for_codegen.json
        # On opening each file we know what leader class it is
        with open(trait_json_data_path, "r") as codegen_stream:
            _tmp = json_load(codegen_stream)
            for rarity in RARITIES:
                if not _tmp['core_modifying_traits'].get(rarity):
                    continue
                for trait in _tmp['core_modifying_traits'][rarity]:
                    trait_name = [*trait][0]
                    root = trait[trait_name]
                    rarity = root['rarity']
                    # Traits with free_or_veteran are almost always veteran traits
                    if rarity == 'free_or_veteran':
                        rarity = 'veteran'
                    effect_contents_items.append(
                        ruler_effect_line.format(
                            trait_name=trait_name,
                            rarity=rarity,
                            indent=indent
                        )
                    )
    subclass_effect_line = (
        "if = {{ limit = {{ has_trait = {trait_name} }} remove_trait = {trait_name} prev ="
        " {{ xvcv_mdlc_core_modifying_country_refund_trait_cost_effect = yes }} }}"
    )
    for subclass in LEADER_SUBCLASSES:
        alt_modifier = ""
        effect_contents_items.append(
            subclass_effect_line.format(trait_name=subclass, alt_modifier=alt_modifier)
        )
    return f"""
{CORE_MODIFYING_RESET_TRAITS_BUTTON_EFFECT_HEADER}
{"\n".join(effect_contents_items)}
{CORE_MODIFYING_RESET_TRAITS_BUTTON_EFFECT_FOOTER}
"""


def gen_xvcv_mdlc_core_modifying_still_has_subclass_traits_picked(input_files_list):
        header = """
xvcv_mdlc_core_modifying_still_has_subclass_traits_picked = {
    optimize_memory
    # Restrict a subclass from being removed from the ruler
    # if there are T2/T3/destiny subclass-specific traits chosen
    custom_tooltip = {
        text = trigger_xvcv_mdlc_core_modifying_must_remove_subclass_trait_notice
    }
    ruler = {
        switch = {
            trigger = leader_class
"""
        footer = """
        }
    }
}
"""
        indent = "                    "
        ruler_traits = {
            'commander': [],
            'official': [],
            'scientist': []
        }

        for trait_json_data_path in input_files_list:
            with open(trait_json_data_path, "r") as codegen_stream:
                _tmp = json_load(codegen_stream)
                for rarity in RARITIES:
                    if not _tmp['core_modifying_traits'].get(rarity):
                        continue
                    for trait in _tmp['core_modifying_traits'][rarity]:
                        trait_name = [*trait][0]
                        root = trait[trait_name]
                        leader_class = root['leader_class']
                        ruler_traits[leader_class].append(
                            f"has_trait = {trait_name}"
                        )
        
        block_official = f"""
            official = {{
                OR = {{
                    {"\n                    ".join(ruler_traits['official'])}
                }}
            }}
"""
        block_commander = f"""
            commander = {{
                OR = {{
                    {"\n                    ".join(ruler_traits['commander'])}
                }}
            }}
"""
        block_scientist = f"""
            scientist = {{
                OR = {{
                    {"\n                    ".join(ruler_traits['scientist'])}
                }}
            }}
"""
        return f"""
{header}
{block_official}
{block_commander}
{block_scientist}
{footer}
"""
