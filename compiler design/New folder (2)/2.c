#include <stdio.h>
int main() {
    char s[100];
    int i,count=0;
    printf("Enter string: ");
    gets(s);
    for(i=0;s[i]!='\0';i++)
        if(s[i]==' ') count++;
    printf("White spaces = %d", count);
    return 0;
}
