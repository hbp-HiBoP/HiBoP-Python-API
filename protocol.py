import json
from tools import Window, BaseData
from typing import List
from project import Project


class Event(BaseData):
    def __init__(self, name: str = "", codes: List[int] = None, type_enum: int = 0, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.codes = codes if codes is not None else []
        self.type_enum = type_enum

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Codes'] = self.codes
        json_data['Type'] = self.type_enum
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'Event':
        return cls(json_data["Name"],
                   json_data["Codes"],
                   json_data["Type"],
                   json_data['ID'])


class Icon(BaseData):
    def __init__(self, name: str = "", illustration_path: str = "", window: Window = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.illustration_path = illustration_path
        self.window = window if window is not None else Window()

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['IllustrationPath'] = self.illustration_path
        json_data['Window'] = self.window.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'Icon':
        return cls(json_data["Name"],
                   json_data["IllustrationPath"],
                   Window.from_json_data(json_data["Window"]))


class Treatment(BaseData):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True, baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(ID)
        self.use_on_window = use_on_window
        self.window = window
        self.use_on_baseline = use_on_baseline
        self.baseline = baseline
        self.order = order

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['UseOnWindow'] = self.use_on_window
        json_data['Window'] = self.window.to_json_data()
        json_data['UseOnBaseline'] = self.use_on_baseline
        json_data['Baseline'] = self.baseline.to_json_data()
        json_data['Order'] = self.order
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'Treatment':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.Experience.Protocol.AbsTreatment, Assembly-CSharp":
            result = AbsTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.ClampTreatment, Assembly-CSharp":
            result = ClampTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.FactorTreatment, Assembly-CSharp":
            result = FactorTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.MaxTreatment, Assembly-CSharp":
            result = MaxTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.MeanTreatment, Assembly-CSharp":
            result = MeanTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.MedianTreatment, Assembly-CSharp":
            result = MedianTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.MinTreatment, Assembly-CSharp":
            result = MinTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.OffsetTreatment, Assembly-CSharp":
            result = OffsetTreatment.from_json_data(json_data)
        elif class_type == "HBP.Data.Experience.Protocol.RescaleTreatment, Assembly-CSharp":
            result = RescaleTreatment.from_json_data(json_data)
        return result


class AbsTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.AbsTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'AbsTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data["Order"],
                   json_data["ID"])


class ClampTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, use_min_clamp: bool = True, min_value: float = 0.0, use_max_clamp: bool = True,
                 max_value: float = 0.0, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)
        self.use_min_clamp = use_min_clamp
        self.use_max_clamp = use_max_clamp
        self.min_value = min_value
        self.max_value = max_value

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['UseMinClamp'] = self.use_min_clamp
        json_data['Min'] = self.min_value
        json_data['UseMaxClamp'] = self.use_max_clamp
        json_data['Max'] = self.max_value
        json_data["$type"] = "HBP.Data.Experience.Protocol.ClampTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'ClampTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data['UseMinClamp'],
                   json_data['Min'],
                   json_data['UseMaxClamp'],
                   json_data['Max'],
                   json_data["Order"],
                   json_data["ID"])


class FactorTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, factor: float = 0.0, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)
        self.factor = factor

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Factor'] = self.factor
        json_data["$type"] = "HBP.Data.Experience.Protocol.FactorTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'FactorTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data['Factor'],
                   json_data["Order"],
                   json_data["ID"])


class MaxTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.MaxTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'MaxTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data["Order"],
                   json_data["ID"])


class MeanTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.MeanTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'MeanTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data["Order"],
                   json_data["ID"])


class MedianTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.MedianTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'MedianTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data["Order"],
                   json_data["ID"])


class MinTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.MinTreatment, Assembly-CSharp"
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'MinTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data["Order"],
                   json_data["ID"])


class OffsetTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, offset: float = 0.0, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)
        self.offset = offset

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.OffsetTreatment, Assembly-CSharp"
        json_data['Offset'] = self.offset
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'OffsetTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data['Offset'],
                   json_data["Order"],
                   json_data["ID"])


class RescaleTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, before_min: float = 0.0, before_max: float = 0.0,
                 after_min: float = 0.0, after_max: float = 0.0, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)
        self.before_min = before_min
        self.before_max = before_max
        self.after_min = after_min
        self.after_max = after_max

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["$type"] = "HBP.Data.Experience.Protocol.RescaleTreatment, Assembly-CSharp"
        json_data['BeforeMin'] = self.before_min
        json_data['BeforeMax'] = self.before_max
        json_data['AfterMin'] = self.after_min
        json_data['AfterMax'] = self.after_max
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'RescaleTreatment':
        return cls(json_data["UseOnWindow"],
                   Window.from_json_data(json_data["Window"]),
                   json_data["UseOnBaseline"],
                   Window.from_json_data(json_data["Baseline"]),
                   json_data['BeforeMin'],
                   json_data['BeforeMax'],
                   json_data['AfterMin'],
                   json_data['AfterMax'],
                   json_data["Order"],
                   json_data["ID"])


class SubBloc(BaseData):
    def __init__(self, name: str = "", order: int = 0, type_enum: int = 0,
                 window: Window = None, baseline: Window = None, events: List[Event] = None,
                 icons: List[Icon] = None, treatments: List[Treatment] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.order = order
        self.type_enum = type_enum
        self.window = window if window is not None else Window()
        self.baseline = baseline if baseline is not None else Window()
        self.events = events if events is not None else []
        self.icons = icons if events is not None else []
        self.treatments = treatments if treatments is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Order'] = self.order
        json_data['Type'] = self.type_enum
        json_data['Window'] = self.window.to_json_data()
        json_data['Baseline'] = self.baseline.to_json_data()
        json_data['Events'] = [event.to_json_data() for event in self.events]
        json_data['Icons'] = [icon.to_json_data() for icon in self.icons]
        json_data['Treatments'] = [treatment.to_json_data() for treatment in self.treatments]
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'SubBloc':
        return cls(json_data["Name"],
                   json_data["Order"],
                   json_data["Type"],
                   Window.from_json_data(json_data["Window"]),
                   Window.from_json_data(json_data["Baseline"]),
                   [Event.from_json_data(event) for event in json_data["Events"]],
                   [Icon.from_json_data(icon) for icon in json_data["Icons"]],
                   [Treatment.from_json_data(treatment) for treatment in json_data["Treatments"]],
                   json_data["ID"])


class Bloc(BaseData):
    def __init__(self, name: str = "", order: int = 0, illustration_path: str = "", sort: str = "",
                 sub_blocs: List[SubBloc] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.order = order
        self.illustration_path = illustration_path
        self.sort = sort
        self.sub_blocs = sub_blocs if sub_blocs is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Order'] = self.order
        json_data['IllustrationPath'] = self.illustration_path
        json_data['Sort'] = self.sort
        json_data['SubBlocs'] = [sub_bloc.to_json_data() for sub_bloc in self.sub_blocs]
        return json_data

    @classmethod
    def from_json_data(cls, json_data, project: Project = None) -> 'Bloc':
        return cls(json_data["Name"],
                   json_data["Order"],
                   json_data["IllustrationPath"],
                   json_data["Sort"],
                   [SubBloc.from_json_data(sub_bloc) for sub_bloc in json_data["SubBlocs"]],
                   json_data["ID"])


class Protocol(BaseData):
    def __init__(self, name: str = "", blocs: List[Bloc] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.blocs = blocs if blocs is not None else []

    def __repr__(self):
        return str(super().__repr__()) + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Blocs'] = [bloc.to_json_data() for bloc in self.blocs]
        return json_data

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f,  indent=2)

    @classmethod
    def from_json_file(cls, json_file: str) -> 'Protocol':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f))

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'Protocol':
        return cls(json_data["Name"],
                   [Bloc.from_json_data(bloc) for bloc in json_data["Blocs"]],
                   json_data["ID"])
