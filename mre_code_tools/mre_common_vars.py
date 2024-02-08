import os

TRAIT_MODIFIER_KEYS = (
    "army_modifier",
    "councilor_modifier",
    "fleet_modifier",
    "modifier",
    "planet_modifier",
    "sector_modifier",
    "self_modifier",
    "triggered_army_modifier",
    "triggered_councilor_modifier",
    "triggered_fleet_modifier",
    "triggered_planet_modifier",
    "triggered_sector_modifier",
    "triggered_self_modifier",
)

MISSING = "MISSING_VALUE"
PLACEHOLDER = "PLACEHOLDER_VALUE"

BUILD_FOLDER = os.path.join(
    os.getcwd(),
    'build'
)

LEADER_CLASSES = (
    "commander", "official", "scientist"
)

BASE_TRAIT_FILES = (
    "00_admiral_traits.txt",
    "00_general_traits.txt",
    "00_generic_leader_traits.txt",
    "00_governor_traits.txt",
    "00_scientist_traits.txt",
    "00_starting_ruler_traits.txt"
)
