#!/usr/bin/python3

import os

def shuffle1(a1, a2):
    v3 = 2
    for _ in range(a2):
        v4 = v3
        v5 = a1
        while v5 > 0:
            if v5 < v4:
                v5, v4 = v4, v5
            v5 %= v4
        if v4 != 1:
            v3 += 1
            if v3 < a1:
                continue
    return v3

def shuffle2(a1, a2, a3):
    if a1 >= a3:
        a1 %= a3
    result = a1
    if a2 != 1:
        for _ in range(a2 - 1):
            result = a1 * result % a3
    return result

def initTable(i1=11, i2=19, i3=6):
    table = [''] * 32
    table[0] = chr(i1 + ord('0'))
    table[1] = chr(i2 + ord('0'))
    table[2] = chr(i3 + ord('0'))
    table[3] = "6"
    table[4] = "7"
    table[5] = "8"
    table[6] = "9"

    chksum = sum(ord(table[i]) for i in range(7))
    for i in range(7, 32):
        chksum = 33676 * chksum + 12345
        table[i] = chr(((chksum >> 16) & 0x7FFF) % 43 + ord('0'))

    v3 = i1 * i2
    v4 = shuffle1((i1 - 1) * (i2 - 1), i3)
    for i in range(32):
        table[i] = chr(shuffle2(ord(table[i]) - ord('0'), v4, v3))

    return table

def calculatePassword(date, table):
    date = int(date.replace("-", ""), 16)
    chksum = date
    password = ""
    for _ in range(8):
        chksum = 33676 * chksum + 12345
        index = (chksum >> 16) & 31
        pwdC = ord(table[index]) % 36
        if pwdC > 9:
            password += chr(pwdC + ord('7'))
        else:
            password += chr(pwdC + ord('0'))
    return password

if __name__ == "__main__":
    table = initTable()
    print("Master Password Generator for Asus laptops (system date version)")
    print("Copyright (C) 2016 dogbert <dogber1@gmail.com>")
    print("")
    print("When asked for a password, enter an incorrect password, then press Alt+R. A prompt with the system date will appear, e.g. 2013-12-31")
    print("")
    inDate = input("Please enter the system date: ").strip().replace('/', '-').replace('.', '-')
    password = calculatePassword(inDate, table)
    print("")
    print("The master password is: " + password)
    print("")
    print("Please note that the password is encoded for US QWERTY keyboard layouts.")
    if os.name == 'nt':
        input("Press a key to exit...")