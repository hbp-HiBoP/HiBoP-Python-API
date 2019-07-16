import os
import csv
from patient import *


def create_project_from_bids(path):
    # General
    try:
        if os.path.exists(path):
            participants_path = path + os.altsep + "participants.tsv"
            if os.path.exists(participants_path):
                with open(participants_path) as tsv_file:
                    reader = csv.reader(tsv_file, delimiter='\t')
                    rows = []
                    for row in reader:
                        rows.append(row[0])
                patients_name = rows[1:]

                # Patient
                for patient_name in patients_name:
                    patient_directory = path + os.altsep + patient_name
                    if os.path.exists(patient_directory):
                        patient = Patient(patient_name)

                        # Post
                        post_directory = patient_directory + os.altsep + "ses-post"
                        if os.path.exists(post_directory):

                            # Anat
                            anat_directory = post_directory + os.altsep + "anat"
                            if os.path.exists(anat_directory):
                                post_file = anat_directory + os.altsep + patient.name + "_ses-post_T1w.nii"
                                if os.path.exists(post_file):
                                    patient.MRIs.append(MRI("post", post_file))

                            # iEEG
                            ieeg_directory = post_directory + os.altsep + "ieeg"
                            if os.path.exists(ieeg_directory):

                                # MNI implantation
                                mni_electrodes_file = ieeg_directory + os.altsep + patient.name + \
                                                      "_ses-post_space-MNI152Lin_electrodes.tsv"
                                if os.path.exists(mni_electrodes_file):
                                    patient.implantations.append(Implantation("MNI 152", mni_electrodes_file))

                                # Patient implantation
                                patient_electrodes_file = ieeg_directory + os.altsep + patient.name + \
                                                          "_ses-post_space-T1w_electrodes.tsv"
                                if os.path.exists(patient_electrodes_file):
                                    patient.implantations.append(Implantation("patient", patient_electrodes_file))

                        # Pre
                        pre_directory = patient_directory + os.altsep + "ses-pre"
                        if os.path.exists(pre_directory):

                            # Anat
                            anat_directory = pre_directory + os.altsep + "anat"
                            if os.path.exists(anat_directory):
                                pre_file = anat_directory + os.altsep + patient.name + "_ses-pre_T1w.nii"
                                if os.path.exists(pre_file):
                                    patient.MRIs.append(MRI("pre", pre_file))

                        # Derivatives
                        derivatives_directory = path + os.altsep + "derivatives" + os.altsep + patient.name
                        if os.path.exists(derivatives_directory):
                            # Anat
                            anat_directory = derivatives_directory + os.altsep + "anat"
                            if os.path.exists(anat_directory):

                                # Transformation
                                transformation_file = anat_directory + os.altsep + patient.name + ".trm"

                                # Grey matter
                                grey_matter_left_file = anat_directory + os.altsep + patient.name + "_T1w_pial.L.gii"
                                grey_matter_right_file = anat_directory + os.altsep + patient.name + "_T1w_pial.R.gii"
                                if os.path.exists(grey_matter_left_file) and os.path.exists(grey_matter_right_file) and os.path.exists(transformation_file):
                                    patient.meshes.append(LeftRightMesh("White matter", grey_matter_left_file, grey_matter_right_file, transformation=transformation_file))

                                # White matter
                                white_matter_left_file = anat_directory + os.altsep + patient.name + "_T1w_white.L.surf.gii"
                                white_matter_right_file = anat_directory + os.altsep + patient.name + "_T1w_white.R.surf.gii"
                                if os.path.exists(white_matter_left_file) and os.path.exists(white_matter_right_file) and os.path.exists(transformation_file):
                                    print(patient.meshes[0])
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
