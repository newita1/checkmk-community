#!/usr/bin/env python3

from .agent_based_api.v1 import check_levels, Metric, register, Result, Service, State
import re

# Función de descubrimiento para detectar métricas disponibles en los datos de piggyback
def discovery_velocloud_links(section):
    for line in section:
        # Asumimos que la primera parte de la línea es el nombre del enlace
        link_name = line[1]
        yield Service(item=link_name)

_velocloud_map_vpn_state = {
    '1': (State.WARN, 'Initial'),
    '2': (State.CRIT, 'Dead'),
    '3': (State.CRIT, 'Unusable'),
    '4': (State.WARN, 'Quiet'),
    '5': (State.OK, 'Standby'),
    '6': (State.WARN, 'Unstable'),
    '7': (State.OK, 'Stable'),
    '8': (State.CRIT, 'Unknown'),
}
# Función de chequeo para evaluar el estado de cada métrica
def check_velocloud_links(item, section):
    for line in section:
        link_name = line[1]
        if link_name == item:
#0  1  2            3               4                   5      6           7                8                9                  10
#0;GE3;Cemex Espana;bytesRx=3275314;bytesTx=3051156;scorerx;scoretx;bestJitterMsRx=0;bestJitterMsTx=0;bestLatencyMsRx=11;bestLatencyMsTx=6
            state = line[0]
            isp = line[2]
            bytesrx = line[3].split("=")[1]
            bytestx = line[4].split("=")[1]
            scorerx = line[5].split("=")[1]
            scoretx = line[6].split("=")[1]
            bestjittermsrx = line[7].split("=")[1]
            bestjittermstx = line[8].split("=")[1]
            bestlatencymsrx = line[9].split("=")[1]
            bestlatencymstx = line[10].split("=")[1]
            perfdata = [
                ("bytesrx", int(bytesrx)),
                ("bytestx", int(bytestx)),
                ("scorerx", int(scorerx)),
                ("scoretx", int(scoretx)),
                ("bestjittermsrx", float(bestjittermsrx)),
                ("bestjittermstx", float(bestjittermstx)),
                ("bestlatencymsrx", float(bestlatencymsrx)),
                ("bestlatencymstx", float(bestlatencymstx)),
            ]
            for p in perfdata:
                yield Metric(p[0], p[1])

            if state in ['5', '7']:
                yield Result(state=State.OK, summary=f"{isp} - {_velocloud_map_vpn_state[state][1]}")
                return
            elif state in ['1', '4', '6']:
                yield Result(state=State.WARN, summary=f"{isp} - {_velocloud_map_vpn_state[state][1]}")
                return
            elif state in ['2', '3', '8']:
                yield Result(state=State.CRIT, summary=f"{isp} - {_velocloud_map_vpn_state[state][1]}")
                return



def parse_velocloud_links(string_table):
    return string_table

register.agent_section(
    name = "velocloud_links",
    parse_function = parse_velocloud_links,
)

# Registro del plugin con el nombre de la sección especificada
register.check_plugin(
    name="velocloud_links",
    service_name="VeloCloud Link %s",
    discovery_function=discovery_velocloud_links,
    check_function=check_velocloud_links
)
