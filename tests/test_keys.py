
#!usr/bin/python
# encoding: utf-8

import os, sys
import unittest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = ROOT_DIR.split('/tests')[0]
sys.path.append(ROOT_DIR)


from starkBankLib.starkBankLib import StarkBank

from utils.lib_manager import (
    get_keys_from_files, print_log
)

class TestKeys(unittest.TestCase):

    sbo = StarkBank()
    msg = '''

        New {key_type} KEY do not match with OLD ONE

    '''

    print_log(f'\n\t TESTING KEIS ONGOING ...\n\n\n')

    def test_private_key(self):
        new_key, _ = self.sbo.create_starkbank_keys()
        old_key = get_keys_from_files(key_type='private')

        self.assertEqual(new_key, old_key,
            msg=self.msg.format(key_type='PRIVATE'))


    def test_public_key(self):
        _, new_key = self.sbo.create_starkbank_keys()
        old_key = get_keys_from_files(key_type='public')

        self.assertEqual(
            new_key, old_key, msg=self.msg.format(key_type='PUBLIC'))


if __name__ == '__main__':
    unittest.main()