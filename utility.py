from typing import List
from patient import Coordinate, Site
from settings import BaseTag
from tools import Vector3


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
