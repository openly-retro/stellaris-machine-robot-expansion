This is an attempt to bring XVCV's "Machines & Robot Expansion" mod for Stellaris up to date, to be compatible with Stellaris version 3.10.*

The original author has abandoned the work and is no longer available for contact.

# TO DO:

## GUI, Generally

- Go through all the .gui files, and look up quadTextureSprite references. Usually the file name can be derived from the naming pattern. In any case, there are some references to texture files that no longer exist. Those references should get updated to what their counterpart now is
- Also copy those texture files (probably?) to this mod for future safekeeping, in case Paradox delete them or make them unavailable, so we dont end up with broken dependencies.

## Leader subclasses

- There are references to leader subclasses throughout the code. These are typically in the context of "does the leader have this trait" and looks to see if it is a subclass.
- From what I gather, subclasses are mainly a Paragons DLC thing, meaning, the most variety of subclasses are found in that DLC.
- There are a few approaches:
-- Define subclasses that match the old ones
-- Do away with subclasses
-- Match the names of the subclasses the author originally used, as closely as possible with the subclasses available in the Paragons DLC

## Tooltips

- Some tooltips refer to subclasses, dynamically. Fix em.

## Translations needed

These languages are filled with English content and aren't useful to native speakers of those languages:

- Brazilian Portuguese
- French
- German
- Japanese
- Polish
- Russian
- Simple Chinese
- Spanish

We can either:

1. Ask for volunteers
2. Attempt to use online translation tools to create them

# More info

This doc will be continually expanded.

# Mod design patterns

TBD.. I want to have notes here for future maintainers.

# Maintenance / update guidelines

- Avoid renaming files
- Avoid renaming custom variables where possible

# Resources

Graphics: Use paint.net
Code: VSCode with cwtools extension

# Quick references for renames:

Placeholders for monkeypatching the plumbing so it works again
There are only 4 subclasses per class to go around, some of the previous ones
will have to go. 

    3.9 -> 3.10
    
    subclass_scientist_analyst -> subclass_scientist_scholar
    subclass_scientist_explorer -> (same)
    
    subclass_governor_pioneer -> subclass_official_governor
    subclass_governor_economist -> subclass_official_economy_councilor
    subclass_governor_visionary -> subclass_official_diplomacy_councilor
    subclass_governor_? -> subclass_official_delegate


    3.10 veteran classes:
    subclass_commander_general      subclass_scientist_explorer
    subclass_commander_councilor    subclass_scientist_councilor
    subclass_commander_governor     subclass_scientist_governor
    subclass_commander_admiral      subclass_scientist_scholar
    
    subclass_official_economy_councilor
    subclass_official_diplomacy_councilor
    subclass_official_governor
    subclass_official_delegate
    
    3.9 veteran classes:
    subclass_general_invader    -> subclass_commander_general
    subclass_general_protector  -> subclass_commander_governor
    subclass_general_none       -> subclass_commander_none  <- check for dupes
    subclass_general_marshall   -> X (subclass_commander_general) <- dupes
    
    subclass_admiral_strategist -> subclass_commander_councilor
    subclass_admiral_aggressor  -> X (subclass_commander_admiral) <- dupes
    subclass_admiral_none       -> subclass_commander_none  <- check for dupes
    subclass_admiral_tactician  -> subclass_commander_admiral

# Leader-making feature
## Veteran-class bonuses

The commander subclasses all have bonuses because there were two General subclasses from the 3.9 version that got converted to Commander subclasses.

See https://stellaris.paradoxwikis.com/Leader#Leader_classes
