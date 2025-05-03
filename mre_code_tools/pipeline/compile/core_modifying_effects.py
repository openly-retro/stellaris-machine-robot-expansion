from json import load as json_load
from pipeline.mre_common_vars import LEADER_SUBCLASSES, RARITIES, TRAITS_REQUIRING_DLC


def gen_core_modifying_button_effects_code(
    leader_class: str, trait_name: str, rarity: str,
    required_subclass: str='', prerequisites: list = [],
    requires_paragon_dlc: bool=False
):
    # This needs to generate two effects: add, and remove
    # xvcv_mdls_button_effects_core_modifying_traits_<LEADER_CLASS>_customgui.txt
    if rarity not in ['paragon', 'common', 'veteran']:
        raise ValueError(
            f"{rarity} rarity must be one of paragon, common, veteran"
        )
    trait_ends_in_num = trait_name[-1].isdigit()
    needs_remove_tier_num_trait_effect = True if trait_ends_in_num else False
    if trait_ends_in_num:
        trait_name_no_tier = trait_name.rsplit('_',1)[0]
    else:
        trait_name_no_tier = trait_name

    # commend out skill level trigger if it's not a veteran trait
    trait_comment = f"#{"destiny" if rarity == "paragon" else rarity} trait"

    allowances = []
    allowances.append(f"custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_{leader_class}_{trait_name}")
    if required_subclass:
        allowances.append(
            "xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = "
            f"{{ CLASS = {leader_class} ID = {required_subclass} }}"
        )
    allowances.append(f"xvcv_mdlc_core_modifying_check_trait_resources_cost_{rarity} = yes")
    allowances.append(f"xvcv_mdlc_core_modifying_check_trait_points_cost_{rarity} = yes")
    # requires skill level trigger
    if rarity in ['veteran', 'paragon']:
        allowances.append(f"xvcv_mdlc_core_modifying_trait_skill_level_{rarity}_trigger = yes")
    allowances.append("xvcv_mdlc_core_modifying_check_trait_picks = yes")
    if requires_paragon_dlc:
        allowances.append("has_paragon_dlc = yes")
    # Get fancy about picking up DLC requirements per trait
    if dlc_dependecy := TRAITS_REQUIRING_DLC.get(trait_name):
        allowances.append(f"{dlc_dependecy} = yes")
    # Assuming that prerequisites will always be tech *fingers crossed*
    if len(prerequisites):
        for tech in prerequisites:
            allowances.append(f"has_technology = {tech}")

    effects = []
    if needs_remove_tier_num_trait_effect:
        effects.append(
            f"xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = {{ ID = {trait_name_no_tier} }}"
        )
    effects.append(
        f"xvcv_mdlc_core_modifying_change_class_add_trait = {{ CLASS = {leader_class} ID = {trait_name} }}"
    )
    effects.append(
        f"hidden_effect = {{ xvcv_mdlc_core_modifying_deduct_cost_points_picks_{rarity} = yes }}"
    )

    return f"""
#{trait_name} {trait_comment}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect = {{
    potential = {{
        ruler = {{ NOT = {{ has_trait = {trait_name} }} }}
    }}
    allow = {{
        {"\n        ".join(allowances)}
    }}
    effect = {{
        {"\n        ".join(effects)}
    }}
}}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect = {{
    potential = {{
        ruler = {{ has_trait = {trait_name} }}
    }}
    allow = {{ always = yes }}
    effect = {{
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_{leader_class}_{trait_name}
        hidden_effect = {{
            ruler = {{ remove_trait = {trait_name} }}
            xvcv_mdlc_core_modifying_refund_trait_points_picks_{rarity} = yes
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
            limit = { check_variable = { which = xvcv_mdlc_core_modifying_trait_points value = 0 } }
            custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_points_tooltip
            else = { custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_points_tooltip_alt }
        }
        if = {
            limit = { check_variable = { which = xvcv_mdlc_core_modifying_trait_picks value = 0 } }
            custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_picks_tooltip
            else = { custom_tooltip = effect_xvcv_mdlc_core_modifying_trait_picks_tooltip_alt }
        }
        custom_tooltip = xvcv_mdlc_core_modifying_reset_traits_button_effect_tooltip_2
        hidden_effect = {
            ruler = {
"""

# output goes here

CORE_MODIFYING_RESET_TRAITS_BUTTON_EFFECT_FOOTER = """
            }
            xvcv_mdlc_core_modifying_clear_trait_variables_effect = yes
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
        with open(trait_json_data_path, "r") as codegen_stream:
            _tmp = json_load(codegen_stream)
            for rarity in RARITIES:
                if not _tmp['core_modifying_traits'].get(rarity):
                    continue
                for trait in _tmp['core_modifying_traits'][rarity]:
                    trait_name = [*trait][0]
                    root = trait[trait_name]
                    rarity = root['rarity']
                    effect_contents_items.append(
                        ruler_effect_line.format(
                            trait_name=trait_name,
                            rarity=rarity,
                            indent=indent
                        )
                    )
    subclass_effect_line = (
        "if = {{ limit = {{ has_trait = {trait_name} }} remove_trait = {trait_name} prev ="
        " {{ xvcv_mdlc_core_modifying_trait_return_cost_effect = yes }} }}"
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
