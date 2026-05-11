#include <stdio.h>
int main() {
    char ch;
    int lines=0;
    printf("Enter text (Ctrl+Z to stop):\n");
    while((ch=getchar())!=EOF)
        if(ch=='\n') lines++;
    printf("Lines = %d", lines);
    return 0;
}
