"""Provides an API for sending e-mails to the smtprelay server.

    The smtprelay project provides a single-point for gathering and sending e-mails for a system for cases where a
    single exit point is needed and for providing additional redundancy if the e-mail server is down.

    This API can be used to send e-mails to the server for later sending. Configuration is done via zirconium.

    To use it, ensure your configuration has been set using Zirconium, then inject instances of RelaySendClient where
    needed.
"""
import requests
import json
import zirconium as zr
from autoinject import injector
import pathlib
from threading import Lock
import typing as t


@injector.injectable_global
class RelayClient:
    """Client class for sending emails"""

    cfg: zr.ApplicationConfig = None

    @injector.construct
    def __init__(self):
        """Construct the object."""
        self.end_point = self.cfg.as_str(('smtp_relay','end_point'), default=None)
        self.bearer_token = self.cfg.as_str(('smtp_relay', 'bearer_token'), default=None)
        self.default_send_group = self.cfg.as_str(('smtp_relay', 'send_group'), default=None)
        self.default_send_from = self.cfg.as_str(('smtp_relay', 'send_from'), default=None)
        self.retry_file = self.cfg.as_path(('smtp_relay', 'retry_file'), default=None)
        self.show_errors = self.cfg.as_bool(('smtp_relay', 'show_errors'), default=True)
        self.request_timeout = self.cfg.as_float(('smtp_relay', 'request_timeout'), default=2)
        self.cap_on_retry = self.cfg.as_int(('smtp_relay', 'cap_on_retry'), default=50)
        if self.end_point is None:
            raise ValueError('End point is required')
        if self.bearer_token is None:
            raise ValueError('Bearer token is none')
        self._file_lock = Lock()

    def retry_all(self):
        """Try to send all of the e-mails that failed again."""
        if not self.retry_file:
            return
        if not self.retry_file.exists():
            return
        with self._file_lock:
            k = 0
            t_retry = pathlib.Path(self.retry_file.path + f".tmp.{k}")
            while t_retry.exists():
                k += 1
                t_retry = pathlib.Path(self.retry_file.path + f".tmp.{k}")
            count = 0
            with open(t_retry, "w") as h2:
                with open(self.retry_file, "r") as h:
                    for line in h:
                        content = line.rstrip("\n").replace("\0", "\n")
                        count += 1
                        if count > self.cap_on_retry:
                            h2.write(content.replace("\n", "\0"))
                            h2.write("\n")
                        else:
                            try:
                                self._actual_send_email(content)
                            except (requests.HTTPError, requests.exceptions.ConnectionError) as ex:
                                if self.show_errors:
                                    print(ex)
                                h2.write(content.replace("\n", "\0"))
                                h2.write("\n")
            t_retry.replace(self.retry_file)

    def send_email(
            self,
            from_email: t.Optional[str] = None,
            to_emails: t.Optional[str] = None,
            cc_emails: t.Optional[str] = None,
            bcc_emails: t.Optional[str] = None,
            send_group: t.Optional[str] = None,
            subject: t.Optional[str] = None,
            plain_message: t.Optional[str] = None,
            html_message: t.Optional[str] = None
    ):
        """Send an email via the smtprelay server.

            Note that smtprelay requires at least one address be passed as either the To, CC, or BCC e-mail. All
            e-mails are concatenated together for sending. CC e-mails are added to the header as a CC. BCC e-mails are
            not added to the header to prevent them from being leaked if the sending server doesn't respect the BCC
            privacy.

            One of plain_message or html_message must be specified. If both are specified, a multi-part e-mail is
            created with both elements.

            Parameters
            ----------
            from_email: t.Optional[str]
                The e-mail to send from. If omitted, the default from configuration is used.
            to_emails: t.Optional[str]
                An e-mail address or a comma-delimited list of e-mail addresses to send to.
            cc_emails: t.Optional[str]
                An e-mail address or a comman-delimited list of e-mail addresses for the CC header.
            bcc_emails: t.Optional[str]
                An e-mail address or a comma-delimited list of e-mail addresses for BCC.
            send_group: t.Optional[str]
                A text string to organize e-mails by on smtprelay. If omitted, the default from configuration is used.
            subject: t.Optional[str]
                The subject to send with the e-mail.
            plain_message: t.Optional[str]
                The plain message to send as text/plain.
            html_message: t.Optional[str]
                An HTML message to send.

            Raises
            ------
            ValueError
                If there is no send from, if all of the To/CC/BCC fields are empty, or both messages were omitted.
            requests.HTTPError
                If there is an error during sending.
            requests.exceptions.ConnectionError
                If the server cannot be found during sending.
        """
        if not send_group:
            send_group = self.default_send_group
        if not from_email:
            if self.default_send_from:
                from_email = self.default_send_from
            else:
                raise ValueError("Missing send from email")
        if (not to_emails) and (not cc_emails) and (not bcc_emails):
            raise ValueError("Missing an email to send to")
        if (not plain_message) and not (html_message):
            raise ValueError("No message to send")
        if plain_message:
            plain_message = plain_message.replace("\r\n", "\n").replace("\r", "\n")
        if html_message:
            html_message = html_message.replace("\r\n", "\n").replace("\r", "\n")
        body = {
            "send_group": send_group if send_group else "",
            "send_from": from_email,
            "send_to": to_emails if to_emails else "",
            "send_cc": cc_emails if cc_emails else "",
            "send_bcc": bcc_emails if bcc_emails else "",
            "subject": subject if subject else "",
            "plain_message": plain_message if plain_message else "",
            "html_message": html_message if html_message else ""
        }
        content = json.dumps(body)
        try:
            self._actual_send_email(content)
        except (requests.HTTPError, requests.exceptions.ConnectionError) as ex:
            if self.show_errors:
                print(ex)
            if self.retry_file:
                with self._file_lock:
                    with open(self.retry_file, 'a') as h:
                        h.write(content.replace("\n", "\0"))
                        h.write("\n")
            raise ex

    def _actual_send_email(self, body):
        """Perform the request to send the body to the smtprelay server."""
        resp = requests.request(
            'put',
            self.end_point,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.bearer_token}',
            },
            timeout=self.request_timeout
        )
        resp.raise_for_status()
