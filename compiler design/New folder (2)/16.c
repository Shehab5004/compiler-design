#include <stdio.h>
int main() {
    char c;
    int i;
    printf("Enter 3 characters:\n");
    for(i=0;i<3;i++){
        scanf(" %c",&c);
        printf("%c ",c+1);
    }
    return 0;
}
