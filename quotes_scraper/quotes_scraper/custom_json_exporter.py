import json
from scrapy.exporters import JsonItemExporter

class CustomJsonItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        kwargs['ensure_ascii'] = False
        super().__init__(file, **kwargs)

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        data = json.dumps(itemdict, ensure_ascii=False, indent=self.indent)
        self.file.write(data + "\n")
