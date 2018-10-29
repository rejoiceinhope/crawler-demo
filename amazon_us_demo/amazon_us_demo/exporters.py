# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class CustomCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = settings.get('CSV_DELIMITER', '\t')

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(CustomCsvItemExporter, self).__init__(*args, **kwargs)
