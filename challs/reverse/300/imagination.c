#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void base85(char* buf, const unsigned char* data, int bytes) {
  while (bytes) {
    unsigned acc = 0;
    int cnt;
    for (cnt = 24; cnt >= 0; cnt -= 8) {
      unsigned ch = *data++;
      acc |= ch << cnt;
      if (--bytes == 0)
        break;
    }
    for (cnt = 4; cnt >= 0; cnt--) {
      int val = acc % 85;
      acc /= 85;
      buf[cnt] = (char)(val + 33);
    }
    buf += 5;
  }

  *buf = 0;
}

int test_imagination(int fd) {
  //srand(time(NULL));
  //int r = rand() % (sizeof(imagination) / sizeof(imagination[0]));

  char buf[1024]; 
  char* data = "Man is d";

  base85(&buf, data, 8);
  printf("herp");
  printf(&buf);

  return 1;
}

int main() {
	test_imagination(1);
}