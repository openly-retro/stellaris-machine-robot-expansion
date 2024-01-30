from trait_tooltip_generator import (
    convert_stellaris_script_to_standard_yaml,
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

def test_convert_stellaris_script_to_standard_yaml():

    test_input = """
leader_trait_private_mines_2 = {
    replace_traits = { "leader_trait_private_mines" }
    inline_script = {
        script = trait/icon
        CLASS = leader
        ICON = "GFX_leader_trait_private_mines"
        RARITY = common
        COUNCIL = no
        TIER = 2
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                NOT = { is_planet_class = pc_shattered_ring_habitable }
            }
            trait_is_gestalt_check = no
        }
        job_miner_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                NOT = { is_planet_class = pc_shattered_ring_habitable }
            }
            trait_is_gestalt_check = yes
        }
        job_mining_drone_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                is_planet_class = pc_shattered_ring_habitable
            }
            trait_is_gestalt_check = no
        }
        job_scrap_miner_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                is_planet_class = pc_shattered_ring_habitable
            }
            trait_is_gestalt_check = yes
        }
        job_scrap_miner_drone_add = 4
    }
    planet_modifier = {
        planet_miners_minerals_produces_mult = 0.10
    }
    sector_modifier = {
        planet_miners_minerals_produces_mult = 0.05
    }
    leader_class = { commander scientist official }
"""
    actual_output = convert_stellaris_script_to_standard_yaml(test_input)

    expected_output = """
leader_trait_private_mines_2:
    replace_traits: "leader_trait_private_mines"
    inline_script:
        script: trait/icon
        CLASS: leader
        ICON: "GFX_leader_trait_private_mines"
        RARITY: common
        COUNCIL: no
        TIER: 2
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
#               #NOT: { is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: no
        job_miner_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
#               #NOT: { is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: yes
        job_mining_drone_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
                is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: no
        job_scrap_miner_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
                is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: yes
        job_scrap_miner_drone_add: 4
    planet_modifier:
        planet_miners_minerals_produces_mult: 0.10
    sector_modifier:
        planet_miners_minerals_produces_mult: 0.05
    leader_class: commander scientist official
"""
    assert expected_output == actual_output

def test_convert_stellaris_script__destiny_trait():
    
    stellaris_script = """
leader_trait_naturalist_3 = {
    replace_traits = { "leader_trait_naturalist_2" }
    inline_script = {
        script = trait/icon
        CLASS = official
        ICON = "GFX_leader_trait_naturalist"
        RARITY = veteran
        COUNCIL = no
        TIER = 3
    }
    planet_modifier = {
        deposit_blockers_natural_unity_produces_add = 12
    }
    sector_modifier = {
        deposit_blockers_natural_unity_produces_add = 6
    }
    veteran_class_locked_trait = yes
    leader_class = { official scientist }
}
"""

    expected_output = """
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
    actual_output = convert_stellaris_script_to_standard_yaml(stellaris_script)

    assert expected_output == actual_output

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
