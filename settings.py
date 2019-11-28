import uuid
import json
from typing import List
from tools import BaseData


class Alias:
    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

    def to_json_data(self) -> dict:
        return dict(Key=self.key, Value=self.value)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Alias':
        return cls(json_data["Key"], json_data["Value"])


class BaseTag(BaseData):
    def __init__(self, name: str = "", ID: str = ""):
        self.name = name
        super().__init__(ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BaseTag':
        return cls(json_data["Name"], json_data["ID"])


class BoolTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        return super().to_json_data()

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BoolTag':
        return cls(json_data["Name"], json_data["ID"])


class EmptyTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        return super().to_json_data()

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'EmptyTag':
        return cls(json_data["Name"], json_data["ID"])


class StringTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        return super().to_json_data()

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'StringTag':
        return cls(json_data["Name"], json_data["ID"])


class EnumTag(BaseTag):
    def __init__(self, name: str = "", values: List[str] = None, ID: str = ""):
        super().__init__(name, ID)
        self.values = values

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Values'] = self.values
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'EnumTag':
        return cls(json_data["Name"], json_data["Values"], json_data["ID"])


class FloatTag(BaseTag):
    def __init__(self, name: str = "", clamped: bool = False, min_value: float = 0.0, max_value: float = 0.0, ID: str = ""):
        super().__init__(name, ID)
        self.clamped = clamped
        self.min_value = min_value
        self.max_value = max_value

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Clamped'] = self.clamped
        json_data['Min'] = self.min_value
        json_data['Max'] = self.max_value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'FloatTag':
        return cls(json_data['Name'], json_data['Clamped'], json_data['Min'], json_data['Max'], json['ID'])


class IntTag(BaseTag):
    def __init__(self, name: str = "", clamped: bool = False, min_value: int = 0, max_value: int = 0, ID: str = ""):
        super().__init__(name, ID)
        self.clamped = clamped
        self.min_value = min_value
        self.max_value = max_value

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Clamped'] = self.clamped
        json_data['Min'] = self.min_value
        json_data['Max'] = self.max_value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'IntTag':
        return cls(json_data['Name'], json_data['Clamped'], json_data['Min'], json_data['Max'], json['ID'])


class BaseTagValue(BaseData):
    def __init__(self, tag: BaseTag = None, value=None, ID: str = ""):
        self.tag = tag
        self.value = value
        super().__init__(ID)

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Tag'] = self.tag.ID
        json_data['Value'] = self.value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BaseTagValue':
        return cls(json_data['Tag'], json_data['Value'])


class Settings:
    def __init__(self, name: str = "", patient_database: str = "", localizer_database: str = "",
                 aliases: List[Alias] = None, ID: str = ""):
        self.name = name
        self.patient_database = patient_database
        self.localizer_database = localizer_database
        self.aliases = aliases if aliases is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def __repr__(self):
        result = super().__repr__()
        result += "\n" + json.dumps(self.to_json_data())
        return result

    def to_json_data(self) -> dict:
        return dict(ID=self.ID, Name=self.name, PatientDatabase=self.patient_database,
                    LocalizerDatabase=self.localizer_database,
                    Aliases=[alias.to_json_data() for alias in self.aliases])

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file) -> 'Settings':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f))

    @classmethod
    def from_json_data(cls, json_data):
        return cls(json_data["Name"], json_data["PatientDatabase"], json_data["LocalizerDatabase"],
                   [Alias.from_json_data(alias_json_data) for alias_json_data in json_data["Aliases"]],
                   json_data["ID"])
