#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char dataset[1000];
    printf("Enter dataset (end with EOF / Ctrl+Z):\n");
    
    // Read multiline input
    int i = 0;
    char ch;
    while((ch = getchar()) != EOF && i < 999) {
        dataset[i++] = ch;
    }
    dataset[i] = '\0';

    //Record count
    int records = 0;
    for(i = 0; dataset[i]; i++) {
        if(dataset[i] == '\n') records++;
    }
    if(i > 0 && dataset[i-1] != '\n') records++; // last line without newline

    //Clean numeric field (remove leading zeros)
    char cleanNum[100] = "";
    int j = 0;
    for(i = 0; dataset[i]; i++) {
        if(isdigit(dataset[i])) {
            cleanNum[j++] = dataset[i];
        }
    }
    cleanNum[j] = '\0';
    // Remove leading zeros
    int start = 0;
    while(cleanNum[start] == '0') start++;
    char *cleaned = cleanNum + start;

    //Count vowels and consonants
    int vowels = 0, consonants = 0;
    for(i = 0; dataset[i]; i++) {
        char c = tolower(dataset[i]);
        if(isalpha(c)) {
            if(c=='a'||c=='e'||c=='i'||c=='o'||c=='u')
                vowels++;
            else
                consonants++;
        }
    }

    //Check for "N/A"
    int hasNA = strstr(dataset, "N/A") != NULL;

    //Count total spaces
    int spaces = 0;
    for(i = 0; dataset[i]; i++) {
        if(dataset[i] == ' ')
            spaces++;
    }

    //Final Output
    printf("\nRecord count: %d\n", records);
    printf("Clean number: %s\n", cleaned[0] ? cleaned : "0");
    printf("Vowels: %d , Consonants: %d\n", vowels, consonants);
    printf("Contains N/A: %s\n", hasNA ? "Yes" : "No");
    printf("Total spaces: %d\n", spaces);

    return 0;
}
