from cz2json.converter import input_cz_output_json
from pipeline.mre_common_vars import GAME_RESOURCES

"""
Look in xvcv_mdlc_common_categories, and oxr_mdlc_economic_categores
for each object, take the economic category key,
and check for generate_add_modifiers, generate_mult_modifiers

generate loc strings for all create all possible permutations, ex:

from xvcv_mdlc_world_machines_cooling_districts, generate_mult_modifiers, upkeep

mod_xvcv_mdlc_world_machines_cooling_districts_upkeep_mult: "$xvcv_mdlc_world_machines_cooling_districts$ upkeep:"
mod_xvcv_mdlc_world_machines_cooling_districts_minerals_upkeep_mult: "$xvcv_mdlc_world_machines_cooling_districts$ £minerals£ upkeep:"
etc.
"""
