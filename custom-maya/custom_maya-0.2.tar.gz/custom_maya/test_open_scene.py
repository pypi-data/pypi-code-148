# import maya.standalone
# maya.standalone.initialize(name='python')
# import maya.cmds as cmds
# import pymel.core as pm
#
# def open_file(file_path):
#     cmds.file(file_path, f=True, options='v=0', iv=True, typ='mayaBinary', o=True)
#
#
# def import_fbx(file_path):
#     cmds.file(file_path, i=True, type='FBX', iv=True)
#
# def get_d():
#     all_joint = pm.ls(type='joint')
#
#     joint_index = {}
#
#     for i in all_joint:
#         index = len(i.longName().split('|'))
#         joint_index[i.name()] = index
#     return joint_index
#
#
#
# import_fbx(r"")
# try:
#     cmds.parent('NULL', w=True)
# except Exception as ret:
#     print(ret)
# scene1 = get_d()
#
# cmds.file(new=True, f=True)
#
#
# import_fbx(r"")
# try:
#     cmds.parent('NULL', w=True)
# except Exception as ret:
#     print(ret)
# scene2 = get_d()
#
# cmds.file(new=True, f=True)
#
# l1 = list(scene1.keys())
# l2 = list(scene2.keys())
#
# common_list = list(set(l1).intersection(set(l2)))
#
# text = ''
# diff_joint_list = []
# for i in common_list:
#     if scene1[i] != scene2[i]:
#         diff_joint_list.append(i)
#
#
# with open('xx.txt','w')as f:
#     f.write('\n'.join(diff_joint_list))