
from asyncio import sleep
from enum import Enum
import importlib
from mimetypes import MimeTypes
import os
from typing import AsyncGenerator, List

from xbridge import file
from xbridge.MyInfo import MyInfo
from xbridge.config import Config
from xbridge.transmsg import  Codable, NormalMsg, MsgType, ParamRequire, ParamSelection, ParamType


class AvailableActions:
    SendFiles = 'send_files'
    GetFiles = 'get_files'
    ListFiles = 'list_files'
    GetInfo = 'info'
    Trust = 'trust'
    GetActions = "get_actions"
    
    # for test
    Echo = "echo"


async def handle_list_actions(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:

    actions = [
        ParamSelection(AvailableActions.GetFiles, "Get Files"),
        ParamSelection(AvailableActions.SendFiles, "Send Files"),
        ParamSelection(AvailableActions.ListFiles, "Get Files List"),
    ]

    for item in os.listdir(Config.config_dir):
        if item.endswith(".py"):
            actions.append(ParamSelection(item.removesuffix(".py")))


    yield NormalMsg(MsgType.Reply, action=msg.action, requires=[
        ParamRequire("", ParamType.SelectableList, "可用的操作", selections=actions)
    ])

    # print("actions", actions)
    # yield NormalMsg(MsgType.Reply, msg.app, msg.action, params=actions)


#
# client request get file list from me
#
# list <path>
#
async def handle_list_files(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:
    files = []
    p = ''
    params = msg.params
    if params is not None and len(params) > 0:
        p = params[0]
    dir = os.path.join(Config.files_dir, p)

    for item in os.listdir(dir):
        files.append(os.path.join(p, item))

    # await sleep(60)

    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, files)


async def handle_echo(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:
    
    # if msg.params is None or len(msg.params) == 0:
    #     # params error, reply param requirements
    #     print("echo: params is invalid! reply requirements")
    #     # require: ParamRequire = 
    #     yield NormalMsg(MsgType.Reply, action=msg.action, requires=[
    #         ParamRequire("", ParamType.SelectableList, "想要取得的文件", selections=[
    #             ParamSelection(select="a.txt"),
    #             ParamSelection(select="b.txt"),
    #         ])
    #     ])
    #     return

    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, files=received_files)



#
# otherside request get files/dirs from me
#
# get <file_path_on_otherside>...
#
async def handle_get_files(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:
    
    if msg.params is None or len(msg.params) == 0:
        # params error, reply param requirements
        print("get_files: params is invalid! reply requirements")
        # require: ParamRequire = 
        yield NormalMsg(MsgType.Reply, action=msg.action, requires=[
            ParamRequire("", ParamType.SelectableList, "想要取得的文件", selections=[
                ParamSelection(select="a.txt"),
                ParamSelection(select="b.txt"),
            ])
        ])
        return

    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, files=msg.params)



#
# otherside request send files to me
#
# send <file_path_on_otherside>...
#
async def handle_sendfiles(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:

    if msg.params is None or len(msg.params) == 0:
        # params error, reply param requirements
        print("send_files: params is invalid! reply requirements")
        # require: ParamRequire = 
        yield NormalMsg(MsgType.Reply, action=msg.action, requires=[
            ParamRequire("", ParamType.FileOrDirList, "待发送的文件")
        ])
        return

    # save received files to files dir
    file.save_files(received_files)

    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action)


async def handle_get_info(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:

    # load my info
    info = MyInfo(os.path.join(Config.config_dir, "info.json"))

    if len(msg.params) > 0 and msg.params[0] == info.version:
        yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, params=[info.version])
        return
           
    # reply result
    # head_img = "data:image/webp;base64,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"
    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, params=[info.version, info.name, info.avatar_url])


# request: trust with params[<code>]
# reply: params[1]
#           "passcode_required" if no code provided
#           "accepted" if code is correct
#           "refused" if code if incorrect 
#
async def handle_trust(msg: NormalMsg, received_files: List[str]) -> AsyncGenerator[NormalMsg, None]:
    reply = "refused"
    if len(msg.params) > 0:
        if msg.params[0] == "0000":
            reply = "accepted"
    else:
        reply = "passcode_required"
    yield NormalMsg(MsgType.Reply, None, msg.app, msg.action, params=[reply])



def get_handler_func(action: str):
        # find an handler to handle the request
        handle = None
        # print("config dir=", Config.config_dir)
        module_file_path = os.path.join(Config.config_dir, "scripts", action + '.py')
        module_name = action
        if not os.path.isfile(module_file_path):
            if Config.files_dir != '':
                # intergrated action handlers
                if action == AvailableActions.GetFiles:
                    handle = handle_get_files
                elif action == AvailableActions.SendFiles:
                    handle = handle_sendfiles
                elif action == AvailableActions.ListFiles:
                    handle = handle_list_files
                elif action == AvailableActions.GetInfo:
                    handle = handle_get_info
                elif action == AvailableActions.Trust:
                    handle = handle_trust
                elif action == AvailableActions.Echo:
                    handle = handle_echo
                elif action == AvailableActions.GetActions:
                    handle = handle_list_actions
        else:
            # custom action handlers
            print("load %s from %s" % (module_name, module_file_path))
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_file_path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            handle = module.handle_action
        return handle