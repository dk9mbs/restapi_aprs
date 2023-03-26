import datetime
import socket
from datetime import datetime

from core.fetchxmlparser import FetchXmlParser
from services.database import DatabaseServices
from core import log
from core.meta import read_table_meta

logger=log.create_logger(__name__)

def send(aprs,callsign,passcode, logger):
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
