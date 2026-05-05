import json
import argparse
import subprocess
import time
import xml.etree.ElementTree as ET
from typing import Any, Union
import os,sys
from utils.xml_parser import load_gmd
import utils.levellist as levellist
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

def main():
    import argparse
    p = argparse.ArgumentParser(description="Parse GD level lists from exported lists or savefile, and check existence in lists for every level you copied in clipboard")
    p.add_argument("input", help="path to the list file, CCLocalLevels.dat save file, or a folder containing the lists")
    args = p.parse_args()

    inputFile = str(args.input)
    
    level_lists:list[levellist.LevelList]=[]
    
    files = listTree(inputFile)
    print(files)
    
    for file in files:
        
        if file.endswith('.dat'):
            print(f"Try to parse save file {file} ...")
            from utils.save_to_lists import load_cclocallevels_file,load_lists
            levels,lists=load_cclocallevels_file(file)
            if(lists==None):
                print(f"Failed to parse save file, please make sure it's CCLocalLevels.dat")
                continue
            level_lists.extend(load_lists(lists))
        elif file.endswith('.gmd') or file.endswith('.gmdl') or file.endswith('.xml'):
            print(f"Try to parse exported list file {file} ...")
            obj = load_gmd(file)
            level_lists.append(levellist.LevelList(obj))
            
    for level_list in level_lists:
        print(f"Loaded list '{level_list.name}' with {level_list.levels.__len__()} levels")
    
    
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
            contained_lists:list[str]=[]
            for list1 in level_lists:
                if id in list1.get_levels().keys():
                    contained_lists.append('"'+list1.name+'"')
                    found=True
            
            if not found:
                notify(f"Level {id} is not in any list")
            else:
                notify(f"Level {id} is in list {", ".join(contained_lists)}")
            
        except:
            pass
        
        
        time.sleep(1)
        

if __name__ == "__main__":
    main()