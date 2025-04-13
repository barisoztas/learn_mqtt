import datetime
import json
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


class GenericClock:

    def __init__(self):

        self.time_initiate = pd.Timestamp.now()

    @property
    def difference(self):
        """The difference between the current time and the time of initiation."""
        return datetime.datetime.now() - self.time_initiate


@dataclass
class ClockReading:
    """Data representation of p1 water level sensor reading"""

    clock_id: str
    time_initiate: pd.Timestamp
    difference_now: pd.Timedelta

    @staticmethod
    def _json_timestamp_serial(obj):
        """custom JSON serializer for pandas.Timestamp"""
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        if isinstance(obj, pd.Timedelta):
            return str(obj)
        raise TypeError("Type %s not serializable" % type(obj))

    def asdict_considering_repr(self) -> dict:
        return {
            k: v for k, v in asdict(self).items() if self.__dataclass_fields__[k].repr
        }

    def json(self):
        """return data as p1 json object"""
        return json.dumps(asdict(self), default=self._json_timestamp_serial)
