#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
    #### This module hold attributes and/or methods necessary to help
    build this app better.

"""

import os
import errno

from .lib_manager import read_content_fromfile

from IJGeneralUsagePackage.IJGeneralLib import (
    chdir_witout_log
)

# -----------------------------------------------------------------


def get_project_informations(filename_=None):
    """
    ### return PROJECT_ID, PROJECT_NAME

    """


    if not filename_:
        filename_ = 'project_infos.text'

    infos = read_content_fromfile(
        path_dir='stage/FILES_DIR',
        file_name=filename_
    )

    infos = infos.split('\n')
    id_ = infos[0].replace('PROJECT_ID=', '')
    name_ = infos[1].replace('PROJECT_NAME=', '')

    return id_, name_


def home_path(destiny_dir):
    """
    Defines path based on OS
    """

    # root_project = chdir_witout_log(return_cwdir='YES')
    root_project = os.getcwd()


    # Emulate path for current project
    return_path = os.path.join(str(root_project), destiny_dir, '')

    # Create if not exists
    try:
        os.makedirs(return_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(return_path):
            pass
        else:
            raise

    return return_path


def home_stage_path(destiny_dir):
    """
    Defines path based on OS
    """

    # root_project = chdir_witout_log(return_cwdir='YES')
    root_project = os.getcwd()

    # Emulate path for current project
    return_path = os.path.join(str(root_project), 'stage', destiny_dir, '')

    # Create if not exists
    try:
        os.makedirs(return_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(return_path):
            pass
        else:
            raise

    return return_path
