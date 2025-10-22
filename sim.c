#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>

/*
Ansi escape codes:
\033                    is the escape code

ESCc                    clear the screen
ESC[{line};{column}H    move to line column

ESC[38;5;{ID}m          Set foreground color
ESC[48;5;{ID}m          Set background color

ESC[#A                  moves up # lines
ESC[#D                  moves down # lines
ESC[#C                  moves right # lines
ESC[#B                  moves left # lines

ESC[0k                  Erase from cursor to end of line
ESC[1k                  Erase from start of line to cursor
ESC[2k                  Erase entire line

*/

#define WALL_COLOR 0
#define EMPTY_COLOR 231
#define SMOKE_COLOR(smoke_index) (255 - (((smoke_index) < 13)? (smoke_index) : 13))
#define PERSON_COLOR 136 
#define FIRE_COLOR 9
#define EXIT_COLOR 5
#define PATH_COLOR 1
// 229

const int SIZEX = 42, SIZEY = 20;

uint8_t map[SIZEY][SIZEX];

const uint8_t colours[] = { EMPTY_COLOR, WALL_COLOR, PERSON_COLOR, FIRE_COLOR, EXIT_COLOR, PATH_COLOR };
// Can add symbols array if needed

void printmaze() {
    printf("\033c");
    printf("\t\tFloor 1\t\t\t\t\t\t\tFloor 2\n");
    for (int i=0; i < SIZEY; i++) {
        for (int j=0; j < SIZEX; j++) {
            if (map[i][j] < 6) printf("\033[48;5;%dm%s\033[0m", colours[map[i][j]], "  ");
            else {
                if (map[i][j] < 20)
                    printf("\033[48;5;%dm%s\033[0m", SMOKE_COLOR(map[i][j] - 6), "  ");
                else 
                    printf("\033[48;5;%dm%s\033[0m", PATH_COLOR, "  ");
            }
        }
        printf("\n");
    }
}

void updateMap(char *filename) {
    FILE *fp = fopen(filename, "r");

    flock(fileno(fp), LOCK_EX);
    int inp; int i = 0, j = 0;
    char hex[13] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'};
    while ((inp = fgetc(fp)) != EOF) {
        if (j >= SIZEX) {
            i ++;
            j = 0;
        } if (i >= SIZEY) break;
        switch(inp) {
        case ' ':
            map[i][j ++] = 0;
            break;
        case '#':
            map[i][j ++] = 1;
            break;
        case 'P':
            map[i][j ++] = 2;
            break;
        case 'F':
            map[i][j ++] = 3;
            break;
        case 'E':
            map[i][j ++] = 4;
            break;
        case '+':
            map[i][j ++] = 5;
            break;
        case '\n':
            i ++;
            j = 0;
            break;
        default:
            for (int k = 0; k < 13; k ++) {
                if (inp == hex[k]) {
                    map[i][j ++] = k+6;
                    break;
                }
            }
            break;
        }
    }

    flock(fileno(fp), LOCK_UN);
    fclose(fp);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    
    while (1) {
        updateMap(argv[1]);
        printmaze();
        usleep(100);
    }

    return 0;
}