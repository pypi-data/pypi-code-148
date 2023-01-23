#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
import socket
import errno
import sys
from pysnmp.carrier.asyncore.base import AbstractSocketTransport
from pysnmp.carrier import sockfix, sockmsg, error
from pysnmp import debug

# Ignore these socket errors
sockErrors = {errno.ESHUTDOWN: True,
              errno.ENOTCONN: True,
              errno.ECONNRESET: False,
              errno.ECONNREFUSED: False,
              errno.EAGAIN: False,
              errno.EWOULDBLOCK: False}

if hasattr(errno, 'EBADFD'):
    # bad FD may happen upon FD closure on n-1 select() event
    sockErrors[errno.EBADFD] = True


class DgramSocketTransport(AbstractSocketTransport):
    sockType = socket.SOCK_DGRAM
    retryCount = 3
    retryInterval = 1
    addressType = lambda x: x

    def __init__(self, sock=None, sockMap=None):
        self.__outQueue = []
        self._sendto = lambda s, b, a: s.sendto(b, a)

        def __recvfrom(s, sz):
            d, a = s.recvfrom(sz)
            return d, self.addressType(a)

        self._recvfrom = __recvfrom
        AbstractSocketTransport.__init__(self, sock, sockMap)

    def openClientMode(self, iface=None):
        if iface is not None:
            try:
                self.socket.bind(iface)
            except OSError:
                raise error.CarrierError(
                    'bind() for {} failed: {}'.format(iface is None and "<all local>" or iface, sys.exc_info()[1]))
        return self

    def openServerMode(self, iface):
        try:
            self.socket.bind(iface)
        except OSError:
            raise error.CarrierError(f'bind() for {iface} failed: {sys.exc_info()[1]}')
        return self

    def enableBroadcast(self, flag=1):
        try:
            self.socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_BROADCAST, flag
            )
        except OSError:
            raise error.CarrierError(f'setsockopt() for SO_BROADCAST failed: {sys.exc_info()[1]}')
        debug.logger & debug.flagIO and debug.logger('enableBroadcast: {} option SO_BROADCAST on socket {}'.format(flag and "enabled" or "disabled", self.socket.fileno()))
        return self

    def enablePktInfo(self, flag=1):
        if (not hasattr(self.socket, 'sendmsg') or
                not hasattr(self.socket, 'recvmsg')):
            raise error.CarrierError('sendmsg()/recvmsg() interface is not supported by this OS and/or Python version')

        try:
            if self.socket.family == socket.AF_INET:
                self.socket.setsockopt(socket.SOL_IP, socket.IP_PKTINFO, flag)

            if self.socket.family == socket.AF_INET6:
                self.socket.setsockopt(socket.SOL_IPV6, socket.IPV6_RECVPKTINFO, flag)

        except OSError:
            raise error.CarrierError('setsockopt() for {} failed: {}'.format(self.socket.family == socket.AF_INET6 and "IPV6_RECVPKTINFO" or "IP_PKTINFO", sys.exc_info()[1]))

        self._sendto = sockmsg.getSendTo(self.addressType)
        self._recvfrom = sockmsg.getRecvFrom(self.addressType)

        debug.logger & debug.flagIO and debug.logger('enablePktInfo: {} option {} on socket {}'.format(self.socket.family == socket.AF_INET6 and "IPV6_RECVPKTINFO" or "IP_PKTINFO", flag and "enabled" or "disabled", self.socket.fileno()))
        return self

    def enableTransparent(self, flag=1):
        try:
            if self.socket.family == socket.AF_INET:
                self.socket.setsockopt(
                    socket.SOL_IP, socket.IP_TRANSPARENT, flag
                )
            if self.socket.family == socket.AF_INET6:
                self.socket.setsockopt(
                    socket.SOL_IPV6, socket.IPV6_TRANSPARENT, flag
                )

        except OSError:
            raise error.CarrierError('setsockopt() for IP_TRANSPARENT failed: %s' % sys.exc_info()[1])

        except OSError:
            raise error.CarrierError('IP_TRANSPARENT socket option requires superusre previleges')

        debug.logger & debug.flagIO and debug.logger('enableTransparent: {} option IP_TRANSPARENT on socket {}'.format(flag and "enabled" or "disabled", self.socket.fileno()))
        return self

    def sendMessage(self, outgoingMessage, transportAddress):
        self.__outQueue.append(
            (outgoingMessage, self.normalizeAddress(transportAddress))
        )
        debug.logger & debug.flagIO and debug.logger('sendMessage: outgoingMessage queued (%d octets) %s' % (len(outgoingMessage), debug.hexdump(outgoingMessage)))

    def normalizeAddress(self, transportAddress):
        if not isinstance(transportAddress, self.addressType):
            transportAddress = self.addressType(transportAddress)

        if not transportAddress.getLocalAddress():
            transportAddress.setLocalAddress(self.getLocalAddress())

        return transportAddress

    def getLocalAddress(self):
        # one evil OS does not seem to support getsockname() for DGRAM sockets
        try:
            return self.socket.getsockname()

        except Exception:
            return '0.0.0.0', 0

    # asyncore API
    def handle_connect(self):
        pass

    def writable(self):
        return self.__outQueue

    def handle_write(self):
        outgoingMessage, transportAddress = self.__outQueue.pop(0)
        debug.logger & debug.flagIO and debug.logger('handle_write: transportAddress %r -> %r outgoingMessage (%d octets) %s' % (transportAddress.getLocalAddress(), transportAddress, len(outgoingMessage), debug.hexdump(outgoingMessage)))
        if not transportAddress:
            debug.logger & debug.flagIO and debug.logger('handle_write: missing dst address, loosing outgoing msg')
            return
        try:
            self._sendto(
                self.socket, outgoingMessage, transportAddress
            )
        except OSError:
            if sys.exc_info()[1].args[0] in sockErrors:
                debug.logger & debug.flagIO and debug.logger(f'handle_write: ignoring socket error {sys.exc_info()[1]}')
            else:
                raise error.CarrierError(f'sendto() failed for {transportAddress}: {sys.exc_info()[1]}')

    def readable(self):
        return 1

    def handle_read(self):
        try:
            incomingMessage, transportAddress = self._recvfrom(self.socket, 65535)
            transportAddress = self.normalizeAddress(transportAddress)
            debug.logger & debug.flagIO and debug.logger(
                'handle_read: transportAddress %r -> %r incomingMessage (%d octets) %s' % (transportAddress, transportAddress.getLocalAddress(), len(incomingMessage), debug.hexdump(incomingMessage)))
            if not incomingMessage:
                self.handle_close()
                return
            else:
                self._cbFun(self, transportAddress, incomingMessage)
                return
        except OSError:
            if sys.exc_info()[1].args[0] in sockErrors:
                debug.logger & debug.flagIO and debug.logger(f'handle_read: known socket error {sys.exc_info()[1]}')
                sockErrors[sys.exc_info()[1].args[0]] and self.handle_close()
                return
            else:
                raise error.CarrierError(f'recvfrom() failed: {sys.exc_info()[1]}')

    def handle_close(self):
        pass  # no datagram connection
