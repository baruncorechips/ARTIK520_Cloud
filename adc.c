/****************************************************************************
*
* Copyright 2018 Barun Corechips All Rights Reserved.
*
* Filename: adc.c
* Author: sj.yang
* Release date: 2018/10/11 
* Version: 1.1
*
****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#define ANALOG_PIN 0	// A0

int analogRead(int pin)
{
	FILE * fd;
	char fName[64];
	char val[8];
	
	// open value file
	sprintf(fName, "/sys/devices/126c0000.adc/iio:device0/in_voltage%d_raw", pin);
	fd = fopen(fName, "r");
	if (!fd)
	{
		printf("Error: can't open analog voltage value\n");
		return 0;
	}
	
	fgets(val, 8, fd);
	fclose(fd);
	return atoi(val);
}

int main(void)
{
	long SenVal = 0;
	while(1) {
		SenVal = analogRead(ANALOG_PIN);
		printf("val: %d\n", SenVal);
                   FILE *fp = fopen("send_data.txt","w");
		fprintf(fp, "%d",SenVal);
		fclose(fp);
		sleep(5);
	}
}