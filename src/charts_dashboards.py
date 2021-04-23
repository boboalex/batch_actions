import json

from requests import HTTPError
from src.basic import BasicHttpClient
from configparser import ConfigParser
from src.readConfig import ReadConfig

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
cfg = ConfigParser()
cfg.read('config.ini')

class TestBatchActions(BasicHttpClient):
    def __init__(self, source_ki, target_ki):
        super().__init__()

        self._headers = {'Accept': 'application/vnd.apache.kylin-v2+json',
                         'Accept-Language': 'en',
                         'Content-Type': 'application/json;charset=utf-8'
                         }
        self.source_ki = source_ki
        self.target_ki = target_ki
        # self.chart_ids = cfg.get(server)

    # def _request(self, method, url, **kwargs):  # pylint: disable=arguments-differ
    #     return super()._request(method, self._ki_base_url + url, **kwargs)

    def import_export_chart(self, chart_id):
        try:
            response_json = self.source_ki.export_chart(chart_id)
            self.target_ki.import_chart(response_json)
        except HTTPError as e:
            logging.error(f"Failed to import chart which id is {chart_id}")

    # def batch_import_export_charts(self, ):




if __name__ == '__main__':
    rc = ReadConfig()
    client = TestBatchActions(rc.get_server(""))
    client.import_export_chart()