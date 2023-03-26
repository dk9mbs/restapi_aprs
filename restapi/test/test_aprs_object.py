import unittest

from core.database import CommandBuilderFactory
from core.database import FetchXmlParser
from config import CONFIG
from core.appinfo import AppInfo
from core.fetchxmlparser import FetchXmlParser
from core.plugin import Plugin
from services.database import DatabaseServices
from aprs_send_objects import execute

class TestAprsObject(unittest.TestCase):
    def setUp(self):
        AppInfo.init(__name__, CONFIG['default'])
        session_id=AppInfo.login("root","password")
        self.context=AppInfo.create_context(session_id)

    def test_combo_source(self):
        params={"input": {}, "output": {}}
        #plugin_context=Plugin.create_context("$timer_every_minute","execute","after")
        #print(execute(self.context,plugin_context, {"input": params, "output": {}}))

        from plugins.aprs_send_objects import execute
        execute(self.context, {}, params)


    def tearDown(self):
        AppInfo.save_context(self.context, True)
        AppInfo.logoff(self.context)


if __name__ == '__main__':
    unittest.main()
