from tools import *
from typing import List
from protocol import Protocol
from patient import Patient
import enum


class NormalizationType(enum.Enum):
    No = 0
    SubTrial = 1
    Trial = 2
    SubBloc = 3
    Bloc = 4
    Protocol = 5
    Auto = 6


class DataContainer(BaseData):
    def __init__(self, ID: str = ""):
        super().__init__(ID)

    @abc.abstractmethod
    def to_json_data(self):
        return super().to_json_data()

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'DataContainer':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Core.Data.Container.BrainVision, Assembly-CSharp" or class_type == "HBP.Data.Container.BrainVision, Assembly-CSharp":
            result = BrainVision.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.Container.Elan, Assembly-CSharp" or class_type == "HBP.Data.Container.Elan, Assembly-CSharp":
            result = Elan.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.Container.EDF, Assembly-CSharp" or class_type == "HBP.Data.Container.EDF, Assembly-CSharp":
            result = EDF.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.Container.Micromed, Assembly-CSharp" or class_type == "HBP.Data.Container.Micromed, Assembly-CSharp":
            result = Micromed.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.Container.FIF, Assembly-CSharp" or class_type == "HBP.Data.Container.FIF, Assembly-CSharp":
            result = FIF.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.Container.Nifti, Assemby-CSharp" or class_type == "HBP.Data.Container.Nifti, Assemby-CSharp":
            result = Nifti.from_json_data(json_data)
        return result


class BrainVision(DataContainer):
    def __init__(self, header: str = "", ID: str = ""):
        super().__init__(ID)
        self.header = header

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.BrainVision, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Header"] = self.header
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'BrainVision':
        return cls(json_data["Header"], json_data["ID"])


class EDF(DataContainer):
    def __init__(self, edf: str = "", ID: str = ""):
        super().__init__(ID)
        self.edf = edf

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.EDF, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["EDF"] = self.edf
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'EDF':
        return cls(json_data["EDF"], json_data["ID"])


class Micromed(DataContainer):
    def __init__(self, trc: str = "", ID: str = ""):
        super().__init__(ID)
        self.trc = trc

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.Micromed, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["TRC"] = self.trc
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'Micromed':
        return cls(json_data["TRC"], json_data["ID"])


class Elan(DataContainer):
    def __init__(self, eeg: str = "", pos: str = "", notes: str = "", ID: str = ""):
        super().__init__(ID)
        self.eeg = eeg
        self.pos = pos
        self.notes = notes

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.Elan, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["EEG"] = self.eeg
        json_data["POS"] = self.pos
        json_data["Notes"] = self.notes
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'Elan':
        return cls(json_data["EEG"], json_data["POS"], json_data["Notes"], json_data["ID"])


class FIF(DataContainer):
    def __init__(self, fif: str = "", ID: str = ""):
        super().__init__(ID)
        self.fif = fif

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.FIF, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["FIF"] = self.fif
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'FIF':
        return cls(json_data["FIF"], json_data["ID"])


class Nifti(DataContainer):
    def __init__(self, file: str = "", ID: str = ""):
        super().__init__(ID)
        self.file = file

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.Container.Nifti, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["File"] = self.file
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'Nifti':
        return cls(json_data["File"], json_data["ID"])


class DataInfo(BaseData):
    def __init__(self, name: str, data_container: DataContainer = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.data_container = data_container

    @abc.abstractmethod
    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['DataContainer'] = self.data_container.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, patients: List[Patient] = None) -> 'DataInfo':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Core.Data.IEEGDataInfo, Assembly-CSharp" or class_type == "HBP.Data.Experience.Dataset.IEEGDataInfo, Assembly-CSharp":
            result = IEEGDataInfo.from_json_data(json_data, patients)
        elif class_type == "HBP.Core.Data.CCEPDataInfo, Assembly-CSharp" or class_type == "HBP.Data.Experience.Dataset.CCEPDataInfo, Assembly-CSharp":
            result = CCEPDataInfo.from_json_data(json_data, patients)
        elif class_type == "HBP.Core.Data.FMRIDataInfo, Assembly-CSharp" or class_type == "HBP.Data.Experience.Dataset.FMRIDataInfo, Assembly-CSharp":
            result = FMRIDataInfo.from_json_data(json_data, patients)
        elif class_type == "HBP.Core.Data.MEGcDataInfo, Assembly-CSharp" or class_type == "HBP.Data.Experience.Dataset.MEGcDataInfo, Assembly-CSharp":
            result = MEGcDataInfo.from_json_data(json_data, patients)
        elif class_type == "HBP.Core.Data.MEGvDataInfo, Assembly-CSharp" or class_type == "HBP.Data.Experience.Dataset.MEGvDataInfo, Assembly-CSharp":
            result = MEGvDataInfo.from_json_data(json_data, patients)
        return result


class IEEGDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None, patient: Patient = None,
                 normalization: NormalizationType = NormalizationType.No, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient
        self.normalization = normalization

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.IEEGDataInfo, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Patient"] = self.patient.ID
        json_data["Normalization"] = self.normalization.value
        return json_data

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None) -> 'IEEGDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in patients if patient.ID == json_data["Patient"]),
                   NormalizationType(json_data["Normalization"]),
                   json_data["ID"])


class CCEPDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None,
                 patient: Patient = None, stimulated_channel: str = 0, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient
        self.stimulated_channel = stimulated_channel

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.CCEPDataInfo, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Patient"] = self.patient.ID
        json_data["StimulatedChannel"] = self.stimulated_channel
        return json_data

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None) -> 'CCEPDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in patients if patient.ID == json_data["Patient"]),
                   json_data["StimulatedChannel"],
                   json_data["ID"])


class FMRIDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None, patient: Patient = None, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.FMRIDataInfo, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Patient"] = self.patient.ID
        return json_data

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None) -> 'FMRIDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in patients if patient.ID == json_data["Patient"]),
                   json_data["ID"])


class MEGcDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None, patient: Patient = None, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MEGcDataInfo, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Patient"] = self.patient.ID
        return json_data

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None) -> 'MEGcDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in patients if patient.ID == json_data["Patient"]),
                   json_data["ID"])


class MEGvDataInfo(DataInfo):
    def __init__(self, name: str = "", data_container: DataContainer = None, patient: Patient = None, ID: str = ""):
        super().__init__(name, data_container, ID)
        self.patient = patient

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.MEGvDataInfo, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Patient"] = self.patient.ID
        return json_data

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None) -> 'MEGvDataInfo':
        return cls(json_data["Name"],
                   DataContainer.from_json_data(json_data["DataContainer"]),
                   next(patient for patient in patients if patient.ID == json_data["Patient"]),
                   json_data["ID"])


class Dataset(BaseData):
    def __init__(self, name: str = "", protocol: Protocol = None, data: List[DataInfo] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.protocol = protocol
        self.data = data if data is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Protocol'] = self.protocol.ID
        json_data['Data'] = [data.to_json_data() for data in self.data]
        return json_data

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file, project_protocols: List[Protocol], project_patients: List[Patient]) -> 'Dataset':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), project_protocols, project_patients)

    @classmethod
    def from_json_data(cls, json_data: dict, protocols: List[Protocol] = None, patients: List[Patient] = None) -> 'Dataset':
        return cls(json_data["Name"],
                   next(protocol for protocol in protocols if protocol.ID == json_data["Protocol"]),
                   [DataInfo.from_json_data(data, patients) for data in json_data["Data"]],
                   json_data["ID"])