#include <stdio.h>
#include <string.h>
int main() {
    char s[200],w[50],mw[50];
    int max=0;
    printf("Enter string: ");
    gets(s);
    char temp[200];
    strcpy(temp,s);
    char *t1=strtok(s," ");
    while(t1){
        int c=0;
        char *t2=strtok(temp," ");
        while(t2){
            if(strcmp(t1,t2)==0) c++;
            t2=strtok(NULL," ");
        }
        if(c>max){
            max=c;
            strcpy(mw,t1);
        }
        strcpy(temp,s);
        t1=strtok(NULL," ");
    }
    printf("Word=%s Frequency=%d",mw,max);
    return 0;
}
