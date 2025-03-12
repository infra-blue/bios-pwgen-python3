#!/usr/bin/python3

import os, struct

def getMasterPwd(serial):
	if len(serial) != 7:
		print("The serial must be exactly 7 characters in length!")
		return 

	table = "0987654321876543210976543210982109876543109876543221098765436543210987"
	pos = 0
	code = ""
	for c in serial:
		code += table[int(c)+10*pos]
		pos += 1
	return code

print("Master Password Generator for Sony laptops (serial number)")
print("Copyright (C) 2009-2010 dogbert <dogber1@gmail.com>")
print("")
print("This script generates master passwords for old Sony laptops from their serial ")
print("number.")
print("")
print("Please enter the serial number: ")
code = input()
password = getMasterPwd(code)
if password:
	print("The password is: " + password)

if (os.name == 'nt'):
	print("Press a key to exit...")
	input()
