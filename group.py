import json
from tools import BaseData
from typing import List
from project import Project
from patient import Patient


class Group(BaseData):
    def __init__(self, name: str = "", patients: List[Patient] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.patients = patients if patients is not None else []

    def __repr__(self):
        return str(super().__repr__()) + "\n" + json.dumps(self.to_json_data(), indent=2)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Patients'] = [patient.ID for patient in self.patients]
        return json_data

    def to_json_file(self, json_file):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file, project: Project) -> 'Group':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), project)

    @classmethod
    def from_json_data(cls, json_data: dict, project: Project = None) -> 'Group':
        return cls(json_data["Name"],
                   [next(patient for patient in project.patients if patient.ID == patient_ID) for patient_ID in
                    json_data["Patients"]],
                   json_data["ID"])
