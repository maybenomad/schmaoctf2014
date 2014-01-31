import SocketServer
import subprocess
import random
import string

def random_string():
    return ''.join(random.sample(string.hexdigits, 8))

def run_command(cmd):
    print cmd
    return subprocess.check_output(cmd, shell=True)

class Server(SocketServer.ForkingMixIn, 
        SocketServer.TCPServer): 
    allow_reuse_address = True
    request_queue_size = 1024

class Handler(SocketServer.BaseRequestHandler):

    def handle(self):
        shell = True
        while shell:
            COMMANDS = ["read", "write", "list", "help"]

            self.request.sendall('$ ')
            data = self.request.recv(1024).split(' ')

            cmd = data[0].strip()
            args = map(lambda x: x.strip(), data[1:])

            print data[0]
            if cmd not in COMMANDS:
                self.request.send("HACKING ATTEMPT!")
                exit(0)

            if cmd == "read":
                if len(args) != 1:
                    self.request.send("You must provide a valid filename!\n")
                    continue
                args[0] = args[0].strip()
                if len(args[0]) != 16:
                    self.request.send("You must provide a valid filename!\n")
                    continue
                filename = "messages/" + args[0]
                self.request.send(run_command("/bin/cat %s" % filename))
            elif cmd == "write":
                msg = ' '.join(args)
                filename = "messages/%s%s" % ("message_", random_string())
                self.request.send(run_command("/bin/echo \"%s\" > %s" % (msg, filename)))
                self.request.send("Message written to %s!\n" % filename)
            elif cmd == "list": 
                self.request.send(run_command("/bin/ls messages"))
            elif cmd == "help":
                self.request.send("""
                list - list all previously deposited messages!\n
                write <data> - create a new message!\n
                read <filename> - read a message (filename of format message_XXXXXXXX)!\n""")

def drop_privs(gid, uid):
    if os.getuid() == 0:
        if os.setgid(gid) != 0 or os.setuid(uid) != 0:
            print "Could not drop privs"

if __name__ == '__main__':

    HOST, PORT = "0.0.0.0", 31337

    server = Server((HOST, PORT), Handler)

    #drop_privs()
    server.serve_forever()
