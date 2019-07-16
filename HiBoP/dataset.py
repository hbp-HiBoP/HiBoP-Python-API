import uuid
import json
import abc
from typing import List
from HiBoP.protocol import Protocol
from HiBoP.patient import Patient


class DataContainer(abc.ABC):
    def __init__(self, ID: str = ""):
        self.ID = ID if ID != "" else str(uuid.uuid4())

    @abc.abstractmethod
    def to_json_data(self):
        pass

    @classmethod
    def from_json_data(cls, json_data):
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.Container.BrainVision, Assembly-CSharp":
            result = BrainVision.from_json_data(json_data)
        elif class_type == "HBP.Data.Container.Elan, Assembly-CSharp":
            result = Elan.from_json_data(json_data)
        return result


class BrainVision(DataContainer):
    def __init__(self, header: str = "", ID: str = ""):
        super().__init__(ID)
        self.header = header

    def to_json_data(self) -> dict:
        result = dict()
        result["&type"] = "HBP.Data.Container.BrainVision, Assembly-CSharp"
        result["ID"] = self.ID
        result["Header"] = self.header
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'BrainVision':
        return cls(json_data["Header"], json_data["ID"])


class Elan(DataContainer):
    def __init__(self, eeg: str = "", pos: str = "", notes: str = "", ID: str = ""):
        super().__init__(ID)
        self.eeg = eeg
        self.pos = pos
        self.notes = notes

    def to_json_data(self) -> dict:
        result = dict()
        result["&type"] = "HBP.Data.Container.Elan, Assembly-CSharp"
        result["ID"] = self.ID
        result["EEG"] = self.eeg
        result["POS"] = self.pos
        result["Notes"] = self.notes
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'Elan':
        return cls(json_data["EEG"], json_data["POS"], json_data["Notes"], json_data["ID"])


class DataInfo(abc.ABC):
    def __init__(self, name: str, data_container: DataContainer = None, ID: str = ""):
        self.name = name
        self.data_container = data_container
        self.ID = ID if ID != "" else str(uuid.uuid4())

    @abc.abstractmethod
    def to_json_data(self):
        pass

    @classmethod
    def from_json_data(cls, json_data, project_patients: List[Patient]):
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.Experience.Dataset.iEEGDataInfo, Assembly-CSharp":
            result = IEEGDataInfo.from_json_data(json_data, project_patients)
        elif class_type == "HBP.Data.Experience.Dataset.CCEPDataInfo, Assembly-CSharp":
            result = CCEPDataInfo.from_json_data(json_data, project_patients)
        return result


class IEEGDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None, patient: Patient = None,
                 normalization: int = 0, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient
        self.normalization = normalization

    def to_json_data(self) -> dict:
        result = dict()
        result["&type"] = "HBP.Data.Experience.Dataset.iEEGDataInfo, Assembly-CSharp"
        result["ID"] = self.ID
        result["Name"] = self.name
        result["Patient"] = self.patient.ID
        result["DataContainer"] = self.data_container.to_json_data()
        result["Normalization"] = self.normalization
        return result

    @classmethod
    def from_json_data(cls, json_data, project_patients) -> 'IEEGDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in project_patients if patient.ID == json_data["Patient"]),
                   json_data["Normalization"],
                   json_data["ID"])


class CCEPDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None,
                 patient: Patient = None, stimulated_channel: str = 0, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient
        self.stimulated_channel = stimulated_channel

    def to_json_data(self) -> dict:
        result = dict()
        result["&type"] = "HBP.Data.Experience.Dataset.CCEPDataInfo, Assembly-CSharp"
        result["ID"] = self.ID
        result["Name"] = self.name
        result["Patient"] = self.patient.ID
        result["DataContainer"] = self.data_container.to_json_data()
        result["StimulatedChannel"] = self.stimulated_channel
        return result

    @classmethod
    def from_json_data(cls, json_data, project_patients: List[Patient]) -> 'CCEPDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in project_patients if patient.ID == json_data["Patient"]),
                   json_data["StimulatedChannel"],
                   json_data["ID"])


class Dataset:
    def __init__(self, name: str = "", protocol: Protocol = None, data: List[DataInfo] = None, ID: str = ""):
        self.name = name
        self.protocol = protocol
        self.data = data if data is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def __repr__(self):
        return str(super().__repr__()) + "\n" + json.dumps(self.to_json_data(), indent=2)

    def to_json_data(self) -> dict:
        return dict(ID=self.ID,
                    Name=self.name,
                    Protocol=self.protocol.ID,
                    Data=[data.to_json_data() for data in self.data])

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file, project_protocols: List[Protocol], project_patients: List[Patient]) -> 'Dataset':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), project_protocols, project_patients)

    @classmethod
    def from_json_data(cls, json_data, project_protocols: List[Protocol], project_patients: List[Patient]) -> 'Dataset':
        return cls(json_data["Name"],
                   next(protocol for protocol in project_protocols if protocol.ID == json_data["Protocol"]),
                   [DataInfo.from_json_data(data, project_patients) for data in json_data["Data"]],
                   json_data["ID"])
