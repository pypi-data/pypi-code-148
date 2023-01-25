import maskpass 
import base64 
from colorama import Fore, init
import time
import os
from tkinter import *
init()
tk=Tk()
print("If you want to lock a hidden folder, It is highly recommended to hide the folder using command prompt. See the tutorial here : https://bit.ly/3Iazjpb")
time.sleep(3)
print("\n\nYou can also use this app to open URLs that you want. These URLs will be opened in your default browser.")
time.sleep(3)
a = int(input("\n\nIf you already know this step enter 1 and if not (It is highly recommended to complete first step): "))
if a == 1:
		
	lockedDirectory = input("Enter your directory which is locked (Case sensetive, copy and paste the path): ")

	dict = {'Arjun': b'cmFodWw=',
				'Hrishikesh': b'U2FuZGVlcA=='}
	def signUp():
			print("\n===========Create Account============")
			name = input("Username : ")
			pwd = maskpass.askpass("Password : ")
			encpwd = base64.b64encode(pwd.encode("utf-8"))
			dict[name] = encpwd
	def logIn():
		while True:
			print(Fore.RESET + "\n\n============Login Page==============")
			name = input("Username : ")
			pwd = maskpass.askpass("Password : ")
			encpwd = base64.b64encode(pwd.encode("utf-8"))
			password = dict[name]
			if(encpwd == password):
				print("Please wait while we are checking the login info...")
				time.sleep(3)
				print(Fore.GREEN + "Successfully logged in.")
				print("Here you are!")
				os.startfile(lockedDirectory) 
				exit()
			else:
				print("Please wait while we are checking the login info...")
				time.sleep(3)
				print(Fore.RED + "Login Failed. Please try again in 3 seconds. (This is done to prevent Brute Forcing)")
				time.sleep(3)		

	signUp()
	logIn()
elif a == 2:
	print("\n\nYou are not allowed to use this app unless you see that video tutorial.\n\n")