from typing import List
from pipeline.compile.gui_headers import gui_header
from pipeline.compile.gui_headers import gui_footer
from datetime import datetime
from pipeline.mre_common_vars import EXCLUDE_SUBCLASSES_FROM_CORE_MODIFYING, LEADER_SUBCLASSES_NAMES, RARITIES


def gen_core_modifying_trait_gui_code(
    leader_class, trait_name, column_num, row_num,
    gfx_sprite_name,
    is_xvcv_custom_trait=False, is_veteran_trait=False, is_destiny_trait=False
):
    root_gfx_name = "GFX_xvcv_mdlc_leader_trait_background"
    effect_button_background_gfx = f"{root_gfx_name}_green"
    effect_button_background_gfx_red = f"{root_gfx_name}_red"
    if is_veteran_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_veteran"
        effect_button_background_gfx_red = f"{effect_button_background_gfx}_red"
    elif is_destiny_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_destiny"
        effect_button_background_gfx_red = f"{effect_button_background_gfx}_red"
    return f"""
# {leader_class}: {trait_name}
containerWindowType = {{
    name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}"
    position = {{ x = @xvcv_mdlc_core_modifying_trait_position_column_{column_num} y = @xvcv_mdlc_core_modifying_trait_position_row_{row_num} }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_bg"
        position = {{ x = @xvcv_mdlc_core_modifying_traits_background_offset_width y = @xvcv_mdlc_core_modifying_traits_background_offset_height }}
        spriteType = "{effect_button_background_gfx}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_bg"
        position = {{ x = @xvcv_mdlc_core_modifying_traits_background_offset_width y = @xvcv_mdlc_core_modifying_traits_background_offset_height }}
        spriteType = "{effect_button_background_gfx_red}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect"
    }}
}}
"""


def gen_core_modifying_leader_subclass_gui_code(
    subclass: str, column_num: int, row_num: int
) -> str:
    """ Subclass pickers for the core-modifying GUI"""
    leader_class = subclass.split('_')[1]
    return f"""
#{leader_class} #{subclass} #{LEADER_SUBCLASSES_NAMES[subclass]}
containerWindowType = {{
    name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{subclass}"
    position = {{ x = @xvcv_mdlc_core_modifying_trait_position_column_{column_num} y = @xvcv_mdlc_core_modifying_trait_position_row_{row_num} }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{subclass}_add"
        position = {{ x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }}
        spriteType = "GFX_leader_{subclass}_medium"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{subclass}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{subclass}_remove"
        position = {{ x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }}
        spriteType = "GFX_leader_{subclass}_medium_red"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{subclass}_remove_button_effect"
    }}
}}
"""


def iterate_traits_make_coremodifying_gui_code(organized_traits_dict, for_class: str):
    """ The core-modifying GUI sections for leader classes are oddly shaped.
    the 'admiral' section has to have shorter rows than the other sections, but 
    only for the first 3 rows."""

    header_classname_spaced = ' '.join([char for char in for_class])
    header = gui_header.format(
        classname=header_classname_spaced,
        now=str(datetime.now())
    )
    footer = gui_footer.format(
        classname=header_classname_spaced
    )
    gui_code_bloblist = [header,]
    # To accomodate the irregular shape of the container,
    # The first row for Commander has 4, the second row has 5, and the rest are 6 
    row_width_limits = {
        "1": 4,
        "2": 5
    }
    trait_column_num = 3 if for_class == "official" else 2  # offset for the subclass pickers
    trait_row_num = 1
    for rarity_level in RARITIES:
        for leader_trait in organized_traits_dict["core_modifying_traits"][rarity_level]:
            trait_name = [*leader_trait][0]
            root = leader_trait[trait_name]
            trait_gui_code = gen_core_modifying_trait_gui_code(
                leader_class=for_class,
                gfx_sprite_name=root['gfx'],
                trait_name=trait_name,
                column_num=trait_column_num,
                row_num=trait_row_num,
                is_veteran_trait=(root.get('rarity')=="veteran"),
                is_destiny_trait=(root.get('rarity')=="paragon"),
            )
            # Advance the x / y coordinates
            trait_column_num = trait_column_num + 1
            if for_class=="commander":
                # Special maths rules
                if trait_row_num == 1:
                    # Go to the next row after 4 traits
                    if trait_column_num > 4:
                        trait_row_num = trait_row_num + 1
                        trait_column_num = 1
                elif trait_row_num == 2:
                    # Go to the next row after 5 traits
                    if trait_column_num > 5:
                        trait_row_num = trait_row_num + 1
                        trait_column_num = 1
                else:
                    # Permit only 6 traits in a row therafter, like normal
                    if trait_column_num > 6:
                        trait_column_num = 1
                        trait_row_num = trait_row_num + 1
            else:
                # No special x / y rules for the other classes
                if trait_column_num > 6:
                    trait_column_num = 1
                    trait_row_num = trait_row_num + 1
            gui_code_bloblist.append(trait_gui_code)

    gui_code_bloblist.append(footer)
    return ''.join(gui_code_bloblist)


def iterate_subclasses_make_core_modifying_subclasses_gui_code(subclasses_list: List[str]) -> str:
    """ Iterate over a SORTED LIST of subclasses, 4 each per class
    I'm too tired to divide subclasses by classes and then iterate leader classes
    to do each subclass, so here just make gui code for 4 subclasses and
    reset the column number after every 4
    """
    header = """
############################
## {leader_class} SUBCLASSES
############################
"""
    gui_blob_list = []
    row_num = 1
    column_num = 1
    for subclass in subclasses_list:
        # Cheat a little, for every 4 subclasses, reset the column, but keep the same row number
        # Then we just carefully copy/paste the subclasses into their respective spots in the GUI file
        if subclass in EXCLUDE_SUBCLASSES_FROM_CORE_MODIFYING:
            continue
        if column_num == 1:
            gui_blob_list.append(
                header.format(leader_class=subclass.split('_')[1])
            )
        subclass_gui_code = gen_core_modifying_leader_subclass_gui_code(
            subclass, column_num=column_num, row_num=row_num
        )
        gui_blob_list.append(subclass_gui_code)
        column_num = column_num + 1
        if column_num > 4:
            column_num = 1
    return "".join(gui_blob_list)


def gen_core_modifying_gui_subclass_pickers_code():
    return """
#subclass_general_marshall
    containerWindowType = {
        name = "xvcv_mdlc_core_modifying_traits_general_subclass_general_marshall"
        position = { x = @xvcv_mdlc_core_modifying_trait_position_width_3 y = @xvcv_mdlc_core_modifying_trait_position_height_1 }
        effectbuttonType = {
            name = "xvcv_mdlc_core_modifying_traits_general_subclass_general_marshall_add"
            position = { x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }
            spriteType = "GFX_leader_subclass_commander_general_medium"
            effect = "xvcv_mdlc_core_modifying_traits_general_subclass_general_marshall_add_button_effect"
        }
        effectbuttonType = {
            name = "xvcv_mdlc_core_modifying_traits_general_subclass_general_marshall_remove"
            position = { x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }
            spriteType = "GFX_xvcv_mdlc_leader_subclass_visionary_medium_red"
            effect = "xvcv_mdlc_core_modifying_traits_general_subclass_general_marshall_remove_button_effect"
        }
    }
"""