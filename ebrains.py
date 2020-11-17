import os
import re
from patient import *
from group import *
from settings import *
from protocol import *
from dataset import *
from visualization import *
from project import *

# DISCLAIMER: This python script is to be used with the Human Intracranial Database of EBRAINS and may not work in any
# other case

# User Input
database_path = "D:\\HBP\\export"  # Replace this variable with the path to your EBRAINS database (directory that contains anat and seeg sub-directories)
project_name = "EBRAINS"  # Name of your project
project_directory = "D:\\HBP\\Projects"  # Path to the directory to save your project

# Project information
anat_database = os.path.join(database_path, "anat")
func_database = os.path.join(database_path, "seeg")
project_preferences = ProjectPreferences(project_name, anat_database, func_database)

# Anatomical data
patients = []
patient_names = next(os.walk(anat_database))[1]
for patient_name in patient_names:
    patient_path = os.path.join(anat_database, patient_name)
    patients.append(
        Patient(
            patient_name, "0", "Unknown",
            [
                LeftRightMesh(
                    "Grey matter",
                    os.path.join(patient_path, patient_name + "_Lhemi.gii"),
                    os.path.join(patient_path, patient_name + "_Rhemi.gii"),
                    "",
                    "",
                    os.path.join(patient_path, patient_name + "_T1pre_TO_ScannerBased.trm")
                ),
                LeftRightMesh(
                    "White matter",
                    os.path.join(patient_path, patient_name + "_Lwhite.gii"),
                    os.path.join(patient_path, patient_name + "_Rwhite.gii"),
                    os.path.join(patient_path, patient_name + "_Lwhite_parcels_marsAtlas.gii"),
                    os.path.join(patient_path, patient_name + "_Rwhite_parcels_marsAtlas.gii"),
                    os.path.join(patient_path, patient_name + "_T1pre_TO_ScannerBased.trm")
                )
            ],
            [MRI("MRI", os.path.join(patient_path, patient_name + ".nii"))],
            Site.from_intranat_files(
                os.path.join(patient_path, patient_name + ".pts"),
                os.path.join(patient_path, patient_name + "_MNI.pts")
            )
        )
    )


# Functional data
protocols = [
    Protocol.from_json_file("./resources/protocols/AUDI.prov"),
    Protocol.from_json_file("./resources/protocols/LEC1.prov"),
    Protocol.from_json_file("./resources/protocols/LEC2.prov"),
    Protocol.from_json_file("./resources/protocols/MVEB.prov"),
    Protocol.from_json_file("./resources/protocols/MVIS.prov"),
    Protocol.from_json_file("./resources/protocols/MCSE.prov"),
    Protocol.from_json_file("./resources/protocols/MOTO.prov"),
    Protocol.from_json_file("./resources/protocols/VISU.prov")
]
groups = []
datasets = []


def generate_group_and_dataset_by_protocol(prov: Protocol):
    dataset_datainfo = []
    dataset_patients = []
    for patient_name_func in patient_names:
        patient_path_func = os.path.join(func_database, patient_name_func)
        pos_file = ""
        ab_file = ""
        gamma_file = ""
        files = next(os.walk(patient_path_func))[2]
        for file in files:
            if re.match(patient_name_func + "_" + protocol.name + "_ds\\d+.pos$", file):
                pos_file = os.path.join(patient_path_func, file)
            elif re.match(patient_name_func + "_" + protocol.name + "_f8f24_ds\\d+_sm0.eeg$", file):
                ab_file = os.path.join(patient_path_func, file)
            elif re.match(patient_name_func + "_" + protocol.name + "_f50f150_ds\\d+_sm0.eeg$", file):
                gamma_file = os.path.join(patient_path_func, file)
        if os.path.isfile(pos_file) and os.path.isfile(ab_file) and os.path.isfile(gamma_file):
            patient = [x for x in patients if x.name == patient_name_func][0]
            dataset_patients.append(patient)
            dataset_datainfo.append(IEEGDataInfo("alpha_beta", Elan(ab_file, pos_file), patient, NormalizationType.Auto))
            dataset_datainfo.append(IEEGDataInfo("gamma", Elan(gamma_file, pos_file), patient, NormalizationType.Auto))
    return Group(protocol.name, dataset_patients), Dataset(protocol.name, protocol, dataset_datainfo)


for protocol in protocols:
    group, dataset = generate_group_and_dataset_by_protocol(protocol)
    groups.append(group)
    datasets.append(dataset)

project = Project(project_preferences, patients, groups, protocols, datasets, [])
project.save(project_directory)
print("HiBoP Project created successfully!")
