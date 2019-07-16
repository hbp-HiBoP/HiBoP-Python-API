import uuid
import json
import abc
from typing import List


class Mesh(abc.ABC):
    def __init__(self, name: str = "", transformation: str = "", ID: str = ""):
        self.name = name
        self.transformation = transformation
        self.ID = ID if ID != "" else str(uuid.uuid4())

    @abc.abstractmethod
    def to_json_data(self):
        pass

    @classmethod
    def from_json_data(cls, json_data):
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.Anatomy.LeftRightMesh, Assembly-CSharp":
            result = LeftRightMesh.from_json_data(json_data)
        elif class_type == "HBP.Data.Anatomy.SingleMesh, Assembly-CSharp":
            result = SingleMesh.from_json_data(json_data)
        return result


class LeftRightMesh(Mesh):
    def __init__(self, name: str = "", left_hemisphere_mesh: str = "", right_hemisphere_mesh: str = "",
                 left_marsAtlas_hemisphere: str = "", right_marsAtlas_hemisphere: str = "", transformation: str = "",
                 ID: str = ""):
        self.left_hemisphere_mesh = left_hemisphere_mesh
        self.right_hemisphere_mesh = right_hemisphere_mesh
        self.left_marsAtlas_hemisphere = left_marsAtlas_hemisphere
        self.right_marsAtlas_hemisphere = right_marsAtlas_hemisphere
        super().__init__(name, transformation, ID)

    def to_json_data(self):
        result = dict()
        result["&type"] = "HBP.Data.Anatomy.LeftRightMesh, Assembly-CSharp"
        result["ID"] = self.ID
        result["Name"] = self.name
        result["LeftHemisphere"] = self.left_hemisphere_mesh
        result["RightHemisphere"] = self.right_hemisphere_mesh
        result["LeftMarsAtlasHemisphere"] = self.left_marsAtlas_hemisphere
        result["RightMarsAtlasHemisphere"] = self.right_marsAtlas_hemisphere
        result["Transformation"] = self.transformation
        return result

    @classmethod
    def from_json_data(cls, json_data):
        result = cls(json_data["Name"], json_data["LeftHemisphere"], json_data["RightHemisphere"],
                     json_data["LeftMarsAtlasHemisphere"], json_data["RightMarsAtlasHemisphere"],
                     json_data["Transformation"], json_data["ID"])
        return result


class SingleMesh(Mesh):
    def __init__(self, name: str = "", mesh: str = "", marsAtlas: str = "", transformation: str = "", ID: str = ""):
        self.mesh = mesh
        self.marsAtlas = marsAtlas
        super().__init__(name, transformation, ID)

    def to_json_data(self):
        result = dict()
        result["&type"] = "HBP.Data.Anatomy.SingleMesh, Assembly-CSharp"
        result["ID"] = self.ID
        result["Name"] = self.name
        result["Mesh"] = self.mesh
        result["MarsAtlas"] = self.marsAtlas
        result["Transformation"] = self.transformation
        return result

    @classmethod
    def from_json_data(cls, json_data):
        result = cls(json_data["Name"], json_data["Mesh"], json_data["MarsAtlas"],
                     json_data["Transformation"], json_data["ID"])
        return result


class MRI:
    def __init__(self, name: str = "", file: str = ""):
        self.name = name
        self.file = file

    def to_json_data(self):
        return dict(Name=self.name, File=self.file)

    @classmethod
    def from_json_data(cls, json_data):
        return cls(json_data["Name"], json_data["File"])


class Implantation:
    def __init__(self, name: str = "", file: str = "", marsAtlas: str = ""):
        self.name = name
        self.file = file
        self.marsAtlas = marsAtlas

    def to_json_data(self):
        return dict(Name=self.name, File=self.file, MarsAtlas=self.marsAtlas)

    @classmethod
    def from_json_data(cls, json_data):
        return cls(json_data["Name"], json_data["File"], json_data["MarsAtlas"])


class Patient:
    def __init__(self, name: str = "John Doe", date: int = 0, place: str = "Unknown", meshes: List[Mesh] = None,
                 MRIs: List[MRI] = None, connectivities=None, implantations: List[Implantation] = None, ID: str = ""):
        self.name = name
        self.date = date
        self.place = place
        self.meshes = meshes if meshes is not None else []
        self.MRIs = MRIs if MRIs is not None else []
        self.connectivities = connectivities if connectivities is not None else []
        self.implantations = implantations if implantations is not None else []
        self.ID = ID if ID != "" else str(uuid.uuid4())

    def __repr__(self):
        return str(super().__repr__()) + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self):
        brain_dictionary = dict(Meshes=[mesh.to_json_data() for mesh in self.meshes],
                                MRIs=[mri.to_json_data() for mri in self.MRIs],
                                Connectivities=self.connectivities,
                                Implantations=[implantation.to_json_data() for implantation in self.implantations])
        return dict(ID=self.ID, Name=self.name, Date=self.date, Place=self.place, Brain=brain_dictionary)

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    @classmethod
    def from_json_file(cls, json_file: str) -> 'Patient':
        with open(json_file, "r") as f:
            json_data = json.load(f)
            return cls.from_json_data(json_data)

    @classmethod
    def from_json_data(cls, json_data) -> 'Patient':
        brain_dictionary = json_data["Brain"]
        return cls(json_data["Name"],
                   json_data["Date"],
                   json_data["Place"],
                   [Mesh.from_json_data(mesh) for mesh in brain_dictionary["Meshes"]],
                   [MRI.from_json_data(mri) for mri in brain_dictionary["MRIs"]],
                   brain_dictionary["Connectivities"],
                   [Implantation.from_json_data(implantation) for implantation in brain_dictionary["Implantations"]],
                   json_data["ID"])
