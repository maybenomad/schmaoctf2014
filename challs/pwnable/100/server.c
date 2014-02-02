#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

char* one = "To pass this bridge, you must first pass the test of the riddle.\n";
char* two = "Brace yourself, fool, for this riddle comes from a mysterious, far-away land.\n";
char* three = "Yes, um... The riddle, uh... It... cometh... uh...\n";
char* four = "THE RIDDLE COMETH! Tell me, voyager. What is simple, and yet also... a riddle?\n";
char* nope = "THAT IS THE WRONG ANSWER!! The penalty is... DEATH BY SNAKES!!\n";
char* ded = "U DED! :(";

/*****
 * 
 * Challenge code goes here. 
 *
  **/
void handle(int fd)
{
  int can_has_flagz = 0;
  char attack[4096];

  send(fd, one, strlen(one), 0);
  sleep(3);
  send(fd, two, strlen(two), 0);
  sleep(3);
  send(fd, three, strlen(three), 0);
  sleep(3);
  send(fd, four, strlen(four), 0);

  recv(fd, attack, 0x1003, 0);

  if (can_has_flagz) {
    dup2(fd, 0); dup2(fd, 1); dup2(fd, 2);
    char* argv[] = {"/bin/cat", "flag", NULL};
    execve(argv[0], argv, NULL);
    exit(0);
  }

  send(fd, nope, strlen(nope), 0);
  sleep(3);
  send(fd, ded, strlen(ded), 0);
}

/*****
 *
 * Drops privileges to the specified user/group so as to keep people
 *   from rooting our challenge VMs. ;)
 *
 **/
void drop_privs(gid_t groupid, uid_t userid)
{
  if (getuid() == 0)
  {
    if (setgid(groupid) != 0)
      printf("setgid: Unable to drop group privileges: %s", strerror(errno));
    if (setuid(userid) != 0)
      printf("setuid: Unable to drop user privileges: %s", strerror(errno));
  }
}

/*****
 *
 * A simple wrapper for all of the shitty TCP socket
 *  server boilerplate. 
 *
  **/
int create_tcp_server(int port) 
{
  int fd;
  struct sockaddr_in serveraddr;

  // Spawn the TCP socket. 
  fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd < 0)
    perror("Error opening socket.");
  
  // Allow us to restart the server instantaneously, 
  //  avoiding obnoxious "address in use" errors.
  setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, 
      (const void*) 1, sizeof(int));

  // Set up our socket struct and fill it with
  //  all sorts of goodies. 
  memset((char*) &serveraddr, 0x00, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short) port);

  // Bind our new socket to the specified port. 
  if (bind(fd, (struct sockaddr*) &serveraddr, 
        sizeof(serveraddr)) < 0)
    perror("Error on binding.");

  // Prepare socket for calls to accept(). 
  listen(fd, 1024);

  return fd;
}

/*****
 *
 * A simple wrapper for all of the shitty boilerplate
 *  for accepting client connections. 
 *
  **/
int accept_tcp_connection(int server_fd) 
{
  int fd;
  socklen_t client_len;      
  struct sockaddr_in clientaddr;

  client_len = sizeof(clientaddr);
  
  // Picks the first connection off of the server's 
  //  queue, create a new socket, and return that 
  //  socket's file descriptor.
  fd = accept(server_fd, (struct sockaddr*) &clientaddr,
      &client_len);

  return fd;
}

int main(int argc, char** argv)
{
  int PORT = 31337;
  char* HOST = "0.0.0.0";

  // The process ID returned from fork(). 
  pid_t proc_id;

  // Socket file descriptors
  int server_fd, client_fd;
  
  server_fd = create_tcp_server(PORT);
  //drop_privs();

  for(;;)
  {
    client_fd = accept_tcp_connection(server_fd);

    if ((proc_id = fork()) == 0)
    {
      close(server_fd);
      handle(client_fd);
      exit(0);
    }

    close(client_fd);
  }
}