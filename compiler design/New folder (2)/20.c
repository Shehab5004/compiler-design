#include <stdio.h>
#include <string.h>

int is_ab_star(char s[]) {
    int i=0;
    while(s[i]) {
        if(s[i]=='a' && s[i+1]=='b')
            i+=2;
        else
            return 0;
    }
    return 1;
}

int is_ab_star_only(char s[]) {
    if(s[0]!='a') return 0;
    for(int i=1;s[i];i++)
        if(s[i]!='b') return 0;
    return 1;
}

int is_ab_plus(char s[]) {
    if(s[0]!='a' || s[1]!='b') return 0;
    for(int i=1;s[i];i++)
        if(s[i]!='b') return 0;
    return 1;
}

int is_a_middle_a(char s[]) {
    int n=strlen(s);
    if(s[0]!='a' || s[n-1]!='a') return 0;
    for(int i=1;i<n-1;i++)
        if(s[i]!='a' && s[i]!='b') return 0;
    return 1;
}

int main() {
    char s[100];
    int ch;

    printf("Enter string: ");
    gets(s);

    printf("\n1. (ab)*\n");
    printf("2. ab*\n");
    printf("3. ab+\n");
    printf("4. a(a|b)*a\n");
    printf("Enter choice: ");
    scanf("%d",&ch);

    if(ch==1 && is_ab_star(s))
        printf("Valid for (ab)*");
    else if(ch==2 && is_ab_star_only(s))
        printf("Valid for ab*");
    else if(ch==3 && is_ab_plus(s))
        printf("Valid for ab+");
    else if(ch==4 && is_a_middle_a(s))
        printf("Valid for a(a|b)*a");
    else
        printf("Invalid string");

    return 0;
}
