#include <stdio.h>
#include <string.h>
int main() {
    char s[200];
    int count=0;
    char *t;
    printf("Enter string: ");
    gets(s);
    t=strtok(s," ");
    while(t){
        if(strcmp(t,"a")==0||strcmp(t,"an")==0||strcmp(t,"the")==0)
            count++;
        t=strtok(NULL," ");
    }
    printf("Articles = %d",count);
    return 0;
}
