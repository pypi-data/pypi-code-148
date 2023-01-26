from atfdb.ophyd import ATFSignalNoConn


def test_ophyd_atfsignal(socket_server):
    test = ATFSignalNoConn(psname="test", db="test", name="test")
    print(test.get())
    print(test.read())
    test.put(1)
    print(test.get())
