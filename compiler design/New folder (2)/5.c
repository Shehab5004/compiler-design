#include <stdio.h>
#include <string.h>
int main() {
    char s[100];
    char *t;
    printf("Enter string: ");
    gets(s);
    t=strtok(s," ");
    while(t){
        printf("%s\n",t);
        t=strtok(NULL," ");
    }
    return 0;
}
