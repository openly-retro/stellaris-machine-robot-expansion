from generate_trait_tooltips import (
    create_tooltip_for_leader
)
from yaml import safe_load

"""
We do encode on the trait output to stop pytest from expanding \n
"""

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
    expected_output = """
#leader_making #official #leader_trait_naturalist_3
xvcv_mdlc_leader_making_tooltip_official_leader_trait_naturalist_3:0 "§H$leader_trait_naturalist$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$governing_planet_effect$\\n$mod_deposit_blockers_natural_unity_produces_add$: §G+12§!\\n$governing_sector_effect$\\n$mod_deposit_blockers_natural_unity_produces_add$: §G+6§!\\n--------------\\n§L$leader_trait_naturalist_desc$§!"
"""

    assert expected_output.encode('utf-8') == trait_output.encode('utf-8')

def test_leader_trait_aggressive_2_fleet_modifier():
    trait_data = {
        "leader_trait_aggressive_2": {
            "trait_name": "leader_trait_aggressive_2",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_aggressive",
            "rarity": "common",
            "fleet_modifier": {
                "ship_fire_rate_mult": 0.05,
                "ship_weapon_damage": 0.05
            },
            "requires_paragon_dlc": False
        }
    }
    expected_output = """
#leader_making #commander #leader_trait_aggressive_2
xvcv_mdlc_leader_making_tooltip_commander_leader_trait_aggressive_2:0 "§H$leader_trait_aggressive$ II§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$commanding_navy_effect$\\n$mod_ship_fire_rate_mult$: §G+5%§!\\n$mod_ship_weapon_damage$: §G+5%§!\\n--------------\\n§L$leader_trait_aggressive_desc$§!"
"""
    actual = create_tooltip_for_leader(trait_data, leader_class="commander")
    # breakpoint()
    assert expected_output.encode('utf-8') == actual.encode('utf-8')

def test_leadermaking_tooltip_leader_trait_generator_focus_3():
    """ Check mre_ gets substituted in front of mod_ in certain cases """
    test_data = {
        "leader_trait_generator_focus_3": {
            "trait_name": "leader_trait_generator_focus_3",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_financial",
            "rarity": "veteran",
            "planet_modifier": {
                "planet_jobs_energy_produces_mult": 0.45
            },
            "sector_modifier": {
                "planet_jobs_energy_produces_mult": 0.225
            },
            "requires_paragon_dlc": False,
            "custom_tooltip": "only_one_governor_focus"
        }
    }
    expected = """
#leader_making #commander #leader_trait_generator_focus_3
xvcv_mdlc_leader_making_tooltip_commander_leader_trait_generator_focus_3:0 "§H$leader_trait_generator_focus$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$governing_planet_effect$\\n$mre_mod_planet_jobs_energy_produces_mult$: §G+45%§!\\n$governing_sector_effect$\\n$mre_mod_planet_jobs_energy_produces_mult$: §G+22%§!\\n--------------\\n§L$leader_trait_generator_focus_desc$§!"
"""
    actual = create_tooltip_for_leader(test_data, leader_class="commander")
    assert expected.encode('utf-8') == actual.encode('utf-8')
