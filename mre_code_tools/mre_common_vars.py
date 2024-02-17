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

BUTTON_EFFECTS_FOLDER = os.path.join(
    os.getcwd(),
    'common', 'button_effects'
)

LOCALISATION_HEADER = "l_english:\n"

# TODO: Write all the English localisations to all the other language folders!!
LOCALISATION_FOLDER = os.path.join(
    os.getcwd(),
    'localisation',
    'english'
)
OUTPUT_FILE_BUTTON_FX_NAME = "xvcv_mdlc_button_effects_{feature}_{leader_class}_customgui.txt"
OUTPUT_FILE_LOCALISATION_NAME = "xvcv_mdlc_l_english_{feature}_{leader_class}_customgui.yml"

""" We will write directly to these files during the code generation workflow """
OUTPUT_FILES_DESTINATIONS = {
    "core_modifying": {
        "effects": {
            "commander": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="core_modifying", leader_class="commander"
                )
            ),
            "official": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="core_modifying", leader_class="official"
                )
            ),
            "scientist": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="core_modifying", leader_class="scientist"
                )
            ),
        },
        "tooltips": {
            "commander": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="core_modifying", leader_class="commander"
                )
            ),
            "official": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="core_modifying", leader_class="official"
                )
            ),
            "scientist": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="core_modifying", leader_class="scientist"
                )
            ),
        },
    },
    "leader_making": {
        "effects": {
            "commander": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="leader_making", leader_class="commander"
                )
            ),
            "official": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="leader_making", leader_class="official"
                )
            ),
            "scientist": os.path.join(
                BUTTON_EFFECTS_FOLDER,
                OUTPUT_FILE_BUTTON_FX_NAME.format(
                    feature="leader_making", leader_class="scientist"
                )
            ),
        },
        "tooltips": {
            "commander": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="leader_making", leader_class="commander"
                )
            ),
            "official": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="leader_making", leader_class="official"
                )
            ),
            "scientist": os.path.join(
                LOCALISATION_FOLDER,
                OUTPUT_FILE_LOCALISATION_NAME.format(
                    feature="leader_making", leader_class="scientist"
                )
            ),
        },
    },
}

LEADER_CLASSES = (
    "commander", "official", "scientist"
)

LEADER_SUBCLASSES = (
    "subclass_commander_general",
    "subclass_commander_councilor",
    "subclass_commander_governor",
    "subclass_commander_admiral",
    "subclass_scientist_explorer",
    "subclass_scientist_councilor",
    "subclass_scientist_governor",
    "subclass_scientist_scholar",
    "subclass_official_economy_councilor",
    "subclass_official_diplomacy_councilor",
    "subclass_official_governor",
    "subclass_official_delegate",
)

# Used to add a comment in code to refer to the in-game name for the subclass
LEADER_SUBCLASSES_NAMES = {
    "subclass_commander_general": "general",
    "subclass_commander_councilor": "strategist",
    "subclass_commander_governor": "commissioner",
    "subclass_commander_admiral": "admiral",
    "subclass_scientist_explorer": "explorer",
    "subclass_scientist_councilor": "statistician",
    "subclass_scientist_governor": "analyst",
    "subclass_scientist_scholar": "scholar",
    "subclass_official_economy_councilor": "advisor",
    "subclass_official_diplomacy_councilor": "ambassador",
    "subclass_official_governor": "industrialist",
    "subclass_official_delegate": "delegate"
}

BASE_TRAIT_FILES = (
    "00_generic_leader_traits.txt",
    "00_admiral_traits.txt",
    "00_general_traits.txt",
    "00_governor_traits.txt",
    "00_scientist_traits.txt",
    "00_starting_ruler_traits.txt"
)

# These subclasses can't be added to the ruler because of a NAND with gestalt consciousness
# Or they just don't work (ruler can't be admiral/general)
EXCLUDE_SUBCLASSES_FROM_CORE_MODIFYING = {
    "subclass_official_governor": 1,
    "subclass_official_delegate":1,
    "subclass_scientist_explorer":1,
    "subclass_scientist_governor":1,
    "subclass_scientist_scholar":1,
    "subclass_commander_general": 1,
    "subclass_commander_governor": 1,
    "subclass_commander_admiral": 1,
}
# Files created by sort_merge_traits_files
PIPELINE_OUTPUT_FILES = [
    f"00_mre_{leader_class}_traits.json" for leader_class in LEADER_CLASSES
]

# Files created by mre_process_traits_for_codegen
INPUT_FILES_FOR_CODEGEN = (
    "99_mre_commander_traits_for_codegen.json",
    "99_mre_official_traits_for_codegen.json",
    "99_mre_scientist_traits_for_codegen.json"
)

DEFAULT_UPPERCASE_MODIFIERS_MAP_FILES = [
    os.path.join(BUILD_FOLDER, 'modifiers_l_english_upper.json'),
    os.path.join(BUILD_FOLDER, 'megacorp_l_english_upper.json'),
    os.path.join(BUILD_FOLDER, 'paragon_2_l_english_upper.json')
]

GENERATED_CODE_TYPES = (
  "effects",
  "gui",
  "tooltips",
)
LEADER_MAKING = "leader_making"
CORE_MODIFYING = "core_modifying"

UNICORN = '''
                \\
                 \%,     ,'     , ,.
                  \%\,';/J,";";";;,,.
     ~.------------\%;((`);)));`;;,.,-----------,~
    ~~:           ,`;@)((;`,`((;(;;);;,`         :~~
   ~~ :           ;`(@```))`~ ``; );(;));;,      : ~~
  ~~  :            `X `(( `),    (;;);;;;`       :  ~~
 ~~~~ :            / `) `` /;~   `;;;;;;;);,     :  ~~~~
~~~~  :           / , ` ,/` /     (`;;(;;;;,     : ~~~~
  ~~~ :          (o  /]_/` /     ,);;;`;;;;;`,,  : ~~~
   ~~ :           `~` `~`  `      ``;,  ``;" ';, : ~~
    ~~:                             `'   `'  `'  :~~
     ~`-----------------------------------------`~
'''
