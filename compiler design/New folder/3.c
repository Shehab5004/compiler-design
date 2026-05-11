
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include<stdlib.h>
int main() {
    char input[] = "int a,b,c;";
    char type[10];
    char *token;
    printf("Symbol Table:\n");
    printf("Name | Type | Scope | Line\n");
    printf("------------------\n");
    sscanf(input, "%s", type);
    token = strtok(input + strlen(type) + 1, ",;");
    while (token != NULL) {
        while (isspace(*token)) token++; // Remove spaces
        printf("%s | %s | global | 1\n", token, type);
        token = strtok(NULL, ",;");
    }

    return 0;
}
