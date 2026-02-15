from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range

MAX_MAX_LEVEL = 50
MAX_LOCATIONS_PER_LEVEL = 10


class Goal(Choice):
    """
    Determines the win condition
    """

    display_name = "Goal"
    option_quest_weirdwire_conduit = 0
    option_quest_more_than_a_willing_spirit = 1
    option_quest_decoding_the_signal = 2
    option_quest_the_earl_of_omonporch = 3
    option_quest_a_call_to_arms = 4
    default = 2


class LocationsPerLevel(Range):
    """
    Determines the number of locations to check when gaining XP.
    Each level contains the number of locations chosen here,
    distributed across the XP range between current and next level.
    Including the level up itself.
    """

    display_name = "Extra locations per level"
    range_start = 4
    range_end = MAX_LOCATIONS_PER_LEVEL
    default = 5


class ExtraLocationLevels(Range):
    """
    Determines the number of extra levels with locations beyond the in-logic level for the final
    goal quest step (selected by the goal option). This also controls the extra amount of stat ups
    that are in the item pool.
    """

    display_name = "Extra levels beyond the final quest"
    range_start = 0
    range_end = 20
    default = 5


class TrapPercentage(Range):
    """
    Determines the percentage of filler items that are replaced by
    traps.
    """

    display_name = "Percentage of filler items replaced with traps"
    range_start = 0
    range_end = 100
    default = 50


@dataclass
class CoQOptions(PerGameCommonOptions):
    goal: Goal
    locations_per_level: LocationsPerLevel
    extra_location_levels: ExtraLocationLevels
    trap_percentage: TrapPercentage
    # death_link: DeathLink
