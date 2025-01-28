#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .agent_based_api.v1 import *
import pprint
import re

#default_threslholds_values = (100.0, 20.0)
#.1.3.6.1.4.1.12276.1.2.1.4.1.1.2 -> memavailable
#.1.3.6.1.4.1.12276.1.2.1.4.1.1.3 -> memfree
#.1.3.6.1.4.1.12276.1.2.1.4.1.1.4-> percentageused
#.1.3.6.1.4.1.12276.1.2.1.4.1.1.5  -> memplatformTotal
#.1.3.6.1.4.1.12276.1.2.1.4.1.1.6 -> mem Platform used

def discover_check_velos_mem(section):
    yield Service()

def check_check_velos_mem(params, section):

    warning = int(params["memory_thresholds"][0])
    critical = int(params["memory_thresholds"][1])
    
    for i in section:
        
        perfdata = [("memavailable", float(i[0])),
                    ("memfree", float(i[1])),
                    ("memplatformtotal", float(i[3])),
                    ("memplatformused", float(i[4]))]
        
        for p in perfdata:
            yield Metric(p[0], p[1])
            yield Metric("percentageused", float(i[2]), levels=(warning, critical))
        if float(i[2]) >= critical:
            yield Result(state=State.CRIT, summary=f"Used Memory: {float(i[2])}%")
            return
        elif float(i[2]) >= warning:
            yield Result(state=State.WARN, summary=f"Used Memory: {float(i[2])}%")
            return
        else:
            yield Result(state=State.OK, summary=f"Used Memory: {float(i[2])}%")
            return
                    

register.check_plugin(
    name="check_velos_mem",
    service_name="Memory",
    discovery_function = discover_check_velos_mem,
    check_function=check_check_velos_mem,
    check_default_parameters={"memory_thresholds": (80, 90)},
    check_ruleset_name="check_velos_advanced",
)

register.snmp_section(
    name = "check_velos_mem",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12276.1.3.1.5"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12276.1.2.1.4.1.1",
        oids=[
            "2",
            "3",
            "4",
            "5",
            "6",
        ],
    ),
)