from fastapi import APIRouter,Query,WebSocket,WebSocketException
from connection import Connections
from fastapi.responses import Response,RedirectResponse,FileResponse
import sys

id=0

rooms=[]

router=APIRouter()

@router.get('/')
async def mainpage():
    return FileResponse('templates/mainpage.html')

@router.post('/append')
async def add_room(name=Query()):
    global id
    target=Connections(name=name,cons=[], history=[], id=id)
    id+=1
    rooms.append(target)
    return {'status':'success'}

@router.get('/rooms')
async def roomsSHOW():
    return {'rooms': [{'id': room.id, 'name': room.name} for room in rooms]}

@router.get('/room')
async def room(id:int):
    return FileResponse('templates/room.html')

@router.websocket('/ws/{id}')
async def ws(websocket:WebSocket, id:int):
    for i in rooms:
        if i.id==id:
            print(websocket.state)
            await i.connect(websocket)
            try:
                await i.receive(websocket)
            except:
                await i.disconnect(websocket)
                return 


