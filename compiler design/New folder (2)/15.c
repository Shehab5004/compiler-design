#include <stdio.h>
int main() {
    char s[100];
    int i,c=0;
    printf("Enter string: ");
    gets(s);
    for(i=0;s[i]!='\0';i++)
        if(s[i]!=' ') c++;
    printf("Characters=%d",c);
    return 0;
}
