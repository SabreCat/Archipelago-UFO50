from worlds.AutoWorld import WebWorld, World

from . import Items, Locations, Options, Regions


class CoQWeb(WebWorld):
    theme = "jungle"
    bug_report_page = (
        "https://github.com/lonesurv1vor/CavesOfQudArchipelagoRandomizer/issues"
    )


class CoQWorld(World):
    """
    Live and drink
    """

    game = "Caves of Qud"
    web = CoQWeb()
    options_dataclass = Options.CoQOptions
    options: Options.CoQOptions  # type: ignore
    topology_present = False
    required_client_version = (0, 6, 0)
    required_server_version = (0, 6, 0)

    item_name_to_id = {item: id for id, item in enumerate(Items.all_items, 1)}
    location_name_to_id = {
        name: id for id, name in enumerate(Locations.all_locations, 1)
    }

    # World gen calls

    def fill_slot_data(self) -> dict:
        return self.options.as_dict(
            *[name for name in self.options_dataclass.type_hints.keys()]
        )

    def create_regions(self):
        Regions.create_regions(self)

    def create_items(self):
        Items.create_items(self)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state, p=self.player: state.has("Victory", p)
        )

    def create_item(self, name: str):
        return Items.create_any_item_static(self, name)
