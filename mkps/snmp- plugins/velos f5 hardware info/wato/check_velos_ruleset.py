#!/usr/bin/env python3
# This file is explained in the Checkmk User Guide:
# https://docs.checkmk.com/master/en/devel_check_plugins.html#rule_set
# 
# Store in your Checkmk site at:
# local/share/check_mk/web/plugins/wato/check_velos_temp_advanced_parameters.py

from cmk.gui.i18n import _

from cmk.gui.valuespec import (
    Dictionary,
    Percentage,
    Tuple,
    Integer,
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)

def _parameter_valuespec_check_velos_advanced():
    return Dictionary(
        elements = [
            ("cpu_thresholds",
                Tuple(
                    title = _("Umbrales de alerta para CPU"),
                    elements = [
                        Percentage(title=_("Warning at"), default_value=80.0),
                        Percentage(title=_("Critical at"), default_value=90.0),
                    ],
                )
            ),
            ("memory_thresholds",
                Tuple(
                    title = _("Umbrales de alerta para Memoria"),
                    elements = [
                        Percentage(title=_("Warning at"), default_value=80.0),
                        Percentage(title=_("Critical at"), default_value=90.0),
                    ],
                )
            ),
            ("temperature_thresholds",
                Tuple(
                    title = _("Umbrales de alerta para Temperatura"),
                    elements = [
                        Integer(title=_("Warning at"), default_value=30.0, unit="°C"),
                        Integer(title=_("Critical at"), default_value=35.0, unit="°C"),
                    ],
                )
            ),
            ("diskwrite_thresholds",
                Tuple(
                    title = _("Umbrales de alerta para Latencia de escritura de Disco"),
                    elements = [
                        Integer(title=_("Warning at"), default_value=80.0, unit="ms"),
                        Integer(title=_("Critical at"), default_value=160.0, unit="ms"),
                    ],
                )
            ),
            ("diskread_thresholds",
                Tuple(
                    title = _("Umbrales de alerta para Latencia de lectura de Disco"),
                    elements = [
                        Integer(title=_("Warning at"), default_value=80.0, unit="ms"),
                        Integer(title=_("Critical at"), default_value=160.0, unit="ms"),
                    ],
                )
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name = "check_velos_advanced",
        group = RulespecGroupCheckParametersApplications,
        match_type = "dict",
        parameter_valuespec = _parameter_valuespec_check_velos_advanced,
        title = lambda: _("Velos F5 thresholds"),
    )
)