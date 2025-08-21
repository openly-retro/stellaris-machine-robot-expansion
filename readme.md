This is a continuation of XVCV's "Machines & Robot Expansion" mod for Stellaris. The goals are to keep it up to date with the latest game version, fix bugs, and add new content.

The original author has abandoned the work and is no longer available for contact.

# Welcome

I (openly-retro) am a web developer by day, and a fan of Stellaris. I enjoy science fiction a lot.

I invite you to collaborate, but I also want you to know I'm not desperate for help and this mod will continue to thrive even if you only just stop by to say hi.

## Communicating

Chat with me about this mod in the [Stellaris Modding Den](https://discord.gg/vKwNs93g ) discord! Look for `mag-sanchusa#4206 (openlyretro)`. We can discuss this mod in the `machines-robots-expac` channel.

I will also respond to comments in the Github wiki and issues for this project.

## Contributing

Please visit the Github repo wiki for this project: [https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki](https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki)

Warnings about working with Clausewitz syntax (what base Stellaris traits files are written in)

- It MAKES UP ITS OWN RULES
- IT MAY NOT FOLLOW THE RULES IT MAKES
- It wiLL DaNcE On yOuR SaNiTy
- You may lose yourself to possession of a psionic avatar if you stare too long or try to apply your ideas of "rules" and "well this could be standardized pretty easily"

## Translations

Welcome translators!! I am very happy to have you here.

If you would like to submit a translation, please go ahead and create a pull request from a fork of this repo.

The translation files should go in:

`localisation/<language>/replace`

So if you are translating Korean files, the changes should go in `localisation/korean/replace/` because I have a language copy tool which copies all changes from English to all other languge folders.

If you place the files in `localisation/<language>` and not in `localisation/<language>/replace` then the files will be overwritten.

If they are in the `replace` folder then your correctly translated files will always take precedence over the English version. If your translation files are missing any keys then the missing keys will show up in English.

This way, players will never see only the localisation key with no content if there are translations missing.

### Patches

I do updates using the concept of patches. A patch consists of:

1. A group of bug fixes or small features, OR
2. A large feature

Workflow:

1. Create a branch for the patch, following the next in the series at https://github.com/openly-retro/stellaris-machine-robot-expansion/tags (if 2.3.2 is the latest then the next is 2.3.3), named `patch-#.#.#` where #.#.# is the patch version
2. Do some work in your feature or bug branch and then make a pull request to the patch branch

# Art Credits

- [https://www.deviantart.com/xxaries1970xx/art/Digital-Circuit-936780185](Digital Circuit, by XxAries1970xX), used for the Source Code Reprogramming event-related banners.
- https://pixabay.com/illustrations/water-technology-sci-fi-futuristic-7547817/ by [https://pixabay.com/users/joker39-30858803/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7547817](Melvyn Thevenin) from [https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7547817"](Pixabay) , used for World Machine planetary deposits and other artworks
- https://pixabay.com/illustrations/futuristic-architecture-wallpaper-6694976/ by  <a href="https://pixabay.com/users/tommyvideo-3092371/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6694976">Tomislav Jakupec</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6694976">Pixabay</a>, used for World Machine technology art
- https://pixabay.com/illustrations/blueprint-engineering-technology-6944719/ by Image by <a href="https://pixabay.com/users/xresch-7410129/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6944719">Reto Scheiwiller</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6944719">Pixabay</a>, used for World Machine event art
- https://pixabay.com/illustrations/futuristic-background-pattern-7831598/ Image by <a href="https://pixabay.com/users/placidplace-25572496/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7831598">Peace,love,happiness</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7831598">Pixabay</a>, used for World Machine art
- https://pixabay.com/illustrations/fantastic-technology-futuristic-4805591/ Image by <a href="https://pixabay.com/users/gtuignatov-3540393/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4805591">Alexander Ignatov</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4805591">Pixabay</a>
- https://pixabay.com/illustrations/blur-background-pattern-geometric-7281360/ Image by <a href="https://pixabay.com/users/placidplace-25572496/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7281360">Peace,love,happiness</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7281360">Pixabay</a>, used for World Machine event art
- https://pixabay.com/photos/industry-stole-iron-blast-furnace-647399/ Image by <a href="https://pixabay.com/users/zephylwer0-621585/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=647399">zephylwer0</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=647399">Pixabay</a>, used for World Machine district background art

# Overwritten Vanilla elements

## Economic categories

- pop_category_drones
- pop_category_workers
- pop_category_specialists
- pop_category_rulers

## Game rules

- **can_release_vassal_from_species**: Let Machine empires with a certain AP release vassals
- **can_colonize_planet**: Block colonizing a planet if it's a habitat that's being dismantled, or if it's a ruined World Machine that's being rebooted
- **can_species_be_assembled**: Block Bio-Mech species from being generated via the pop assembly system
- **can_generate_leader_from_species**: Permit Bio-Mech / Mechanical empires to recruit leaders

## Scripted triggers:
- **is_individual_machine**: Triggers yes if empire primary species has machine trait
- **can_add_genetic_traits**: Yes for the Genetic Mastery AP
- **can_remove_beneficial_genetic_traits**: Yes for the Genetic Mastery AP
- **can_add_overclocked_traits**: Yes for the Overclocked origin

## Technology:

Changed weight to consider custom World-Machine blockers

- tech_volcano
- tech_noxious_swamp
- tech_mountain_range
- tech_massive_glacier

## Traits

- trait_mechanical: Add triggered habitability for Mechanical Worlds 
