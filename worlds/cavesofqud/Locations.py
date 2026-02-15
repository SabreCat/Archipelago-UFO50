import itertools
import json
import pkgutil
from typing import Dict, Iterable, NamedTuple

from BaseClasses import Location

from . import Options, Quests


class CoQLocation(Location):
    game: str = "Caves of Qud"


class CoQLocationData(NamedTuple):
    name: str
    type: str
    min_level: int


location_data = pkgutil.get_data(__name__, "data/Locations.json")
assert location_data is not None
static_locations: Dict[str, CoQLocationData] = {
    name: CoQLocationData(
        name=name,
        type=loc["type"],
        min_level=loc["minLevel"] if "minLevel" in loc else 1,
    )
    for name, loc in json.loads(location_data).items()
}


def xp_locations(frm: int, to: int, per_level: int) -> Iterable[str]:
    assert frm >= 1
    assert to <= Options.MAX_MAX_LEVEL
    assert per_level <= Options.MAX_LOCATIONS_PER_LEVEL

    for level in range(frm, to):
        for step in range(0, per_level):
            # We start at level 1.0, so skip first element
            if level == 1 and step == 0:
                continue
            yield f"Level {level}.{step}"


all_locations: Iterable[str] = itertools.chain(
    Quests.main_quests_table.keys(),
    Quests.side_quests_table.keys(),
    [name for name, data in static_locations.items()],
    xp_locations(1, Options.MAX_MAX_LEVEL, Options.MAX_LOCATIONS_PER_LEVEL),
)
