import datetime
import socket
from datetime import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log
from core.meta import read_table_meta
from plugins.aprs_lib_network import send
from plugins.aprs_lib_geocoordinate import GeoCoordinateTools

logger=log.create_logger(__name__)

def __validate(params):
    if not 'data' in params:
        return False
    if not 'lat' in params['data']:
        return False
    if not 'lon' in params['data']:
        return False
    if not 'client_id' in params['data']:
        return False

    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    fetch=f"""
    <restapi type="select">
        <table name="aprs_owntrack_client" alias="c"/>
        <filter type="and">
            <condition field="id" value="{params['data']['client_id']['value']}" operator="="/>
            <condition field="login_id" value="" operator="notnull"/>
        </filter>
    </restapi>
    """
    fetchparser=FetchXmlParser(fetch,context)
    rs_client=DatabaseServices.exec(fetchparser, context,fetch_mode=1, run_as_system=True)
    if rs_client.get_eof():
        logger.warning(f"no aprs login defined for client {params['data']['client_id']['value']}")
        return

    fetch=f"""
    <restapi type="select">
        <table name="aprs_login" alias="l"/>
        <filter type="and">
            <condition field="id" value="{rs_client.get_result()['login_id']}" operator="="/>
        </filter>
    </restapi>
    """
    fetchparser=FetchXmlParser(fetch,context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=1, run_as_system=True)

    lat_dec=params['data']['lat']['value']
    lon_dec=params['data']['lon']['value']
    callsign=rs.get_result()['callsign']
    passcode=rs.get_result()['passcode']
    timestamp=datetime.today().strftime('%d%H%M')+'z'
    lat,lon=GeoCoordinateTools.decimal_to_aprs(lat_dec, lon_dec)

    obj_name="CALL-5".ljust(9)
    type="*"
    overlay="/".ljust(1)
    symbol="[".ljust(1)
    comment=""
    source_address="CALL"
    payload=f";{obj_name}{type}{timestamp}{lat}{overlay}{lon}{symbol}{comment}"
    aprs=f"{source_address}>APRS,TCPIP*:{payload}"

    if params['data']['client_id']['value']=='01':
        send(aprs,callsign,passcode, logger)


