#include <stdio.h>
#include <ctype.h>

int main() {
    char str[1000];
    int i = 0;

    printf("Enter a string to tokenize: ");
    fgets(str, sizeof(str), stdin);

    printf("Tokens:\n");

    while (str[i] != '\0') {
        if (isspace(str[i])) { 
            i++; 
            continue; 
        }
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