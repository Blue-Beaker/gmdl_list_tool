import json
import argparse
import xml.etree.ElementTree as ET
from typing import Any, Union
import os,sys
from utils.xml_parser import load_gmd
import utils.levellist as levellist

def listTree(rootpath:str)->list[str]:
    def filenameMatches(filepath:str):
        return filepath.endswith(".gmd")
    
    if not os.path.isdir(rootpath):
        return [rootpath]
    
    files:list[str]=[]
    
    for file in os.listdir(rootpath):
        fullpath = os.path.join(rootpath,file)
        
        if os.path.isdir(fullpath):
            files.extend(listTree(fullpath))
        elif filenameMatches(file):
            files.append(fullpath)
            
    return files

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="读取 .gmd XML 并反序列化为 Python 类型（仅读取/反序列化）")
    p.add_argument("input", help="输入 .gmd 文件路径")
    args = p.parse_args()

    inputFile = str(args.input)
    
    files = listTree(inputFile)
    print(files)
    
    for file in files:
        obj = load_gmd(file)
        # # 以 Python 表示输出，便于进一步在脚本中 eval/repr 使用
        # from pprint import pprint
        # pprint(obj, width=120)
            
        level_list=levellist.LevelList(obj)
        
        print(level_list.get_levels())