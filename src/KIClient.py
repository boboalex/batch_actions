from requests import HTTPError
from src.basic import BasicHttpClient


class KIClient(BasicHttpClient):
    def __init__(self, ki_host, ki_port):
        super().__init__()
        self._headers = {'Accept': 'application/vnd.apache.kylin-v2+json',
                         'Accept-Language': 'en',
                         'Content-Type': 'application/json;charset=utf-8'
                         }
        self.ki_host = ki_host
        self.ki_port = ki_port
        self.ki_base_url = f"http://{self.ki_host}:{self.ki_port}"
        # self.chart_ids = chart_ids

    def _request(self, method, url, **kwargs):  # pylint: disable=arguments-differ
        return super()._request(method, self.ki_base_url + url, **kwargs)

    def _get_charts_desc(self, project, page=0, p_size=1000):
        # url = "/chart/api/read"
        # 在进行对参数解析时，不知为什么_flt_2_database会多出来很多的25
        # payload = {
        #     "_page_SliceModelView": page,
        #     "_psize_SliceModelView": p_size,
        #     "_oc_SliceModelView": "id",
        #     "_od_SliceModelView": "desc",
        #     "_flt_2_database": f"%7B%22name%22%3A%22database_name%22%2C%22val%22%3A%5B%22{project}%22%5D%7D"
        # }
        payload = {}
        url = f"/chart/api/read?" \
              f"_page_SliceModelView={page}&_psize_SliceModelView={p_size}" \
              "&_oc_SliceModelView=id&_od_SliceModelView=desc" \
              f"&_flt_2_database=%7B%22name%22%3A%22database_name%22%2C%22val%22%3A%5B%22{project}%22%5D%7D"
        # 上面一行的f不可省略
        resp = self._request('GET', url=url, params=payload)
        return resp

    def export_chart(self, chart_id):
        payload = {
            'id': chart_id
        }
        resp = self._request('GET', f'/kylin/charts/export/{chart_id}', params=payload)
        return resp

    def import_chart(self, response_json):
        resp = self._request('POST', '/kylin/charts/import', json=response_json)
        return resp

    def import_export_chart(self, chart_id):
        try:
            response_json = self.export_chart(chart_id)
            self.import_chart(response_json)
        except HTTPError as e:
            logging.error(f"Failed to import chart which id is {chart_id}")

