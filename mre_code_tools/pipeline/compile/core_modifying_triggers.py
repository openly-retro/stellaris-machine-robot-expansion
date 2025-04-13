from pipeline.mre_common_vars import LEADER_SUBCLASSES, RARITIES


from json import load as json_load


def gen_xvcv_mdlc_core_modifying_ruler_traits_trigger(input_files_list):
    """ Entire trigger with updated list of 3.10 traits for core modifying. for copy/paste """
    indentation = " "*8
    preamble = """
xvcv_mdlc_core_modifying_ruler_traits_trigger = {
    optimize_memory
    OR = {"""
    closing = """    }
}
"""
    buffer = set()
    for trait_json_data_path in input_files_list:
        with open(trait_json_data_path, "r") as codegen_stream:
            _tmp = json_load(codegen_stream)
            for rarity in RARITIES:
                if not _tmp['core_modifying_traits'].get(rarity):
                    continue
                trait_names_list = [
                    [*trait][0] for trait in _tmp['core_modifying_traits'][rarity]
                ]
                buffer = buffer | set(trait_names_list)

    trait_conditions_list = []
    for subclass in LEADER_SUBCLASSES:
        trait_conditions_list.append(
            f"{indentation}has_trait = {subclass}"
        )
    for unique_trait in buffer:
        trait_conditions_list.append(
            f"{indentation}has_trait = {unique_trait}"
        )
    compiled_trigger = f"""{preamble}
{"\n".join(sorted(trait_conditions_list))}
{closing}"""
    return compiled_trigger