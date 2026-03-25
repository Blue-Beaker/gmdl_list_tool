
from enum import Enum


class ICONS(Enum):
    EASY = 10
    EASY_DEMON = 10
    NORMAL = 20
    MEDIUM_DEMON = 20
    HARD = 30
    HARD_DEMON = 30
    HARDER = 40
    INSANE_DEMON = 40
    INSANE = 50
    EXTREME_DEMON = 50

class ListLevel:
    id:int
    name:str
    author:str
    song:int
    
    stars:int
    
    icon_id:int
    
    def __init__(self,keys:dict|None) -> None:
        if keys:
            self.load(keys)
    
    def load(self,keys:dict):
        self.id=keys.get('k1',0)
        self.name=keys.get('k2','')
        self.author=keys.get('k5','')
        self.song=keys.get('k45',0)
        self.stars=keys.get('k26',0)
        self.icon_id=keys.get('k10',0)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.__dict__}"
        
    
class LevelList:
    id:int
    name:str
    author:str
    levels:list[ListLevel]
    
    def __init__(self,keys:dict|None) -> None:
        self.levels=[]
        if keys:
            self.load(keys)
    
    def load(self,keys:dict):
        self.id=keys.get('k1',0)
        self.name=keys.get('k2','')
        self.author=keys.get('k5','')
        
        levels:dict[str,dict]=keys.get('k97',{})
        for level in levels:
            
            self.levels.append(ListLevel(levels[level]))
    
    def get_levels(self) -> dict[int,ListLevel]:
        return {level.id:level for level in self.levels}
            
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.__dict__}"