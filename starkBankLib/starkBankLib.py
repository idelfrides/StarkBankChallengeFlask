#!usr/bin/python
# encoding: utf-8


# Internal python importation
import imp
import time
from datetime import datetime
from random import randint
from dateutil.relativedelta import relativedelta

# External lib importation
import starkbank

# External lib importation
from IJGeneralUsagePackage.IJGeneralLib import (
    chdir_witout_log,
    print_log,
)

# Thi project importation
from utils.config_contants_paths import (
    DAYS_OF_DUE_DATE,
    DEFAULT_PERSON_NAME,
    TOTAL_TRIES,
    WEBHOOK_WAIT_TIME
)
from libs.lib_manager import (
    HoldInvoices,
    get_keys_from_files,
    get_random_person_from_local_file,
    show_info, write_output_file
)

# ----------------------------------------------------------------
#                         BEGIN CLASS HERE
# ----------------------------------------------------------------

class StarkBank(object):
    """
    # Stark Bank class
    ---

    ##### This is the main object class. It has all attributes and methods  need and used, n fact to build the app. The class define and manage all logic to comunicate with starkbanck API.

    """

    def __init__(self, project_id=None, project_name=None, round_=None) -> None:

        self.DAYS_OF_DUE_DATE = DAYS_OF_DUE_DATE
        self.__PROJECT_ID__ = project_id
        self.__PROJECT_NAME__ = project_name
        self.file_log = f'starkbank_log_round-{round_}.log'
        self.holding_obj = HoldInvoices(0)


    def create_starkbank_project_user(self):
        private_key_content = get_keys_from_files(key_type='private')

        user_project = starkbank.Project(
            id=self.__PROJECT_ID__,
            environment='sandbox',
            private_key=private_key_content,
            name=self.__PROJECT_NAME__
        )
        starkbank.user = user_project
        starkbank.language = 'en-US'

        return


    def create_starkbank_keys(self, key_folder=''):
        print_log(f'CREATING PRIVATE KEY AND PUBLIC KEY')

        if key_folder:

            current_dir = chdir_witout_log(
                workspace=key_folder,
                return_cwdir='yes'
            )

            private_key, public_key = starkbank.key.create(current_dir)
        else:
            private_key, public_key = starkbank.key.create()

        return private_key, public_key


    def validate_cpf(self, payer_cpf, invoices):
        """
        # Make CPF validation

        #### For each CFP , check if that one already belongs to some invoice.
        #### This action is very important for CPF abriution to garantee no CPF will repeat

        """

        content = f'VALIDATION CPF --> [ {payer_cpf} ] ...'
        print_log(content)

        if not payer_cpf:
            return False

        write_output_file(filename=self.file_log, content=content)

        valid_cpf = True

        for one_invoice in invoices:
            try:
                if payer_cpf == one_invoice.tax_id:
                    content = f'\n\n--- WARNING ---\n CPF -> {payer_cpf} ALREADY EXISTS'

                    print_log(content)
                    write_output_file(filename=self.file_log, content=content)

                    valid_cpf = False
                    break
            except Exception as e:
                print_log(f'EXCEPTION:  {e}')
                valid_cpf = False

        print_log(f'CPF VALIDATION DONE')
        return valid_cpf


    def create_invoices(self, total_invoices):
        """
        # Create invoices

        ##### Create a number of invoices according to parameter total_invoices for random person with their random brasilian CPF

        """
        invoice_list = []
        content_ = f'CREATING [ {total_invoices} ] INVOICES ...'
        print_log(content_)
        write_output_file(filename=self.file_log, content=content_)

        due_date = datetime.today() + relativedelta(days=self.DAYS_OF_DUE_DATE)
        person_cpf_list = get_random_person_from_local_file()

        invoices = starkbank.invoice.query()


        for one_inv in range(1, total_invoices+1):

            invoice_amount = randint(100, 10000)
            value_discount = randint(1, 10)
            fine_percentage = randint(1, 3)       # 3 % de multa

            payer_cpf_index = randint(0, len(person_cpf_list) - 1)
            payer_name_cpf_list = person_cpf_list.pop(payer_cpf_index)
            payer_name_cpf_list = payer_name_cpf_list.split('|')

            try:
                person_name = str(payer_name_cpf_list[0]).strip()
                person_cpf = str(payer_name_cpf_list[1]).strip()
            except Exception as error:
                print_log(f'EXCEPTION: {error}')
                continue

            user_content = f'USER: {person_name} | CPF: {person_cpf}'
            write_output_file(filename=self.file_log, content=user_content)
            show_info(some_code=one_inv, person=user_content)

            if not self.validate_cpf(payer_cpf=person_cpf, invoices=invoices):
                continue

            one_invoive = {
                'amount': invoice_amount,
                'descriptions': [{'key': person_name, 'value': person_cpf}],
                'discounts':[
                    {'percentage': value_discount, 'due': due_date}
                ],
                'due': due_date,
                'name': person_name,
                'fine': fine_percentage,
                'tax_id': person_cpf
            }

            invoice_list.append(one_invoive)

            content = f'\n ------ INVOICE ----- \n{one_invoive}'
            write_output_file(filename=self.file_log, content=content)


        if not invoice_list:
            self.holding_obj.set_invoices(all_invoices)
            print_log('NO VALID INVOICE TO CREATED')
            return

        all_invoices = starkbank.invoice.create(invoice_list)

        self.holding_obj.set_invoices(all_invoices)
        print_log('INVOICES CREATION DONE')

        return


    def get_balance(self):
        """ # Showing Actual Balance """

        print_log('SHOWING ACTUAL BALANCE')

        try:
            balance = starkbank.balance.get()
        except Exception as error:
            print_log(f'EXCEPTION --> {error}')
            return

        content = {
        	'amount': balance.amount,
        	'currency': balance.currency,
        	'id': balance.id,
        	'updated': balance.updated
        }

        write_output_file(filename=self.file_log, content=content)
        print(f'\n\n {content}')

        return


    def validate_transfer(self, paid_invoice, success_transfer_made):
        """
        # Make validation of transfer
        ---

        ##### For each invoice  check if that one already was transfared to  garantee no transfer will be failed because of duplication

        """

        content = f'VALIDATE INVOICE --> {paid_invoice} ...'
        print_log(content)

        if not paid_invoice:
            return False


        if paid_invoice in success_transfer_made:
            valid_invoice = False

            print_log(
                f'INVOICE: [ {paid_invoice} ] HAVE BEEN SUCCESSFULY TRANFERED'
            )

        else:
            valid_invoice = True
            print_log(f'INVOICE --> [ {paid_invoice} ] READY TO TRANSFER')


        return valid_invoice


    def make_transfer_flask(self, all_invoices):
        """# Transfer invoices paid
        ---

        ##### Transfer all invoices paid whenever endpoint starkbank_webhook target by NGROK POST by a stark banck apid webhook event and still able to be tranfered to Stark Bank account
        """

        all_transfer_made = True

        content = f'TRANSFER {len(all_invoices)} INVOICES TO STARK BANK '

        print_log(content)
        write_output_file(filename=self.file_log, content=content)

        if not all_invoices:
            print_log('NO INVOICE TO MAKE TRANSFER')
            return

        yesterday_date = datetime.today() - relativedelta(days=1)

        try:

            if all_transfer_made:
                transfers = starkbank.transfer.query()
            else:
                transfers = starkbank.transfer.query(
                    after=yesterday_date
                )
        except Exception as error:
            print_log(f'EXCEPTION: {error}')
            print_log('TRANSFER ABORTED')
            return

        success_transfer_made = self.find_invoice_transfered(
            transfer_obj=transfers
        )

        transfer_list = []
        for one_invoice in all_invoices:
            invoice_id = one_invoice['id']

            if not self.validate_transfer(invoice_id, success_transfer_made):
                continue

            owner_invoice = one_invoice['name']
            amount_transfer = one_invoice['amount']
            created_date = one_invoice['created']
            due_date = one_invoice['due']

            one_trandfer = {
                'amount': amount_transfer,
                'tax_id': '20.018.183/0001-80',
                'name': 'Stark Bank S.A.',
                'bank_code': '20018183',
                'branch_code': '0001',
                'account_number': '6341320293482496',
                'account_type': 'payment',
                'tags': [
                    'OWNER: %s' %owner_invoice, 'INVOICE ID: %s'%invoice_id,
                    'CREATED: %s'%str(created_date), 'DUE: %s'%str(due_date)
                ]
            }

            transfer_list.append(one_trandfer)

            content = f'\n ---- TRANSFER ---- \n {one_trandfer}'
            write_output_file(filename=self.file_log, content=content)


        if not transfer_list:
            print_log('NO INVOICE TO MAKE TRANSFER')
            return

        transfers = starkbank.transfer.create(transfer_list)

        print_log('TRANSFER COMPLETE')

        return


    def make_transfer(self, all_invoices):
        """# Transfer invoices paid
        ---

        ##### Transfer all invoices paid and present in webhook event and still able to be tranfered to Stark Bank account
        """

        all_transfer_made = True

        content = f'TRANSFER {len(all_invoices)} INVOICES TO STARK BANK '

        print_log(content)
        write_output_file(filename=self.file_log, content=content)

        if not all_invoices:
            print_log('NO INVOICE TO MAKE TRANSFER')
            return

        yesterday_date = datetime.today() - relativedelta(days=1)

        try:

            if all_transfer_made:
                transfers = starkbank.transfer.query()
            else:
                transfers = starkbank.transfer.query(
                    after=yesterday_date
                )
        except Exception as error:
            print_log(f'EXCEPTION: {error}')
            print_log('TRANSFER ABORTED')
            return

        success_transfer_made = self.find_invoice_transfered(
            transfer_obj=transfers
        )

        transfer_list = []
        for one_invoice in all_invoices:
            invoice_id = one_invoice.id

            if not self.validate_transfer(invoice_id, success_transfer_made):
                continue

            owner_invoice = one_invoice.name
            amount_transfer = one_invoice.amount
            created_date = one_invoice.created
            due_date = one_invoice.due

            one_trandfer = {
                'amount': amount_transfer,
                'tax_id': '20.018.183/0001-80',
                'name': 'Stark Bank S.A.',
                'bank_code': '20018183',
                'branch_code': '0001',
                'account_number': '6341320293482496',
                'account_type': 'payment',
                'tags': [
                    'OWNER: %s' %owner_invoice, 'INVOICE ID: %s'%invoice_id,
                    'CREATED: %s'%str(created_date), 'DUE: %s'%str(due_date)
                ]
            }

            transfer_list.append(one_trandfer)

            content = f'\n ---- TRANSFER ---- \n {one_trandfer}'
            write_output_file(filename=self.file_log, content=content)


        if not transfer_list:
            print_log('NO INVOICE TO MAKE TRANSFER')
            return

        transfers = starkbank.transfer.create(transfer_list)

        print_log('WAITTING FOR TRANSFER TO COMPLETE . . .')
        time.sleep(2*60)

        print_log('TRANSFER COMPLETE')

        return


    def get_webhook_callback(self, webhook_wait_time):
        """
        # Listen and get events webhook callback
        ---

        ##### - In stark bank API webhook callback is represented by events occurrance in a workspace.

        ##### - Every time a log is created, a corresponding event will be generated and sent to you by webhook, if the appropriate subscription was set. Therefore, the event represents an occurrence in your workspace.

        ##### - NOTE: All the events have a log property containing an entity log. The nature of the log, however, may change according to the subscription that triggered the event. For example, if the subscription is transfer, the log in the event will be a TransferLog. If the subscription is invoice, the log in the event will be a InvoiceLog, and so on.
        """

        print_log(f'APP IS LISTEN TO WEBHOOK EVENT ...')
        time.sleep(webhook_wait_time * 60)
        time.sleep(20)

        print_log('GETTING WEBHOOK EVENT ...')
        content = f'\n\n ---------- GETTING WEBHOOK EVENTS -----------\n'
        write_output_file(filename=self.file_log, content=content)

        yesterday_date = datetime.today() - relativedelta(days=1)

        invoices_paid_dict = {}
        event_seen = set()

        try:
            all_events = starkbank.event.query(
                is_delivered=True,
                after=str(yesterday_date)[:10],   # day after yesterday mean today
                limit=100
            )
        except Exception as error:
            print_log(f'EXCEPTION:  {error}')
            return invoices_paid_dict

        all_events = list(all_events)

        for event in all_events:
            if event.log.invoice.status != 'paid':
                all_events.remove(event)

        for event in all_events:
            if event.log.invoice.id in event_seen:
                continue
            event_seen.add(event.log.invoice.id)

            content = f'EVENT: {event.id}'
            write_output_file(filename=self.file_log, content=content)

            invoices_paid_dict[str(event.log.invoice.id)] = event.log.invoice

        print_log('GETTING WEBHOOK EVENTS DONE')

        return invoices_paid_dict


    def make_events_delivered(self):
        """
        # Make events as delivered
        ---

        ##### This method update all events created before today to delivered events. This is very important to avoid a customer having outdated  informations. This is about StarkBank recommendation.

        #####  NOTE 2: Even if you use Webhook, we strongly recommend that you create a daily task to get all undelivered events and set them as delivered. It's important to add redundancy and resilience to your system, preventing you from having outdated information just in case your system is temporarily unable to receive our Webhook events.

        """

        print_log('UPDATING EVENTS ...')

        undelivered_events = starkbank.event.query(
            is_delivered=False,
            before=str(datetime.today())[:10]
        )

        for event in undelivered_events:
            starkbank.event.update(event.id, is_delivered=True)

        print_log('DONE')

        return


    def validate_invoices(self):
        """
        # Validate all invoices before transfer them

        ##### Make validation of all invoices to ensure that they was come in webhook callback event.

        """

        invoices_acctually_paid = []

        # created_invoices = self.holding_obj.get_invoices()

        created_invoices = self.get_paid_invoices()

        content = f'VALIDATE INVOICES ...' # [ {len(created_invoices)} ]'

        print_log(content)

        write_output_file(filename=self.file_log, content=content)

        if not created_invoices:
            return invoices_acctually_paid


        try_number = 1
        while try_number <= TOTAL_TRIES:

            print_log(f'TRYING: [ {try_number} ]')

            webhook_event_callback = self.get_webhook_callback(
                WEBHOOK_WAIT_TIME)

            if webhook_event_callback:
                break

            try_number += 1
            if try_number  > TOTAL_TRIES:
                print_log(f'THERE ARE NO INVOICES TO TRANSFER')
                return invoices_acctually_paid

        webhook_event_invoices = webhook_event_callback.keys()

        for one_invoice in created_invoices:

            try:
                if not str(one_invoice.id) in webhook_event_invoices:

                    content = f'\n\n--- WARNING ---\n INVOICE [ {one_invoice.id} ] DO NOT EXISTS IN EVENTS'

                    print_log(f'-- WARNING -- ||  INVOICE [ {one_invoice.id} ] DO NOT EXISTS IN EVENTS')

                    write_output_file(filename=self.file_log, content=content)
                    continue

            except Exception as e:
                print_log(f'EXCEPTION: {e}')
                continue

            invoices_acctually_paid.append(
                webhook_event_callback.get(str(one_invoice.id))
            )

        return invoices_acctually_paid


    def transfer_all_invoices(self, invoice_id_list=[]):

        invoices_acctually_paid = []

        webhook_event_callback = self.get_webhook_callback(0)

        if invoice_id_list:        # only invoices in this list
            for one_invoice_id in list(webhook_event_callback.keys()):
                if not str(one_invoice_id) in invoice_id_list:
                    continue

                invoices_acctually_paid.append(
                    webhook_event_callback.get(str(one_invoice_id))
                )
        else:                      # all invoices already created and paid
            for one_invoice_id in list(webhook_event_callback.keys()):

                invoices_acctually_paid.append(
                    webhook_event_callback.get(str(one_invoice_id))
                )

        self.make_transfer(invoices_acctually_paid)

        return


    def get_all_transfer_invoice_paid(self):

        all_transfer = []
        all_invoices = []

        transfers = starkbank.transfer.query()
        time.sleep(20)
        invoices = starkbank.invoice.query()

        for one_invoice in invoices:
            if one_invoice.status == 'paid':
                all_invoices.append(one_invoice.id)


        for transfer in transfers:
            transfered_invoice = str(transfer.tags[1]).split(':')[1]

            if transfered_invoice.strip() in all_invoices:
                all_transfer.append(transfer.id)
                all_transfer.append(transfer.status)
                all_transfer.append(transfer.amount)
                all_transfer.append(transfer.tags[:2])


        all_invoices = []
        for one_invoice in invoices:
            if one_invoice.status == 'paid':
                all_invoices.append(one_invoice.id)
                all_invoices.append(one_invoice.name)
                all_invoices.append(one_invoice.status)
                all_invoices.append(one_invoice.amount)

        transfers_invoices = {
            'ALL_TRANSFER': all_transfer,
            'ALL_INVOICES': all_invoices
        }

        print(transfers_invoices)

        return


    def find_invoice_transfered(self, transfer_obj):
        """# Find  all invoices successfuly transfered

        ##### Return a list of all those invoices
        """

        all_invoices = []

        for transfer in transfer_obj:

            if transfer.status == 'success':
                transfered_invoice = str(transfer.tags[1]).split(':')[1]
                all_invoices.append(transfered_invoice.strip())

        return all_invoices


    def get_paid_invoices(self):
        """# Find and return all paid invoices"""

        invoices_paid = []

        all_invoices_paid = starkbank.invoice.query(status='paid')

        for invoice in all_invoices_paid:
            invoices_paid.append(invoice)

        return invoices_paid


    def create_webhook(self, webhook_url):

        print_log('NEW WEBHOOK CREATION')

        try:
            new_webhook = starkbank.webhook.create(
                url=webhook_url,
                subscriptions=[
                    'invoice'
                ]
            )
        except Exception as error:
            print_log(f'EXCEPTION {error}')
            return

        else:
            print_log('WEBHOOK CREATE DONE')
            print_log(f'WEBHOOK ID: {new_webhook.id}')
            return


    def remove_webhook(self):

        webhooks = starkbank.webhook.query()

        for webhook in webhooks:
            starkbank.webhook.delete(id=webhook.id)

        return
