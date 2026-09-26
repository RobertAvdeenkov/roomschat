from fastapi import APIRouter,Query,WebSocket,WebSocketException,Cookie,HTTPException
from connection import Connections
from fastapi.responses import Response,RedirectResponse,FileResponse
import sys
from urllib.parse import unquote

id=0

rooms=[]

router=APIRouter()

@router.get('/')
async def mainpage():
    return FileResponse('templates/mainpage.html')

@router.post('/append')
async def add_room(name=Query(), nickname=Cookie()):
    global id
    if len(name)>50:
        raise HTTPException(400,'Название должно быть меньше 50 символов!')
    target=Connections(name=name,cons=[], history=[], id=id, creator=nickname)
    id+=1
    rooms.append(target)
    return {'status':'success'}

@router.get('/rooms')
async def roomsSHOW():
    return {'rooms': [{'id': room.id, 'name': f'{room.name} от владельца {room.creator}'} for room in rooms]}

@router.get('/room')
async def room(id:int, nickname=Cookie()):
    return FileResponse('templates/room.html')

@router.websocket('/ws/{id}')
async def ws(websocket:WebSocket, id:int, nickname=Cookie()):
    name=nickname
    for i in rooms:
        if i.id==id:
            await i.connect(websocket,name)
            try:
                await i.receive(websocket,name)
            except:
                await i.disconnect(websocket,name)
                return 


