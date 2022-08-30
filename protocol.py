import json
from tools import Window, BaseData
from typing import List
import enum


class EventType(enum.Enum):
    Main = 0
    Secondary = 1


class Event(BaseData):
    def __init__(self, name: str = "", codes: List[int] = None, event_type: EventType = EventType.Main, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.codes = codes if codes is not None else []
        self.event_type = event_type

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Codes'] = self.codes
        json_data['Type'] = self.event_type.value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Event':
        return cls(json_data["Name"],
                   json_data["Codes"],
                   EventType(json_data["Type"]),
                   json_data['ID'])


class Icon(BaseData):
    def __init__(self, name: str = "", image_path: str = "", window: Window = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.image_path = image_path
        self.window = window if window is not None else Window()

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['ImagePath'] = self.image_path
        json_data['Window'] = self.window.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Icon':
        return cls(json_data["Name"],
                   json_data["ImagePath"],
                   Window.from_json_data(json_data["Window"]),
                   json_data['ID'])


class Treatment(BaseData):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True, baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(ID)
        self.use_on_window = use_on_window
        self.window = window if window is not None else Window()
        self.use_on_baseline = use_on_baseline
        self.baseline = baseline if baseline is not None else Window()
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
    def from_json_data(cls, json_data: dict) -> 'Treatment':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Core.Data.AbsTreatment, Assembly-CSharp":
            result = AbsTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.ClampTreatment, Assembly-CSharp":
            result = ClampTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.FactorTreatment, Assembly-CSharp":
            result = FactorTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.MaxTreatment, Assembly-CSharp":
            result = MaxTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.MeanTreatment, Assembly-CSharp":
            result = MeanTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.MedianTreatment, Assembly-CSharp":
            result = MedianTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.MinTreatment, Assembly-CSharp":
            result = MinTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.OffsetTreatment, Assembly-CSharp":
            result = OffsetTreatment.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.RescaleTreatment, Assembly-CSharp":
            result = RescaleTreatment.from_json_data(json_data)
        return result


class AbsTreatment(Treatment):
    def __init__(self, use_on_window: bool = True, window: Window = None, use_on_baseline: bool = True,
                 baseline: Window = None, order: int = 0, ID: str = ""):
        super().__init__(use_on_window, window, use_on_baseline, baseline, order, ID)

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.AbsTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'AbsTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.ClampTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['UseMinClamp'] = self.use_min_clamp
        json_data['Min'] = self.min_value
        json_data['UseMaxClamp'] = self.use_max_clamp
        json_data['Max'] = self.max_value
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'ClampTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.FactorTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['Factor'] = self.factor
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'FactorTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MaxTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'MaxTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MeanTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'MeanTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MedianTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'MedianTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MinTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'MinTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.OffsetTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['Offset'] = self.offset
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'OffsetTreatment':
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
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.RescaleTreatment, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data['BeforeMin'] = self.before_min
        json_data['BeforeMax'] = self.before_max
        json_data['AfterMin'] = self.after_min
        json_data['AfterMax'] = self.after_max
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'RescaleTreatment':
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


class SubBlocType(enum.Enum):
    Main = 0
    Secondary = 1


class SubBloc(BaseData):
    def __init__(self, name: str = "", order: int = 0, subBloc_type: SubBlocType = 0,
                 window: Window = None, baseline: Window = None, events: List[Event] = None,
                 icons: List[Icon] = None, treatments: List[Treatment] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.order = order
        self.subBloc_type = subBloc_type
        self.window = window if window is not None else Window()
        self.baseline = baseline if baseline is not None else Window()
        self.events = events if events is not None else []
        self.icons = icons if icons is not None else []
        self.treatments = treatments if treatments is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Order'] = self.order
        json_data['Type'] = self.subBloc_type.value
        json_data['Window'] = self.window.to_json_data()
        json_data['Baseline'] = self.baseline.to_json_data()
        json_data['Events'] = [event.to_json_data() for event in self.events]
        json_data['Icons'] = [icon.to_json_data() for icon in self.icons]
        json_data['Treatments'] = [treatment.to_json_data() for treatment in self.treatments]
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'SubBloc':
        return cls(json_data["Name"],
                   json_data["Order"],
                   SubBlocType(json_data["Type"]),
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
    def from_json_data(cls, json_data: dict) -> 'Bloc':
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
    def from_json_data(cls, json_data: dict) -> 'Protocol':
        return cls(json_data["Name"],
                   [Bloc.from_json_data(bloc) for bloc in json_data["Blocs"]],
                   json_data["ID"])
