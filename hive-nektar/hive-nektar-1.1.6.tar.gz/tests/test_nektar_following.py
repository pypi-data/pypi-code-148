import os
import json
from arkivist import Arkivist
from sometime import Sometime
from nektar import Waggle
import nektar

def main():

    dt = Sometime().custom("%Y.%m.%d")

    counter = 0
    print("Initializing tests...")
    path = os.path.expanduser("~").replace("\\", "/")
    tests = Arkivist(path + "/nektar-tests.json", autosave=False)

    ##################################################
    # Waggle Class                                   #
    # Methods for blogging and engagement            #
    ##################################################
    
    NEKTAR_VERSION = nektar.__version__
    # custom_nodes = ["testnet.openhive.network"]
    # TESTNET = "18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e"
    # MAINNET = "beeab0de00000000000000000000000000000000000000000000000000000000"

    counter += 1
    print(f"\nTEST #{counter}: Initialize Waggle class with dictionary of WIFs.")
    hive = Waggle(tests["username2"], wifs=tests["wifs2"])
    
    counter += 1
    print(f"\nTEST #{counter}: Get followers")
    followers = hive.followers()
    print("\n".join(followers))
    
    counter += 1
    print(f"\nTEST #{counter}: Get following")
    following = hive.following()
    print("\n".join(following))


if __name__ == "__main__":
    main()
