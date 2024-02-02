from stellaris_yaml_converter import (
    convert_stellaris_script_to_standard_yaml,
    convert_leader_class_definitions_to_lists,
    concatenate_multiline_has_trait_definitions
)

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
    leader_class: ['commander', 'scientist', 'official']
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
    leader_class: ['official', 'scientist']
"""
    actual_output = convert_stellaris_script_to_standard_yaml(stellaris_script)

    assert expected_output == actual_output

def test_concat_multi_has_trait_lines():
    test_data = """
    leader_potential_add:
        OR:
            has_paragon_dlc: no
            has_trait: subclass_commander_admiral
            has_trait: subclass_scientist_explorer
            has_trait: subclass_scientist_councilor
"""
    actual = concatenate_multiline_has_trait_definitions(test_data)
    expected = """
    leader_potential_add:
        OR:
            has_paragon_dlc: no
            has_trait: ['subclass_commander_admiral', 'subclass_scientist_explorer', 'subclass_scientist_councilor']
"""
    assert expected == actual

def test_convert_stellaris_script__scout_double_subclass():
    test_data = """

####################################
# SHARED TRAITS BLOCKED IN PARAGON #
####################################

leader_trait_scout = {
    veteran_class_locked_trait = yes
    inline_script = {
        script = trait/icon
        CLASS = leader
        ICON = GFX_leader_trait_scout
        RARITY = free_or_veteran
        COUNCIL = no
        TIER = 1
    }
    leader_potential_add = {
        OR = {
            has_paragon_dlc = no
            has_trait = subclass_commander_admiral
            has_trait = subclass_scientist_explorer
            has_trait = subclass_scientist_councilor
        }
    }
    modifier = {
        ship_speed_mult = 0.05 # some comment
        ship_hyperlane_range_add = 2
        fleet_mia_time_mult = -0.1
    }
    triggered_modifier = {
        potential = { has_first_contact_dlc = yes }
        ship_cloaking_strength_add = 1
    }
    leader_class = { commander scientist }
    selectable_weight = {
        inline_script = paragon/subclass_free_trait_weight
        inline_script = paragon/pilot_weight_mult
        inline_script = {
            script = paragon/dual_subclass_weight_mult
            SUBCLASS_1 = commander_admiral
            SUBCLASS_2 = scientist_explorer
        }
    }
}
"""
    expected = """
leader_trait_scout:
    veteran_class_locked_trait: yes
    inline_script:
        script: trait/icon
        CLASS: leader
        ICON: GFX_leader_trait_scout
        RARITY: free_or_veteran
        COUNCIL: no
        TIER: 1
    leader_potential_add:
        OR:
            has_paragon_dlc: no
            has_trait: ['subclass_commander_admiral', 'subclass_scientist_explorer', 'subclass_scientist_councilor']
    modifier:
        ship_speed_mult: 0.05 # some comment
        ship_hyperlane_range_add: 2
        fleet_mia_time_mult: -0.1
    triggered_modifier:
#        potential: has_first_contact_dlc: yes
        ship_cloaking_strength_add: 1
    leader_class: ['commander', 'scientist']
    selectable_weight:
 #       inline_script: paragon/subclass_free_trait_weight
 #       inline_script: paragon/pilot_weight_mult
        inline_script:
            script: paragon/dual_subclass_weight_mult
            SUBCLASS_1: commander_admiral
            SUBCLASS_2: scientist_explorer
"""


def test_structuring_leader_class_lists():

    test_data = """
  leader_class: commander official scientist
  leader_class: official
"""
    actual_output = convert_leader_class_definitions_to_lists(test_data)

    expected_output = """
  leader_class: ['commander', 'official', 'scientist']
  leader_class: ['official']
"""
    assert expected_output == actual_output

def test_replace_var_symbol():

    test_data = """
selectable_weight = {
    weight = @shared_trait_weight
    inline_script = paragon/governor_weight_mult
    inline_script = {
        script = "paragon/existing_trait_weight_mult"
        TRAIT = leader_trait_bureaucrat
    }
}
"""
    actual_output = convert_stellaris_script_to_standard_yaml(test_data)
    expected_output = """
selectable_weight:
    weight: var_shared_trait_weight
    inline_script: paragon/governor_weight_mult
    inline_script:
        script: "paragon/existing_trait_weight_mult"
        TRAIT: leader_trait_bureaucrat
"""
    assert expected_output == actual_output
