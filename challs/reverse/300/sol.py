import socket

def decode(string): 
  ret = ""
  for i in range(len(string)):
    ret += chr(ord(string[i]) + 10)
  return ret

def undestroy(arr):
  bits = len(arr)
  buf = list(arr)
  for i in reversed(range(bits)):
    for j in reversed(range(i)):
      for k in reversed(range(j)):
        buf[k] -= ~(buf[j] ^ buf[i])
      buf[j] ^= ~buf[i]
    buf[i] ^= (i << 4) + bits;
  return buf


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 31337))

s.send('rainydaydaydream\n')

for i in range(85):
  data = s.recv(2048)
  arr = data.split('__')[:-1]
  for i in range(len(arr)):
    arr[i] = int(decode(arr[i]))
  arr = undestroy(arr)
  creature = ''.join(chr(x) for x in arr)
  print creature
  s.send(creature + '\n')

print s.recv(1024)

