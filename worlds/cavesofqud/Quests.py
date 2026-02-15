from typing import TYPE_CHECKING, Dict, Iterable

from . import Options

if TYPE_CHECKING:
    from . import CoQWorld

# This defines the general progress through levels and main quest steps
# (Level required, main quest name)
# The values are oriented on the quests in game level recommendation from Quests.xml
# This is a dict but the entries must be made in correct order. And it requires python 3.7 to retain the order.
main_quests_table: Dict[str, int] = {
    "Fetch Argyve a Knickknack~Find a Knickknack": 3,
    "Fetch Argyve a Knickknack~Return to Argyve": 3,
    "Fetch Argyve Another Knickknack~Find Another Knickknack": 5,
    "Fetch Argyve Another Knickknack~Return to Argyve": 5,
    "Weirdwire Conduit... Eureka!~Find 200 Feet of Wire": 7,
    "Weirdwire Conduit... Eureka!~Return to Argyve": 8,
    "A Canticle for Barathrum~Travel to Grit Gate": 10,
    # Not controllable through conversation, skipped for now
    # "A Canticle for Barathrum~Locate the Barathrumite Enclave":10,
    "A Canticle for Barathrum~Speak with the Barathrumites": 10,
    "More Than a Willing Spirit~Travel to Golgotha": 10,
    "More Than a Willing Spirit~Find a Dysfunctional Waydroid": 12,
    "More Than a Willing Spirit~Repair the Waydroid": 12,
    "More Than a Willing Spirit~Return to Grit Gate": 12,
    "Decoding the Signal~Get Q Girl's Instructions onto the Data Disk": 15,
    "Decoding the Signal~Locate the Mechanimist Compound at Bethesda Susa": 18,
    "Decoding the Signal~Decode the Signal": 20,
    "Decoding the Signal~Return to Grit Gate": 20,
    # The following are not all steps
    "The Earl of Omonporch~Travel to Omonporch": 20,
    "The Earl of Omonporch~Secure the Spindle": 22,
    "The Earl of Omonporch~Return to Grit Gate": 25,
    "A Call to Arms~Prepare Defenses": 25,
    "A Call to Arms~Defend Grit Gate": 25,
}

goal_lookup = {
    Options.Goal.option_quest_weirdwire_conduit: "Weirdwire Conduit... Eureka!~Return to Argyve",
    Options.Goal.option_quest_more_than_a_willing_spirit: "More Than a Willing Spirit~Return to Grit Gate",
    Options.Goal.option_quest_decoding_the_signal: "Decoding the Signal~Return to Grit Gate",
    Options.Goal.option_quest_the_earl_of_omonporch: "The Earl of Omonporch~Return to Grit Gate",
    Options.Goal.option_quest_a_call_to_arms: "A Call to Arms~Defend Grit Gate",
}


def main_quests(world: "CoQWorld") -> Iterable[str]:
    for name in main_quests_table.keys():
        yield name
        if name == goal_lookup[world.options.goal.value]:
            break


def quest_unlock_item(name: str) -> str:
    return "Unlock: " + name


# Max level is last required quest level + some extra
# TODO
def max_level(world: "CoQWorld") -> int:
    return (
        main_quests_table[goal_lookup[world.options.goal.value]]
        + world.options.extra_location_levels
    )


# These all stand by themselves, no logic other than the level requirement per step. There
# are no unlocks for these, so no deadlock possible.
side_quests_table: Dict[str, int] = {
    "What's Eating the Watervine?~Travel to Red Rock": 1,
    "What's Eating the Watervine?~Find the Vermin": 3,
    "What's Eating the Watervine?~Get a Corpse": 3,
    "What's Eating the Watervine?~Return with the Corpse": 5,
    "O Glorious Shekhinah!~Make a Pilgrimage to the Six Day Stilt": 3,
    "Raising Indrix~Find Mamon Souldrinker": 15,
    "Raising Indrix~Recover the Amaranthine Prism": 15,
    "Petals on the Wind~Investigate Bey Lah": 10,
    "Find Eskhind~Find Eskhind": 10,
    "Find Eskhind~Deliver News of Eskhind": 10,
    "Love and Fear~Return the Love Sonnet": 10,
    "Kith and Kin~Brief Warden Neelahind": 10,
    "Kith and Kin~Accuse the thief": 10,
}


def side_quests(world: "CoQWorld") -> Iterable[str]:
    for name, level in side_quests_table.items():
        if level <= max_level(world):
            yield name
