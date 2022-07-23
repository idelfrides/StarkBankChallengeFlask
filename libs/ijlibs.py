#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
    #### This module hold attributes and/or methods necessary to help
    build this app better.

"""


from IJGeneralUsagePackage.IJhandleFilesLib import read_content_fromfile


def get_project_informations(filename_=None):
    """
    ### return PROJECT_ID, PROJECT_NAME

    """

    if not filename_:
        filename_ = 'project_infos.text'

    infos = read_content_fromfile(
        distiny_dir='utils/FILES_DIR',
        file_name=filename_
    )

    infos = infos.split('\n')
    id_ = infos[0].replace('PROJECT_ID=', '')
    name_ = infos[1].replace('PROJECT_NAME=', '')

    return id_, name_
