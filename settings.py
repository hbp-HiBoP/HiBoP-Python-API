import json
from typing import List
from tools import BaseData


class Alias(BaseData):
    def __init__(self, key: str = "", value: str = "", ID: str = ""):
        super().__init__(ID)
        self.key = key
        self.value = value

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Key'] = self.key
        json_data['Value'] = self.value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Alias':
        return cls(json_data["Key"], json_data["Value"], json_data['ID'])


class BaseTag(BaseData):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(ID)
        self.name = name

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BaseTag':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.BoolTag, Assembly-CSharp":
            result = BoolTag.from_json_data(json_data)
        elif class_type == "HBP.Data.EmptyTag, Assembly-CSharp":
            result = EmptyTag.from_json_data(json_data)
        elif class_type == "HBP.Data.EnumTag, Assembly-CSharp":
            result = EnumTag.from_json_data(json_data)
        elif class_type == "HBP.Data.FloatTag, Assembly-CSharp":
            result = FloatTag.from_json_data(json_data)
        elif class_type == "HBP.Data.IntTag, Assembly-CSharp":
            result = IntTag.from_json_data(json_data)
        elif class_type == "HBP.Data.StringTag, Assembly-CSharp":
            result = StringTag.from_json_data(json_data)
        return result


class BoolTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Data.BoolTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BoolTag':
        return cls(json_data["Name"], json_data["ID"])


class EmptyTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Data.EmptyTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'EmptyTag':
        return cls(json_data["Name"], json_data["ID"])


class StringTag(BaseTag):
    def __init__(self, name: str = "", ID: str = ""):
        super().__init__(name, ID)

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Data.StringTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'StringTag':
        return cls(json_data["Name"], json_data["ID"])


class EnumTag(BaseTag):
    def __init__(self, name: str = "", values: List[str] = None, ID: str = ""):
        super().__init__(name, ID)
        self.values = values

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Data.EnumTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
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
        json_data = dict()
        json_data["$type"] = "HBP.Data.FloatTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['Clamped'] = self.clamped
        json_data['Min'] = self.min_value
        json_data['Max'] = self.max_value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'FloatTag':
        return cls(json_data['Name'], json_data['Clamped'], json_data['Min'], json_data['Max'], json_data['ID'])


class IntTag(BaseTag):
    def __init__(self, name: str = "", clamped: bool = False, min_value: int = 0, max_value: int = 0, ID: str = ""):
        super().__init__(name, ID)
        self.clamped = clamped
        self.min_value = min_value
        self.max_value = max_value

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Data.IntTag, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['Clamped'] = self.clamped
        json_data['Min'] = self.min_value
        json_data['Max'] = self.max_value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'IntTag':
        return cls(json_data['Name'],
                   json_data['Clamped'],
                   json_data['Min'],
                   json_data['Max'],
                   json_data['ID'])


class BaseTagValue(BaseData):
    def __init__(self, tag: BaseTag = None, value=None, ID: str = ""):
        super().__init__(ID)
        self.tag = tag
        self.value = value

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Tag'] = self.tag.ID
        json_data['Value'] = self.value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'BaseTagValue':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.BoolTagValue, Assembly-CSharp":
            result = BoolTagValue.from_json_data(json_data, tags)
        elif class_type == "HBP.Data.EmptyTagValue, Assembly-CSharp":
            result = EmptyTagValue.from_json_data(json_data, tags)
        elif class_type == "HBP.Data.EnumTagValue, Assembly-CSharp":
            result = EnumTagValue.from_json_data(json_data, tags)
        elif class_type == "HBP.Data.FloatTagValue, Assembly-CSharp":
            result = FloatTagValue.from_json_data(json_data, tags)
        elif class_type == "HBP.Data.IntTagValue, Assembly-CSharp":
            result = IntTagValue.from_json_data(json_data, tags)
        elif class_type == "HBP.Data.StringTagValue, Assembly-CSharp":
            result = StringTagValue.from_json_data(json_data, tags)
        return result


class BoolTagValue(BaseTagValue):
    def __init__(self, tag: BoolTag = None, value: bool = False, ID: str = ""):
        super().__init__(tag, value, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.BoolTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'BoolTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['Value'], json_data['ID'])


class EmptyTagValue(BaseTagValue):
    def __init__(self, tag: EmptyTag = None, ID: str = ""):
        super().__init__(tag, None, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.EmptyTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'EmptyTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['ID'])


class EnumTagValue(BaseTagValue):
    def __init__(self, tag: EnumTag = None, value: int = 0, ID: str = ""):
        super().__init__(tag, value, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.EnumTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'EnumTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['Value'], json_data['ID'])


class FloatTagValue(BaseTagValue):
    def __init__(self, tag: FloatTag = None, value: float = 0.0, ID: str = ""):
        super().__init__(tag, value, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.FloatTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'FloatTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['Value'], json_data['ID'])


class IntTagValue(BaseTagValue):
    def __init__(self, tag: IntTag = None, value: int = 0, ID: str = ""):
        super().__init__(tag, value, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.IntTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'IntTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['Value'], json_data['ID'])


class StringTagValue(BaseTagValue):
    def __init__(self, tag: StringTag = None, value: str = 0, ID: str = ""):
        super().__init__(tag, value, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Data.StringTagValue, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'StringTagValue':
        return cls(next(tag for tag in tags if tag.ID == json_data['Tag']), json_data['Value'], json_data['ID'])


class ProjectPreferences(BaseData):
    def __init__(self, name: str = "", patient_database: str = "", localizer_database: str = "",
                 aliases: List[Alias] = None, general_tags: List[BaseTag] = None,
                 patients_tags: List[BaseTag] = None, sites_tags: List[BaseTag] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.patient_database = patient_database
        self.localizer_database = localizer_database
        self.aliases = aliases if aliases is not None else []
        self.general_tags = general_tags if general_tags is not None else []
        self.patients_tags = patients_tags if patients_tags is not None else []
        self.sites_tags = sites_tags if sites_tags is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['PatientDatabase'] = self.patient_database
        json_data['LocalizerDatabase'] = self.localizer_database
        json_data['Aliases'] = [alias.to_json_data() for alias in self.aliases]
        json_data['GeneralTags'] = [tag.to_json_data() for tag in self.general_tags]
        json_data['PatientsTags'] = [tag.to_json_data() for tag in self.patients_tags]
        json_data['SitesTags'] = [tag.to_json_data() for tag in self.sites_tags]
        return json_data

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file) -> 'ProjectPreferences':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f))

    @classmethod
    def from_json_data(cls, json_data) -> 'ProjectPreferences':
        return cls(json_data["Name"],
                   json_data["PatientDatabase"],
                   json_data["LocalizerDatabase"],
                   [Alias.from_json_data(alias) for alias in json_data["Aliases"]],
                   [BaseTag.from_json_data(tag) for tag in json_data["GeneralTags"]],
                   [BaseTag.from_json_data(tag) for tag in json_data["PatientsTags"]],
                   [BaseTag.from_json_data(tag) for tag in json_data["SitesTags"]],
                   json_data["ID"])
