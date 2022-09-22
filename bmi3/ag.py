import os
import subprocess
from shutil import which

def parse_ag_result(result: str):
    g1 = lambda l: [(k, list([y for (x,y) in l if x == k])) for k in dict(l).keys()]
    return g1(list(map(lambda z: [z[0].split(":")[0], (":".join(z[0].split(":")[1:]), ' '.join(z[1:]))], filter(lambda x:x!=[], map(lambda x: list(filter(lambda y: y != '', x.split(" "))),result.split("\n"))))))


def execute_ag(filePath: str, searchPattern: str):
    currentPath = os.getcwd()
    if not which("ag"):
        raise ModuleNotFoundError("ag is not installed on the system")
    if os.access(filePath, os.W_OK):
        os.chdir(filePath)
        try:
            result = subprocess.run(['ag', searchPattern], stdout=subprocess.PIPE).stdout
            os.chdir(currentPath)
            if type(result) == str:
                return result 
            elif type(result) == bytes:
                return result.decode("utf-8")
            else:
                return TypeError("Unrecognized type {}".format(type(result)))
        except:
            os.chdir(currentPath)
            raise RuntimeError("Ag search failed")
    else:
        os.chdir(currentPath)
        raise IsADirectoryError("The path {} does not exist".format(filePath))