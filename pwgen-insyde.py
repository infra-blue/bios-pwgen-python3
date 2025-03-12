#!/usr/bin/python

import os

def calcPassword(strHash):
	salt = 'Iou|hj&Z'

	pwd = ""
	for i in range(0, 8):
		b = ord(salt[i]) ^ ord(strHash[i])
		a = b
		a = (a * 0x66666667) >> 32
		a = (a >> 2) | (a & 0xC0)
		if ( a & 0x80000000 ):
			a += 1
		a *= 10
		pwd += str(b-a)
	return pwd


print("Master Password Generator for InsydeH2O BIOS (Acer, HP laptops)")
print("Copyright (C) 2009-2011 dogbert <dogber1@gmail.com>")
print("")
print("Enter three invalid passwords. You will receive a hash code consisting")
print("out of eight numbers ")
print("e.g. 03133610")
print("")
print("Please enter the hash: ")
inHash = input().strip().replace('-', '')
password = calcPassword(inHash)
print("")
print("The master password is: " + password)
print("")
print("Please note that the password is encoded for US QWERTY keyboard layouts.")
if (os.name == 'nt'):
	print("Press a key to exit...")
	input()

