from configparser import ConfigParser


class ReadConfig:
    def __init__(self):
        """
        读取所有配置
        """
        self.cfg = ConfigParser()
        self.cfg.read('config.ini')

    def get_server(self, param):
        value = self.cfg.get("server", param)
        return value

if __name__ == '__main__':
    cfg = ReadConfig()
    chart_ids = [int(id) for id in cfg.get_server("chart_ids").split()]
    print(chart_ids)
