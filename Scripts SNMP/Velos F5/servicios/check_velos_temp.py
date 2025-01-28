#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .agent_based_api.v1 import *

#.1.3.6.1.4.1.12276.1.2.1.3.1.1.2 -> tempcurrent [0]


def discover_check_velos_temp(section):
    yield Service()

def check_check_velos_temp(params, section):
    
    warning = int(params["temperature_thresholds"][0])
    critical = int(params["temperature_thresholds"][1])

    for i in section:
        yield Metric("Temperature", int(i[0]), levels=(warning, critical))
        if float(i[0]) >= critical:
            yield Result(state = State.CRIT, summary = f"Current Temperature: {float(i[0]):.1f}°C")
        elif float(i[0]) >= warning:
            yield Result(state = State.WARN, summary = f"Current Temperature: {float(i[0]):.1f}°C")
        else:
            yield Result(state = State.OK, summary = f"Current Temperature: {float(i[0]):.1f}°C")
        return   

register.check_plugin(
    name="check_velos_temp",
    service_name="Temperature",
    discovery_function = discover_check_velos_temp,
    check_function=check_check_velos_temp,
    check_default_parameters={"temperature_thresholds": (35, 40)},
    check_ruleset_name="check_velos_advanced",
)

register.snmp_section(
    name = "check_velos_temp",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12276.1.3.1.5"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12276.1.2.1.3.1.1",
        oids=[
            "2",
        ],
    ),
)