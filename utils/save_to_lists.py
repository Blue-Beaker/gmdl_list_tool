import os
from .gd_save_decryptor import saves
from . import xml_parser
from .levellist import LevelList

SAVEFILE_PATH="Save/CCLocalLevels.dat"
TEMPFILE_PATH="/tmp/CCLocalLevels.xml"

def load_cclocallevels_file(savepath:str):
    with open(TEMPFILE_PATH,"w") as f:
        f.write(saves.decrypt_save(savepath))
    leveldict=xml_parser.load_gmd(TEMPFILE_PATH)
    os.remove(TEMPFILE_PATH)
    
    if not isinstance(leveldict,dict):
        return None,None
    
    levels:dict[str,dict]=leveldict.get("LLM_01",{})
    lists:dict[str,dict]=leveldict.get("LLM_03",{})
    
    return levels,lists

def load_lists(lists:dict[str,dict]):
    levellists:list[LevelList]=[]
    
    for k,v in lists.items():
        if isinstance(v,dict):
            levellists.append(LevelList(v))
    return levellists
    
if __name__ == "__main__":
    l,levellists=load_cclocallevels_file(SAVEFILE_PATH)
    if(levellists==None):
        exit()
    
    print(load_lists(levellists))