#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include<stdlib.h>
int main() {
    char str[] = "while(i<10){i++;}";
    int i = 0;
    printf("Tokens:\n");
    while (str[i] != '\0') {
        if (isspace(str[i])) { i++; continue; }
        if (isalpha(str[i])) {
            while (isalnum(str[i])) {
                printf("%c", str[i]);
                i++;
            }
            printf("\n");
        }
        else if (isdigit(str[i])) {
            while (isdigit(str[i])) {
                printf("%c", str[i]);
                i++;
            }
            printf("\n");
        }
        else {
            printf("%c\n", str[i]);
            i++;
        }
    }
    return 0;
}