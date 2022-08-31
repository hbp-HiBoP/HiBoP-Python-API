import abc
import uuid
import json

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
