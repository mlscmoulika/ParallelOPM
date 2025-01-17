import json
from ScreenShotBuilder import *
import datetime
from snapshot_status import getStatus


class GameState:
    def __init__(self,level,zoneSheet,user,board_snapshot_id,isSolution=False):
        
        self.user = user

        self.screenshot_destination = f'../DATA/Screenshots/{self.user}/{self.user}_{datetime.datetime.now()}.png'.replace(' ','_')
        self.screenshot = ScreenShot(level,self.screenshot_destination)

        self.board_snapshot_id = board_snapshot_id
        self.text              = getStatus(self.board_snapshot_id,f"{self.user}"+".json")        
        
        #Load Game Properties
        self.level = str(level)
        self.zoneSheet = zoneSheet
        self.level_info      = json.load(open(self.zoneSheet))
                
        self.zones         = self.level_info[self.level]['mapAreas']        

        self.index         = 0
        self.indexMap      = {}
        self.nSemaphores   = 0
        self.nSignals      = 0
        
        #is this state the soltion (False by default)
        self.isSolution = isSolution
        
        #cordinates
        self.semaphorePositions = [] #(id,x,y,zone) 
        self.signalPositions    = [] #(id,x,y,zone)
        self.linkPositions      = [] #(position1,postion2)        
        
        
        
        #abstraction 1
        self.semaphore_zone_dict = {}
        self.signal_zone_dict    = {}
        self.link_dict           = {} #{"zone1zone2" : count}
        

        
        #abstraction2
        
        for zone in self.zones:
            self.indexMap[zone]=self.index
            self.index+=1
        
        self.adjaceny_matrix = [[0 for j in range(len(self.zones))] for i in range(len(self.zones)) ]  
        
        
    def getSemaphoreXY(self,id):
        print(self.semaphorePositions)
        for semaphore in self.semaphorePositions:
            if semaphore[0]==id:
                return (semaphore[1],semaphore[2]) 
        return None
    
    def getSignalXY(self,id):
        for signal in self.signalPositions:
            if signal[0]==id:
                return signal[1],signal[2]
        return None
    

    #place a signal or semaphore
    def putSemaphore(self,x,y,id):
        zone  = self.getZone(x,y)
        self.screenshot.drawSemaphore(x,y)
        if zone in self.semaphore_zone_dict:
            self.semaphore_zone_dict[zone]+=1
        else:
            self.semaphore_zone_dict[zone]=1
            
        #add the element to the board
        self.semaphorePositions.append((id,x,y,zone))
        #update the counts
        self.nSemaphores+=1

    def zoneIndex(self,zone):
        return self.indexMap[zone]

    def putSignal(self,x,y,id_1,id_2):
        print(f'[INFO] Trying to put Signal at {x},{y} for {id_1}')
        print(f'[INFO] Putting a Link Between {id_1},{id_2}')

        zone  = self.getZone(x,y)
        if zone in self.signal_zone_dict:
            self.signal_zone_dict[zone]+=1
        else:
            self.signal_zone_dict[zone]=1

        print(f'[INFO] adding {id_1} to signal positions')
        self.signalPositions.append((id_1,x,y,zone))
        print(self.signalPositions)
        self.nSignals+=1

        #populate link dict
        (connection_x,connection_y) = self.getSemaphoreXY(id_2)
        if connection_x!=None:
            key  = zone + self.getZone(connection_x,connection_y)
            if key in self.link_dict:
                self.link_dict[key]+=1
            else:
                self.link_dict[key]=1
            
            self.screenshot.drawSignal(x,y)
            self.screenshot.drawLink(x,y,connection_x,connection_y)
            
            
            self.adjaceny_matrix[self.zoneIndex(zone)][self.zoneIndex(self.getZone(connection_x,connection_y))]+=1
            self.linkPositions.append([x,y,connection_x,connection_y])
        else:
            print(id_1,id_2)
            print('[INFO] HAVE A SIGNAL BUT NO CONNECTIONNNNNN!!!!!##################')
    #returns which zone a point belongs to 
    def getZone(self,x,y):
        query = [x,y]
        
        for zone in self.zones:
            if query in self.zones[zone]:
                return zone 

        
        print('[WARNING] This Point does not belong to any Marked Zone')
        return None
    
    
    
    def getAbstraction(self):
        # print("-------------- Abstraction of Current Board State ----------")
        # print(f"[INFO] The Current Game Play Level is {self.level}")
        # print(f"[INFO] The Map in this level is divided into {len(self.zones)} Zones  ")
        # print("[INFO] Number of Semaphores: ", self.nSemaphores)
        
        # print(f"[INFO] The location of the Semaphores are as follows {self.semaphorePositions}")
    
        # print("[INFO] Number of Signals:    ",self.nSignals)
        # print(f"[INFO] The location of the Signals are as follows {self.signalPositions}")
        
            
        # # print('#########################################') 
        # print("[INFO] Semaphores per Zone:  ",self.semaphore_zone_dict)
        # print("[INFO] Signals per Zone:     ",self.signal_zone_dict)
        # print("[INFO] Links :     ",self.link_dict)
     
        # print('[INFO] Adjacency Matrix Is :' )
        # for row in self.adjaceny_matrix:
        #     print(row)        
        
        
        abstraction = {
            'nSemaphores'     : self.nSemaphores,
            'nSignals'        : self.nSignals,
            'semaphore_zone_dict':self.semaphore_zone_dict,
            'signal_zone_dict':self.signal_zone_dict,
            'link_dict':self.link_dict,
        }
        
        self.screenshot.drawText(self.text)
        self.screenshot.saveImage()
        return abstraction

#------UNIT TEST -----------

#create gameState
# gameState = GameState(7,'../DATA/maps_with_zones/MapInfo_7.json')

# #CAN BE LOOPED to enter the points
# gameState.putSemaphore(9,2,"aaaaaa") 
# gameState.putSemaphore(6,3,"aaaaab")

# gameState.putSignal(4,2,"aaaaac",'aaaaab') 
# gameState.putSignal(6,0,"aaaaad","aaaaaa")




# gameState.getAbstraction()
#CHECK 1 : Is the student getting the number of semaphores right

#CHECK 2 : Is the student getting the number of signals right

#CHECK 3 : Are the seamphore counts in each zone Matching

#CHECK 4 : Are the signal counts in each zone Matching

#CHECK 5 : Are the links matching    
    