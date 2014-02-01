#!/usr/bin/python
import sys

def encrypt(key, msg):
	ciphertext = ""
	for i in range(len(msg)):
		ciphertext += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
	return ciphertext.encode('hex')

if len(sys.argv) != 3:
	print("Wrong args!")
	exit(0)


msg = """Dear Princess, 
This message is completely stupid and unimportant, I hope you
didn't go through too much trouble decrypting it... just wanted to 
say "sup?" and stuff. Anyways, peace out! 

Sincerely, 
Other Princess

(P.S. l4di3s_l0ve_w0rd_l1sts)
"""

print(encrypt("snickers", msg))
print(encrypt(sys.argv[1], sys.argv[2]))