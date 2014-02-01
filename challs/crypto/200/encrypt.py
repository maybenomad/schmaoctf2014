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
	
print(encrypt(sys.argv[1], sys.argv[2]))