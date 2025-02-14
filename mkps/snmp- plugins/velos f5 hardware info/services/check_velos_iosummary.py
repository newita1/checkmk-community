#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .agent_based_api.v1 import *
import pprint
import re

#default_threslholds_values = (100.0, 20.0)
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.4 -> disktotaliops [0]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.5 -> diskreadiops [1]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.7 -> diskreadbytes [2]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.8 -> diskreadlatencyms [3]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.9 -> diskwriteiops [4]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.11 -> diskwritebytes [5]
# .1.3.6.1.4.1.12276.1.2.1.2.2.1.12 -> diskwritelatencyms [6]


def discover_check_velos_iosummary(section):
    yield Service()

def check_check_velos_iosummary(params, section):
    
    read_warn = float(params["diskread_thresholds"][0])
    read_crit = float(params["diskread_thresholds"][1])
    write_warn = float(params["diskwrite_thresholds"][0])
    write_crit = float(params["diskwrite_thresholds"][1])
    
    for i in section:
        # cambiar valores a milistengundos, kbs....

        diskread_bytes = float(i[2]) / float(i[0])
        diskreadlatencyms = float(i[3]) / float(i[0])
        diskwrite_bytes = float(i[5]) / float(i[0])
        diskwrite_latencyms = float(i[6]) / float(i[0])

        perfdata = [("disktotal_iops", float(i[0])),
                    ("diskread_iops", float(i[1])),
                    ("diskread_bytes", float(diskread_bytes)),
                    ("diskread_latencyms", float(diskreadlatencyms)),
                    ("diskwrite_iops", float(i[4])),
                    ("diskwrite_bytes", float(diskwrite_bytes)),
                    ("diskwrite_latencyms", float(diskwrite_latencyms))]

        for p in perfdata:
            yield Metric(p[0], p[1])
            # Cambiar el output de salida del details
        
        if (float(diskreadlatencyms) >= read_crit) or (float(diskwrite_latencyms) >= write_crit):
            yield Result(state=State.CRIT,
                        summary=f"Read Latency: {float(diskreadlatencyms):.3f}ms Write Latency: {float(diskwrite_latencyms):.3f}ms",
                        details=f"""Total IOPS: {float(i[0])} IOPs\n
                                Read IOPS: {float(i[1])} IOPs\n
                                Read Bytes: {float(diskread_bytes):.3f} bytes\n
                                Read Latency: {float(diskreadlatencyms):.3f}ms\n
                                Write IOPS: {float(i[4])} IOPs\n
                                Write Bytes: {float(diskwrite_bytes):.3f} bytes\n
                                Write Latency: {float(diskwrite_latencyms):.3f}ms""")
            return
        elif (float(diskreadlatencyms) >= read_warn) or (float(diskwrite_latencyms) >= write_warn):
            yield Result(state=State.WARN,
                        summary=f"Read Latency: {float(diskreadlatencyms):.3f}ms Write Latency: {float(diskwrite_latencyms):.3f}ms",
                        details=f"""Total IOPS: {float(i[0])} IOPs\n
                                Read IOPS: {float(i[1])} IOPs\n
                                Read Bytes: {float(diskread_bytes):.3f} bytes\n
                                Read Latency: {float(diskreadlatencyms):.3f}ms\n
                                Write IOPS: {float(i[4])} IOPs\n
                                Write Bytes: {float(diskwrite_bytes):.3f} bytes\n
                                Write Latency: {float(diskwrite_latencyms):.3f}ms""")
            return
        else:
            yield Result(state=State.OK,
                            summary=f"Read Latency: {float(diskreadlatencyms):.3f}ms Write Latency: {float(diskwrite_latencyms):.3f}ms",
                            details=f"""Total IOPS: {float(i[0])} IOPs\n
                                    Read IOPS: {float(i[1])} IOPs\n
                                    Read Bytes: {float(diskread_bytes):.3f} bytes\n
                                    Read Latency: {float(diskreadlatencyms):.3f}ms\n
                                    Write IOPS: {float(i[4])} IOPs\n
                                    Write Bytes: {float(diskwrite_bytes):.3f} bytes\n
                                    Write Latency: {float(diskwrite_latencyms):.3f}ms""")
            return

register.check_plugin(
    name="check_velos_iosummary",
    service_name="Disk IO SUMMARY",
    discovery_function = discover_check_velos_iosummary,
    check_function=check_check_velos_iosummary,
    check_default_parameters={"diskwrite_thresholds": (80, 160),"diskread_thresholds": (80, 160)},
    check_ruleset_name="check_velos_advanced",
)

register.snmp_section(
    name = "check_velos_iosummary",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12276.1.3.1.5"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12276.1.2.1.2.2.1",
        oids=[
            "4",
            "5",
            "7",
            "8",
            "9",
            "11",
            "12",
        ],
    ),
)
