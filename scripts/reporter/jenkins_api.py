import base64

import jenkins
from typing import Tuple


class JenkinsApi(object):
    def __init__(self):
        self.__jenkins = jenkins.Jenkins(*self.__find_user_info()) 

    def __find_user_info(self):
        url = base64.b64decode('aHR0cDovL2NpY2QubW9iaWdlbi5jb20=').decode('utf-8')
        useranme = base64.b64decode('bW9iaWdlbi1ib3Q=').decode('utf-8')
        password = base64.b64decode('YWhxbHdwczEyMzQ=').decode('utf-8')
        return url, useranme, password

        
    def make_header(self, job_name: str, build_number: int) -> Tuple[str]:
        build_info = self.__jenkins.get_build_info(job_name, build_number)
        return (build_info['fullDisplayName'], build_info['url'])


if __name__ == "__main__":
    api = JenkinsApi()
    print(api.make_header('IRIS-E2E', 395))
