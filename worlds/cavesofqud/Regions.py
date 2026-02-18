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
    # Default always-reachable region
    menu = Region("Menu", world.player, world.multiworld)

    world.multiworld.regions += [menu]

    # Level progression, represented by regions on a parallel track. Regions equal to
    # the max level defined by goal quest and extra levels option, and a set of
    # locations within each according to the "locations per level" option.
    level_region = Region(level_region_name(1), world.player, world.multiworld)
    menu.connect(level_region, level_entrance_name(1), None)

    for level in range(1, Quests.max_level(world) + 1):
        # Add Level locations
        for loc_name in Locations.xp_locations(
            level, level + 1, world.options.locations_per_level
        ):
            level_loc = Locations.CoQLocation(
                world.player, loc_name, world.location_name_to_id[loc_name], level_region
            )
            level_loc.progress_type = LocationProgressType.DEFAULT
            level_region.locations += [level_loc]

        next_region = Region(
            level_region_name(level + 1), world.player, world.multiworld
        )
        level_region.connect(
            next_region,
            level_entrance_name(level + 1),
            lambda state, level=level: Items.has_enough_stats_for_level(
                level + 1, state, world
            ),
        )

        world.multiworld.regions += [level_region]
        # We create one extra region that never gets added to the world. Funny
        level_region = next_region

    # Conceptual regions for main game, mostly quest-related
    joppa = Region("Joppa", world.player, world.multiworld)
    red_rock = Region("Red Rock", world.player, world.multiworld)
    joppa_2 = Region("Joppa 2", world.player, world.multiworld)
    rust_wells = Region("Rust Wells", world.player, world.multiworld)
    grit_gate = Region("Grit Gate", world.player, world.multiworld)
    bey_lah = Region("Bey Lah", world.player, world.multiworld)
    golgotha = Region("Golgotha", world.player, world.multiworld)
    grit_gate_2 = Region("Grit Gate 2", world.player, world.multiworld)
    kyakukya = Region("Kyakukya", world.player, world.multiworld)
    bethesda = Region("Bethesda Susa", world.player, world.multiworld)
    bethesda_2 = Region("Bethesda Susa 2", world.player, world.multiworld)
    omonporch = Region("Omonporch", world.player, world.multiworld)

    quest_regions = [joppa, red_rock, joppa_2, rust_wells, grit_gate, bey_lah,
                     golgotha, grit_gate_2, kyakukya, bethesda, bethesda_2, omonporch]
    
    world.multiworld.regions += quest_regions

    # Core progression track with side quest branches
    menu.connect(joppa, "Joppa Start")
    joppa.connect(joppa_2, "Joppa Continued", lambda state: state.has("Ancient Knickknack", world.player))
    red_rock_entrance = joppa.connect(red_rock, "Joppa to Red Rock", lambda state: state.has("Water Farmer Token", world.player)
                  and state.can_reach_region("Level 5", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 5"), red_rock_entrance)
    bey_lah_entrance = joppa.connect(bey_lah, "Joppa to Bey Lah", lambda state: state.has("Hindren Token", world.player)
                  and state.can_reach_region("Level 10", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 10"), bey_lah_entrance)
    kyakukya_entrance = joppa.connect(kyakukya, "Joppa to Kyakukya", lambda state: state.has("Kyakukya Token", world.player)
                  and state.can_reach_region("Level 15", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 15"), kyakukya_entrance)
    rust_wells_entrance = joppa_2.connect(rust_wells, "Joppa to Rust Wells", lambda state: state.has("Prime Knickknack", world.player)
                    and state.can_reach_region("Level 7", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 7"), rust_wells_entrance)
    grit_gate_entrance = rust_wells.connect(grit_gate, "Rust Wells to Grit Gate", lambda state: state.has("Weirdwire Fusor", world.player)
                       and state.can_reach_region("Level 10", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 10"), grit_gate_entrance)
    golgotha_entrance = grit_gate.connect(golgotha, "Grit Gate to Golgotha", lambda state: state.has("Barathrumite Token", world.player)
                      and state.can_reach_region("Level 12", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 12"), golgotha_entrance)
    grit_gate_2_entrance = golgotha.connect(grit_gate_2, "Golgotha to Grit Gate", lambda state: state.has("Waydroid Repair Kit", world.player)
                     and state.can_reach_region("Level 15", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 15"), grit_gate_2_entrance)
    bethesda_entrance = grit_gate_2.connect(bethesda, "Grit Gate to Bethesda Susa", lambda state: state.has("Eschaton Transcoder", world.player)
                        and state.can_reach_region("Level 18", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 18"), bethesda_entrance)
    bethesda_2_entrance = bethesda.connect(bethesda_2, "Bethesda Susa Continued", lambda state: state.has("Baetyl Optronic Adapter", world.player)
                     and state.can_reach_region("Level 20", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 20"), bethesda_2_entrance)
    omonporch_entrance = bethesda_2.connect(omonporch, "Bethesda Susa to Omonporch", lambda state: state.has("Consortium Token", world.player)
                       and state.can_reach_region("Level 25", world.player))
    world.multiworld.register_indirect_condition(world.get_region("Level 25"), omonporch_entrance)

    add_quests(world)
    add_static_locations(world)


def add_quests(world: "CoQWorld"):
    for quest_name in Quests.quest_keys(world):
        region = world.get_region(Quests.quest_locations[quest_name].region)

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

        quest_loc.progress_type = LocationProgressType.PRIORITY if (
            Quests.quest_locations[quest_name].main) else LocationProgressType.DEFAULT
        region.locations += [quest_loc]


def add_static_locations(world: "CoQWorld"):
    for quest in [
        k
        for k in Locations.static_locations.values()
        if k.type == "delivery" or k.type == "lore" or (
            k.type == "artifact" and world.options.lost_artifacts)
            and k.min_level <= Quests.max_level(world)
    ]:
        region = world.get_region(quest.region)
        quest_loc = Locations.CoQLocation(
            world.player, quest.name, world.location_name_to_id[quest.name], region
        )
        quest_loc.progress_type = LocationProgressType.DEFAULT
        region.locations += [quest_loc]
