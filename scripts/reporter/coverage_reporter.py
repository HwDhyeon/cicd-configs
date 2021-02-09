import json
import os

import xmltodict

from typing import Dict
from typing import List

from jenkins_api import JenkinsApi
from markdown import CoverageReportGenerator
from markdown import MarkdownGenerator
from markdown import TableGenerator


class CoverageReader(object):
    def __init__(self, filename: str):
        self.__filename = filename

    def __parse_xml(self):
        if os.path.isfile(self.__filename):
            with open(file=self.__filename, mode='r', encoding='utf-8') as f:
                xml = xmltodict.parse(f.read())
                xml = json.dumps(xml)
                xml = json.loads(xml)
            return xml

    def read(self) -> List[Dict[str, str]]:
        def create_percentage(percente: str) -> str:
            return f"{float(percente) * 100:.2f}%"

        xml = self.__parse_xml()
        coverage_result = {
            'lines-covered': xml['coverage']['@lines-covered'],
            'lines-valid': xml['coverage']['@lines-valid'],
            'line-rate': create_percentage(xml['coverage']['@line-rate']),
            'packages': [{
                'package': package['@name'],
                'line-rate': create_percentage(package['@line-rate']),
                'files': [{
                    'file': p_class['@filename'],
                    'line-rate': create_percentage(p_class['@line-rate'])
                } for p_class in package['classes']['class']]
            } for idx, package in enumerate(xml['coverage']['packages']['package'])]
        }
            
        return coverage_result


if __name__ == "__main__":
    api = JenkinsApi()
    title, link = api.make_header(os.getenv('JOB_NAME'), int(os.getenv('BUILD_NUMBER')))
    cr = CoverageReader('coverage.xml')
    cg = CoverageReportGenerator('coverage.md')
    md = MarkdownGenerator('coverage.md')
    tb = TableGenerator()
    res = cr.read()
    pres = res['packages']
    del res['packages']
    tb.table_maker([res])
    md.save('Coverage', f"[{title}]({link})", tb.table)
    # cg.save(['Package', 'File', 'Line-rate'],pres)
