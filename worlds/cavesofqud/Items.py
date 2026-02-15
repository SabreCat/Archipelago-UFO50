import json
import pkgutil
from typing import TYPE_CHECKING, Dict, Iterable, List, NamedTuple

from BaseClasses import CollectionState, Item, ItemClassification

from . import Quests

if TYPE_CHECKING:
    from . import CoQWorld


class CoQItem(Item):
    game: str = "Caves of Qud"


class CoQItemData(NamedTuple):
    name: str
    category: str
    weight: int


item_data = pkgutil.get_data(__name__, "data/Items.json")
assert item_data is not None
static_items: Dict[str, CoQItemData] = {
    name: CoQItemData(
        name=name,
        category=item["category"],
        weight=item["weight"] if "weight" in item else 1,
    )
    for name, item in json.loads(item_data).items()
}

stat_items = [
    "Hit Points",
    "Attribute Points",
    "Attribute Bonus",
    "Mutation Points",
    "Skill Points",
    "Rapid Mutation Advancement",
]

all_items: Iterable[str] = [
    *stat_items,
    *[i for i in static_items.keys()],
    *[Quests.quest_unlock_item(name) for name in Quests.main_quests_table.keys()],
]


def levelup_levels(max_level: int) -> list[int]:
    return [level for level in range(2, max_level + 1)]


def stat_items_total(max_level: int) -> int:
    return sum(
        [len(stat_items_on_levelup(level)) for level in levelup_levels(max_level)]
    )


def stat_items_count(state: CollectionState, player: int) -> int:
    return sum([state.count(item, player) for item in stat_items])


def has_enough_stats_for_level(
    level: int, state: CollectionState, world: "CoQWorld"
) -> bool:
    return stat_items_count(state, world.player) / stat_items_total(
        Quests.max_level(world)
    ) >= (level - 1) / Quests.max_level(world)


def stat_items_on_levelup(level: int) -> list[str]:
    items = ["Hit Points", "Mutation Points", "Skill Points"]
    if (level + 3) % 6 == 0:
        items.append("Attribute Points")
    if (level + 6) % 6 == 0:
        items.append("Attribute Bonus")
    if (level + 5) % 10 == 0:
        items.append("Rapid Mutation Advancement")

    return items


def create_stat_items_on_levelup(world: "CoQWorld", level: int) -> list[CoQItem]:
    items = stat_items_on_levelup(level)
    return [
        CoQItem(
            name,
            ItemClassification.progression,
            world.item_name_to_id[name],
            world.player,
        )
        for name in items
    ]


def create_filler_item(world: "CoQWorld") -> CoQItem:
    category = world.random.choices(
        ["filler", "trap"],
        [100 - world.options.trap_percentage, float(world.options.trap_percentage)],
    )[0]
    weights = [
        data.weight for name, data in static_items.items() if data.category == category
    ]
    name = world.random.choices(
        [name for name, data in static_items.items() if data.category == category],
        weights,
        k=1,
    )[0]
    return CoQItem(
        name,
        ItemClassification.trap if category == "trap" else ItemClassification.filler,
        world.item_name_to_id[name],
        world.player,
    )


def create_items(world: "CoQWorld"):
    item_pool: List[CoQItem] = []
    total_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Main quest unlock items
    for quest in Quests.main_quests(world):
        item_name = Quests.quest_unlock_item(quest)
        item_pool += [
            CoQItem(
                item_name,
                ItemClassification.progression,
                world.item_name_to_id[item_name],
                world.player,
            )
        ]

    # Stat ups from level ups
    for level in levelup_levels(Quests.max_level(world)):
        item_pool += create_stat_items_on_levelup(world, level)

    # Fill up with fillers
    while len(item_pool) < total_locations:
        item_pool += [create_filler_item(world)]

    world.multiworld.itempool += item_pool


def create_any_item_static(world: "CoQWorld", name: str) -> Item:
    if name in static_items:
        data = static_items[name]
        classification = (
            ItemClassification.trap
            if data.category == "trap"
            else ItemClassification.filler
        )
    elif name in stat_items:
        classification = ItemClassification.progression
    elif name in [
        Quests.quest_unlock_item(name) for name in Quests.main_quests_table.keys()
    ]:
        classification = ItemClassification.progression
    else:
        raise Exception(f"Item {name} couldn't be found in the static table")

    return CoQItem(name, classification, world.item_name_to_id[name], world.player)
