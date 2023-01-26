from atfdb.atfdb import get_channel_index, get_real, put_real


def test_socket_read(socket_server):
    chidx = get_channel_index("RT_DATABASE::PTEN20;RAS;RB_CURRENT_SETPT")
    val = get_real(chidx)

    assert type(val) is float


def test_socket_write(socket_server):
    chidx = get_channel_index("RT_DATABASE::PTEN20;CDS;SET_CURRENT_SETPT")
    put_real(chidx, 100)
