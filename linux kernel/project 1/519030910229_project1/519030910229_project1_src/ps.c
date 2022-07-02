#include <stdio.h>
#include <dirent.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SIZE 512
#define FilePath "/proc/"

int main(void)
{
    /* TODO */
    int i = 0;
	DIR *dir = NULL;  
	struct dirent *entry;
	char *name;
	bool flag = true;
	int len = 0;
	char *pros[MAX_SIZE];
	char stats[MAX_SIZE];
	char cmds[MAX_SIZE];
	char file_path[MAX_SIZE];
	char stat_path[MAX_SIZE];
	char cmd_path[MAX_SIZE];
	
	FILE *fp;
	printf("%5s S CMD\n","PID");

	if((dir = opendir(FilePath))==NULL){  
		printf("opendir failed!");  
		return -1;
	}else{
	 	while((entry=readdir(dir))){  
	 		name = entry->d_name;
	 		i = 0;
	 		flag = true;
	 		while(name[i] != '\0'){
	 			if(!isdigit(name[i++])){
	 				flag = false;
	 				break;
	 			}
	 		}
			if(flag){
				printf("%5s ",name);
				sprintf(stat_path, "/proc/%s/stat", entry->d_name);
				fp = fopen(stat_path, "r");
				if(fp == NULL){
					printf("opendir failed!");
					continue;
				}
				i = 0;
				while(fgets(stats, MAX_SIZE, fp) != NULL){ 
					while(stats[i]!=')'){
						i++;
					}
					printf("%c ", stats[i+2]); 
				}
				fclose(fp);
				
				sprintf(cmd_path, "/proc/%s/cmdline", entry->d_name);
				fp = fopen(cmd_path, "r");
				if(fp == NULL){
					printf("opendir failed!");
				}
				i=0;
				while(fgets(cmds, MAX_SIZE, fp) != NULL){
					while(cmds[i]!='\0'){
						printf("%c", cmds[i]);
						i++;
					}
				}
				if(i == 0){
					fclose(fp);
					sprintf(cmd_path, "/proc/%s/comm", entry->d_name);
					fp = fopen(cmd_path, "r");
					while(fgets(cmds, MAX_SIZE, fp) != NULL){
						int i=0;
						printf("[");
						while(cmds[i]!='\n'){
							printf("%c", cmds[i]);
							i++;
						}
						printf("]");
					}
				}
				printf("\n");
				fclose(fp);
			}
		}
	 	closedir(dir);   
    }

    return 0;
}
