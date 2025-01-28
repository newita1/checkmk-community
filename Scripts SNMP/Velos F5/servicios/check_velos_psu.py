#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .agent_based_api.v1 import *
import pprint
import re

#default_threslholds_values = (100.0, 20.0)
#.1.3.6.1.4.1.12276.1.2.1.9.1.2 -> psuname [0]
#.1.3.6.1.4.1.12276.1.2.1.9.1.5 -> psucurrentin [1]
#.1.3.6.1.4.1.12276.1.2.1.9.1.6 -> psucurrentout [2]
#.1.3.6.1.4.1.12276.1.2.1.9.1.7 -> psuvoltagein [3]
#.1.3.6.1.4.1.12276.1.2.1.9.1.8 -> psuvoltageout [4]
#.1.3.6.1.4.1.12276.1.2.1.9.1.9 -> psutemperature1 [5]
#.1.3.6.1.4.1.12276.1.2.1.9.1.12 -> psufan1speed [6]
#.1.3.6.1.4.1.12276.1.2.1.9.1.14 -> psupowerin [7]
#.1.3.6.1.4.1.12276.1.2.1.9.1.15 -> psupowerout [8]


def discover_check_velos_psu(section):
    for i in section:
        yield Service(item = f"psu {str(i[0])}")

def check_check_velos_psu(item, section):
    for i in section:
        
        perfdata = [("current_in", float(i[1])),
            ("current_out", float(i[2])),
            ("voltage_in", float(i[3])),
            ("voltage_out", float(i[4])),
            ("temperature", float(i[5])),
            ("fan_speed", float(i[6])),
            ("power_in", float(i[7])),
            ("power_out", float(i[8]))]
        
        for p in perfdata:
            yield Metric(p[0], p[1])
            
        if item == f"psu {str(i[0])}":
            yield Result(state=State.OK, 
                         summary=f"PSU OK", 
                         details=f"""
                         current in: f{float(i[1])} mA\n
                         current out: f{float(i[2])} mA\n
                         voltage in: f{float(i[3])} mV\n
                         voltage out: f{float(i[4])} mV\n
                         temperature: f{float(i[5])} °C\n
                         fan speed: f{float(i[6])} RPM\n
                         power in: f{float(i[7])} mW\n
                         power out: f{float(i[8])} mW\n
                         """)
            return


register.check_plugin(
    name="check_velos_psu",
    service_name="%s",
    discovery_function = discover_check_velos_psu,
    check_function=check_check_velos_psu,
)
register.snmp_section(
    name = "check_velos_psu",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12276.1.3.1.5"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12276.1.2.1.9.1.9.1",
        oids=[
            "2",
            "5",
            "6",
            "7",
            "8",
            "9",
            "12",
            "14",
            "15",
        ],
    ),
)