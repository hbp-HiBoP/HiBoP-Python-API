from typing import List
from patient import Patient
from dataset import Dataset
from protocol import Bloc
from tools import *
import enum
import abc


class SiteConfiguration(BaseData):
    def __init__(self, is_blacklisted: bool = False, is_highlighted: bool = False,
                 color: Color = None, labels: List[str] = None, ID: str = ""):
        super().__init__(ID)
        self.is_blacklisted = is_blacklisted
        self.is_highlighted = is_highlighted
        self.color = color
        self.labels = labels if labels is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['IsBlacklisted'] = self.is_blacklisted
        json_data['IsHighlighted'] = self.is_highlighted
        json_data['Color'] = self.color.to_json_data()
        json_data['Labels'] = self.labels
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict) -> 'SiteConfiguration':
        return cls(json_data["IsBlacklisted"],
                   json_data["IsHighlighted"],
                   Color.from_json_data(json_data["Color"]),
                   json_data["Labels"],
                   json_data['ID'])


class BaseConfiguration(BaseData):
    def __init__(self, activity_alpha: float = 0.8, configuration_by_site = None, ID: str = ""):
        super().__init__(ID)
        self.activity_alpha = activity_alpha
        self.configuration_by_site = configuration_by_site if configuration_by_site is not None else {}

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Activity Alpha'] = self.activity_alpha
        json_data['ConfigurationBySite'] = {key: self.configuration_by_site[key].to_json_data() for key in self.configuration_by_site.keys()}
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'BaseConfiguration':
        return cls(json_data['Activity Alpha'], {key: SiteConfiguration.from_json_data(json_data["ConfigurationBySite"][key]) for key in json_data["ConfigurationBySite"].keys()})


class DynamicConfiguration(BaseData):
    def __init__(self, site_maximum_influence: float = 15.0, span_min: float = 0, middle: float = 0.5,
                 span_max: float = 1.0, ID: str = ""):
        super().__init__(ID)
        self.site_maximum_influence = site_maximum_influence
        self.span_min = span_min
        self.middle = middle
        self.span_max = span_max

    def to_json_data(self) -> dict:
        result = super().to_json_data()
        result["Site Maximum Influence"] = self.site_maximum_influence
        result["Span Min"] = self.span_min
        result["Middle"] = self.middle
        result["Span Max"] = self.span_max
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'DynamicConfiguration':
        return cls(json_data["Site Maximum Influence"],
                   json_data["Span Min"],
                   json_data["Middle"],
                   json_data["Span Max"],
                   json_data["ID"])


class AnatomicConfiguration(BaseData):
    def __init__(self, ID: str = ""):
        super().__init__(ID)

    def to_json_data(self) -> dict:
        return super().to_json_data()

    @classmethod
    def from_json_data(cls, json_data) -> 'AnatomicConfiguration':
        return cls(json_data['ID'])


class FMRIConfiguration(BaseData):
    def __init__(self, negative_min: float = 0, negative_max: float = 0, positive_min: float = 0, positive_max: float = 0,
                 hide_lower_values: bool = False, hide_middle_values: bool = False, hide_higher_values: bool = False,
                 ID: str = ""):
        super().__init__(ID)
        self.negative_min = negative_min
        self.negative_max = negative_max
        self.positive_min = positive_min
        self.positive_max = positive_max
        self.hide_lower_values = hide_lower_values
        self.hide_middle_values = hide_middle_values
        self.hide_higher_values = hide_higher_values

    def to_json_data(self) -> dict:
        result = super().to_json_data()
        result["Negative Min"] = self.negative_min
        result["Negative Max"] = self.negative_max
        result["Positive Min"] = self.positive_min
        result["Positive Max"] = self.positive_max
        result["Hide Lower Values"] = self.hide_lower_values
        result["Hide Middle Values"] = self.hide_middle_values
        result["Hide Higher Values"] = self.hide_higher_values
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'FMRIConfiguration':
        return cls(json_data["Negative Min"],
                   json_data["Negative Max"],
                   json_data["Positive Min"],
                   json_data["Positive Max"],
                   json_data["Hide Lower Values"],
                   json_data["Hide Middle Values"],
                   json_data["Hide Higher Values"],
                   json_data["ID"])


class MEGConfiguration(BaseData):
    def __init__(self, negative_min: float = 0, negative_max: float = 0, positive_min: float = 0, positive_max: float = 0,
                 hide_lower_values: bool = False, hide_middle_values: bool = False, hide_higher_values: bool = False,
                 ID: str = ""):
        super().__init__(ID)
        self.negative_min = negative_min
        self.negative_max = negative_max
        self.positive_min = positive_min
        self.positive_max = positive_max
        self.hide_lower_values = hide_lower_values
        self.hide_middle_values = hide_middle_values
        self.hide_higher_values = hide_higher_values

    def to_json_data(self) -> dict:
        result = super().to_json_data()
        result["Negative Min"] = self.negative_min
        result["Negative Max"] = self.negative_max
        result["Positive Min"] = self.positive_min
        result["Positive Max"] = self.positive_max
        result["Hide Lower Values"] = self.hide_lower_values
        result["Hide Middle Values"] = self.hide_middle_values
        result["Hide Higher Values"] = self.hide_higher_values
        return result

    @classmethod
    def from_json_data(cls, json_data) -> 'MEGConfiguration':
        return cls(json_data["Negative Min"],
                   json_data["Negative Max"],
                   json_data["Positive Min"],
                   json_data["Positive Max"],
                   json_data["Hide Lower Values"],
                   json_data["Hide Middle Values"],
                   json_data["Hide Higher Values"],
                   json_data["ID"])


class Column(BaseData):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.base_configuration = base_configuration

    @abc.abstractmethod
    def to_json_data(self):
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['BaseConfiguration'] = self.base_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, datasets: List[Dataset] = None) -> 'Column':
        class_type = json_data["$type"]
        result = None
        if class_type == "HBP.Core.Data.IEEGColumn, Assembly-CSharp" or class_type == "HBP.Data.Visualization.IEEGColumn, Assembly-CSharp":
            result = IEEGColumn.from_json_data(json_data, datasets)
        elif class_type == "HBP.Core.Data.CCEPColumn, Assembly-CSharp" or class_type == "HBP.Data.Visualization.CCEPColumn, Assembly-CSharp":
            result = CCEPColumn.from_json_data(json_data, datasets)
        elif class_type == "HBP.Core.Data.AnatomicColumn, Assembly-CSharp" or class_type == "HBP.Data.Visualization.AnatomicColumn, Assembly-CSharp":
            result = AnatomicColumn.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.FMRIColumn, Assembly-CSharp" or class_type == "HBP.Data.Visualization.FMRIColumn, Assembly-CSharp":
            result = FMRIColumn.from_json_data(json_data)
        elif class_type == "HBP.Core.Data.MEGColumn, Assembly-CSharp" or class_type == "HBP.Data.Visualization.MEGColumn, Assembly-CSharp":
            result = MEGColumn.from_json_data(json_data)
        return result


class IEEGColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None, dataset: Dataset = None,
                 data: str = "", bloc: Bloc = None, dynamic_configuration: DynamicConfiguration = None, ID: str = ""):
        super().__init__(name, base_configuration, ID)
        self.dataset = dataset
        self.data = data
        self.bloc = bloc
        self.dynamic_configuration = dynamic_configuration

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.IEEGColumn, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Dataset"] = self.dataset.ID
        json_data["DataName"] = self.data
        json_data["Bloc"] = self.bloc.ID
        json_data["DynamicConfiguration"] = self.dynamic_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, datasets: List[Dataset] = None) -> 'IEEGColumn':
        dataset = next(dataset for dataset in datasets if dataset.ID == json_data["Dataset"])
        return cls(json_data["Name"],
                   BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                   dataset,
                   json_data["DataName"],
                   next(bloc for bloc in dataset.protocol.blocs if bloc.ID == json_data["Bloc"]),
                   DynamicConfiguration.from_json_data(json_data["DynamicConfiguration"]),
                   json_data['ID'])


class CCEPColumn(Column):
    def __init__(self, name: str = '', base_configuration: BaseConfiguration = None, dataset: Dataset = None, data: str = '', bloc: Bloc = None, dynamic_configuration: DynamicConfiguration = None, ID: str = ""):
        super().__init__(name, base_configuration, ID)
        self.dataset = dataset
        self.data = data
        self.bloc = bloc
        self.dynamic_configuration = dynamic_configuration

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.CCEPColumn, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Dataset"] = self.dataset.ID
        json_data["Bloc"] = self.bloc.ID
        json_data["DataName"] = self.data
        json_data["DynamicConfiguration"] = self.dynamic_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, datasets: List[Dataset] = None) -> 'CCEPColumn':
        dataset = next(dataset for dataset in datasets if dataset.ID == json_data["Dataset"])
        bloc = next(bloc for bloc in dataset.protocol.blocs if bloc.ID == json_data["Bloc"])
        return cls(json_data["Name"],
                   BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                   dataset,
                   json_data["DataName"],
                   bloc,
                   DynamicConfiguration.from_json_data(json_data["DynamicConfiguration"]),
                   json_data['ID'])


class AnatomicColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None,
                 anatomic_configuration: AnatomicConfiguration = None, ID: str = ""):
        super().__init__(name, base_configuration, ID)
        self.anatomic_configuration = anatomic_configuration

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.AnatomicColumn, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["AnatomicConfiguration"] = self.anatomic_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, patients: List[Patient] = None) -> 'AnatomicColumn':
        return cls(json_data["Name"],
                   BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                   AnatomicConfiguration.from_json_data(json_data["AnatomicConfiguration"]),
                   json_data['ID'])


class FMRIColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None, dataset: Dataset = None,
                 fmri_configuration: FMRIConfiguration = None, ID: str = ""):
        super().__init__(name, base_configuration, ID)
        self.dataset = dataset
        self.fmri_configuration = fmri_configuration

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.FMRIColumn, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Dataset"] = self.dataset.ID
        json_data["FMRIConfiguration"] = self.fmri_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, datasets: List[Dataset] = None) -> 'FMRIColumn':
        dataset = next(dataset for dataset in datasets if dataset.ID == json_data["Dataset"])
        return cls(json_data["Name"],
                   BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                   dataset,
                   FMRIConfiguration.from_json_data(json_data["FMRIConfiguration"]),
                   json_data['ID'])


class MEGColumn(Column):
    def __init__(self, name: str = "", base_configuration: BaseConfiguration = None, dataset: Dataset = None,
                 meg_configuration: MEGConfiguration = None, ID: str = ""):
        super().__init__(name, base_configuration, ID)
        self.dataset = dataset
        self.meg_configuration = meg_configuration

    def to_json_data(self) -> dict:
        json_data = dict()
        json_data["$type"] = "HBP.Core.Data.FMRIColumn, Assembly-CSharp"
        json_data.update(super().to_json_data())
        json_data["Dataset"] = self.dataset.ID
        json_data["MEGConfiguration"] = self.meg_configuration.to_json_data()
        return json_data

    @classmethod
    def from_json_data(cls, json_data: dict, datasets: List[Dataset] = None) -> 'MEGColumn':
        dataset = next(dataset for dataset in datasets if dataset.ID == json_data["Dataset"])
        return cls(json_data["Name"],
                   BaseConfiguration.from_json_data(json_data["BaseConfiguration"]),
                   dataset,
                   MEGConfiguration.from_json_data(json_data["MEGConfiguration"]),
                   json_data['ID'])


class ColorType(enum.Enum):
    Grayscale = 0
    Hot = 1
    Winter = 2
    Warm = 3
    Surface = 4
    Cool = 5
    RedYellow = 6
    BlueGreen = 7
    ACTC = 8
    Bone = 9
    GEColor = 10
    Gold = 11
    XRain = 12
    MatLab = 13
    Default = 14
    BrainColor = 15
    White = 16
    SoftGrayscale = 17


class CutOrientation(enum.Enum):
    Axial = 0
    Coronal = 1
    Sagittal = 2
    Custom = 3


class MeshPart(enum.Enum):
    Left = 0
    Right = 1
    Both = 2
    No = 3


class CameraControl(enum.Enum):
    Trackball = 0
    Orbital = 1


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


class Cut:
    def __init__(self, normal: Vector3, orientation: CutOrientation, flip: bool, position: float):
        self.normal = normal
        self.orientation = orientation
        self.flip = flip
        self.position = position

    def __repr__(self):
        return super().__repr__() + "\n" + str(json.dumps(self.to_json_data(), indent=2))

    def to_json_data(self):
        return dict(Normal=self.normal, Orientation=self.orientation.value, Flip=self.flip, Position=self.position)

    @classmethod
    def from_json_data(cls, json_data) -> 'Cut':
        return cls(json_data["Normal"], CutOrientation(json_data["Orientation"]), json_data["Flip"], json_data["Position"])


class VisualizationConfiguration(BaseData):
    def __init__(self, brain_color: ColorType = ColorType.Grayscale, brain_cut_color: ColorType = ColorType.Grayscale,
                 colormap: ColorType = ColorType.Grayscale, mesh_part: MeshPart = MeshPart.Left,
                 mesh_name: str = "", MRI_name: str = "", implantation_name: str = "", show_edges: bool = False, transparent_brain: bool = False,
                 brain_alpha: float = 0.2, strong_cuts: bool = False, hide_blacklisted_sites: bool = False, show_all_sites: bool = False, automatic_cut_around_selected_site: bool = False,
                 site_gain: float = 1.0, MRI_min: float = 0, MRI_max: float = 1, camera_type: CameraControl = CameraControl.Trackball,
                 cuts: List[Cut] = None, views: List[View] = None, regions_of_interest: List[RegionOfInterest] = None, ID: str = ""):
        super().__init__(ID)
        self.brain_color = brain_color
        self.brain_cut_color = brain_cut_color
        self.colormap = colormap
        self.mesh_part = mesh_part
        self.mesh_name = mesh_name
        self.MRI_name = MRI_name
        self.implantation_name = implantation_name
        self.show_edges = show_edges
        self.transparent_brain = transparent_brain
        self.brain_alpha = brain_alpha
        self.strong_cuts = strong_cuts
        self.hide_blacklisted_sites = hide_blacklisted_sites
        self.show_all_sites = show_all_sites
        self.automatic_cut_around_selected_site = automatic_cut_around_selected_site
        self.site_gain = site_gain
        self.MRI_min = MRI_min
        self.MRI_max = MRI_max
        self.camera_type = camera_type
        self.cuts = cuts if cuts is not None else []
        self.views = views if views is not None else []
        self.regions_of_interest = regions_of_interest if regions_of_interest is not None else []

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data["Brain Color"] = self.brain_color.value
        json_data["Brain Cut Color"] = self.brain_cut_color.value
        json_data["Colormap"] = self.colormap.value
        json_data["Mesh Part"] = self.mesh_part.value
        json_data["Mesh"] = self.mesh_name
        json_data["MRI"] = self.MRI_name
        json_data["Implantation"] = self.implantation_name
        json_data["Edges"] = self.show_edges
        json_data["Transparent Brain"] = self.transparent_brain
        json_data["Brain Alpha"] = self.brain_alpha
        json_data["Strong Cuts"] = self.strong_cuts
        json_data["Hide Blacklisted Sites"] = self.hide_blacklisted_sites
        json_data["ShowAllSites"] = self.show_all_sites
        json_data["AutomaticCutAroundSelectedSite"] = self.automatic_cut_around_selected_site
        json_data["Site Gain"] = self.site_gain
        json_data["MRI Min"] = self.MRI_min
        json_data["MRI Max"] = self.MRI_max
        json_data["Camera Type"] = self.camera_type.value
        json_data["Cuts"] = [cut.to_json_data() for cut in self.cuts]
        json_data["Views"] = [view.to_json_data() for view in self.views]
        json_data['RegionsOfInterest'] = [region_of_interest.to_json_data() for region_of_interest in self.regions_of_interest]
        return json_data

    @classmethod
    def from_json_data(cls, json_data) -> 'VisualizationConfiguration':
        return cls(ColorType(json_data["Brain Color"]),
                   ColorType(json_data["Brain Cut Color"]),
                   ColorType(json_data["Colormap"]),
                   MeshPart(json_data["Mesh Part"]),
                   json_data["Mesh"],
                   json_data["MRI"],
                   json_data["Implantation"],
                   json_data["Edges"],
                   json_data["Transparent Brain"],
                   json_data["Brain Alpha"],
                   json_data["Strong Cuts"],
                   json_data["Hide Blacklisted Sites"],
                   json_data["ShowAllSites"],
                   json_data["AutomaticCutAroundSelectedSite"],
                   json_data["Site Gain"],
                   json_data["MRI Min"],
                   json_data["MRI Max"],
                   CameraControl(json_data["Camera Type"]),
                   [Cut.from_json_data(cut) for cut in json_data["Cuts"]],
                   [View.from_json_data(view) for view in json_data["Views"]],
                   [RegionOfInterest.from_json_data(roi) for roi in json_data["RegionsOfInterest"]],
                   json_data['ID'])


class Visualization(BaseData):
    def __init__(self, name: str = "", patients: List[Patient] = None,
                 columns: List[Column] = None, configuration: VisualizationConfiguration = None, ID: str = ""):
        super().__init__(ID)
        self.name = name
        self.patients = patients if patients is not None else []
        self.columns = columns if columns is not None else []
        self.configuration = configuration

    def to_json_file(self, json_file: str):
        with open(json_file, "w") as f:
            json.dump(self.to_json_data(), f, indent=2)

    def to_json_data(self) -> dict:
        json_data = super().to_json_data()
        json_data['Name'] = self.name
        json_data['Patients'] = [patient.ID for patient in self.patients]
        json_data['Configuration'] = self.configuration.to_json_data()
        json_data['Columns'] = [column.to_json_data() for column in self.columns]
        return json_data

    @classmethod
    def from_json_file(cls, json_file: str, patients: List[Patient], datasets: List[Dataset]) -> 'Visualization':
        with open(json_file, "r") as f:
            return cls.from_json_data(json.load(f), patients, datasets)

    @classmethod
    def from_json_data(cls, json_data, patients: List[Patient] = None, datasets: List[Dataset] = None) -> 'Visualization':
        return cls(json_data["Name"],
                   [next(patient for patient in patients if patient.ID == patient_ID) for patient_ID in json_data["Patients"]],
                   [Column.from_json_data(column, datasets) for column in json_data["Columns"]],
                   VisualizationConfiguration.from_json_data(json_data["Configuration"]),
                   json_data["ID"])
