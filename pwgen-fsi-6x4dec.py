#!/usr/bin/python

import os

# someone smacked his head onto the keyboard
XORkey = "<7#&9?>s"

def codeToBytes(code):
	numbers = (int(code[0:5]), int(code[5:10]), int(code[10:15]), int(code[15:20]))
	bytes = []
	for i in numbers:
		bytes.append(i % 256)
		bytes.append(i / 256)
	return bytes 

def byteToChar(byte):
	if byte > 9:
		return chr(ord('a') + byte - 10)
	else:
		return chr(ord('0') + byte)

def decryptCode(bytes):
	# swap two bytes
	#bytes[2], bytes[6] = bytes[6], bytes[2]
	#bytes[3], bytes[7] = bytes[7], bytes[3]

	# interleave the nibbles 
	bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7] = ((bytes[3] & 0xF0) | (bytes[0]  & 0x0F), (bytes[2] & 0xF0) | (bytes[1] & 0x0F), (bytes[5] & 0xF0) | (bytes[6] & 0x0F), (bytes[4] & 0xF0) | (bytes[7] & 0x0F), (bytes[7] & 0xF0) | (bytes[4] & 0x0F), (bytes[6] & 0xF0) | (bytes[5] & 0x0F), (bytes[1] & 0xF0)  | (bytes[2] & 0x0F), (bytes[0] & 0xF0) | (bytes[3] & 0x0F))

	# apply XOR key
	for i in range(len(bytes)):
		bytes[i] = bytes[i] ^ ord(XORkey[i])

	# final rotations
	bytes[0] = ((bytes[0] << 1) & 0xFF) | (bytes[0] >> 7)
	bytes[1] = ((bytes[1] << 7) & 0xFF) | (bytes[1] >> 1)
	bytes[2] = ((bytes[2] << 2) & 0xFF) | (bytes[2] >> 6)
	bytes[3] = ((bytes[3] << 8) & 0xFF) | (bytes[3] >> 0)
	bytes[4] = ((bytes[4] << 3) & 0xFF) | (bytes[4] >> 5)
	bytes[5] = ((bytes[5] << 6) & 0xFF) | (bytes[5] >> 2)
	bytes[6] = ((bytes[6] << 4) & 0xFF) | (bytes[6] >> 4)
	bytes[7] = ((bytes[7] << 5) & 0xFF) | (bytes[7] >> 3)

	# len(solution space) = 10+26
	bytes = [x % 36 for x in bytes]

	masterPwd = ""
	for x in bytes:
		masterPwd += byteToChar(x)
	return masterPwd

print("Master Password Generator for FSI laptops (6x4 digits version)")
print("Copyright (C) 2013 dogbert <dogber1@gmail.com>")
print("")
print("When asked for a password, enter these:")
print("First password:  3hqgo3")
print("Second password: jqw534")
print("Third password:  0qww294e")
print("")
print("You will receive a hash code with five blocks, each with four numbers, ")
print("e.g. 1234-4321-1234-4321-1234")
print("")
print("Please enter the hash: ")
inHash = input().strip().replace('-', '').replace(' ', '')
inHash = inHash[4:]
password = decryptCode(codeToBytes(inHash))
print("")
print("The master password is: " + password)
print("")
print("Please note that the password is encoded for US QWERTY keyboard layouts.")
if (os.name == 'nt'):
	print("Press a key to exit...")
	input()

