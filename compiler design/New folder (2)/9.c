#include <stdio.h>
int main() {
    char s[200];
    int i=0;
    printf("Enter line: ");
    gets(s);
    if(s[i]=='/'&&s[i+1]=='/')
        return 0;
    if(s[i]=='/'&&s[i+1]=='*'){
        i+=2;
        while(!(s[i]=='*'&&s[i+1]=='/')) i++;
        i+=2;
    }
    printf("%s",&s[i]);
    return 0;
}
