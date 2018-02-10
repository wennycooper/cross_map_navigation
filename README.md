# Cross Map Navigation 
This repository is for robot to navigate cross multuple maps.
The algorothm of abstract route planning is based on Dijkstra.

## Protocol

>Subscribers
```
/hotelGoal String
/checkEVcb Bool
/enterEVcb Bool
/alightEVcb Bool
/emergentStop Bool
/elevatorCB Bool
```

>Publisher
```
/enterEV Bool
/alightEV Bool
/map_server/reload String
/hotelGoalCB String
/hotelGoalReach String
/callEV Int16
/doorOpen Bool
/doorClose Bool
```

## Architecture
![architecture](https://github.com/advancedroboticsaws/cross_map_navigation/blob/master/pics/architecture.jpg)

## Dijkstra Map
![dijkstra](https://github.com/advancedroboticsaws/cross_map_navigation/blob/master/pics/dijkstra.jpg)

## Take elevator Process
![process](https://github.com/advancedroboticsaws/cross_map_navigation/blob/master/pics/process.jpg)





