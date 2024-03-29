from patient import *
from group import *
from settings import *
from protocol import *
from dataset import *
from visualization import *
from project import *


def demo_project_preferences():
    # Create a project preferences
    project_preferences = ProjectPreferences('MyProject', 'Patient_database_path', 'Localizers_database_path', [Alias('Key1', 'Value1'), Alias("Key2", "Value2"), Alias("Key3", 'Value3')], [BoolTag("IsOk")],  [EnumTag("Laterality", ['Left', 'Right']), IntTag("Age")], [FloatTag("Size")])

    # Save the project preferences to a settings file
    project_preferences.to_json_file("./sample/MyProject.settings")

    # Load project preferences from a settings file
    project_preferences.from_json_file("./sample/MyProject.settings")


def demo_patient():
    # Tags of the project
    project_tags = [BoolTag("isOk"), EmptyTag("Tutu"), FloatTag("Size"), IntTag("Age"), EmptyTag("Toto")]

    # Create a patient
    patient = Patient()
    patient.name = "John Doe"
    patient.date = 2017
    patient.place = "Lyon"
    patient.meshes = [SingleMesh('Grey Matter', "grey_matter.gii", "", "grey_matter_transformation.trm"), LeftRightMesh('White Matter', "left_hemisphere_white_matter.gii", "right_hemisphere_white_matter.gii", "left_hemisphere_marsAtlas.gii", "right_hemisphere_marsAtlas.gii", "white_matter_transformation.trm")]
    patient.MRIs = [MRI("Preimplantation", "preimplantation.nii"),  MRI("Postimplantation", "postimplantation.nii")]
    patient.sites = [Site("A'1", [Coordinate("Patient", Vector3(0.0, 1.0, 2.0)), Coordinate("MNI", Vector3(20.0, 40.0, 10.0))], [BoolTagValue(project_tags[0], True), EmptyTagValue(project_tags[1])]), Site("A'3", [Coordinate("Patient", Vector3(0.0, 4.0, 3.0)), Coordinate("MNI", Vector3(24.0, 45.0, 15.0))], [FloatTagValue(project_tags[2], 0.54)])]
    patient.tags = [IntTagValue(project_tags[3], 124), EmptyTagValue(project_tags[4])]

    # Save the patient to a patient file
    patient.to_json_file("./sample/John_Doe.patient")

    # Load a patient from a patient file
    patient = Patient.from_json_file('./sample/John_Doe.patient', project_tags)


def demo_group():
    # Patients of the project
    project_patients = [Patient('John Doe'), Patient('Barack Obama'), Patient("Xi Jinping"), Patient("Luke Skywalker"), Patient("Yoda"), Patient("Mace Windu")]

    # Create a group
    group = Group('Jedis', project_patients[3:])

    # Save the group to a group file
    group.to_json_file('./sample/Jedis.group')

    # Load a group from a group file
    group = Group.from_json_file('./sample/Jedis.group', project_patients)


def demo_protocol():
    # Create some blocs
    fruit_bloc = Bloc('FRUIT', 0, "", "", [SubBloc('Main', 0, SubBlocType.Main, Window(-500, 100), Window(-200, 0), [Event('FRUIT', [80], EventType.Main), Event('RESPONSE', [1], EventType.Secondary)], [Icon("Cross", "", Window(-500, 0)), Icon("FRUIT", "", Window(0, 100))])])
    face_bloc = Bloc('FACE', 7, "", "", [SubBloc('Main', 0, SubBlocType.Main, Window(-500, 1000), Window(-200, 0), [Event('FACE', [20], EventType.Main)], None, [MaxTreatment(True, Window(-500, 100))])])

    # Create a protocol
    protocol = Protocol('VISU', [fruit_bloc, face_bloc])

    # Save the protocol to a protocol file
    protocol.to_json_file('./sample/VISU.prov')

    # Load a protocol from a protocol file
    protocol = Protocol.from_json_file('./sample/VISU.prov')


def demo_dataset():
    # Protocols of the project
    project_protocols = [Protocol('VISU'), Protocol('LEC1'), Protocol('LEC2'), Protocol('MVEB')]

    # Patients of the project
    project_patients = [Patient('John Doe'), Patient('Barack Obama'), Patient("Xi Jinping"), Patient("Luke Skywalker"), Patient("Yoda"), Patient("Mace Windu")]

    # Create a dataset
    dataset = Dataset('VISU', project_protocols[0], [CCEPDataInfo('CCEP data', BrainVision("John_doe_VISU.vhdr"), project_patients[0], "A'1"), IEEGDataInfo('IEEG data', EDF("Yoda_VISU.edf"), project_patients[4], NormalizationType.Bloc)])

    # Save the dataset to a dataset file
    dataset.to_json_file('./sample/VISU.dataset')

    # Load a dataset from a dataset file
    dataset = Dataset.from_json_file('./sample/VISU.dataset', project_protocols, project_patients)


def demo_visualization():
    # Patients of the project
    project_patients = [Patient('John Doe'), Patient('Barack Obama'), Patient("Xi Jinping"), Patient("Luke Skywalker"), Patient("Yoda"), Patient("Mace Windu")]

    # Datasets of the project
    project_datasets = [Dataset('VISU', Protocol('VISU', [Bloc('Main')])), Dataset('LEC1', Protocol('LEC1')), Dataset('LEC2', Protocol('LEC2'))]

    # Create a visualization
    ieeg_column = IEEGColumn('FRUIT', BaseConfiguration(0.8, {"A'1": SiteConfiguration(False, False, Color(0.1, 0.2, 0.3, 1.2), ["Tutu"])}), project_datasets[0], '', project_datasets[0].protocol.blocs[0], DynamicConfiguration())
    ccep_column = CCEPColumn('CCEP', BaseConfiguration(), project_datasets[0], '', project_datasets[0].protocol.blocs[0], DynamicConfiguration())
    anatomic_column = AnatomicColumn('Anatomic', BaseConfiguration(), AnatomicConfiguration())
    visualization = Visualization('New Visualization', project_patients[3:], [ieeg_column, ccep_column, anatomic_column], VisualizationConfiguration())

    # Save the visualization in a visualization file
    visualization.to_json_file('./sample/Visualization.visualization')

    # Load a visualization from a visualization file
    visualization = Visualization.from_json_file('./sample/Visualization.visualization', project_patients, project_datasets)


def demo_project():
    # Create a project preferences
    project_tags = [BoolTag("isOk"), EmptyTag("Tutu"), FloatTag("Size"), IntTag("Age"), EmptyTag("Toto")]
    project_preferences = ProjectPreferences('SampleProject', 'Patient_database_path', 'Localizers_database_path', [Alias('Key1', 'Value1'), Alias("Key2", "Value2"), Alias("Key3", 'Value3')], project_tags)

    # Patients of the project
    john_doe = Patient('John Doe', 2020, 'Anywhere', [LeftRightMesh('Grey Matter', 'left.gii', 'right.gii', 'left_mars_atlas.gii', 'right_mars_atlas.gii', 'transformation.trm')], [MRI('MRI', 'mri.nii')])
    john_doe.sites = [Site("A'1", [Coordinate("Patient", Vector3(0.0, 1.0, 2.0)), Coordinate("MNI", Vector3(20.0, 40.0, 10.0))], [BoolTagValue(project_tags[0], True), EmptyTagValue(project_tags[1])]), Site("A'3", [Coordinate("Patient", Vector3(0.0, 4.0, 3.0)), Coordinate("MNI", Vector3(24.0, 45.0, 15.0))], [FloatTagValue(project_tags[2], 0.54)])]
    barack_obama = Patient('Barack Obama')
    xi_jinping = Patient("Xi Jinping")
    luke_skywalker = Patient("Luke Skywalker")
    yoda = Patient("Yoda")
    mace_windu = Patient("Mace Windu")
    patients = [john_doe, barack_obama, xi_jinping, luke_skywalker, yoda, mace_windu]

    # Create a group
    groups = [Group('Jedis', patients[3:]), Group("Presidents", patients[1:3])]

    # Create some blocs
    fruit_bloc = Bloc('FRUIT', 0, "", "", [SubBloc('Main', 0, SubBlocType.Main, Window(-500, 1000), Window(-200, 0), [Event('FRUIT', [80], EventType.Main), Event('RESPONSE', [1], EventType.Secondary)], [Icon("Cross", "", Window(-500, 0)), Icon("FRUIT", "", Window(0, 100))])])
    face_bloc = Bloc('FACE', 7, "", "", [SubBloc('Main', 0, SubBlocType.Main, Window(-500, 1000), Window(-200, 0), [Event('FACE', [20], EventType.Main)], None, [MaxTreatment(True, Window(-500, 100))])])
    ccep_bloc = Bloc('CCEP', 0, "", "", [SubBloc('Main', 0, SubBlocType.Main, Window(-300, 300), Window(0,0), [Event('CCEP', [2], EventType.Main)])])

    # Create a protocol
    protocols = [Protocol('VISU', [fruit_bloc, face_bloc]), Protocol('CCEP', [ccep_bloc])]

    # Create a dataset
    datasets = [Dataset('VISU', protocols[0], [IEEGDataInfo('IEEG data', EDF("Yoda_VISU.edf"), patients[4], NormalizationType.Bloc)]), Dataset('CCEP', protocols[1], [CCEPDataInfo('CCEP data', BrainVision("John_doe_CCEP.vhdr"), patients[0], "A'1")])]

    # Create a visualization
    ieeg_column = IEEGColumn('FRUIT', BaseConfiguration(0.8, {"A'1": SiteConfiguration(False, False, Color(0.1, 0.2, 0.3, 1.2), ["Tutu"])}), datasets[0], '', datasets[0].protocol.blocs[0], DynamicConfiguration())
    ccep_column = CCEPColumn('CCEP', BaseConfiguration(), datasets[0], '', datasets[0].protocol.blocs[0], DynamicConfiguration())
    anatomic_column = AnatomicColumn('Anatomic', BaseConfiguration(), AnatomicConfiguration())
    visualizations = [Visualization('New Visualization', patients[3:], [ieeg_column, ccep_column, anatomic_column], VisualizationConfiguration())]

    project = Project(project_preferences, patients, groups, protocols, datasets, visualizations)
    project.save("./sample")


if not os.path.exists("./sample"):
    os.mkdir("./sample")

demo_project_preferences()
demo_patient()
demo_group()
demo_protocol()
demo_dataset()
demo_visualization()
demo_project()
