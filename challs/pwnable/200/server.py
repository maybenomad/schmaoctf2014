import SocketServer
import subprocess
import random
import string
import os

def random_string():
    return ''.join(random.sample(string.hexdigits, 8))

def shell_exec(cmd):
    return subprocess.check_output(cmd, shell=True)

class Server(SocketServer.ForkingMixIn, 
        SocketServer.TCPServer): 
    allow_reuse_address = True
    request_queue_size = 1024

class Handler(SocketServer.BaseRequestHandler):

    def handle(self):
        shell = True
        files = []

        while shell:
            COMMANDS = ["read", "new", "list"]

            self.request.sendall('\n%')
            data = self.request.recv(1024).strip().split(' ')

            cmd = data[0].strip()
            args = data[1:]

            if cmd not in COMMANDS:
                self.request.send("KEEP OUT!")
                break

            if cmd == "read":
                if len(args) != 1 or len(args[0]) != 13:
                    self.request.send("You must provide a valid filename!\n")
                    continue
                filename = "notes/" + args[0]
                output = shell_exec("/bin/cat %s" % filename)
                self.request.send(output)
            elif cmd == "new":
                msg = ' '.join(args)
                filename = "notes/note_" + random_string()
                output = shell_exec("/bin/echo \"%s\" > %s" % (msg, filename))
                self.request.send(output)
                self.request.send("Note written to %s!\n" % filename)
                files.append(filename)
            elif cmd == "list": 
                output = shell_exec("/bin/ls notes")
                self.request.send(output)

        for f in files:
            os.remove(f)



def drop_privs(gid, uid):
    if os.getuid() == 0:
        if os.setgid(gid) != 0 or os.setuid(uid) != 0:
            print "Could not drop privs"

if __name__ == '__main__':

    HOST, PORT = "0.0.0.0", 31337

    server = Server((HOST, PORT), Handler)

    # drop_privs()
    server.serve_forever()
