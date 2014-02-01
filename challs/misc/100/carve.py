import struct
import binascii

with open('original_qr.png') as f:
	data = f.read()

data = data.split('IEND')

fake_chunk_data = "require 'socket'; s = TCPSocket.new 'localhost', 31337; s.write('IAMLEET.'); data = s.read(4); while data do $stdout.write data; data = s.read(4) end; s.close"
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
