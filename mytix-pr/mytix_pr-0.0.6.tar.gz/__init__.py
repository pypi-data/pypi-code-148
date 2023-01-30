from colorama import Fore
import time



def pr(content):
    
    print(Fore.LIGHTBLACK_EX + time.strftime("%H:%M:%S", time.gmtime()) + Fore.WHITE + " - " +  content + Fore.WHITE)
    
def pr_success(content):
    
    print(Fore.LIGHTBLACK_EX + time.strftime("%H:%M:%S", time.gmtime()) + Fore.WHITE + " - " + "("+Fore.GREEN+"+"+Fore.WHITE+") "+Fore.GREEN + content + Fore.WHITE)
    
    
    
def pr_fail(content):
    
    print(Fore.LIGHTBLACK_EX + time.strftime("%H:%M:%S", time.gmtime()) + Fore.WHITE + " - " + "("+Fore.RED+"-"+Fore.WHITE+") "+Fore.RED + content + Fore.WHITE)
    
    
def pr_input(content):
    input(Fore.LIGHTBLACK_EX + time.strftime("%H:%M:%S", time.gmtime()) + Fore.WHITE + " - " + "("+Fore.YELLOW+"?"+Fore.WHITE+") "+Fore.LIGHTBLACK_EX + content + Fore.WHITE)   
    
    
    
def pr_warn(content):
    
    print(Fore.LIGHTBLACK_EX + time.strftime("%H:%M:%S", time.gmtime()) + Fore.WHITE + " - " + "("+Fore.RED+"!"+Fore.WHITE+") "+Fore.RED + content + Fore.WHITE)