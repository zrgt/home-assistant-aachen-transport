from dataclasses import dataclass
from datetime import datetime

from .const import TRANSPORT_TYPE_VISUALS, DEFAULT_ICON, TRANSPORT_TYPE_CODES, \
    CONF_TYPE_BUS, SIMPLIFIED_DIRECTION


@dataclass
class Departure:
    """Departure dataclass to store data from widget API:
    https://abfahrt.avv.de/"""

    trip_id: str
    line_name: str
    line_type: str
    timestamp: datetime
    time: datetime
    minutes_left: int
    delay: int
    direction: str | None = None
    icon: str | None = None
    bg_color: str | None = None
    fallback_color: str | None = None
    location: tuple[float, float] | None = None

    @classmethod
    def from_dict(cls, source):
        line_name: str = source.get("line")

        line_type = CONF_TYPE_BUS
        for code in TRANSPORT_TYPE_CODES:
            if line_name.startswith(code):
                line_type = TRANSPORT_TYPE_CODES[code]

        line_visuals = TRANSPORT_TYPE_VISUALS.get(line_type) or {}
        time = source.get('rtTime') if source.get("hasRtTime") else source.get('time')
        timestamp=datetime.fromisoformat(f"{source.get('date')}T{time}")
        secs_left = (timestamp-datetime.now()).total_seconds()
        if secs_left<0:
            minutes_left=0
        else:
            minutes_left=secs_left//60
        direction = str(source.get("direction"))
        for i in SIMPLIFIED_DIRECTION:
            if direction.startswith(i):
                direction = SIMPLIFIED_DIRECTION[i]

        return cls(
            trip_id=source["jr"],
            line_name=line_name,
            line_type=line_type,
            timestamp=timestamp,
            time=time,
            minutes_left=minutes_left,
            delay=source.get("diff") if source.get("diff") else 0,
            direction=direction,
            icon=line_visuals.get("icon") or DEFAULT_ICON,
            fallback_color=line_visuals.get("color"),
        )

    def to_dict(self):
        return {
            "line_name": self.line_name,
            "line_type": self.line_type,
            "time": self.time,
            "minutes_left": self.minutes_left,
            "delay": self.delay,
            "direction": self.direction,
            "color": self.fallback_color or self.bg_color,
        }
