from yaml import load
from dataclasses import dataclass
from enum import Enum
from typing import List

MESSAGE_OFF_TOOLTIP = "This Feature is §RDeactivated§! now. Click to turn it §GOn§!."
MESSAGE_ON_TOOLTIP = "This Feature is §GActivated§! now. Click to turn it §ROff§!."

class OptionInteractionType(Enum):

	TOGGLE = 'toggle'
	EFFECT = 'effect'
	NAV = 'nav'

@dataclass
class MenuBase:
	event_id: int 						# For which game event is this option
	event_namespace: str 				# for building out localisation references
	description: str 					# arbitrary text, hopefully helpful
	name: str 							# button text or page title

@dataclass
class MenuToggleOption(MenuBase):
	option_id: int 						# index of this option in this page's list of options
	short_name: str 					# used to build out localisation references? I dont remember
	interaction: OptionInteractionType
	toggle_flag: None 					# If this menu option toggles a flag, which flag
	immediate_effect: None              # If the option runs an effect, which effect
	extra_triggers: List[str]

	def get_option_loc_id(self) -> str:
		# xvcv_mdlc_config.1.1
		return f"{self.event_namespace}.{self.event_id}.{self.option_id}"

	def make_button_text_name_locs(self) -> tuple:
		# These go in the localisation .yml files so the game can render option text 
		loc_id = self.get_option_loc_id()
		loc_key_on_id = f"{loc_id}.on"
		loc_key_off_id = f"{loc_id}.off"

		loc_key_on_value = f"{self.name}\n$xvcv_mdlc_config.message.on.tooltip$"
		loc_key_off_value = f"{self.description}\n$xvcv_mdlc_config.message.off.tooltip$"

		return f" {loc_key_on_id}: \"{loc_key_on_value}\"", f" {loc_key_off_id}: \"{loc_key_off_value}\""

@dataclass
class MenuNavOption(MenuBase):
	event_id: int 						# For which game event is this option
	event_namespace: str 				# for building out localisation references
	option_id: int 						# index of this option in this page's list of options
	next_page_event_id: int 			# event namespace + next_page_event_id


@dataclass
class MenuPage(MenuBase):
	page_id: int 						# automatically assigned
	picture_gfx_ref: str 				# GFX_evt_xvcv_mdlc
	options: List[MenuToggleOption]
	exclude_from_menu: bool = False 	# ignore, if it's for testing for example


def emit_cz_for_menu_option_toggle(menu_option: MenuToggleOption) -> str:
	# Generate Stellaris Clausewitz code for a given menu option
	current_page_event_id = f"{menu_option.event_namespace}.{menu_option.event_id}"
	option_loc_id = menu_option.get_option_loc_id()

	option_block = f"""
	option = {{
		# click this to turn off
		name = {option_loc_id}.on
		custom_tooltip = {option_loc_id}.on.tooltip
		trigger = {{
			has_country_flag = {menu_option.toggle_flag}
		}}
		hidden_effect = {{
			remove_country_flag = {menu_option.toggle_flag}
			country_event = {{ id = {current_page_event_id} }}
		}}
	}}
	option = {{
		# click this to turn on
		name = {option_loc_id}.off
		custom_tooltip = {option_loc_id}.off.tooltip
		trigger = {{
			NOT = {{ has_country_flag = {menu_option.toggle_flag} }}
			{"\n".join(menu_option.extra_triggers)}
		}}
		hidden_effect = {{
			set_country_flag = {menu_option.toggle_flag}
			country_event = {{ id = {current_page_event_id} }}
		}}
	}}
"""