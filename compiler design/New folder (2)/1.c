#include <stdio.h>
int main() {
    char s[100];
    int i=0;
    printf("Enter string: ");
    gets(s);
    while(s[i]!='\0') i++;
    printf("Length = %d", i);
    return 0;
}
