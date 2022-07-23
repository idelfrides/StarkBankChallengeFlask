#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
    #### This module hold attributes and methods necessary to help
    build this app better.

"""

import requests
from datetime import datetime
import time


from IJGeneralUsagePackage.IJGeneralLib import (
    build_line,
    chdir_witout_log,
    print_log
)

from IJGeneralUsagePackage.IJhandleFilesLib import (
    read_content_fromfile,
    readlines_content_fromfile
)

from utils.config_contants_paths import (
    PERSON_QUANTITY,
    FILE_OPERATION
)

# -------------------------------------------------------------------


def save_project_informations(project_id, project_name):
    file_name = 'project_infos.text'

    project_id = f'PROJECT_ID={project_id}'
    project_name = f'PROJECT_NAME={project_name}'

    content_ = [project_id, project_name]

    write_content_infile(
        content_list=content_,
        filename=file_name,
        operation=FILE_OPERATION['write']
    )

    return


def brasilian_api_generator(type_data, quantity):

    BASE_URL = 'https://geradorbrasileiro.com/api/faker'
    rest_url = '/'.join([BASE_URL, type_data])

    url_params = {
        'limit': quantity
    }

    try:
        payload = requests.get(rest_url, params=url_params)
    except Exception as error:
        print_log(f'EXCEPTION: {error}')
        return []

    _content_ = payload.json()

    return _content_.get('values')


def brasilian_api_generator_tofile(**kwargs):

    """
    # Generate random brasilian person
    ---

    ##### Generate random brasilian person data like , NAME, CPF, MOTHER, FATHER, PHONE, ADRESS, WEBSITISE, ... For our propose, we going to need only NAME nad CPF.

    ##### Informe values for all paramters separated with comma.

    ## Required parameters

        * type_data='TYPE DATA', can be [pessoa, cpf, cnpj, cnh, ...], default = pessoa\n
        * quantity='QUANTITY NUMBER', interger > 0\n

    """

    persons_data = []
    exists_person = True

    type_data = kwargs.get('type_data', 'pessoa')
    quantity = kwargs.get('quantity', PERSON_QUANTITY)

    print_log(f'GET [ {quantity} ] RANDOM PERSONs TO FILE [ RANDOM_PERSON.text ]...')

    content_persons = brasilian_api_generator(
        type_data=type_data, quantity=quantity
    )

    if content_persons:
        for person in content_persons:
            name_cpf = ' | '.join([person['nome'], person['cpf']])
            persons_data.append(name_cpf)

        write_content_infile(content_list=persons_data)

        exists_person = True
        print_log('DONE')

    else:
        exists_person = False
        print_log('NO PERSON WRITED')

    return exists_person


def write_content_infile(content_list, filename=None, operation=None):

    if not filename:
        filename = 'RANDOM_PERSON.text'

    if not operation:
        operation = 'a'

    # print_log(f'WRITTING [ {len(cpf_list)} ] CPFs IN FILE [ {file_name} ]...')

    chdir_witout_log(workspace='utils/FILES_DIR')

    with open(filename, operation, encoding='utf-8') as file_obj:
        for content_ in content_list:
            content_ += '\n'
            file_obj.write(content_)

    chdir_witout_log()
    # print_log('WRITTING DONE')

    return


def write_output_file(**kwarg):

    chdir_witout_log(workspace='OUTPUT_FILES')

    filename = kwarg['filename']
    content = str(kwarg['content'])

    with open(filename, 'a', encoding='utf-8') as file_obj:
        content += '\n'
        log_time = datetime.now()
        log_time = f'[ {str(log_time)[:19]} ] '
        real_content  = '| '.join([log_time, content])
        file_obj.write(real_content)

    chdir_witout_log()

    return


def get_random_person_from_local_file(local_dir='utils/FILES_DIR', filename='RANDOM_PERSON.text'):

    # print_log('GETTING ALL CPF FROM LOCAL FILE')

    chdir_witout_log(workspace=local_dir)

    with open(filename, 'r', encoding='utf-8') as file_obj:
        cpf_content = file_obj.read()
        cpf_content = cpf_content.split('\n')

    chdir_witout_log()
    # print_log('DONE')

    return cpf_content


def get_keys_from_files(key_type=''):

    # print_log('GETTING [ {} ] KEY FROM FILE ...'.format(key_type))

    chdir_witout_log(workspace='SB_SDK_KEYS')

    if key_type == 'private':
        pk_file_name = 'private-key.pem'

        with open(pk_file_name, 'r', encoding='utf-8') as private_obj:
            key_content = private_obj.read()

    if key_type == 'public':
        pubk_file_name = 'public-key.pem'

        with open(pubk_file_name, 'r', encoding='utf-8') as public_obj:
            key_content = public_obj.read()

    # print_log('DONE')

    return key_content


def show_info(some_code, person):
    info = """
    -----------------------------------------------
            CREATING INVOICE FOR --> [ {} ]
            INVOICE ORDER --> [ {} ]
    -----------------------------------------------
    """.format(person, some_code)

    print(info)
    time.sleep(3)

    return


def make_reponse(endpoint):

    ij_jsonify = {
        'state': 'SUCCESS',
        'status': 200,
        'function': '{}'.format(str(endpoint))
    }

    return ij_jsonify


class HoldInvoices:

    def __init__(self, some_obj):
        self.__some_sent = some_obj

    # Getter
    def get_invoices(self):
        return self.__some_sent

    # Setter
    def set_invoices(self, something):
        self.__some_sent = something
