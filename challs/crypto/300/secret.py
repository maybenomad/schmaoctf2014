#!/usr/bin/python
import sys

def encrypt(key, msg):
	ciphertext = ""
	for i in range(len(msg)):
		ciphertext += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
	return ciphertext.encode('hex')

msg = """Dear Ghost Princess, 
Oh, my Glob, ever since Clara stopped eating meat, 
her skin looks so good! I mean, she still looks fat, but, like, 
I can't say that junk to her face.

Sincerely, 
LSP

(P.S. l4di3s_l0ve_th3_X0R)
"""

print encrypt("ecxincftw", msg)