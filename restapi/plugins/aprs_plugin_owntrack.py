import datetime
import json

from core import log
from services.database import DatabaseServices
from core.fetchxmlparser import FetchXmlParser
from services.fetchxml import build_fetchxml_by_alias, build_fetchxml_lookup
from plugins.aprs_lib_network import send


logger=log.create_logger(__name__)

def __validate(params):
    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    #data=json.loads(params)
    data=params
    target=None

    if data['data']['_type']=="location":
        target={
            "batt": data['data']['batt'],
            "lon": data['data']['lon'],
            "lat": data['data']['lat'],
            "ele": data['data']['alt'],
            "client_id": data['data']['tid'],
            "topic": data['topic'],
            "type_id": "TRACKPOINT"
        }

        if data['data']['_type']=="waypoint":
            device=(data['topic']).split("/")[2]
            print(device)
            fetch_xml=build_fetchxml_lookup(context,"aprs_owntrack_client",auto_commit=0, filter_field_name="device", filter_value=device)
            print(fetch_xml)
            fetch=FetchXmlParser(fetch_xml, context, page=0, page_size=0)
            rs=DatabaseServices.exec (fetch, context, run_as_system=True, fetch_mode=1)
            print(rs.get_result())
            if not rs.get_eof():
                target={
                    "batt": "0",
                    "lon": data['data']['lon'],
                    "lat": data['data']['lat'],
                    "client_id": rs.get_result()['id'],
                    "topic": data['topic'],
                    "description": data['data']['desc'],
                    "type_id": "WAYPOINT"
                }


        if target!=None:
            fetch_xml=build_fetchxml_by_alias(context,"aprs_owntrack_log",id=None,data=target,auto_commit=0, type="insert")
            fetch=FetchXmlParser(fetch_xml, context, page=0, page_size=0)
            rs=DatabaseServices.exec (fetch, context, run_as_system=True, fetch_mode=1)
