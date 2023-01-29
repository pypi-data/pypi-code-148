
from ...base import *
from imaplib import IMAP4_SSL
import email
from email.header import decode_header
import re
from datetime import datetime
from contextlib import contextmanager
import os
from enum import Enum

'''Instructions:
1. create app password
https://support.google.com/accounts/answer/185833
'''
@contextmanager
def IMAP4_conn_manager(
    host: str = None,
    account_email: str = None, 
    app_password: str = None
    ):
    try:
        _conn = IMAP4_SSL(host)
        _conn.login(account_email, app_password)
        yield _conn
    finally:
        _conn.close()

class EmailEnum(str, Enum):
    ALL = 'ALL'
    INBOX = 'INBOX'
    COPY = 'COPY'
    STORE = 'STORE'
    BODY = '(RFC822)'
    UID = "(UID)"

class EmailAcct:
    def __init__(
        self, 
        account_email: str = None,
        app_password: str = None, 
        which_mailbox: str = 'INBOX',
        host: str = 'imap.gmail.com'
        ):
        
        self.mailbox = which_mailbox

        with IMAP4_conn_manager(
            host=host, 
            account_email=account_email, 
            app_password=app_password) as conn:
            conn.select()
            self.conn = conn

    @property
    def logout(self):
        try:
            self.conn.logout()
        except IMAP4_SSL.error as err:
            raise Exception(f'Logout Error: {err}')

    @classmethod
    def from_gmail(cls, app_password, default_mailbox):
        return cls('imap.gmail.com', app_password, default_mailbox)

    @property
    def list_inboxes(self) -> List[str]:
        box_bytes = self.conn.list()
        decoded_boxes = [item.decode('utf-8') for item in box_bytes[1]]
        return [box.split('" "')[1].replace('"', '') for box in decoded_boxes]

    @property
    def get_namespace(self):
        return self.conn.namespace()

    @property
    def total_emails(self) -> int:
        """Total emails in all mail boxes.

		Returns:
			int: Count of total emails in all inboxes.
		"""
        status, messages = self.conn.select('inbox')
        return int(messages[0])

    def get_recent(self):
        # Prompt server for an update. 
        # Returned data is None if no new messages, 
        # else value of RECENT response.
        new_emails = self.conn.recent()
        return new_emails

    def create_new_mailbox(self, new_mailbox_name):
        '''
        Create new mailbox by name.
        If mailbox exists will fail.

        on failure: ('NO', [b'[ALREADYEXISTS] Duplicate folder name text_mailbox (Failure)'])
        '''
        m = self.conn.create(new_mailbox_name)
        return m

    def delete_emails(self, email_address: str = None):
        # select the mailbox I want to delete in
        # if you want SPAM, use imap.select("SPAM") instead
        self.conn.select("INBOX")
        # search for specific mails by sender
        status, messages = self.conn.search(None, f'(FROM "{email_address}")')
        # # to get mails by subject
        # status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')
        # # to get mails after a specific date
        # status, messages = self.conn.search(None, 'SINCE "01-JAN-2020"')
        # # to get mails before a specific date
        # status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')
        # convert messages to a list of email IDs
        messages = messages[0].split(b' ')
        print(messages)
        for mail in messages:
            _, raw_msg = self.conn.fetch(mail, "(RFC822)")

            # you can delete the for loop for performance if you have a long list of emails
            # because it is only for printing the SUBJECT of target email to delete
            for response in raw_msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    print(msg)
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes type, decode to str
                        subject = subject.decode()
                print(subject)

        #             print("Deleting", subject)
            # mark the mail as deleted
            # self.conn.store(mail, "+FLAGS", "\\Deleted")
        #     # permanently remove mails that are marked as deleted
        #     # from the selected mailbox (in this case, INBOX)
        #     self.conn.expunge()
        #     # close the mailbox
        #     self.conn.close()
        #     # logout from the account
        #     self.conn.logout()


    def get_unique_sender_emails(
        self, 
        neg_list: Optional[List[Any]] = None,
        which_mailbox: str = 'INBOX'
        ):
        self.conn.list()
        # list of "folders" aka labels in gmail.
        # self.mail.select("[Gmail]/Trash") # connect to inbox.
        self.conn.select(which_mailbox) # connect to inbox.
        # data: [b'1, 2, 3, ..., 1282'] index of all emails in all folders
        result, data = self.conn.search(None, "ALL")
        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        # fetch the email body (RFC822) for the given ID
        unique_senders = set()
        for i in id_list:
            result, data = self.conn.fetch(i, "(RFC822)")
            email_message = email.message_from_bytes(data[0][1])
            unique_senders.add(email_message['From'])
            pprint(unique_senders)
        return unique_senders

    def _search_params(self, params):
        try:
            typ, msg_ids = self.conn.search(None, params)
            if typ == 'OK':
                return msg_ids[0]
            raise Exception('Search Error')
        except Exception as err:
            return err

    def get_raw_email(self, ids):
        id_list = ids.split()# ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        # fetch the email body (RFC822)
        result, data = self.conn.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1].decode("utf-8")
        return raw_email

    def search_emails(self, search_term: str) -> Any:
        self.conn.select()
        email_ids = self._search_params(search_term)
        print(f'{email_ids}')
        # logger.info(f'found: {len(email_ids)} emails')
        # raw_email = self.get_raw_email(email_ids)
        # return raw_email


    def save_as_local(self, filename, payload):
        save_path = os.path.join(f'{os.getcwd()}', f'{datetime.now()}_{filename}')
        fp = open(save_path, 'wb')
        fp.write(payload.get_payload(decode=True))
        fp.close()
        # logger.info(f'filename: {filename}')
        return 'Success'

    def return_attachment_bytes(self, raw_email):
        email_message = email.message_from_string(raw_email)
        for item in email_message.walk():
            filename = item.get_filename()
            # logger.info(f'filename: {filename}')
            if filename:
                file_bytes = item.get_payload(decode=True)
                return file_bytes

    def save_attachment_local(self, raw_email):
        email_message = email.message_from_string(raw_email)
        for item in email_message.walk():
            filename = item.get_filename()
            # logger.info(f'filename: {filename}')
            if filename:
                self.save_as_local(filename, item)


    def get_all_attachments(self, raw_email, as_bytes=True):
        email_message = email.message_from_string(raw_email)
        try:
            for item in email_message.walk():
                filename = item.get_filename()
                # logger.info(f'filename: {filename}')
                if filename:
                    if as_bytes:
                        file_bytes = item.get_payload(decode=True)
                        return file_bytes
                    else:
                        return self.save_as_local(filename, item)
        except Exception as err:
            # logger.info(f'err: {err}')
            return err


    def parse_uid(self, data):
        pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')
        match = pattern_uid.match(data)
        return match.group('uid')
    
    def move_by_email_addr(self, email_address: str, to_mailbox: str = 'text_mailbox'):
        self.conn.select(mailbox='INBOX', readonly=False)
        status, data = self.conn.search(None, f'(FROM "{email_address}")')
        if status == 'OK':
            email_id_list  = data[0].split()
            print(f'{len(email_id_list)} Emails Found for: {email_address}')

            for email_id in email_id_list:
                result, message_id = self.conn.fetch(email_id, "(UID)")
                decoded_id = message_id[0]
                # print(decoded_id)
                if decoded_id:
                    # print(decoded_id.decode('utf-8'))
                    msg_uid = self.parse_uid(decoded_id.decode('utf-8'))
                    result = self.conn.uid('COPY', msg_uid, to_mailbox)
                    if result[0] == 'OK':
                        print(f'Message Copy Success for ID: {msg_uid}')
                        mov, data = self.conn.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
                        self.conn.expunge()
                    else:
                        print('Copy Failed')
        else:
            print('Search Failed')
    
    def move_email(self, to_mailbox: str='text_mailbox'):
        self.conn.select(mailbox='inbox', readonly=False)
        resp, items = self.conn.search(None, 'All')
        email_ids  = items[0].split()
        latest_email_id = email_ids[-1]

        # fetch the email body (RFC822) for the given ID
        # result, message = self.conn.fetch(latest_email_id, "(RFC822)")
        # email_message = email.message_from_bytes(message[0][1])
        # print(email_message['Subject'])

        # fetch uid of the latest email
        resp, message_id = self.conn.fetch(latest_email_id, "(UID)")
        decoded_id = message_id[0].decode('utf-8')
        msg_uid = self.parse_uid(decoded_id)
        # print(msg_uid)
        result = self.conn.uid('COPY', msg_uid, to_mailbox)
        if result[0] == 'OK':
            mov, data = self.conn.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
            self.conn.expunge()
        else:
            print('Copy Failed')



class Gmail:

    def __init__(self):
        self.mail = IMAP4_SSL('imap.gmail.com')
        self.mail.login('email@gmail.com', 'gmail password')
        self.save_dir = '/path/to/dir'

    def save_as_local(self, filename, payload):
        att_path = os.path.join(self.save_dir, f'{datetime.now()}_{filename}')
        fp = open(att_path, 'wb')
        fp.write(payload.get_payload(decode=True))
        fp.close()
        print('Downloaded file:', filename)

    def save_as_bytes(self, email_message):
        for item in email_message.walk():
            filename = item.get_filename()
            # logger.info(f'filename: {filename}')
            if filename:
                file_bytes = item.get_payload(decode=True)
                return file_bytes


    def save_attachment(self, email_message):
        for item in email_message.walk():
            filename = item.get_filename()
            # logger.info(f'filename: {filename}')
            if filename:
                self.save_as_local(filename, item)


    def search_mail(self):
        self.mail.list()
        # logger.info(f'list: {self.mail.list()}')
        
        # list of "folders" aka labels in gmail.
        # self.mail.select("[Gmail]/Trash") # connect to inbox.
        self.mail.select("inbox") # connect to inbox.
        # result: 'OK'
        # data: [b'1, 2, 3, ..., 1282'] index of all emails in all folders
        # result, data = self.mail.search(None, "ALL")
        # logger.info(data)


    def list_mail(self):
        self.mail.list()
        # logger.info(f'list: {self.mail.list()}')
        
        # list of "folders" aka labels in gmail.
        # self.mail.select("[Gmail]/Trash") # connect to inbox.
        self.mail.select("inbox") # connect to inbox.
        
        # result: 'OK'
        # data: [b'1, 2, 3, ..., 1282'] index of all emails in all folders
        result, data = self.mail.search(None, "ALL")

        ids = data[0] # data is a list.
        # logger.info(f'ids: {data}')

        id_list = ids.split() # ids is a space separated string
        # logger.info(f'id_list: {id_list}')
        
        latest_email_id = id_list[-1] # get the latest
        # logger.info(f'latest_email_id: {latest_email_id}')

        # fetch the email body (RFC822) for the given ID
        result, data = self.mail.fetch(latest_email_id, "(RFC822)") 
        # logger.info(f'data:      {data}')

        raw_email = data[0][1].decode("utf-8")

        email_message = email.message_from_string(raw_email)
        # logger.info(f'email_message: \n\n{email_message}')

        # logger.info(f'email payload: {email_message.keys()}')
        # self.save_attachment(email_message)
        # bts = self.save_as_bytes(email_message)
        # return bts
        return email_message

    def get_attachment_as_bytes(self, email_message):
        # logger.info(f'email payload: {email_message.keys()}')
        bts = self.save_as_bytes(email_message)
        return bts
