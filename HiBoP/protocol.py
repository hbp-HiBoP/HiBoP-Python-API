import uuid
import json
from HiBoP.tools import Window
from typing import List


class Event:
    def __init__(self, name: str = "", codes: List[int] = None, typeEnum: int = 0):
        self.name = name
        self.codes = codes
        self.typeEnum = typeEnum

    def to_json_data(self):
        return dict(Name=self.name, Codes=self.codes, Type=self.typeEnum)

    @classmethod
    def from_json_data(cls, json_data) -> 'Event':
        return cls(json_data["Name"], json_data["Codes"], json_data["Type"])


class Icon:
    def __init__(self, name: str = "", illustration_path: str = "", window: Window = None):
        self.name = name
        self.illustration_path = illustration_path
        self.window = window

    def to_json_data(self) -> dict:
        return dict(Name=self.name, IllustrationPath=self.illustration_path, Window=self.window)

    @classmethod
    def from_json_data(cls, json_data) -> 'Icon':
        return cls(json_data["Name"], json_data["IllustrationPath"], json_data["Window"])


class Treatment:
    def __init__(self, order: int = 0, window: Window = None):
        self.order = order
        self.window = window

    def to_json_data(self) -> dict:
        return dict(Order=self.order, Window=self.window)

    @classmethod
    def from_json_data(cls, json_data) -> 'Treatment':
        return cls(json_data["Order"], json_data["Window"])


class SubBloc:
    def __init__(self, name: str = "", order: int = 0, type_enum: int = 0,
                 window: Window = None, baseline: Window = None, events: List[Event] = None,
                 icons: List[Icon] = None, treatments: List[Treatment] = None, ID: str = ""):
        self.name = name
        self.order = order
        self.type_enum = type_enum
        self.window = window
        self.baseline = baseline
        self.events = events if events is not None else []
        self.icons = icons if events is not None else []
        self.treatments = treatments if treatments is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def to_json_data(self):
        return dict(ID=self.ID, Name=self.name, Order=self.order, Type=self.type_enum,
                    Window=self.window, Baseline=self.baseline,
                    Events=[event.to_json_data() for event in self.events],
                    Icons=[icon.to_json_data() for icon in self.icons],
                    Treatments=[treatment.to_json_data() for treatment in self.treatments])

    @classmethod
    def from_json_data(cls, json_data) -> 'SubBloc':
        return cls(json_data["Name"], json_data["Order"], json_data["Type"], json_data["Window"], json_data["Baseline"],
                   [Event.from_json_data(event) for event in json_data["Events"]],
                   [Icon.from_json_data(icon) for icon in json_data["Icons"]],
                   [Treatment.from_json_data(treatment) for treatment in json_data["Treatments"]],
                   json_data["ID"])


class Bloc:
    def __init__(self, name: str = "", order: int = 0, sort: str = "", illustration_path: str = "",
                 sub_blocs: List[SubBloc] = None, ID: str = ""):
        self.name = name
        self.order = order
        self.sort = sort
        self.illustration_path = illustration_path
        self.sub_blocs = sub_blocs if sub_blocs is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def to_json_data(self):
        return dict(ID=self.ID, Name=self.name, Order=self.order, Sort=self.sort,
                    SubBlocs=[sub_bloc.to_json_data() for sub_bloc in self.sub_blocs],
                    IllustrationPath=self.illustration_path)

    @classmethod
    def from_json_data(cls, json_data) -> 'Bloc':
        return cls(json_data["Name"], json_data["Order"], json_data["Sort"], json_data["IllustrationPath"],
                   [SubBloc.from_json_data(sub) for sub in json_data["SubBlocs"]], json_data["ID"])


class Protocol:
    def __init__(self, name: str = "", blocs: List[Bloc] = None, ID: str = ""):
        self.name = name
        self.blocs = blocs if blocs is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def __repr__(self):
        return str(super().__repr__()) + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self):
        return dict(ID=self.ID, Name=self.name, Blocs=[bloc.to_json_data() for bloc in self.blocs])

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f,  indent=2)

    @classmethod
    def from_json_file(cls, json_file: str) -> 'Protocol':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f))

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Protocol':
        return cls(json_data["Name"], [Bloc.from_json_data(bloc) for bloc in json_data["Blocs"]], json_data["ID"])
