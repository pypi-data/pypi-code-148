# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 16:17:39 2023

@author: Spandan03
"""

import random

##FACTORIAL
def fact(a):
    b=1
    for i in range (1,a+1):
        b=b*i
    print(b)    
 
##SUM OF NUMBERS
def sum_num(a):
    b=0
    for i in range (1,a+1):
        b+=i
    print(b)

##SUM OF SQUARES
def sum_sq(a):
    b=0
    for i in range (1,a+1):
        b+=(i**2)
    print(b)

##SUM OF CUBES
def sum_cub(a):
    b=0
    for i in range (1,a+1):
        b+=(i**3)
    print(b)

##ROLLING A DIE
def roll_dice():
    a=input("Do you want to roll the dice(y/n):",)
    while a=="y" or a=="Y":
        print(random.randint(1,6))
        a=input("Do you want to roll the dice again:",)
    if a=="n" or a=="N":
        print("Thank You")
        
##TOSSING A COIN
def toss_coin():
    a=input("Do you want to toss the coin(y/n):",)
    while a=="y" or a=="Y":
        b=random.randint(1,2)
        if b==1:
            print("heads")
        else:
            print("Tails")
        a=input("Do you want to toss the coin again(y/n):",)
    if a=="n" or a=="N":
        print("Thank You")
