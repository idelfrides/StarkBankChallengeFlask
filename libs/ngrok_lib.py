#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
    # This module is the ngrok lib to coonsume thrier API.

"""

import requests
import time

from utils.config_contants_paths import (
    NGROK_API_KEY,
    TOTAL_TRIES
)

from IJGeneralUsagePackage.IJGeneralLib import (
    print_log
)


class NgrokAPI(object):

    __BASE_URL__  = 'https://api.ngrok.com/{}'

    def __init__(self) -> None:

        self.__rest_header__ = {
            'Authorization': 'Bearer {}'.format(NGROK_API_KEY),
            'Content-Type': 'application/json',
            'Ngrok-Version': '2'
        }

        self.wait_time = 3  # unit time  in minutes


    def get_ngrok_entity(self, endpoint):

        rest_url = self.__BASE_URL__.format(endpoint)

        try_number = 1
        while try_number <= TOTAL_TRIES:

            print_log(f'TRYING: [ {try_number} ]')

            try:
                payload = requests.get(rest_url, headers=self.__rest_header__)
            except Exception as error:
                print_log(f'EXCEPTION : {error}')
                print_log(f'WAITTING [ {self.wait_time} ] seconds')
                time.sleep(self.wait_time*60)

            if payload.status_code == 200:
                break

            try_number += 1
            if try_number  > TOTAL_TRIES:
                print_log(f'TRIES COMPLETED: NO [ {endpoint} ] TO GET')
                return {}

        paylod_content = payload.json()

        ngrok_public_url = paylod_content.get('tunnels')[0]['public_url']

        return ngrok_public_url
