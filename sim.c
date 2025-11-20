#include <stdio.h>
#include <stdlib.h>
//#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <CommonCrypto/CommonDigest.h>

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
#define EXIT_COLOR 34
#define PATH_COLOR 1
#define OBJECT_COLOR 19
#define STAIR_COLOR 129
#define DOOR_COLOR 239
#define FIRE_DOOR_COLOR 51
// 229

int SIZEX = 0, SIZEY = 0;

char *floors;
uint8_t **map;

#define numColours 10
const uint8_t colours[numColours] = { EMPTY_COLOR, WALL_COLOR, PERSON_COLOR, FIRE_COLOR, EXIT_COLOR, PATH_COLOR, OBJECT_COLOR, STAIR_COLOR, DOOR_COLOR, FIRE_DOOR_COLOR };
// Can add symbols array if needed

char *buffer;

// SHA256 hash function for file contents
void hashFile(char *filename, unsigned char *hash_out) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        memset(hash_out, 0, CC_SHA256_DIGEST_LENGTH);
        return;
    }
    
    flock(fileno(fp), LOCK_SH);
    
    // Get file size
    fseek(fp, 0, SEEK_END);
    long file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    
    // Read entire file
    unsigned char *file_contents = malloc(file_size);
    fread(file_contents, 1, file_size, fp);
    
    // Hash it all at once
    CC_SHA256(file_contents, (CC_LONG)file_size, hash_out);
    
    free(file_contents);
    flock(fileno(fp), LOCK_UN);
    fclose(fp);
}

void printmaze() {
    // printf("\033c");
    int index = 0;
    index += sprintf(buffer, "%s\n", floors);
    for (int i=0; i < SIZEY; i++) {
        for (int j=0; j < SIZEX; j++) {
            if (map[i][j] < numColours) index += sprintf(buffer + index, "\033[48;5;%dm%s\033[0m", colours[map[i][j]], "  ");
            else {
                if (map[i][j] < 14 + numColours)
                    index += sprintf(buffer + index, "\033[48;5;%dm%s\033[0m", SMOKE_COLOR(map[i][j] - numColours), "  ");
                else 
                    index += sprintf(buffer + index, "\033[48;5;%dm%s\033[0m", PATH_COLOR, "  ");
            }
        }
        index += sprintf(buffer + index, "\n");
    }
    buffer[index] = 0;
    printf("\033c%s\n", buffer);
}

void updateMap(char *filename) {
    FILE *fp = fopen(filename, "r+");
    flock(fileno(fp), LOCK_EX);
    flock(fileno(fp), LOCK_UN);
    fclose(fp);
    fp = fopen(filename, "r");
    // flock(fileno(fp), LOCK_EX);

    int tmpX, tmpY;
    fscanf(fp, "%d %d\n", &tmpX, &tmpY);

    if (tmpX > 10000 || tmpY > 10000)
        return;

    if (tmpX != SIZEX || tmpY != SIZEY) {
        if (SIZEX != 0 && SIZEY != 0) {
            for (int i = 0; i < SIZEY; i ++) free(map[i]);
            free(map);
            free(floors);
            free(buffer);
        }
        SIZEX = tmpX;
        SIZEY = tmpY;
        map = malloc(SIZEY * sizeof(uint8_t *));
        for (int i = 0; i < SIZEY; i ++) map[i] = calloc(SIZEX, sizeof(uint8_t));

        floors = calloc(SIZEX, sizeof(char));
        buffer = calloc((SIZEX) * (SIZEY) * 25, sizeof(char));
    }
    int in, iter = 0;
    while ((in = fgetc(fp)) != EOF) {
        if (iter >= SIZEX - 1 || (in == '\n' && iter != 0)) break;
        else if (in == '\n') continue;
        floors[iter ++] = in;
    }
    floors[iter] = 0;

    int inp; int i = 0, j = 0;
    char hex[13] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'};
    while ((inp = fgetc(fp)) != EOF) {
        if (j >= SIZEX) {
            i ++;
            j = 0;
            while (inp != '\n' && inp != EOF) inp = fgetc(fp);
            continue;
        } if (i >= SIZEY) break;
        switch(inp) {
        case ' ':
            map[i][j ++] = 0;
            break;
        case '#':
            map[i][j ++] = 1;
            break;
        case '|':
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
        case 'O':
            map[i][j ++] = 6;
            break;
        case 'S':
            map[i][j ++] = 7;
            break;
        case 'd':
            map[i][j ++] = 8;
            break;
        case 'D':
            map[i][j ++] = 9;
            break;
        case '\n':
            i ++;
            j = 0;
            break;
        default:
            for (int k = 0; k < 13; k ++) {
                if (inp == hex[k]) {
                    map[i][j ++] = k+numColours;
                    break;
                }
            }
            break;
        }
    }

    // flock(fileno(fp), LOCK_UN);
    fclose(fp);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;

    FILE *fp = fopen(argv[1], "r");

    flock(fileno(fp), LOCK_EX);

    sleep(1);

    flock(fileno(fp), LOCK_UN);
    fclose(fp);
    
    unsigned char prevHash[CC_SHA256_DIGEST_LENGTH];
    unsigned char currentHash[CC_SHA256_DIGEST_LENGTH];
    memset(prevHash, 0, CC_SHA256_DIGEST_LENGTH);
    
    while (1) {
        hashFile(argv[1], currentHash);
        
        if (memcmp(currentHash, prevHash, CC_SHA256_DIGEST_LENGTH) != 0) {
            updateMap(argv[1]);
            printmaze();
            memcpy(prevHash, currentHash, CC_SHA256_DIGEST_LENGTH);
        }
        
        usleep(100); // 100 microseconds sleep
    }

    return 0;
}