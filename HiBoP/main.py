from HiBoP.settings import *
from HiBoP.project import *
from HiBoP.group import Group
from HiBoP.patient import *
from HiBoP.protocol import *

# mon_group = Group.Group("Mon group", ["MonPatient1", "MonPatient2"])
# mon_group.to_json_file("C:/Users/Adrien/PycharmProjects/HiBoP_API/debug/Groups/MonGroup.group")
#
# mes_settings = Settings.Settings("Debug", "patientDatabase", "localizerDatabase", [Alias.Alias("MonAlias", "MonValue"),
#                                                                                    Alias.Alias("Alias2", "MonAlias2")])
# mes_settings.to_json_file("C:/Users/Adrien/PycharmProjects/HiBoP_API/debug/MesSettings.settings")


# Project creation
project = Project(Settings("Mon Projet"))

# Patients
single_mesh = SingleMesh("MonCerveau", "MonPath", "MonMarsAtlas", "MaTransformation")
left_right_mesh = LeftRightMesh("MesHemisphere", "LeftHemisphere", "RightHemisphere", "LeftMarsAtlas",
                                 "RightMarsAtlas", "MaTransformation")
adrien = Patient("Adrien", 1991, "Lyon", [single_mesh, left_right_mesh])
marine = Patient("Marine", 1995, "Toulouse", [left_right_mesh])
project.patients.append(adrien)
project.patients.append(marine)

# Groups
group = Group("Mon groupe", [adrien, marine])
group_marine = Group("Marine groupe", [marine])
project.groups.append(group)
project.groups.append(group_marine)

# Protocols
visu_protocol = Protocol("VISU")
fruit = Bloc("FRUIT", 0, "C0L1", "")
main_fruit_sub_bloc = SubBloc("Main", 0, 0, Window(-500, 100), Window(-200, 0),
                              [Event("FRUIT", [80], 0), Event("RESPONSE", [1], 1)])
fruit.sub_blocs.append(main_fruit_sub_bloc)

face = Bloc("FACE", 7, "C0L1", "")
main_face_sub_bloc = SubBloc("Main", 0, 0, Window(-500, 100), Window(-200, 0), [Event("FACE", [20], 0)])
face.sub_blocs.append(main_face_sub_bloc)

visu_protocol.blocs.extend([fruit, face])

# Save
# project.save('C:/Users/Adrien/Desktop')


Project.load("D:/HBPProjects/DEBUG.hibop")
