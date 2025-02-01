#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .agent_based_api.v1 import *
import pprint
import re

#default_threslholds_values = (100.0, 20.0)
#.1.3.6.1.4.1.12276.1.2.1.1.2.1.3 -> cpucurrent [0]
#.1.3.6.1.4.1.12276.1.2.1.1.2.1.4-> cputotal5secavg [1]
#.1.3.6.1.4.1.12276.1.2.1.1.2.1.5  -> cputotal1minavg [2]
#.1.3.6.1.4.1.12276.1.2.1.1.2.1.6 -> cputotal5minavg [3]

def discover_check_velos_cpu(section):
    yield Service()

def check_check_velos_cpu(params, section):
    
    warning = int(params["cpu_thresholds"][0])
    critical = int(params["cpu_thresholds"][1])
    
    for i in section:

        yield Metric("cpucurrent", float(i[0]), levels=(warning, critical))
            
        if (float(i[0])) >= critical:
            yield Result(state=State.CRIT, summary=f"Total CPU: {float(i[0])}%")
            return
        elif (float(i[0])) >= warning:
            yield Result(state=State.WARN, summary=f"Total CPU: {float(i[0])}%")
            return
        else:
            yield Result(state=State.OK, summary=f"Total CPU: {float(i[0])}%")
            return
                    

register.check_plugin(
    name="check_velos_cpu",
    service_name="CPU Usage",
    discovery_function = discover_check_velos_cpu,
    check_function=check_check_velos_cpu,
    check_default_parameters={"cpu_thresholds": (80, 90)},
    check_ruleset_name="check_velos_advanced",
)

register.snmp_section(
    name = "check_velos_cpu",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12276.1.3.1.5"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12276.1.2.1.1.2.1",
        oids=[
            "2",
            "3",
            "4",
            "5",
        ],
    ),
)