from tabulate import tabulate
from prettytable import PrettyTable
import json

GREEN = '\033[32m' # Green
CYAN =  '\033[36m' # Cyan Text
RED =  '\033[31m' # Red Text
PURPLE =  '\033[35m' # Purple Text
YELLOW =  '\033[33m' # Yellow Text
BLUE =  '\033[34m' # Blue Text

ENDC = '\033[m'


class Parser:
    def __init__(self,obj):
        self.obj = obj
    
    def ParsePreChangeResults(self,response,pre_change_analysis_name,verbose_flag,table_response,early_epoch_id,later_epoch_id):
        epoch1_only_count = 0
        epoch2_only_count = 0
        both_epochs_count = 0
        epoch1_count = 0
        epoch2_count = 0
        for x in response.json()['value']['data']:
            if(x['bucket'] == "EVENT_SEVERITY_INFO"):
                print(GREEN + "----------------------------", ENDC)
                print(GREEN + "<-------- ✓ INFO ✓ -------->", ENDC)
                print(GREEN + "----------------------------", ENDC)
                if(table_response):
                    t = PrettyTable(['Epoch','Event Name','Severity','Event Category','Description'])
                    for item in table_response.json()['value']['data']:
                        for ele in item.values():
                            if(isinstance(ele,dict)):
                                if("EVENT_SEVERITY_INFO" in ele.values()):
                                    # print(ele)
                                    rows = []
                                    for v in ele.values():
                                        rows.append(v)
                                    # print(rows)
                                    t.add_row(rows)
                    t.align["Description"] = "l"
                    t.align["Epoch UUID"] = "l"
                    t.align["Event Name"] = "l"
                    print(t)
            if(x['bucket'] == "EVENT_SEVERITY_WARNING"):
                print(CYAN + "-------------------------------", ENDC)
                print(CYAN + "<-------- ! WARNING ! -------->", ENDC)
                print(CYAN + "-------------------------------", ENDC)
                if(table_response):
                    t = PrettyTable(['Epoch','Event Name','Severity','Event Category','Description'])
                    for item in table_response.json()['value']['data']:
                        for ele in item.values():
                            if(isinstance(ele,dict)):
                                if("EVENT_SEVERITY_WARNING" in ele.values()):
                                    # print(ele)
                                    rows = []
                                    for v in ele.values():
                                        rows.append(v)
                                    # print(rows)
                                    t.add_row(rows)
                    t.align["Description"] = "l"
                    t.align["Epoch UUID"] = "l"
                    t.align["Event Name"] = "l"
                    print(t)
            if(x['bucket'] == "EVENT_SEVERITY_MINOR"):
                print(YELLOW + "-------------------------------", ENDC)
                print(YELLOW + "<-------- !! MINOR !! -------->", ENDC)
                print(YELLOW + "-------------------------------", ENDC)
                if(table_response):
                    t = PrettyTable(['Epoch','Event Name','Severity','Event Category','Description'])
                    for item in table_response.json()['value']['data']:
                        for ele in item.values():
                            if(isinstance(ele,dict)):
                                if("EVENT_SEVERITY_MINOR" in ele.values()):
                                    # print(ele)
                                    rows = []
                                    for v in ele.values():
                                        rows.append(v)
                                    # print(rows)
                                    t.add_row(rows)
                    t.align["Description"] = "l"
                    t.align["Epoch UUID"] = "l"
                    t.align["Event Name"] = "l"
                    print(t)
            if(x['bucket'] == "EVENT_SEVERITY_MAJOR"):
                print(PURPLE + "-----------------------------", ENDC)
                print(PURPLE + "<-------- ⚠ MAJOR ⚠ -------->", ENDC)
                print(PURPLE + "-----------------------------", ENDC)
                if(table_response):
                    t = PrettyTable(['Epoch','Event Name','Severity','Event Category','Description'])
                    for item in table_response.json()['value']['data']:
                        for ele in item.values():
                            if(isinstance(ele,dict)):
                                if("EVENT_SEVERITY_MAJOR" in ele.values()):
                                    # print(ele)
                                    rows = []
                                    for v in ele.values():
                                        rows.append(v)
                                        # print(v)
                                        # if(v == early_epoch_id):
                                        #     continue
                                        # else:
                                    # print(rows)
                                    t.add_row(rows)
                    t.align["Description"] = "l"
                    t.align["Epoch UUID"] = "l"
                    t.align["Event Name"] = "c"
                    print(t)
            if(x['bucket'] == "EVENT_SEVERITY_CRITICAL"):
                print(RED + "-----------------------------------", ENDC)               
                print(RED + "<-------- ⓧ  CRITICAL ⓧ  -------->", ENDC)
                print(RED + "-----------------------------------", ENDC)
                if(table_response):
                    t = PrettyTable(['Epoch','Event Name','Severity','Event Category','Description'])
                    for item in table_response.json()['value']['data']:
                        for ele in item.values():
                            if(isinstance(ele,dict)):
                                if("EVENT_SEVERITY_CRITICAL" in ele.values()):
                                    # print(ele)
                                    rows = []
                                    for v in ele.values():
                                        rows.append(v)
                                    # print(rows)
                                    t.add_row(rows)
                    t.align["Description"] = "l"
                    t.align["Epoch UUID"] = "l"
                    t.align["Event Name"] = "l"
                    print(t)
            for y in (x['output']):
                if(y['bucket'] == "EPOCH1_ONLY"):
                    epoch1_only_count += y['count']
                    print("Earlier Epoch Only: " + str(y['count']))
                if(y['bucket'] == "EPOCH2_ONLY"):
                    epoch2_only_count += y['count']
                    print("Later Epoch Only: " + str(y['count']))              
                if(y['bucket'] == "BOTH_EPOCHS"):
                    both_epochs_count += y['count']
                    print("Common: " + str(y['count']))
                if(y['bucket'] == "EPOCH1"):
                    epoch1_count += y['count']
                    print("Earlier Epoch: " + str(y['count']))
                if(y['bucket'] == "EPOCH2"):
                    epoch2_count += y['count']
                    print("Later Epoch: " + str(y['count']))    
        print("====================================")
        print("Totals:")
        print("Earlier Epoch Only: " + str(epoch1_only_count))
        print("Earlier Epoch: " + str(epoch1_count))
        print("Common: " + str(both_epochs_count))
        print("Later Epoch: " + str(epoch2_count))
        if(epoch2_only_count > 0):
            print(RED + "Later Epoch Only: " + str(epoch2_only_count), ENDC)
            print(RED + "Pre-change Analyis '" + pre_change_analysis_name + "' failed.", ENDC)
            print("====================================")
            return False
        print(GREEN + "Later Epoch Only: " + str(epoch2_only_count), ENDC)
        print(GREEN + "Pre-change Analyis '" + pre_change_analysis_name + "' passed.", ENDC)
        print("====================================")
        return True   

