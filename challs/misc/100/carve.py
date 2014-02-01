import struct
import binascii

with open('original_qr.png') as f:
	data = f.read()

data = data.split('IEND')

fake_chunk_data = "import socket;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect(('localhost', 31337));s.send('RDY.');print s.recv(4096);s.close()"
fake_chunk_header = "eCXI"
fake_chunk_len = struct.pack('<I', len(fake_chunk_data))
fake_chunk_crc = struct.pack('<I', binascii.crc32(fake_chunk_data))

new_file = data[0]
new_file += fake_chunk_header
new_file += fake_chunk_len
new_file += fake_chunk_data
new_file += fake_chunk_crc
new_file += "IEND"
new_file += data[1]

print new_file
