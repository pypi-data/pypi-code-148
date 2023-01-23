"""Provide a log handler that allows for e-mails to be sent via smtprelay."""
from .client import RelayClient
import logging
import requests
from autoinject import injector
import typing as t


class RelayHandler(logging.Handler):
    """Implement logging.Handler for the smtprelay server.

        Note that, where possible, the parameter names have been aligned with the existing SMTPHandler for
        ease of replacement, but omitting the details that are handled by the Zirconium configuration instead. If
        specified here, arguments in the handler override the Zirconium configuration.

        Parameters
        ----------
        subject: str
            The subject of the e-mail. You may pass a string for use with a Formatter instead; if so, set format_subject
            to True.
        fromaddr: t.Optional[str]
            The e-mail address to send from.
        toaddrs: t.Optional[str]
            E-mail address or comma-delimited list of e-mail addresses to send to.
        ccaddrs: t.Optional[str]
            E-mail address or comma-delimited list of e-mail addresses to send in CC.
        bbccaddrs: t.Optional[str]
            E-mail address or comma-delimited list of e-mail addresses to send in BCC.
        send_group: t.Optional[str]
            Text to group together messages of a given type.
        format_as_html: bool
            Set to true if the formatter returns HTML instead of plain text (defaults to False)
        format_subject: bool
            Set to true if the subject parameter should be passed to a Formatter object.
        level: int
            Default logging level
    """

    rsc: RelayClient = None

    @injector.construct
    def __init__(self,
                 subject: str,
                 fromaddr: t.Optional[str] = None,
                 toaddrs: t.Optional[str] = None,
                 ccaddrs: t.Optional[str] = None,
                 bccaddrs: t.Optional[str] = None,
                 send_group: t.Optional[str] = None,
                 format_as_html: bool = False,
                 format_subject: bool = False,
                 level: int = logging.NOTSET
                 ):
        self.subject_pattern = subject
        self.to_addresses = toaddrs
        self.cc_addresses = ccaddrs
        self.bcc_addresses = bccaddrs
        self.from_address = fromaddr
        self.send_group = send_group
        self.format_as_html = format_as_html
        self.format_subject = format_subject
        super().__init__(level)

    def emit(self, record):
        """Implement emit() for the logger by creating and sending an email."""
        try:
            args = {
                'to_emails': self.to_addresses,
                'cc_emails': self.cc_addresses,
                'bcc_emails': self.bcc_addresses,
                'subject': self.get_subject(record),
                'from_email': self.from_address,
                'send_group': self.send_group,
            }
            if self.format_as_html:
                args['html_message'] = self.get_body(record)
            else:
                args['plain_message'] = self.get_body(record)
            self.rsc.send_email(**args)
        except ValueError as ex:
            print(ex)
            self.handleError(record)
        except requests.HTTPError:
            self.handleError(record)

    def get_body(self, record):
        """Convert the record into a body."""
        return self.format(record)

    def get_subject(self, record):
        """Convert the record into a subject (if format_subject is True)."""
        if self.format_subject:
            frmt = logging.Formatter(self.subject_pattern)
            return frmt.format(record)
        return self.subject_pattern
