from trait_tooltip_generator import (
    create_tooltip_for_leader
)
from yaml import safe_load

def test_leader_trait_private_mines_2():
    # Common trait
    stellaris_script = """

"""
    expected_output = """

 leader_trait_private_mines_2:0 "$leader_trait_private_mines$ II"
 leader_trait_private_mines_2_desc:0 "$leader_trait_private_mines_desc$"
"""
    pass

def test_generate_leader_trait_naturalist_3():
    input_yaml = """
leader_trait_naturalist_3:
    replace_traits: "leader_trait_naturalist_2"
    inline_script:
        script: trait/icon
        CLASS: official
        ICON: "GFX_leader_trait_naturalist"
        RARITY: veteran
        COUNCIL: no
        TIER: 3
    planet_modifier:
        deposit_blockers_natural_unity_produces_add: 12
    sector_modifier:
        deposit_blockers_natural_unity_produces_add: 6
    veteran_class_locked_trait: yes
    leader_class: official scientist
"""
    parsed_yaml = safe_load(input_yaml)
    trait_output = create_tooltip_for_leader(
        parsed_yaml, "official"
    )
    expected_output = """xvcv_mdlc_leader_making_tooltip_official_leader_trait_naturalist_3:0 "§H$leader_trait_naturalist_machine$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\n$governing_planet_effect$\n$mod_deposit_blockers_natural_unity_produces_add$: §G+12§!\n$governing_sector_effect$\n$mod_deposit_blockers_natural_unity_produces_add$: §G+6§!\n--------------\n§L$leader_trait_naturalist_machine_desc$§!"
"""

    assert expected_output == trait_output
