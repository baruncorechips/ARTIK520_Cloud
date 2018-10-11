#/****************************************************************************
#*
#* Copyright 2018 Barun Corechips All Rights Reserved.
#*
#* Filename: GetAction.py
#* Author: sj.yang
#* Release date: 2018/10/11
#* Version: 2.2
#*
#****************************************************************************/

import artikcloud
from artikcloud.rest import ApiException
import sys, getopt
import time, json
from pprint import pprint

# For LED
LED_1 = 121
LED_2 = 122
path_export = '/sys/class/gpio/export'
path_unexport = '/sys/class/gpio/unexport'
led_1_path_dir = '/sys/class/gpio/gpio%d/direction' % LED_1 
led_1_path_val = '/sys/class/gpio/gpio%d/value' % LED_1 

led_2_path_dir = '/sys/class/gpio/gpio%d/direction' % LED_2
led_2_path_val = '/sys/class/gpio/gpio%d/value' % LED_2


def main(argv):
        DEFAULT_CONFIG_PATH = 'config.json'

        with open(DEFAULT_CONFIG_PATH, 'r') as config_file:
                config = json.load(config_file)

        artikcloud.configuration = artikcloud.Configuration();
        artikcloud.configuration.access_token = config['device_token']

        # create an instance of the API class
        api_instance = artikcloud.MessagesApi()
        count = 1
        start_date = int(time.time()*1000) - 86400000   # 24 hours ago
        end_date = int(time.time()*1000)                # current
        order = 'desc'

        try:
                # Get Normalized Actions
                api_response = api_instance.get_normalized_actions(count=count, end_date = end_date, start_date = start_date, order = order)
                actionName = api_response.data[0].data.actions[0].name;
                if actionName == "LED1":
                        pinVAL = open(led_1_path_val, "wb", 0)
                        pinVAL.write(str(1))
                        pinVAL.close()
                        pinVAL = open(led_2_path_val, "wb", 0)
                        pinVAL.write(str(0))
                        pinVAL.close()

                        print('[RECEIVED] LED 1 On')
                else:
                        pinVAL = open(led_2_path_val, "wb", 0)
                        pinVAL.write(str(1))
                        pinVAL.close()
                        pinVAL = open(led_1_path_val, "wb", 0)
                        pinVAL.write(str(0))
                        pinVAL.close()

                        print('[RECEIVED]  LED 2 ON')

        except ApiException as e:
                print("Exception when calling MessagesApi->get_normalized_actions: %s\n" % e)


if __name__ == "__main__":
        # export
        pinCTL = open(path_export, "wb", 0)
        try:
                pinCTL.write(str(LED_1))
                print "Exported pin", str(LED_1)
                pinCTL.write(str(LED_2))
                print "Exported pin", str(LED_2)
        except:
                print "Pin ", str(LED_1), "has been exported"
                print "Pin ", str(LED_2), "has been exported"
        pinCTL.close()

        # direction
        pinDIRr = open(led_1_path_dir, "wb", 0)
        try:
                pinDIRr.write("out")
                print "Set pin ", str(LED_1), "as digital output"
        except:
                print "Failed to set pin direction"
        pinDIRr.close()

        # direction
        pinDIRg = open(led_2_path_dir, "wb", 0)
        try:
                pinDIRg.write("out")
                print "Set pin ", str(LED_2), "as digital output"
        except:
                print "Failed to set pin direction"
        pinDIRg.close()

        # value & unexport
        while True:
                main(sys.argv[1:])
                time.sleep(5)