
import logging
import os
import sys
from typing import List
import uuid

import pkg_resources

from xbridge import bonjour, file, server, client
from xbridge.config import Config
from xbridge.inner_actions import AvailableActions
from xbridge.transmsg import NormalMsg, MsgType

# logging.basicConfig(level=logging.DEBUG)

FILES_FLAG = '--with-files'

def handle_reply(msg: NormalMsg, received_files: List[str]):
    if msg.type == MsgType.Reply:
        # print('reply:', msg.toPrettyString())
        if msg.action == AvailableActions.GetFiles:
            # move received file to files_dir
            file.save_files(received_files)
            pass
        else:
            # do nothing
            pass
    elif msg.type == MsgType.Reply:
        print("requirements:", msg.toPrettyString())
        print("\n======= Usage =====\n")
        print("%s" % msg.action, end=" ")
        for requireItem in msg.require_params:
            if requireItem.param != "":
                print("--%s" % requireItem.param, end=" ")
            print("<%s>" % requireItem.type.value, end=" ")
        print("")
        for requireItem in msg.require_params:
            selections = requireItem.selections
            if selections:
                # if requireItem.param == "":
                #         print("Selections for default param:")
                # else:
                print("\nSelections for %s %s:" % (requireItem.param if requireItem.param else "default", requireItem.localized if requireItem.localized else ""))
                for selection in selections:
                    print("  %s \t%s" % (selection.select, selection.localized if selection.localized else ""))

        print("==================\n")



def main():
    args = sys.argv[1:]
    cmd(args)

def cmd(args: List[str]):
    argslen = len(args)
    # no params
    if argslen == 0 or args[0] == '-h' or args[0] == '--help':
        version = pkg_resources.require("xbridge")[0].version
        print("xbridge v%s" % version)

        print('\nStart service:')
        print('\txbridge [-c <config>] <server>')
        print('\nClient:')
        print('  Discover services nearby:')
        print('\txbridge -d')
        print('  Get Service info:')
        print('\txbridge <server> info')
        print('  Normoal Request:')
        print('\txbridge [-c <config>] <server> request <action> [<params...> [ --with-files <files...> ]]')
        print('  Send/Get/List file:')
        print('\txbridge [-c <config>] <server> send/get/ls [<files...>]')
        print('  Continue Session:')
        print('\txbridge [-c <config>] <server> session <id> <msgtype> [ <params...> [ --with-files <files...> ]')
    else:

        if args[0] == '-d':
            bonjour.discover_service()
            return

        if args[0] == '-c':
            config_dir = args[1]
            args = args[2:]
        else:
            config_dir = os.path.join(os.environ['HOME'], '.xbridge')

        if not os.path.exists(config_dir):
            os.makedirs(config_dir, 0o755)
        elif not os.path.isdir(config_dir):
            raise Exception("Config dir %s is not a dir!" % config_dir)
        
        service_name = args[0]
        args = args[1:]

        if args[0] == 'resume':
            session_id = args[1]
            args = args[2:]
        else:
            session_id = str(uuid.uuid1())

        Config.config_dir = config_dir
        subcmd = args[0]

        if subcmd == 'discover':
            bonjour.discover_service()
            return

        if subcmd == 'start':
            # start
            server.start_service(service_name, config_dir, config_dir)
            return

        if subcmd == 'info':
            # info
            args = ['request', 'info']

        if subcmd == 'actions':
            args = ['request', 'get_actions']
           
        if subcmd == 'trust':
            # trust
            newArgs = ['request', 'trust']
            newArgs.extend(args[1:])
            args = newArgs
            # print("args:", args)
        elif subcmd == 'send':
            # send <files...>
            newArgs = ['request', AvailableActions.SendFiles]
            files = args[1:]
            # print("files1:", files)
            # newArgs.extend(files)
            newArgs.append("")
            newArgs.append(FILES_FLAG)
            newArgs.extend(files)
            # print("files:", files)
            # print("new args:", newArgs)
            args = newArgs
        elif subcmd == 'get':
            # get <files...>
            newArgs = ['request', AvailableActions.GetFiles]
            newArgs.extend(args[1:])
            args = newArgs
        elif subcmd == 'ls':
            # ls <files...>
            newArgs = ['request', AvailableActions.ListFiles]
            newArgs.extend(args[1:])
            args = newArgs

        # basic invoke request
        # <msg_type> [<action>] [<params...>] [--with-files <files...>]  
        # print(args)
        msg_type = args[0]
        action = ''
        if msg_type == 'request':
            params_index = 2
            try:
                action = args[1]
            except:
                pass
        else:
            params_index = 1

        try:
            dash_index = args.index(FILES_FLAG)
            params = args[params_index:dash_index]
            files = args[dash_index+1:]
        except:
            params = args[params_index:]
            files = []
            
        # print("action:", action)
        msg = NormalMsg(MsgType(msg_type), session_id, '', action, params, files)
        # print('req:', msg.toPrettyString())
        client.request(service_name, msg, handle_reply)


if __name__ == '__main__':
    main()

