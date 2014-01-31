import SocketServer
import subprocess
import random
import string

BANNER = ("""Welcome to NOTEBOX, the PREMIERE note saving service!
Use `help` to see options.\n\n""")

HELP = ("""list - list all previous notes!
new <data> - create a new note!
read <filename> - read a note (filename of format note_XXXXXXXX)\n""")

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
        self.request.send(BANNER)

        while shell:
            COMMANDS = ["read", "new", "list", "help"]

            self.request.sendall('NOTEBOX> ')
            data = self.request.recv(1024).strip().split(' ')

            cmd = data[0].strip()
            args = data[1:]

            print data[0]
            if cmd not in COMMANDS:
                self.request.send("HACKING ATTEMPT!")
                exit(0)

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
            elif cmd == "list": 
                output = shell_exec("/bin/ls notes")
                self.request.send(output)
            elif cmd == "help":
                self.request.send(HELP)


def drop_privs(gid, uid):
    if os.getuid() == 0:
        if os.setgid(gid) != 0 or os.setuid(uid) != 0:
            print "Could not drop privs"

if __name__ == '__main__':

    HOST, PORT = "0.0.0.0", 31337

    server = Server((HOST, PORT), Handler)

    # drop_privs()
    server.serve_forever()
