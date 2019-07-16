from typing import List
from HiBoP.patient import Patient
from HiBoP.dataset import Dataset
from HiBoP.protocol import Bloc
import json
from HiBoP.tools import *
import abc


class SiteConfiguration:
    def __init__(self, is_blacklisted: bool = False, is_highlighted: bool = False,
                 color: Color = None, labels: List[str] = None):
        self.is_blacklisted = is_blacklisted
        self.is_highlighted = is_highlighted
        self.color = color
        self.labels = labels if labels is not None else []

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        return dict(IsBlacklisted=self.is_blacklisted,
                    IsHighlighted=self.is_highlighted,
                    Color=self.color.to_json_data(),
                    Labels=self.labels)

    @classmethod
    def from_json_data(cls, json_data) -> 'SiteConfiguration':
        return cls(json_data["IsBlacklisted"], json_data["IsHighlighted"],
                   Color.from_json_data(json_data["Color"]), json_data["Labels"])


class RegionOfInterest:
    def __init__(self, name: str = "", spheres: List[Sphere] = None):
        self.name = name
        self.spheres = spheres if spheres is not None else []

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        return dict(Name=self.name, Spheres=[sphere.to_json_data() for sphere in self.spheres])

    @classmethod
    def from_json_data(cls, json_data) -> 'RegionOfInterest':
        return cls(json_data["Name"], [Sphere.from_json_data(sphere) for sphere in json_data["Spheres"]])


class BaseConfiguration:
    def __init__(self, site_size: int = 0, region_of_interest=None, configuration_by_site=None):
        self.site_size = site_size
        self.region_of_interest = region_of_interest if region_of_interest is not None else []
        self.configuration_by_site = configuration_by_site if configuration_by_site is not None else {}

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        configuration_by_site = dict()
        for key in self.configuration_by_site:
            configuration_by_site[key] = self.configuration_by_site[key].to_json_data()
        return dict(SiteSize=self.site_size,
                    RegionOfInterest=[roi.to_json_data() for roi in self.region_of_interest],
                    ConfigurationBySite=configuration_by_site)

    @classmethod
    def from_json_data(cls, json_data) -> 'BaseConfiguration':
        configuration_by_site = json_data["ConfigurationBySite"]
        for key in configuration_by_site:
            configuration_by_site[key] = SiteConfiguration.from_json_data(configuration_by_site[key])
        result = cls(json_data["SiteSize"],
                     [RegionOfInterest.from_json_data(roi) for roi in json_data["RegionsOfInterest"]],
                     configuration_by_site)
        return result


class IEEGConfiguration:
    def __init__(self, site_gain: float = 1.0, site_maximum_influence: float = 15.0, transparency: float = 0.8,
                 span_min: float = 0, middle: float = 0.5, span_max: float = 1.0):
        self.site_gain = site_gain
        self.site_maximum_influence = site_maximum_influence
        self.transparency = transparency
        self.span_min = span_min
        self.middle = middle
        self.span_max = span_max

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        result["Site Gain"] = self.site_gain
        result["Site Maximum Influence"] = self.site_maximum_influence
        result["Transparency"] = self.transparency
        result["Span Min"] = self.span_min
        result["Middle"] = self.middle
        result["Span Max"] = self.span_max
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'IEEGConfiguration':
        return cls(json_data["Site Gain"], json_data["Site Maximum Influence"], json_data["Transparency"],
                   json_data["Span Min"], json_data["Middle"], json_data["Span Max"])


class AnatomicConfiguration:
    def __init__(self):
        pass

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'AnatomicConfiguration':
        return cls()


class CCEPConfiguration:
    def __init__(self):
        pass

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'CCEPConfiguration':
        return cls()


class Column(abc.ABC):
    def __init__(self, name: str = "", base_configuration=None):
        self.name = name
        self.base_configuration = base_configuration
        pass

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    @abc.abstractmethod
    def to_json_data(self):
        pass

    @classmethod
    def from_json_data(cls, json_data, project_datasets: List[Dataset]):
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Data.Visualization.IEEGColumn, Assembly-CSharp":
            result = IEEGColumn.from_json_data(json_data, project_datasets)
        elif class_type == "HBP.Data.Visualization.CCEPColumn, Assembly-CSharp":
            result = CCEPColumn.from_json_data(json_data, project_datasets)
        elif class_type == "HBP.Data.Visualization.AnatomicColumn, Assembly-CSharp":
            result = AnatomicColumn.from_json_data(json_data)
        return result


class IEEGColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None, dataset: Dataset = None,
                 data: str = "", bloc: Bloc = None, iEEG_configuration: IEEGConfiguration = None):
        super().__init__(name, base_configuration)
        self.dataset = dataset
        self.data = data
        self.bloc = bloc
        self.iEEG_configuration = iEEG_configuration

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        result["$type"] = "HBP.Data.Visualization.IEEGColumn, Assembly-CSharp"
        result["Name"] = self.name
        result["BaseConfiguration"] = self.base_configuration.to_json_data()
        result["Dataset"] = self.dataset.ID
        result["Bloc"] = self.bloc.ID
        result["DataName"] = self.data
        result["IEEGConfiguration"] = self.iEEG_configuration.to_json_data()
        return result

    @classmethod
    def from_json_data(cls, json_data, project_datasets: List[Dataset]) -> 'IEEGColumn':
        dataset = next(dataset for dataset in project_datasets if dataset.ID == json_data["Dataset"])
        result = cls(json_data["Name"], BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                     dataset, json_data["DataName"],
                     next(bloc for bloc in dataset.protocol.blocs if bloc.ID == json_data["Bloc"]),
                     IEEGConfiguration.from_json_data(json_data["IEEGConfiguration"]))
        return result


class CCEPColumn(Column):
    def __init__(self, name, base_configuration, dataset, data, bloc, CCEP_configuration):
        super().__init__(name, base_configuration)
        self.dataset = dataset
        self.data = data
        self.bloc = bloc
        self.CCEP_configuration = CCEP_configuration

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        result["$type"] = "HBP.Data.Visualization.CCEPColumn, Assembly-CSharp"
        result["Name"] = self.name
        result["BaseConfiguration"] = self.base_configuration.to_json_data()
        result["Dataset"] = self.dataset.ID
        result["Bloc"] = self.bloc.ID
        result["DataName"] = self.data
        result["CCEPConfiguration"] = self.CCEP_configuration.to_json_data()
        return result

    @classmethod
    def from_json_data(cls, json_data, project_datasets: List[Dataset] = None) -> 'CCEPColumn':
        dataset = next(dataset for dataset in project_datasets if dataset.ID == json_data["Dataset"])
        bloc = next(bloc for bloc in dataset.protocol.blocs if bloc.ID == json_data["Bloc"])
        result = cls(json_data["Name"],
                     BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                     dataset,
                     json_data["DataName"],
                     bloc,
                     CCEPConfiguration.from_json_data(json_data["CCEPConfiguration"]))
        return result


class AnatomicColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None,
                 anatomic_configuration: AnatomicConfiguration = None):
        super().__init__(name, base_configuration)
        self.anatomic_configuration = anatomic_configuration

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        result["$type"] = "HBP.Data.Visualization.AnatomicColumn, Assembly-CSharp"
        result["Name"] = self.name
        result["BaseConfiguration"] = self.base_configuration.to_json_data()
        result["CCEPConfiguration"] = self.anatomic_configuration.to_json_data()
        return result

    @classmethod
    def from_json_data(cls, json_data, project_patients: List[Patient] = None) -> 'AnatomicColumn':
        result = cls(json_data["Name"],
                     BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                     AnatomicConfiguration.from_json_data(json_data["AnatomicConfiguration"]))
        return result


class View:
    def __init__(self, position: Vector3 = None, rotation: Quaternion = None, target: Vector3 = None):
        self.position = position
        self.rotation = rotation
        self.target = target

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        return dict(Position=self.position, Rotation=self.rotation, Target=self.target)

    @classmethod
    def from_json_data(cls, json_data) -> 'View':
        return cls(json_data["Position"], json_data["Rotation"], json_data["Target"])


class Cut:
    def __init__(self, normal: Vector3, orientation: int, flip: bool, position: float):
        self.normal = normal
        self.orientation = orientation
        self.flip = flip
        self.position = position

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self):
        return dict(Normal=self.normal, Orientation=self.orientation, Flip=self.flip, Position=self.position)

    @classmethod
    def from_json_data(cls, json_data) -> 'Cut':
        return cls(json_data["Normal"], json_data["Orientation"], json_data["Flip"], json_data["Position"])


class VisualizationConfiguration:
    def __init__(self, brain_color: int = 0, brain_cut_color: int = 0, EEG_color: int = 0, mesh_part: int = 0,
                 mesh_name: str = "", MRI_name: str = "", implantation_name: str = "", show_edges: bool = False,
                 strong_cuts: bool = False, hide_blacklisted_sites: bool = False, show_all_sites: bool = False,
                 MRI_min: float = 0, MRI_max: float = 0, camera_type: int = 0, cuts: List[Cut] = None,
                 views: List[View] = None):
        self.brain_color = brain_color
        self.brain_cut_color = brain_cut_color
        self.EEG_color = EEG_color
        self.mesh_part = mesh_part
        self.mesh_name = mesh_name
        self.MRI_name = MRI_name
        self.implantation_name = implantation_name
        self.show_edges = show_edges
        self.strong_cuts = strong_cuts
        self.hide_blacklisted_sites = hide_blacklisted_sites
        self.show_all_sites = show_all_sites
        self.MRI_min = MRI_min
        self.MRI_max = MRI_max
        self.camera_type = camera_type
        self.cuts = cuts if cuts is not None else []
        self.views = views if views is not None else []

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self) -> dict:
        result = dict()
        result["Brain Color"] = self.brain_color
        result["Brain Cut Color"] = self.brain_cut_color
        result["EEG Colormap"] = self.EEG_color
        result["Mesh Part"] = self.mesh_part
        result["Mesh"] = self.mesh_name
        result["MRI"] = self.MRI_name
        result["Implantation"] = self.implantation_name
        result["Edges"] = self.show_edges
        result["Strong Cuts"] = self.strong_cuts
        result["Hide Blacklisted Sites"] = self.hide_blacklisted_sites
        result["ShowAllSites"] = self.show_all_sites
        result["MRI Min"] = self.MRI_min
        result["MRI Max"] = self.MRI_max
        result["Camera Type"] = self.camera_type
        result["Cuts"] = [cut.to_json_data() for cut in self.cuts]
        result["Views"] = [view.to_json_data() for view in self.views]
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'VisualizationConfiguration':
        return cls(json_data["Brain Color"], json_data["Brain Cut Color"], json_data["EEG Colormap"],
                   json_data["Mesh Part"], json_data["Mesh"], json_data["MRI"], json_data["Implantation"],
                   json_data["Edges"], json_data["Strong Cuts"], json_data["Hide Blacklisted Sites"],
                   json_data["ShowAllSites"], json_data["MRI Min"], json_data["MRI Max"], json_data["Camera Type"],
                   [Cut.from_json_data(cut) for cut in json_data["Cuts"]],
                   [View.from_json_data(view) for view in json_data["Views"]])


class Visualization:
    def __init__(self, name: str = "", patients: List[Patient] = None, configuration: VisualizationConfiguration = None,
                 columns: List[Column] = None, ID: str = ""):
        self.name = name
        self.patients = patients if patients is not None else []
        self.configuration = configuration
        self.columns = columns if columns is not None else []
        self.ID = ID

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    def to_json_data(self) -> dict:
        return dict(ID=self.ID, Name=self.name, Patients=[patient.ID for patient in self.patients],
                    Configuration=self.configuration.to_json_data(),
                    Columns=[column.to_json_data() for column in self.columns])

    @classmethod
    def from_json_file(cls, json_file: str, project_patients: List[Patient], project_datasets: List[Dataset]) -> 'Visualization':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), project_patients, project_datasets)

    @classmethod
    def from_json_data(cls, json_data, project_patients: List[Patient], project_datasets: List[Dataset]) -> 'Visualization':
        result = cls(json_data["Name"],
                     [next(patient for patient in project_patients if patient.ID == patient_ID)
                      for patient_ID in json_data["Patients"]],
                     VisualizationConfiguration.from_json_data(json_data["Configuration"]),
                     [Column.from_json_data(column, project_datasets) for column in json_data["Columns"]],
                     json_data["ID"])
        return result
