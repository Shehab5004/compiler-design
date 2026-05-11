#include <stdio.h>
#include <string.h>

int main() {
    char str[200];
    char temp[200];
    char *word1, *word2;
    int count, max = 0;

    printf("Enter a string:\n");
    gets(str);

    strcpy(temp, str);   // copy original string

    word1 = strtok(str, " ");
    while (word1 != NULL) {
        count = 1;

        word2 = strtok(temp, " ");
        while (word2 != NULL) {
            if (strcmp(word1, word2) == 0)
                count++;
            word2 = strtok(NULL, " ");
        }

        if (count > max)
            max = count;

        strcpy(temp, str);   // reset temp string
        word1 = strtok(NULL, " ");
    }

    printf("Maximum frequency = %d\n", max);

    return 0;
}
