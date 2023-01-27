# The current version 
__major__, __minor__, __patch__, __state__ = 0, 1, 0,"beta1"
if __state__ is None: 
    __version__=f"{__major__}.{__minor__}.{__patch__}"
    version_number = "{}.{}.{}".format(__major__, __minor__, __patch__)
else:
    __version__=f"{__major__}.{__minor__}.{__patch__}-{__state__}"
    version_number = "{}.{}.{}-{}".format(__major__, __minor__, __patch__,__state__)
dct_major = {0: "orc"  , 1: "knight", 2: "magician", 3: "king"  , 4: "fairy" , 5: "devil"}
dct_minor = {0: "space", 1: "valley", 2: "mountain", 3: "castle", 4: "heaven", 5: "hell"}
version_name = "{}-{}".format(dct_major[__major__], dct_minor[__minor__])


__code_name__ =f""" 

 ██████╗██╗  ██╗██╗██╗     ██╗     ██╗   ██████╗ ██╗   ██╗
██╔════╝██║  ██║██║██║     ██║     ██║   ██╔══██╗╚██╗ ██╔╝
██║     ███████║██║██║     ██║     ██║   ██████╔╝ ╚████╔╝ 
██║     ██╔══██║██║██║     ██║     ██║   ██╔═══╝   ╚██╔╝  
╚██████╗██║  ██║██║███████╗███████╗██║██╗██║        ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝╚═╝        ╚═╝   
chilli.py [chilli_py] 
version: {version_name}//{version_number}
"""
# Reference: 
#   - https://patorjk.com/software/taag/#p=display&h=2&v=2&f=ANSI%20Shadow&t=Chilli

__goodbye__ = """                                      
                                      _     
 _ __   _____      _____ _ __ ___  __| |    
| '_ \ / _ \ \ /\ / / _ \ '__/ _ \/ _` |    
| |_) | (_) \ V  V /  __/ | |  __/ (_| |    
| .__/ \___/ \_/\_/ \___|_|  \___|\__,_|    
|_|                                         
 _                        __  __            
| |__  _   _    ___ ___  / _|/ _| ___  ___  
| '_ \| | | |  / __/ _ \| |_| |_ / _ \/ _ \ 
| |_) | |_| | | (_| (_) |  _|  _|  __/  __/ 
|_.__/ \__, |  \___\___/|_| |_|  \___|\___| 
       |___/  

          ██    ██    ██
        ██      ██  ██
        ██    ██    ██
          ██  ██      ██
          ██    ██    ██

      ████████████████████
      ██                ██████
      ██                ██  ██
      ██                ██  ██
      ██                ██████
        ██            ██
    ████████████████████████
    ██                    ██
      ████████████████████


"""
# Ref.: [1] http://patorjk.com/software/taag/#p=display&f=Ogre&t=powered%20%0Aby%20coffee%20
#       [2] https://textart.sh/topic/coffee


if __name__ == "__main__":
    print(__code_name__)
    print(__goodbye__)
