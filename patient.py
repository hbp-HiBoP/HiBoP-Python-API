import json
import abc
from settings import BaseTagValue, BaseTag
from tools import Vector3, BaseData
from typing import List


class BaseMesh(BaseData):
    def __init__(self, name: str = "", transformation: str = "", ID: str = ""):
        self.name = name
        self.transformation = transformation
        super().__init__(ID)

    @abc.abstractmethod
    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Transformation'] = self.transformation
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'BaseMesh':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Core.Data.LeftRightMesh, Assembly-CSharp":
            result = LeftRightMesh.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.SingleMesh, Assembly-CSharp":
            result = SingleMesh.from_json_data(json_data)
        return result


class LeftRightMesh(BaseMesh):
    def __init__(self, name: str = "", left_hemisphere_mesh: str = "", right_hemisphere_mesh: str = "",
                 left_marsAtlas_hemisphere: str = "", right_marsAtlas_hemisphere: str = "", transformation: str = "",
                 ID: str = ""):
        self.left_hemisphere_mesh = left_hemisphere_mesh
        self.right_hemisphere_mesh = right_hemisphere_mesh
        self.left_marsAtlas_hemisphere = left_marsAtlas_hemisphere
        self.right_marsAtlas_hemisphere = right_marsAtlas_hemisphere
        super().__init__(name, transformation, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.LeftRightMesh, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["LeftHemisphere"] = self.left_hemisphere_mesh
        json_data["RightHemisphere"] = self.right_hemisphere_mesh
        json_data["LeftMarsAtlasHemisphere"] = self.left_marsAtlas_hemisphere
        json_data["RightMarsAtlasHemisphere"] = self.right_marsAtlas_hemisphere
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'LeftRightMesh':
        return cls(json_data["Name"],
                   json_data["LeftHemisphere"],
                   json_data["RightHemisphere"],
                   json_data["LeftMarsAtlasHemisphere"],
                   json_data["RightMarsAtlasHemisphere"],
                   json_data["Transformation"],
                   json_data["ID"])


class SingleMesh(BaseMesh):
    def __init__(self, name: str = "", path: str = "", marsAtlasPath: str = "", transformation: str = "", ID: str = ""):
        self.path = path
        self.marsAtlasPath = marsAtlasPath
        super().__init__(name, transformation, ID)

    def to_json_data(self):
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.SingleMesh, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Path"] = self.path
        json_data["MarsAtlasPath"] = self.marsAtlasPath
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'SingleMesh':
        return cls(json_data["Name"],
                   json_data["Path"],
                   json_data["MarsAtlasPath"],
                   json_data["Transformation"],
                   json_data["ID"])


class MRI(BaseData):
    def __init__(self, name: str = "", file: str = "", ID: str = ""):
        self.name = name
        self.file = file
        super().__init__(ID)

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['File'] = self.file
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'MRI':
        return cls(json_data["Name"],
                   json_data["File"],
                   json_data['ID'])


class Coordinate(BaseData):
    def __init__(self, reference_system: str = "", position: Vector3 = None, ID: str = ""):
        self.reference_system = reference_system
        self.position = position
        super().__init__(ID)

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['ReferenceSystem'] = self.reference_system
        json_data['Position'] = self.position.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'Coordinate':
        return cls(json_data["ReferenceSystem"], Vector3.from_json_data(json_data["Position"]), json_data['ID'])


class Site(BaseData):
    def __init__(self, name: str = "", coordinates: List[Coordinate] = None, tags: List[BaseTagValue] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.coordinates = coordinates if coordinates is not None else []
        self.tags = tags if tags is not None else []

    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Coordinates'] = [coordinate.to_json_data() for coordinate in self.coordinates]
        json_data['Tags'] = [tag.to_json_data() for tag in self.tags]
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'Site':
        return cls(json_data['Name'],
                   [Coordinate.from_json_data(coordinate) for coordinate in json_data['Coordinates']],
                   [BaseTagValue.from_json_data(tagID, tags) for tagID in json_data['Tags']],
                   json_data['ID'])


class Patient(BaseData):
    def __init__(self, name: str = "John Doe", date: int = 0, place: str = "Unknown", meshes: List[BaseMesh] = None,
                 MRIs: List[MRI] = None, sites: List[Site] = None, tags: List[BaseTagValue] = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.date = date
        self.place = place
        self.meshes = meshes if meshes is not None else []
        self.MRIs = MRIs if MRIs is not None else []
        self.sites = sites if sites is not None else []
        self.tags = tags if tags is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Date'] = self.date
        json_data['Place'] = self.place
        json_data['Meshes'] = [mesh.to_json_data() for mesh in self.meshes]
        json_data['MRIs'] = [mri.to_json_data() for mri in self.MRIs]
        json_data['Sites'] = [site.to_json_data() for site in self.sites]
        json_data['Tags'] = [tag.to_json_data() for tag in self.tags]
        return json_data

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file: str, tags: List[BaseTag] = None) -> 'Patient':
        with open(json_file, "r") as f:
            json_data = json.load(f)
            return cls.from_json_data(json_data, tags)

    @classmethod
    def from_json_data(cls, json_data: dict, tags: List[BaseTag] = None) -> 'Patient':
        return cls(json_data["Name"],
                   json_data["Date"],
                   json_data["Place"],
                   [BaseMesh.from_json_data(mesh) for mesh in json_data["Meshes"]],
                   [MRI.from_json_data(mri) for mri in json_data["MRIs"]],
                   [Site.from_json_data(site, tags) for site in json_data["Sites"]],
                   [BaseTagValue.from_json_data(tag, tags) for tag in json_data["Tags"]],
                   json_data["ID"])
