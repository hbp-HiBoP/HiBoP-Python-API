import abc
import uuid
import json

from patient import Coordinate, Site
from settings import BaseTag
from typing import List


class BaseData(abc.ABC):
    def __init__(self, ID: str = ""):
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def __repr__(self):
        return str(super().__repr__()) + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    @abc.abstractmethod
    def to_json_data(self) -> dict:
        return dict(ID=self.ID)

    @classmethod
    def from_json_data(cls, json_data) -> 'BaseData':
        pass


class Quaternion:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def to_json_data(self) -> dict:
        return dict(x=self.x, y=self.y, z=self.z, w=self.w)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Quaternion':
        return cls(json_data["x"], json_data["y"], json_data["z"], json_data["w"])


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_json_data(self) -> dict:
        return dict(x=self.x, y=self.y, z=self.z)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Vector3':
        return cls(json_data["x"], json_data["y"], json_data["z"])


class Window:
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

    def to_json_data(self) -> dict:
        return dict(Start=self.start, End=self.end)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Window':
        return cls(json_data["Start"],
                   json_data["End"])


class Sphere:
    def __init__(self, center: Vector3, radius: float):
        self.center = center
        self.radius = radius

    def to_json_data(self) -> dict:
        return dict(Position=self.center.to_json_data(), Radius=self.radius)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Sphere':
        return cls(Vector3.from_json_data(json_data["Position"]), json_data["Radius"])


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_json_data(self) -> dict:
        return dict(r=self.r,
                    g=self.g,
                    b=self.b,
                    a=self.a)

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Color':
        return cls(json_data["r"],
                   json_data["g"],
                   json_data["b"],
                   json_data["a"])


def generate_site_list_from_intranat_files(patient_pts_path: str, mni_pts_path: str, csv_path: str = "", site_name_correction: bool = True, tags: List[BaseTag] = None) -> 'List[Site]':
    def fix_name(name: str) -> str:
        name = name.upper()
        name = name.replace("PLOT", "")
        prime = name.rfind('P')
        if prime > 0:
            name = name[:prime] + "\'" + name[prime+1:]
        return name
    result = []
    patient_pts_file = open(patient_pts_path, "r")
    patient_pts_file.readline()
    patient_pts_file.readline()
    number_of_sites_in_patient_pts = int(patient_pts_file.readline())
    mni_pts_file = open(mni_pts_path, "r")
    mni_pts_file.readline()
    mni_pts_file.readline()
    number_of_sites_in_mni_pts = int(mni_pts_file.readline())
    if number_of_sites_in_patient_pts != number_of_sites_in_mni_pts:
        print("ERROR: Number of sites is not equal between mni and patient pts files")
        return []
    for i in range(number_of_sites_in_patient_pts):
        patient_line = patient_pts_file.readline().split()
        mni_line = mni_pts_file.readline().split()
        site_name = patient_line[0]
        if site_name_correction:
            site_name = fix_name(site_name)
        patient_coordinate = Coordinate("Patient", Vector3(float(patient_line[1]), float(patient_line[2]), float(patient_line[3])))
        mni_coordinate = Coordinate("MNI", Vector3(float(mni_line[1]), float(mni_line[2]), float(mni_line[3])))
        result.append(Site(site_name, [patient_coordinate, mni_coordinate]))
    patient_pts_file.close()
    mni_pts_file.close()
    return result
