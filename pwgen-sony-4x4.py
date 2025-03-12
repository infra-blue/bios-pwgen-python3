#!/usr/bin/python3

import os
import struct

otpChars = "9DPK7V2F3RT6HX8J"
pwdChars = "47592836"

def decodeHash(hashCode):
    s = b""
    for c in range(len(hashCode) // 2):
        s = bytes([otpChars.find(hashCode[2 * c]) * 16 + otpChars.find(hashCode[2 * c + 1])]) + s
    return s.rjust(8, b'\x00')

def encodePassword(d):
    n = struct.unpack("<I", d[0:4])[0]
    p = ""
    for i in range(8):
        p += pwdChars[(n >> (21 - i * 3)) & 0x7]
    return p

def extEuclideanAlg(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = extEuclideanAlg(b, a % b)
    return y, x - y * (a // b), gcd

def modInvEuclid(a, m):
    x, y, gcd = extEuclideanAlg(a, m)
    if gcd == 1:
        return x % m
    else:
        return None

def modular_pow(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if (exponent & 1) == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def rsaDecrypt(inB):
    c = struct.unpack("<Q", inB)[0]

    p = 2795287379
    q = 3544934711
    n = p * q
    e = 41
    phi = (p - 1) * (q - 1)
    d = modInvEuclid(e, phi)

    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modInvEuclid(q, p)

    m1 = modular_pow(c, dp, p)
    m2 = modular_pow(c, dq, q)
    if m1 < m2:
        h = (qinv * (m1 - m2 + p)) % p
    else:
        h = (qinv * (m1 - m2)) % p
    m = (m2 + h * q)
    return struct.pack("<Q", m)

def getMasterPwd(hashCode):
    a = decodeHash(hashCode)
    d = rsaDecrypt(a)
    return encodePassword(d)

print("Master Password Generator for Sony laptops (16 characters otp)")
print("Copyright (C) 2009-2010 dogbert <dogber1@gmail.com>")
print("")
print("After entering the wrong password for the third time, you will receive a")
print("hexadecimal code from which the password can be calculated,")
print("e.g. 73KR-3FP9-PVKH-K29R")
print("")
print("Please enter the code: ")
code = input().replace("-", "").replace(" ", "").upper()
password = getMasterPwd(code)
print("The password is: " + password)

if os.name == 'nt':
    print("Press a key to exit...")
    input()
