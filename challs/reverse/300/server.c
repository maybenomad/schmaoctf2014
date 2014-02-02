#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include "creatures.h"


void scr4mble(int buf[], char* data, int bytes) {
  for (int i = 0; i < bytes; i++) 
  {
    buf[i] = data[i];
    buf[i] ^= (i << 4) + bytes;
    for (int j = 0; j < i; j++) {
      buf[j] ^= ~buf[i];
      for (int k = 0; k < j; k++) {
        buf[k] += ~(buf[j] ^ buf[i]);
      }
    }
  }
}

void enc0de(char buf[], int bytes) {
  for (int i = 0; i < bytes; i++)
    buf[i] = (char) (buf[i] - 10);
  buf[bytes] = '_';
  buf[bytes+1] = '_';
  buf[bytes+2] = 0;
}

int test_imagination(int fd) {
  int encoded[128];
  char recvbuf[256];

  int r = rand() % 2789;

  scr4mble(&encoded, creatures[r], strlen(creatures[r]));

  char sendbuf[1024];
  memset(sendbuf, 0, 1024);

  char tempbuf[16];
  for (int i = 0; i < strlen(creatures[r]); i++) {
    sprintf(tempbuf, "%d", encoded[i]);
    enc0de(tempbuf, strlen(tempbuf));
    strcat(sendbuf, tempbuf);
  }

  send(fd, sendbuf, strlen(sendbuf), 0);

  int bytes = recv(fd, recvbuf, 256, 0);
  recvbuf[bytes] = 0;
  *(strchr((char*) recvbuf, '\n')) = 0;

  return !strcmp((char*) recvbuf, creatures[r]);
}

int login(int fd) {
  char input[64];
  int bytes = recv(fd, (char*) &input, 63, 0);
  input[bytes] = 0;
  printf(&input);
  *(strchr((char*) &input, '\n')) = 0;
  return !strcmp((char*) &input, "rainydaydaydream");
}

// Encodings:
// Base64
// Hex
// 
void handle(int fd)
{
  if (!login(fd)) {
    exit(0);
  }
  
  srand(time(NULL));
  for (int i = 0; i < 85; i++) {
    printf("%d\n", i);
    if (!test_imagination(fd)) {
      exit(0);
    }
    sleep(.1);
  }

  char flag[48];
  FILE* f;
  f = fopen("flag", "r");
  fgets(flag, 48, f);
  fclose(f);
  send(fd, flag, strlen(flag), 0);
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
