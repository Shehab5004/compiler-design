#include <stdio.h>
int main() {
    char s[100];
    int i;
    gets(s);
    printf("%c",s[0]);
    for(i=1;s[i]!='\0';i++)
        if(s[i]==' ')
            printf("%c",s[i+1]);
    return 0;
}
