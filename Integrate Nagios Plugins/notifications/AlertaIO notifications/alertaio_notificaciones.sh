#!/bin/bash
#Alertaio - Integration

#env | grep NOTIFY_ | soirt > /tmp/foobar.out
#env | sort > /tmp/foobar.out
#echo $NOTIFY_SERVICEDESK > /tmp/foobar.out

case "$NOTIFY_SERVICESTATE" in
    OK)
        hpovstatus="normal"
        group=$NOTIFY_SERVICEGROUPNAMES
        ;;
    WARNING)
        hpovstatus="minor"
        group=$NOTIFY_SERVICEGROUPNAMES
        ;;
    CRITICAL)
        hpovstatus="critical"
        group=$NOTIFY_SERVICEGROUPNAMES
        ;;
    UNKNOWN)
        hpovstatus="Warning"
        group=$NOTIFY_SERVICEGROUPNAMES
        ;;
    *)
        hpovstatus="Warning"
        group=$NOTIFY_SERVICEGROUPNAMES
        ;;
esac

if [-z "$NOTIFY_SERVICEDESC"]; then
    # Asigna el valor "hoststatus" a la variable de entorno
    NOTIFY_SERVICEDESC = "Hoststatus"
    NOTIFY_SERVICEOUTPUT = $NOTIFY_HOSTOUTPUT
    case "NOTIFY_HOSTSTATE" in
        UP)
            hpovstatus="normal"
            group=$NOTIFY_HOSTCONTACTGROUPNAMES
            ;;
        DOWN)
            hpovstatus="critical"
            group=$NOTIFY_HOSTCONTACTGROUPNAMES
            ;;
        UNKNOWN)
            hpovstatus="Warning"
            group=$NOTIFY_HOSTCONTACTGROUPNAMES
            ;;
        *)
            hpovstatus="Warning"
            group=$NOTIFY_HOSTCONTACTGROUPNAMES
            ;;
    esac

fi

group="TEST"
curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Key APIKEY" -d '{
  "text": "'"$NOTIFY_SERVICEOUTPUT"'",
  "severity": "'"$hpovstatus"'",
  "resource": "'"$NOTIFY_HOSTNAME"'",
  "event": "Service '"$NOTIFY_SERVICEDESC"'",
  "origin": "CheckMK",
  "AssignmentGroup": "Infraestructura",
  "environment": "Production",
  "service": {
    "'"$NOTIFY_SERVICEDESC"'": {
      "attributes": {
        "types": "Performance",
        "subcomponent": "'"$NOTIFY_HOSTGROUPNAMES"'",
        "name": "'"$NOTIFY_HOSTALIAS"'",
        "ip": "'"$NOTIFY_HOSTADDRESS"'",
        "subcategory": "'"$NOTIFY_SERVICEDESC"'"
      }
    }
  }
}' "http://ipalerta:puerto/api/alert"

exit 0