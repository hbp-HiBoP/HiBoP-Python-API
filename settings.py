import uuid
import json
from typing import List


class Alias:
    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

    def to_json_data(self) -> dict:
        return dict(Key=self.key, Value=self.value)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Alias':
        return cls(json_data["Key"], json_data["Value"])


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
