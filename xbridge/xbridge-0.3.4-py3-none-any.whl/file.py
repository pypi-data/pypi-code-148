

# from asyncio import sleep
from multiprocessing import Pipe, Process, Queue
from multiprocessing.connection import Connection

import shutil
from typing import AsyncGenerator, List
import os
from xbridge.cipher import Cipher
from xbridge.config import Config
from xbridge.transdata import TransData
from xbridge.transmsg import NormalMsg, MsgType
from xbridge.progress_bar import TranferBar

class FileFormat:
    NormalFile = "normal_file"
    TarArchived = "tar_archived"

async def all_file_paths_generator(dir_or_file) -> AsyncGenerator[str, None]:
    # print("test %s" % dir_or_file)
    if os.path.isfile(dir_or_file):
        yield dir_or_file

    elif os.path.isdir(dir_or_file):
        for item in os.listdir(dir_or_file):
            async for p in all_file_paths_generator('%s/%s' % (dir_or_file, item)):
                yield p
    else:
        print("%s Not found!" % dir_or_file)


async def file_generator(abspath, tempdir, cipher: Cipher) -> AsyncGenerator[bytes, None]:

        print("Will Generate File/Dir %s..." % abspath)
        basename = os.path.basename(abspath)

        if os.path.isdir(abspath):
            temptar = os.path.join(tempdir, basename)
            shutil.make_archive(temptar, "tar", abspath)
            filepath = temptar + ".tar"
            basename = basename + ".tar"
            tar_archieved = True
        else:
            filepath = abspath
            tar_archieved = False 

        # send new file cipher
        file_key = Cipher.random()
        file_iv = Cipher.random()
        msg = NormalMsg(MsgType.SendFileCipher, params=[file_key.hex(), file_iv.hex()])
        yield TransData.encrypted(msg, cipher).toBytes()

        # start a process to read and encrypt files
        (c1, c2) = Pipe()
        fileReader = Process(target=read_file_process, args=(c1, file_key, file_iv))
        fileReader.start()

        # print("File: %s" % file_path)
        # file_related_path = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        # print("file size = %d" % file_size)
        # bar = TranferBar('Sending', max=file_size)

        if tar_archieved:
            # tar format archieved dir
            resp = NormalMsg(MsgType.SendFileInfo, params=[basename, "%d"%file_size, FileFormat.TarArchived])
        else:
            # single file
            resp = NormalMsg(MsgType.SendFileInfo, params=[basename, "%d"%file_size, FileFormat.NormalFile])
            
        yield TransData.encrypted(resp, cipher).toBytes()

        # print("File: \"%s\"" % file_path)

        c2.send((filepath, file_size))
        while True:
            data = c2.recv_bytes()
            if data == b'':
                break
            # await sleep(1)
            yield data

        # send end
        msg = NormalMsg(MsgType.SendFileEnd)
        yield TransData.encrypted(msg, cipher).toBytes()

        # stop read process
        c2.send(('', 0))
        fileReader.join()

        print('end of read file!')
        


def read_file_process(pipe_c: Connection, key: bytes, iv: bytes):
    print('start read files process...')

    cipher = Cipher(key, iv)

    while True:
        file_path, file_size = pipe_c.recv()
        if file_path == '':
            break

        print("File: %s" % file_path)
        bar = TranferBar('Sending', max=file_size)

        with  open(file_path, 'rb') as file:
            while True:
                part = file.read(768*1024)
                if len(part) <= 0:
                    pipe_c.send_bytes(b'')
                    break
                bar.next(len(part))
                pipe_c.send_bytes(TransData.encrypted_bin(part, cipher).toBytes())

        bar.finish()

    print('read files process end!!!')


def write_file_process(pipe: Connection, key: bytes, iv: bytes):
    print('start write files process...')

    cipher = Cipher(key, iv)

    while True:
        file_path, file_size = pipe.recv()
        if file_path == '':
            # process end
            break


        # print("File: %s (size=%d)" % (file_path, file_size))
        print("File: %s" % file_path)
        bar = TranferBar('Receiving', max=file_size)

        received_size = 0
        with open(file_path, 'wb') as file:
            if file_size == 0:
                continue
            while True:
                data = pipe.recv()
                # print("data:", data)
                if isinstance(data, tuple):
                    print("bad data, should exit write process now!")
                    bar.finish()
                    return

                # print('data to write[%d]:'%len(data), data)
                part = cipher.decrypt(data)
                file.write(part)
                partlen = len(part)
                bar.next(partlen)

                received_size += partlen
                if received_size >= file_size:
                    break

        bar.finish()

    print('write files process end!!!')


def start_file_writer_process(key, iv):
    (c1, c2) = Pipe()
    fileWriter = Process(target=write_file_process, args=(c1, key, iv))
    fileWriter.start()
    return (c2, fileWriter)


def save_files(received_files: List[str]):
    # print('save to files dir:  %s' % Config.files_dir)

    files_dir = os.path.join(Config.config_dir, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, 0o755)

    for f in received_files:
        # print("File : %s" % f)
        if not f:
            continue

        # local_path = os.path.join(session_dir, f)
        filename = os.path.basename(f)
        path_on_files_dir = os.path.join(files_dir, filename)

        if Config.rename_save:
            index = 1
            while os.path.exists(path_on_files_dir):
                path_on_files_dir = os.path.join(files_dir, str(index) + '_' + filename)
                index += 1
        else:
            # delete exist dir
            if os.path.isdir(path_on_files_dir):
                print("dir already exist, delete!")
                shutil.rmtree(path_on_files_dir, ignore_errors=True)
        # print('from: ', f)
        shutil.move(f, path_on_files_dir)
        print("File saved in: %s" % path_on_files_dir)
