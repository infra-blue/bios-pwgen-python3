#!/usr/bin/python

import os

# d'oh
def generateCRC16Table():
	table = []
	for i in range(0, 256):
		crc = (i << 8)
		for j in range(0, 8):
			if crc & 0x8000:
				crc = (crc << 1) ^ 0x1021
			else:
				crc = (crc << 1)
		table.append(crc & 0xFFFF)
	return table

# D'OH
def calculateHash(word, table):
	hash = 0
	for c in word:
		d = table[(ord(c) ^ (hash >> 8)) % 256]
		hash = ((hash << 8) ^ d) & 0xFFFF
	return hash

def hashToString(hash):
	return (chr(ord('0') + ((hash>>12) % 16) % 10) + chr(ord('0') + ((hash>>8) % 16) % 10) + chr(ord('0') + ((hash>>4) % 16) % 10)  + chr(ord('0') + ((hash>>0) % 16) % 10)) 
 
def decryptCode(code, table):
	return hashToString(calculateHash(code[0:4], table)) + hashToString(calculateHash(code[4:8], table))

print("Master Password Generator for FSI laptops (hexadecimal digits version)")
print("Copyright (C) 2009 dogbert <dogber1@gmail.com>")
print("")
print("After entering the wrong password for the third time, you will receive a")
print("hexadecimal code from which the master password can be calculated,")
print("e.g. 0A1B2D3E or AAAA-BBBB-CCCC-DEAD-BEEF")
print("")
print("Please enter the code: ")
code = input().replace('-', '')
if len(code) == 20: code = code[12:20]
table = generateCRC16Table()
password = decryptCode(code.upper(), table)

print("The master password is: " + password)
if (os.name == 'nt'):
	print("Press a key to exit...")
	_ = input()
