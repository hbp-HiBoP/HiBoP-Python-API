import zipfile
import os
import shutil
from settings import ProjectPreferences
from patient import Patient
from group import Group
from protocol import Protocol
from dataset import Dataset
from visualization import Visualization

from typing import List


class Project:
    """description of class"""

    def __init__(self, preferences: ProjectPreferences, patients: List[Patient] = None,
                 groups: List[Group] = None, protocols: List[Protocol] = None,
                 datasets: List[Dataset] = None, visualizations: List[Visualization] = None):
        self.preferences = preferences
        self.patients = patients if patients is not None else []
        self.groups = groups if groups is not None else []
        self.protocols = protocols if protocols is not None else []
        self.datasets = datasets if datasets is not None else []
        self.visualizations = visualizations if visualizations is not None else []

    def save(self, path):
        # General
        project_directory_path = os.path.join(path,self.preferences.name)
        try:
            if os.path.exists(project_directory_path):
                shutil.rmtree(project_directory_path)
            os.mkdir(project_directory_path)
        except OSError:
            print("Creation of the directory %s failed" % project_directory_path)
        else:
            print("Successfully created the directory %s " % project_directory_path)

            # Project Preferences
            settings_path = os.path.join(project_directory_path, self.preferences.name + ".settings")
            try:
                self.preferences.to_json_file(settings_path)
            except OSError:
                print("Creation of the file %s failed" % settings_path)
            else:
                print("Successfully created the file %s " % settings_path)

            # Patients
            patients_directory_path = os.path.join(project_directory_path, "Patients")
            try:
                os.mkdir(patients_directory_path)
            except OSError:
                print("Creation of the directory %s failed" % patients_directory_path)
            else:
                print("Successfully created the directory %s " % patients_directory_path)
                for patient in self.patients:
                    patient_path = os.path.join(patients_directory_path, patient.ID + ".patient")
                    try:
                        patient.to_json_file(patient_path)
                    except OSError:
                        print("Creation of the file %s failed" % patient_path)
                    else:
                        print("Successfully created the file %s " % patient_path)

            # Groups
            groups_directory_path = os.path.join(project_directory_path, "Groups")
            try:
                os.mkdir(groups_directory_path)
            except OSError:
                print("Creation of the directory %s failed" % groups_directory_path)
            else:
                print("Successfully created the directory %s " % groups_directory_path)
                for group in self.groups:
                    group_path = os.path.join(groups_directory_path, group.ID + ".group")
                    try:
                        group.to_json_file(group_path)
                    except OSError:
                        print("Creation of the file %s failed" % group_path)
                    else:
                        print("Successfully created the file %s " % group_path)

            # Protocols
            protocols_directory_path = os.path.join(project_directory_path, "Protocols")
            try:
                os.mkdir(protocols_directory_path)
            except OSError:
                print("Creation of the directory %s failed" % protocols_directory_path)
            else:
                print("Successfully created the directory %s " % protocols_directory_path)
                for protocol in self.protocols:
                    protocol_path = os.path.join(protocols_directory_path, protocol.ID + ".prov")
                    try:
                        protocol.to_json_file(protocol_path)
                    except OSError:
                        print("Creation of the file %s failed" % protocol_path)
                    else:
                        print("Successfully created the file %s " % protocol_path)

            # Datasets
            datasets_directory_path = os.path.join(project_directory_path, "Datasets")
            try:
                os.mkdir(datasets_directory_path)
            except OSError:
                print("Creation of the directory %s failed" % datasets_directory_path)
            else:
                print("Successfully created the directory %s " % datasets_directory_path)
                for dataset in self.datasets:
                    dataset_path = os.path.join(datasets_directory_path, dataset.ID + ".dataset")
                    try:
                        dataset.to_json_file(dataset_path)
                    except OSError:
                        print("Creation of the file %s failed" % dataset_path)
                    else:
                        print("Successfully created the file %s " % dataset_path)

            # Visualizations
            visualizations_directory_path = os.path.join(project_directory_path, "Visualizations")
            try:
                os.mkdir(visualizations_directory_path)
            except OSError:
                print("Creation of the directory %s failed" % visualizations_directory_path)
            else:
                print("Successfully created the directory %s " % visualizations_directory_path)
                for visualization in self.visualizations:
                    visualization_path = os.path.join(visualizations_directory_path, visualization.ID + ".visualization")
                    try:
                        visualization.to_json_file(visualization_path)
                    except OSError:
                        print("Creation of the file %s failed" % visualization_path)
                    else:
                        print("Successfully created the file %s " % visualization_path)

            zip_path = project_directory_path + ".hibop"
            try:
                zip_file = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
                for root, dirs, files in os.walk(project_directory_path):
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        zip_file.write(dir_path, os.path.relpath(dir_path, project_directory_path))
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, project_directory_path))
                zip_file.close()
                if os.path.exists(project_directory_path):
                    shutil.rmtree(project_directory_path)
            except OSError:
                print("Creation of the zip %s failed" % zip_path)
            else:
                print("Successfully created the zip %s " % zip_path)

    @classmethod
    def load(cls, path):
        # General
        try:
            with zipfile.ZipFile(path, "r") as zip:
                namelist = zip.namelist()

                # Get into tmp dir
                if not os.path.isdir(".tmp"):
                    os.mkdir(".tmp")
                os.chdir(".tmp")

                # Load Settings
                settings_path = next(name for name in namelist if str.endswith(name, ".settings"))
                settings = None
                try:
                    settings = ProjectPreferences.from_json_file(zip.extract(settings_path))
                except OSError:
                    print("[1/1] Loading of the settings file %s failed" % settings_path)
                else:
                    print("[1/1] Successfully loaded the settings file %s" % settings_path)

                # Load Patients
                patients_path = [name for name in namelist if str.endswith(name, ".patient")]
                patients = []
                for i, patient_path in enumerate(patients_path):
                    try:
                        patients.append(Patient.from_json_file(zip.extract(patient_path), settings.general_tags + settings.patients_tags + settings.sites_tags))
                    except OSError:
                        print("[{0}/{1}] Loading of the patient file {2} failed".format(i + 1, len(patients_path),
                                                                                        patient_path))
                    else:
                        print("[{0}/{1}] Successfully loaded the patient file {2}".format(i + 1, len(patients_path),
                                                                                          patient_path))
                patients = [Patient.from_json_file(zip.extract(patient), settings.general_tags + settings.patients_tags + settings.sites_tags) for patient in patients_path]

                # Load Groups
                groups_path = [name for name in namelist if str.endswith(name, ".group")]
                groups = []
                for i, group_path in enumerate(groups_path):
                    try:
                        groups.append(Group.from_json_file(zip.extract(group_path), patients))
                    except OSError:
                        print("[{0}/{1}] Loading of the group file {2} failed".format(i + 1, len(groups_path),
                                                                                      group_path))
                    else:
                        print("[{0}/{1}] Successfully loaded the group file {2}".format(i + 1, len(groups_path),
                                                                                        group_path))

                # Load Protocols
                protocols_path = [name for name in namelist if str.endswith(name, ".prov")]
                protocols = []
                for i, protocol_path in enumerate(protocols_path):
                    try:
                        protocols.append(Protocol.from_json_file(zip.extract(protocol_path)))
                    except OSError:
                        print("[{0}/{1}] Loading of the protocol file {2} failed".format(i + 1, len(protocols_path),
                                                                                         protocol_path))
                    else:
                        print("[{0}/{1}] Successfully loaded the protocol file {2}".format(i + 1, len(protocols_path),
                                                                                           protocol_path))

                # Load Datasets
                datasets_path = [name for name in namelist if str.endswith(name, ".dataset")]
                datasets = []
                for i, dataset_path in enumerate(datasets_path):
                    try:
                        datasets.append(Dataset.from_json_file(zip.extract(dataset_path), protocols, patients))
                    except OSError:
                        print("[{0}/{1}] Loading of the dataset file {2} failed".format(i + 1, len(datasets_path),
                                                                                        dataset_path))
                    else:
                        print("[{0}/{1}] Successfully loaded the dataset file {2}".format(i + 1, len(datasets_path),
                                                                                          dataset_path))

                # Load Visualizations
                visualizations_path = [name for name in namelist if str.endswith(name, ".visualization")]
                visualizations = []
                for i, visualization_path in enumerate(visualizations_path):
                    try:
                        visualizations.append(Visualization.from_json_file(zip.extract(visualization_path),
                                                                           patients, datasets))
                    except OSError:
                        print("[{0}/{1}] Loading of the visualization file {2} failed".format(i + 1,
                                                                                              len(visualizations_path),
                                                                                              visualization_path))
                    else:
                        print("[{0}/{1}] Successfully loaded the visualization file {2}".format(i + 1,
                                                                                                len(visualizations_path)
                                                                                                , visualization_path))

                # Change dir back and delete tmp
                os.chdir("..")
                for root, dirs, files in os.walk(".tmp", topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(".tmp")
                print("Successfully loaded the project %s " % path)

                return cls(settings, patients, groups, protocols, datasets, visualizations)
        except OSError as err:
            print(err)
            print("Loading of the project %s failed" % path)
