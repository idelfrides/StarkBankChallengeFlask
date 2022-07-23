#!/usr/bin/env python3
# encoding:utf-8

# Pyton importatinons
import os
from random import randint
import time

from starkBankLib import __app__
from flask import request

# external lib importation
from IJGeneralUsagePackage.IJGeneralLib import (
    clean_diretory, build_line,
    convert_minutes_to_second,
    make_sound, print_log,
    show_info
)

# this project importation
from starkBankLib.starkBankLib import (
    StarkBank,
)

from utils.config_contants_paths import (
    SLEEP_MINUTES,TOTAL_ROUNDS,
    MIN_LIMIT, MAX_LIMIT,
)

from libs.ijlibs import get_project_informations

from libs.lib_manager import (
    make_reponse,
    save_project_informations,
)


from setup_app import setupStarkBanckApp


#-------------------------------------------------------------------------
#                  RUN APP FUNCTION BEGIN HERE
#-------------------------------------------------------------------------

def starkBankRunApp(round_):
    """
    # Main function that run this application
    ---

    ##### NOTE: read the file README.md before you do any thing.

    """

    show_info(
        type_='app_info', app_name='STARK BANK CHALLENGE V2',
        desc_='Stark Banck thecnical challenge for join company as Python Developer.', version_='2.0.0',
        user_key='RUNNING APP | ROUND', user_key_value=round_
    )

    TOTAL_INVOICES = randint(MIN_LIMIT, MAX_LIMIT)
    # TOTAL_INVOICES = randint(2, 3)

    PROJECT_ID, PROJECT_NAME = get_project_informations()

    stkb = StarkBank(
        project_id=PROJECT_ID,
        project_name=PROJECT_NAME,
        round_=round_
    )

    stkb.create_starkbank_project_user()

    stkb.get_balance()

    if round_ == 1:
        stkb.make_events_delivered()


    stkb.create_invoices(total_invoices=TOTAL_INVOICES)

    return


# ------------------------------------------------------------------------

@__app__.route('/home')
@__app__.route('/inicio')
@__app__.route('/index')
@__app__.route('/')
def hello():
    return '<h1>HELLO WORLD!!! \n\n MY NAME IS IJ, I AM A FULLSTACK PYTHON DEVELOPER</h1>'


@__app__.route('/gen_project_keys', methods=['GET'])
def gen_project_keys():

    stkb = StarkBank()

    try:
        os.mkdir('SB_SDK_KEYS')
    except Exception as error:
        print_log(f'EXCEPTION --> {error}')

    stkb.create_starkbank_keys(key_folder='SB_SDK_KEYS')

    return make_reponse(endpoint='gen_project_keys')


@__app__.route('/setup_starkbankapp')
@__app__.route('/setup_starkbankapp/<project_id>/<project_name>')
def setup_starkbankapp(project_id=None, project_name=None):

    if project_id:
        save_project_informations(project_id, project_name)

    setupStarkBanckApp()

    return make_reponse(endpoint='setup_starkbankapp')


@__app__.route('/starkbank_webhook', methods=['POST'])
def starkbank_webhook():

    transfer_list = []

    event_data = request.json

    event_status = event_data['event']['log']['invoice']['status']

    if event_status != 'paid':
        return make_reponse('starkbank_webhook | CREATION INVOICE EVENT')


    PROJECT_ID, PROJECT_NAME = get_project_informations()

    stkb = StarkBank(
        project_id=PROJECT_ID,
        project_name=PROJECT_NAME
    )

    invoice_content = event_data['event']['log']['invoice']

    transfer_list.append(invoice_content)

    stkb.create_starkbank_project_user()

    stkb.make_transfer_flask(transfer_list)

    return make_reponse(endpoint='starkbank_webhook | PAID INVOICE EVENT')


@__app__.route('/transfer_all_invoices', methods=['GET'])
def transfer_all_invoices():

    PROJECT_ID, PROJECT_NAME = get_project_informations()

    stkb = StarkBank(
        project_id=PROJECT_ID,
        project_name=PROJECT_NAME
    )

    stkb.create_starkbank_project_user()
    stkb.transfer_all_invoices(invoice_id_list=[])

    return make_reponse(endpoint='transfer_all_invoices')


@__app__.route('/starkbank_runapp', methods=['GET'])
def starkbank_runapp():

    start_time_ = time.time()

    round_ = 1

    time_sleep_seconds = convert_minutes_to_second(SLEEP_MINUTES)

    clean_diretory(folder_path='OUTPUT_FILES')

    while True:

        starkBankRunApp(round_)

        if round_ == TOTAL_ROUNDS:
            build_line('#', 100)
            print(f'\t\t WORKING FOR 24h IS COMPLETE, SO THE APP WILL BE QUITTED\n\n')
            build_line('#', 100)
            make_sound()
            break

        round_ += 1
        build_line('*', 100)
        print(f'\t\t THE APP IS GOING TO SLEEP FOR [ {SLEEP_MINUTES} ]  minutes ..')
        build_line('*', 100)
        time.sleep(time_sleep_seconds)

    stop_time = time.time()
    total_round_time = stop_time - start_time_

    total_round_time /= 60

    total_minutes = str(total_round_time).split('.')[0]
    total_seconds = str(total_round_time).split('.')[1]

    show_info_time = 'TOTAL TIME: %.0f min e %.0f milissegundos' % (int(total_minutes), int(total_seconds))

    endpoint = 'starkBankRunApp | {}'.format(show_info_time)

    return make_reponse(endpoint)


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    __app__.run(
        __app__.config['FLASK_HOST'], port=__app__.config['FLASK_PORT']
    )
