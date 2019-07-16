import uuid
import json
from typing import List
from HiBoP.patient import Patient


class Group:
    def __init__(self, name: str = "", patients: List[Patient] = None, ID: str = None):
        self.name = name
        self.patients = patients if patients is not None else []
        self.ID = ID if ID is not None else str(uuid.uuid4())

    def __repr__(self):
        return str(super().__repr__()) + "\n" + json.dumps(self.to_json_data(), indent=2)

    def to_json_data(self) -> dict:
        return dict(ID=self.ID, Name=self.name, Patients=[patient.ID for patient in self.patients])

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file, project_patients: List[Patient]) -> 'Group':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), project_patients)

    @classmethod
    def from_json_data(cls, json_data, project_patients: List[Patient]) -> 'Group':
        patients = [next(patient for patient in project_patients if patient.ID == patient_ID) for patient_ID in
                    json_data["Patients"]]
        return cls(json_data["Name"], patients, json_data["ID"])
