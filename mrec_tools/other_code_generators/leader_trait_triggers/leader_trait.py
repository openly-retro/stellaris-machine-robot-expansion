from enum import Enum
from typing import Union, List
from dataclasses import dataclass

# This is a dict for faster searching
LEADER_MODIFIER_IDS = {
    "army_modifier": 1,
    "background_planet_modifier": 1,
    "councilor_modifier": 1,
    "federation_modifier": 1,
    "fleet_modifier": 1,
    "galcom_modifier": 1,
    "modifier": 1,
    "planet_modifier": 1,
    "sector_modifier": 1,
    "self_modifier": 1,
    "system_modifier": 1,
    "triggered_army_modifier": 1,
    "triggered_background_planet_modifier": 1,
    "triggered_councilor_modifier": 1,
    "triggered_federation_modifier": 1,
    "triggered_fleet_modifier": 1,
    "triggered_galcom_modifier": 1,
    "triggered_modifier": 1,
    "triggered_planet_modifier": 1,
    "triggered_sector_modifier": 1,
    "triggered_self_modifier": 1,
    "triggered_system_modifier": 1,
    "prerequisites": 1,
    # "allowed_origins": 1,
    "opposites": 1,
}

TRAITS_TO_EXCLUDE = {
    # commander
    "leader_trait_clone_army_commander":1,  # Cant have clone origin with machines
    "leader_trait_clone_army_fertile_commander":1,
    "leader_trait_clone_army_full_commander":1,
    "leader_trait_dragonslayer":1,  # Given via event
    "leader_trait_eager_2":1, # Cant effect leader-building/core-mod
    # "leader_trait_entrepreneur":1, # consumer goods-related trait,
    # "trait_imperial_heir":1, # Gestalt isnt an imperial form of government (but they can form the Imperium)
    # "leader_trait_academia_recruiter":1,  # requires materialist ethic,
    # "leader_trait_shroud_preacher":1,  # requires spiritualist ethic,
    "leader_trait_tzrynn_tithe":1, # given via event
    "leader_trait_emotional_support_pet":1,  # cant be given to machines
    "leader_trait_towel":1,  # given via event,
    "leader_trait_percussive_maintainer":1,  #given via event ancrel.12005
    "leader_trait_intemporal":1,  #given via event,
    # "leader_trait_robotist":1,  # just annoying to deal with code-wise,
    "leader_trait_rift_warped": 1,  # Astral planes event trait
    "leader_trait_partially_digested": 1,  # Astral planes event trait
    "leader_trait_obelisk_curse": 1,  # Astral planes event trait
    "leader_trait_foreign_consciousness": 1,  # Astral planes event trait
    "leader_trait_black_light_blinded": 1,  # Astral planes event trait
    "leader_trait_sanitary_drone": 1,  # Astral planes event trait
    "leader_trait_spacebender": 1,  # Astral planes event trait
    "leader_trait_blorg_insight": 1,  # Astral planes event trait
    # "leader_trait_adaptable": 1,
    # "leader_trait_eager": 1,
    # "leader_trait_eager_machine": 1,
    # "leader_trait_resilient": 1,
    # "leader_trait_collective_wisdom": 1,
    # "leader_trait_society_focus": 1,  # for governor
    # "leader_trait_buccaneer": 1,  # for admirals
    "leader_trait_rift_warped": 1,  # event trait
    # "leader_trait_treasure_hoarder": 1  # should be restricted via origin
}

# If any of these keys are present in the trait, grab them, and save them
# because we will need them to build the trigger to check if the trait can
# be added

class LeaderTier(Enum):

    NONE = 'none'  # (╯°□°)╯︵ ┻━┻
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'

# Describes when a trait may be gained by a leader. Values for 'leader_trait_type'
class TraitGainedType(Enum):

    BASIC = 'basic'
    VETERAN = 'veteran'
    SUBCLASS = 'subclass'
    DESTINY = 'destiny'


# A few scopes that may be used when creating the 'can we add this trait' trigger
class Scopes(Enum):

    COUNTRY = 'country'
    LEADER = 'leader'
    RULER = 'ruler'
    SPECIES = 'species'
    OWNER = 'owner'

TRAIT_ADD_REQUIREMENTS_KEYS_AND_SCOPES = {
    "leader_potential_add": Scopes.LEADER,
    "requires_traits": Scopes.LEADER,
    "requires_governments": Scopes.OWNER,
    "prerequisites": Scopes.OWNER,
    "opposites": Scopes.LEADER,
}

# The values that are allowed for leader classes
class LeaderClass(Enum):

    SCIENTIST = 'scientist'
    COMMANDER = 'commander'
    OFFICIAL = 'official'
    MIXED = 'leader'

class LeaderRarity(Enum):

    COMMON = 'common'
    VETERAN = 'veteran'
    PARAGON = 'paragon'
    FREE = 'free_or_veteran'

# There are some values that would go in place of an int, but have no
# Use like  " 'none' in CustomNoneTypes "
class CustomNoneTypes(Enum):

    NONE_STR = 'none'


# Let's try to stay organized by using this
@dataclass
class LeaderTrait:
    identifier: str  # the trait name
    leader_class_identifier: LeaderClass  # comes from inline_script
    leader_class_list: list  # comes from leader_class = { x y z }
    leader_potential_add: str
    icon: str
    rarity: LeaderRarity
    allowed_for_councilor: bool
    allowed_for_ruler: bool
    tier: LeaderTier
    custom_tooltip_with_modifiers: Union[str, None]
    modifiers: dict
    force_councilor_trait: bool = False


def trait_obj_to_json(trait_obj) -> dict:

    if type(trait_obj.leader_class_list) is list:
        leader_class_list_text = [lclass for lclass in trait_obj.leader_class_list]
    else:
        leader_class_list_text = trait_obj.leader_class_list

    return {
        "identifier": trait_obj.identifier,
        "leader_class_identifier": trait_obj.leader_class_identifier,
        "leader_class_list": leader_class_list_text,
        "leader_potential_add": trait_obj.leader_potential_add,
        "icon": trait_obj.icon,
        "rarity": trait_obj.rarity.value,
        "allowed_for_councilor": trait_obj.allowed_for_councilor,
        "allowed_for_ruler": trait_obj.allowed_for_ruler,
        "tier": trait_obj.tier.value,
        "custom_tooltip_with_modifiers": trait_obj.custom_tooltip_with_modifiers,
        "modifiers": trait_obj.modifiers,
        "force_councilor_trait": trait_obj.force_councilor_trait
    }