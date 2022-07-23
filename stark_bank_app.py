#!/usr/bin/env python3
# encoding:utf-8

# Pyton importatinons

import os
from random import randint
import time

# extrnal lib importation
from IJGeneralUsagePackage.IJGeneralLib import (
    clean_diretory, build_line,
    convert_minutes_to_second,
    make_sound, print_log,
    show_info
)

# this project importation
from starkBankLib.starkBankLib import (
    StarkBank
)
from utils.config_contants_paths import (
    PERSON_QUANTITY, PROJECT_ID,
    PROJECT_NAME, SLEEP_MINUTES,
    TOTAL_ROUNDS, TOTAL_TRIES,
    WEBHOOK_WAIT_TIME,
    MIN_LIMIT, MAX_LIMIT,
    RANDOM_PERSON_FILE_PATH
)
from libs.lib_manager import (
    brasilian_api_generator_tofile,
)

#-------------------------------------------------------------------
#                   RUN APP FUNCTION BEGIN HERE
#-------------------------------------------------------------------


def starkBankRunApp(round_):
    """
    # Main function that run this application
    ---

    ##### NOTE: read the file README.md before you do any thing.

    """

    start_time = time.time()

    show_info(
        type_='app_info', app_name='STARK BANK CHALLENGE V2',
        desc_='Stark Banck thecnical challenge for join company as Python Developer.', version_='2.0.0',
        user_key='RUNNING APP | ROUND', user_key_value=round_
    )

    # TOTAL_INVOICES = randint(MIN_LIMIT, MAX_LIMIT)
    # TOTAL_INVOICES = randint(2, 3)
    TOTAL_INVOICES = 1

    stkb = StarkBank(
        project_id=PROJECT_ID,
        project_name=PROJECT_NAME,
        round_=round_
    )

    stkb.create_starkbank_project_user()
    stkb.get_balance()

    stkb.transfer_all_invoices(invoice_id_list=[])
    return

    if not os.path.exists(RANDOM_PERSON_FILE_PATH):
        if not brasilian_api_generator_tofile(
            type_data='pessoa', quantity=PERSON_QUANTITY):
            return

    if round_ == 1:
        stkb.make_events_delivered()

    stkb.create_invoices(total_invoices=TOTAL_INVOICES)

    invoices_to_transfer = stkb.validate_invoices()

    stkb.make_transfer(invoices_to_transfer)

    stop_time = time.time()
    total_round_time = stop_time - start_time

    total_round_time /= 60

    total_minutes = str(total_round_time).split('.')[0]
    total_seconds = str(total_round_time).split('.')[1]

    print_log('TOTAL TIME: %.0f min e %.0f milissegundos \n' % (int(total_minutes), int(total_seconds)))

    return


if __name__ == '__main__':

    round_ = 1

    time_sleep_seconds = convert_minutes_to_second(SLEEP_MINUTES)

    clean_diretory(folder_path='OUTPUT_FILES')
    # clean_diretory(folder_path='utils/FILES_DIR')

    while True:

        starkBankRunApp(round_)

        if round_ == TOTAL_ROUNDS:
            build_line('#', 100)
            print(f'\t\t WORKING FOR 24h COMPLETED, SO THE APP WILL BE QUITTED\n\n')
            build_line('#', 100)
            make_sound()
            break

        round_ += 1
        build_line('*', 100)
        print(f'\t\t THE APP IS GOING TO SLEEP FOR [ {SLEEP_MINUTES} ]  minutes ..')
        build_line('*', 100)
        make_sound(250)
        time.sleep(time_sleep_seconds)
