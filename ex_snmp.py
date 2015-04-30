#!/usr/bin/env python
#This is a hack to detect if the running configuration has been changed but not saved to startup-config

from snmp_helper import snmp_get_oid, snmp_extract
import snmp_helper

def get_elements():
    ip_addr = '50.242.94.227'
    COMMUNITY_STRING = 'galileo'
    snmp_port1 = 7961
    a_device = (ip_addr, COMMUNITY_STRING, snmp_port1)
    #print a_device
    return a_device

def get_list_of_oids():
    #sysUptime
    sysUptime = '1.3.6.1.2.1.1.3.0'
    #Uptime when running config last changed
    ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
    #Uptime when running config last saved (note any 'write' constitutes a save)   
    ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
    #Uptime when startup config last saved
    ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'
    list_of_oids = (ccmHistoryRunningLastChanged, ccmHistoryRunningLastSaved, ccmHistoryStartupLastChanged)
    #print list_of_oids
    return list_of_oids

def runcommands(a_device, list_of_oids):
    #Convert the OIDs into integers and Print
    ccmHistoryRunningLastChanged, ccmHistoryRunningLastSaved, ccmHistoryStartupLastChanged = list_of_oids
    results = []
    for oid in list_of_oids:
        output = snmp_get_oid(a_device, oid=oid)
        results.append(int(snmp_extract(output)))
    output_StartupLastChanged, output_RunningLastSaved, output_RunningLastChanged = results
    #return results
    if output_StartupLastChanged == 0:
        print 'startup-config has not been saved since the last boot'
    elif output_RunningLastSaved > output_StartupLastChanged:
        print 'Running-Config has been changed but not saved to startup-config'
    else:
        print 'Running-Config has been saved to startup-config'

def main():
    a_device = get_elements()
    list_of_oids = get_list_of_oids()
    results = runcommands(a_device, list_of_oids)
    print results

if __name__ == '__main__':
    main()
