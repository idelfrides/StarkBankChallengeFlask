#!/usr/bin/env python3
# encoding:utf-8


import os
import time

from IJGeneralUsagePackage.IJGeneralLib import (
    clean_diretory,
    print_log
)
from libs.ijlibs import get_project_informations

from starkBankLib.starkBankLib import (
    StarkBank
)

from utils.config_contants_paths import (
    PERSON_QUANTITY,
    RANDOM_PERSON_FILE_PATH,
)

from libs.lib_manager import (
    brasilian_api_generator_tofile,
)

from libs.ngrok_lib import (
    NgrokAPI
)

# --------------------------------------------------------------


def setupStarkBanckApp():

    print_log('START MAKING ALL SETUP . . .')

    try:
        os.mkdir('SB_SDK_KEYS')
    except Exception as error:
        print_log(f'EXCEPTION --> {error}')


    try:
        os.mkdir('OUTPUT_FILES')
    except Exception as error:
        print_log(f'EXCEPTION --> {error}')
        clean_diretory(folder_path='OUTPUT_FILES')


    try:
        os.mkdir('utils/FILES_DIR')
    except Exception as error:
        print_log(f'EXCEPTION --> {error}')
        clean_diretory(
            folder_path='utils/FILES_DIR',
            keet_files=['IJ_NGROK_CONFIG.text', 'project_infos.text']
        )


    if not os.path.exists(RANDOM_PERSON_FILE_PATH):
        if not brasilian_api_generator_tofile(
            type_data='pessoa', quantity=PERSON_QUANTITY):
            return

    create_user_webhook()

    print_log('SET UP DONE')

    return


def create_user_webhook():

    PROJECT_ID, PROJECT_NAME = get_project_informations()

    stkb = StarkBank(
        project_id=PROJECT_ID,
        project_name=PROJECT_NAME,
    )

    ngrok = NgrokAPI()

    stkb.create_starkbank_project_user()

    public_url = ngrok.get_ngrok_entity(endpoint='tunnels')

    public_url = '/'.join([public_url, 'starkbank_webhook'])

    stkb.remove_webhook()

    if public_url:
        time.sleep(2*60)
        stkb.create_webhook(webhook_url=public_url)

    return


if __name__ == '__main__':
    setupStarkBanckApp()
