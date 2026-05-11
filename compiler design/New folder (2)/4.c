#include <stdio.h>
#include <ctype.h>
int main() {
    char s[100];
    int v=0,c=0,d=0,i;
    printf("Enter string: ");
    gets(s);
    for(i=0;s[i]!='\0';i++){
        if(isdigit(s[i])) d++;
        else if(isalpha(s[i])){
            char ch=tolower(s[i]);
            if(ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u') v++;
            else c++;
        }
    }
    printf("Vowel=%d Consonant=%d Digit=%d",v,c,d);
    return 0;
}
