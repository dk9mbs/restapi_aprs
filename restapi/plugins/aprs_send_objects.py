import datetime
import socket
from datetime import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log
from core.meta import read_table_meta

logger=log.create_logger(__name__)

def __validate(params):
    return True

def execute(context, plugin_context, params):
    if not __validate(params):
        logger.warning(f"Missings params")
        return

    data=params['input']

    fetch=f"""
    <restapi type="select">
        <table name="aprs_object" alias="o"/>
        <select>
            <field name="object_name" table_alias="o"/>
            <field name="lat_deg" table_alias="o"/>
            <field name="long_deg" table_alias="o"/>
            <field name="overlay" table_alias="o"/>
            <field name="symbol_code" table_alias="o"/>
            <field name="comment" table_alias="o"/>
            <field name="type" table_alias="o"/>
            <field name="source_address" table_alias="o"/>
            <field name="lat_min" table_alias="o"/>
            <field name="lat_sec" table_alias="o"/>
            <field name="long_min" table_alias="o"/>
            <field name="long_sec" table_alias="o"/>
            <field name="callsign" table_alias="l"/>
            <field name="passcode" table_alias="l"/>
        </select>
        <orderby>
            <field name="id" alias="o" sort="DESC"/>
        </orderby>
        <joins>
            <join table="aprs_login" alias="l" condition="l.id=o.login_id" type="inner"/>
        </joins>
    </restapi>
    """

    fetchparser=FetchXmlParser(fetch,context)
    rs=DatabaseServices.exec(fetchparser, context,fetch_mode=0, run_as_system=True)

    #https://www.koordinaten-umrechner.de
    for obj in rs.get_result():
        callsign=obj['callsign']
        passcode=obj['passcode']
        obj_name=(obj['object_name']).ljust(9)
        timestamp=datetime.today().strftime('%d%H%M')+'z'

        #lat="5205.23N"
        lat_dec_sec=int(round((100.0/60.0)*float(obj['lat_sec']),0))
        lat=str(obj['lat_deg']).rjust(2,'0')+str(obj['lat_min']).rjust(2,'0')+'.'+str(lat_dec_sec).rjust(2,'0')+"N"

        #long="01022.14E"
        long_dec_sec=int(round((100.0/60.0)*float(obj['long_sec']),0))
        long=str(obj['long_deg']).rjust(3,'0')+str(obj['long_min']).rjust(2,'0')+'.'+str(long_dec_sec).rjust(2,'0')+"E"

        overlay=(obj['overlay']).ljust(1)
        symbol=(obj['symbol_code']).ljust(1)
        comment=(obj['comment'])
        type=obj['type']

        payload=f";{obj_name}{type}{timestamp}{lat}{overlay}{long}{symbol}{comment}"
        aprs=f"{obj['source_address']}>APRS,TCPIP*:{payload}"
        __send(aprs,callsign,passcode, logger)

    params['output']['aprs']=""


def __send(aprs,callsign,passcode, logger):
    logger.info(aprs)
    login=f"user {callsign} pass {passcode}\r\n"
    host = "rotate.aprs2.net"
    port = 14580
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(login.encode())
    packet=f"{aprs}\r\n"
    s.send(packet.encode(errors='ignore'))
    s.close()
