import json
import argparse
import subprocess
import time
import xml.etree.ElementTree as ET
from typing import Any, Union
import os,sys
from xml_parser import load_gmd
import levellist
import pyperclip

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

def notify(message:str):
    print(message)
    subprocess.run(["notify-send",
                    "-t","5000",
                    message,message])

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="读取 .gmd XML 并反序列化为 Python 类型（仅读取/反序列化）")
    p.add_argument("input", help="输入 .gmd 文件路径")
    args = p.parse_args()

    inputFile = str(args.input)
    
    files = listTree(inputFile)
    print(files)
    
    level_lists:list[levellist.LevelList]=[]
    
    for file in files:
        obj = load_gmd(file)
        # # 以 Python 表示输出，便于进一步在脚本中 eval/repr 使用
        # from pprint import pprint
        # pprint(obj, width=120)
            
        level_lists.append(levellist.LevelList(obj))
    
    
    last_clip=""
    
    while True:
        
        clip=pyperclip.paste()
        
        if clip==last_clip:
            time.sleep(1)
            continue
        
        last_clip=clip
        
        try:
            id=int(clip)
            
            found=False
            for list1 in level_lists:
                if id in list1.get_levels().keys():
                    notify(f"Level {id} is in list \"{list1.name}\"")
                    found=True
            
            if not found:
                notify(f"Level {id} is not in any list")
            
        except:
            pass
        
        
        time.sleep(1)