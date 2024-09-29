import json
import dataclasses


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o: object):
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        return super().default(o)
