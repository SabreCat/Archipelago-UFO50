from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState, Entrance, LocationProgressType, Region

from . import Items, Locations, Quests

if TYPE_CHECKING:
    from . import CoQWorld


def add_entrance_access_rule(
    entrance: Entrance, rule: Callable[[CollectionState], bool]
):
    existing = entrance.access_rule
    entrance.access_rule = lambda state: existing(state) and rule(state)


def level_region_name(level: int) -> str:
    return f"Level {level}"


def level_entrance_name(level: int) -> str:
    return f"Reach Level {level}"


def create_regions(world: "CoQWorld"):
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions += [menu]
    region = Region(level_region_name(1), world.player, world.multiworld)
    menu.connect(region, level_entrance_name(1), None)

    for level in range(1, Quests.max_level(world) + 1):
        # Add Level locations
        for loc_name in Locations.xp_locations(
            level, level + 1, world.options.locations_per_level
        ):
            level_loc = Locations.CoQLocation(
                world.player, loc_name, world.location_name_to_id[loc_name], region
            )
            level_loc.progress_type = LocationProgressType.DEFAULT
            region.locations += [level_loc]

        next_region = Region(
            level_region_name(level + 1), world.player, world.multiworld
        )
        region.connect(
            next_region,
            level_entrance_name(level + 1),
            lambda state, level=level: Items.has_enough_stats_for_level(
                level + 1, state, world
            ),
        )

        world.multiworld.regions += [region]
        region = next_region

    add_main_quests(world)
    add_side_quests(world)
    add_delivery_quests(world)


def add_main_quests(world: "CoQWorld"):
    prev_quest_name = None
    for quest_name in Quests.main_quests(world):
        quest_level = Quests.main_quests_table[quest_name]
        region = world.get_region(level_region_name(quest_level))

        if quest_name == Quests.goal_lookup[world.options.goal]:
            # Add victory event instead of normal location
            quest_loc = Locations.CoQLocation(world.player, quest_name, None, region)
            quest_loc.place_locked_item(
                Items.CoQItem(
                    "Victory", Items.ItemClassification.progression, None, world.player
                )
            )
        else:
            quest_loc = Locations.CoQLocation(
                world.player, quest_name, world.location_name_to_id[quest_name], region
            )

        quest_loc.access_rule = (
            lambda state,
            quest_name=quest_name,
            prev_quest_name=prev_quest_name: state.has(
                Quests.quest_unlock_item(quest_name), world.player
            )
            and state.has(Quests.quest_unlock_item(prev_quest_name), world.player)
            if prev_quest_name is not None
            else True
        )
        quest_loc.progress_type = LocationProgressType.PRIORITY
        region.locations += [quest_loc]
        entrance = world.get_entrance(level_entrance_name(quest_level + 1))
        add_entrance_access_rule(
            entrance,
            lambda state, quest_name=quest_name: state.has(
                Quests.quest_unlock_item(quest_name), world.player
            ),
        )
        prev_quest_name = quest_name


def add_side_quests(world: "CoQWorld"):
    for quest_name in Quests.side_quests(world):
        quest_level = Quests.side_quests_table[quest_name]
        region = world.get_region(level_region_name(quest_level))
        quest_loc = Locations.CoQLocation(
            world.player, quest_name, world.location_name_to_id[quest_name], region
        )
        quest_loc.progress_type = LocationProgressType.DEFAULT
        region.locations += [quest_loc]


def add_delivery_quests(world: "CoQWorld"):
    for quest in [
        k
        for k in Locations.static_locations.values()
        if k.type == "delivery" and k.min_level <= Quests.max_level(world)
    ]:
        region = world.get_region(level_region_name(quest.min_level))
        quest_loc = Locations.CoQLocation(
            world.player, quest.name, world.location_name_to_id[quest.name], region
        )
        quest_loc.progress_type = LocationProgressType.DEFAULT
        region.locations += [quest_loc]
