#include <stdio.h>

int main() {
    char str[1000]; 
    int quote = 0, paren = 0;

    printf("Enter a string of code: ");
    fgets(str, sizeof(str), stdin); 

    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == '"') quote ^= 1; 
        if (str[i] == '(') paren++;     
        if (str[i] == ')') paren--;    
    }

    if (quote == 1)
        printf("ERROR: Unclosed string literal\n");
    else if (paren != 0)
        printf("ERROR: Mismatched parentheses\n");
    else
        printf("No syntax errors\n");

    return 0;
}