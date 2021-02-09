import os
from typing import Dict
from typing import List

from markdown import MarkdownGenerator
from markdown import TableGenerator
from jenkins_api import JenkinsApi


class Flake8Reader(object):
    def __init__(self, filename: str):
        self.__filename = filename

    def read(self) -> List[Dict[str, str]]:
        if os.path.isfile(self.__filename):
            print(f"{self.__filename} is find...")
            with open(file=self.__filename, mode='r', encoding='utf-8') as f:
                data = [{
                    'file':
                        line.split(':')[0],
                    'line':
                        f"{line.split(':')[1]}line {line.split(':')[2]}pos",
                    'message':
                        line.split(':')[-1].strip()
                } for line in f.readlines()]

            return data


if __name__ == "__main__":
    api = JenkinsApi()
    title, link = api.make_header(os.getenv('JOB_NAME'), int(os.getenv('BUILD_NUMBER')))
    reader = Flake8Reader('flake8.txt')
    tb = TableGenerator()
    tb.table_maker(reader.read())
    md = MarkdownGenerator('flake8.md')
    md.save('Flake8', f"[{title}]({link})", tb.table)
