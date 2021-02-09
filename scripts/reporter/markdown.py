import os
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union


class TableGenerator(object):
    def __init__(self):
        self.__table = ''

    @property
    def table(self) -> str:
        return self.__table

    def __row_maker(self, string: List[str]):
        return f'|{"|".join(string)}|\n'

    def __header_maker(self, string: List[str]):
        header = self.__row_maker(string)
        header += '|:---:' * (len(string)) + '|\n'
        return header

    def table_maker(self, string: List[Dict[str, str]]):
        print('Making markdown table...')

        if not string:
            self.__table = 'This build is perfect ✔'
            return

        self.__table += self.__header_maker(string[0].keys())
        for row in string:
            self.__table += self.__row_maker(row.values())


class MarkdownGenerator(object):
    def __init__(self, filename: str):
        self.__filename = filename

    def save(self, title: str, header: str, data: str) -> NoReturn:
        if os.path.isfile(self.__filename):
            print(f"{self.__filename} is find. Will remove it...")
            os.remove(self.__filename)

        print(f"Will save markdown table at {self.__filename}...")
        with open(file=self.__filename, mode='w', encoding='utf-8') as f:
            f.write(f'## {title} result\n')
            f.write(f'Link -> {header}\n')
            f.write(data)
        print('Done')


class CoverageReportGenerator(object):
    def __init__(self, filename: str):
        self.__filename = filename
        self.__table = '<table>\n'
    
    def __header(self, headers: List[str]) -> str:
        self.__table += '  <tr>\n'
        for header in headers:
            self.__table += f'    <th>{header}</th>\n'
        self.__table += '  </tr>\n'

    def __body(self, datas: List[Dict[str, Union[List[str], str]]]) -> str:
        for data in datas:
            self.__table += '  <tr>\n'
            self.__table += f'    <td rowspan="{len(data["files"]) + 1}">{data["package"]}</td>\n'
            self.__table += f'    <td><b>Total</b></td>\n'
            self.__table += f'    <td>{data["line-rate"]}</td>\n'
            self.__table += '  </tr>\n'
            for file in data['files']:
                self.__table += '  <tr>\n'
                self.__table += f'    <td>{file["file"]}</td>\n'
                self.__table += f'    <td>{file["line-rate"]}</td>\n'
                self.__table += '  </tr>\n'

    def save(self, header: List[str], body: List[Dict[Union[List[str], str], str]]):
        self.__header(header)
        self.__body(body)
        self.__table += "</table>"
        with open(file=self.__filename, mode='a', encoding='utf-8') as f:
            f.write('## Packages\n')
            f.write(self.__table)


if __name__ == "__main__":
    pass