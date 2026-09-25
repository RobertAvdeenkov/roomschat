from datetime import datetime

class Connections:
    def __init__(self,name, cons, history, id):
        self.name=name
        self.id=int(id)
        self.cons=list()
        self.history=list()

    async def connect(self, websocket):
        await websocket.accept()
        active=''
        for i in self.cons:
            active+=f'{i.scope['client'][0]}<br>'
        await websocket.send_text(
            f'''
            Добро пожаловать в чат!<br>
            Список активных пользователей:
            {active}
            '''
        )
        self.cons.append(websocket)
        for i in self.history:
            await websocket.send_text(i)

    async def disconnect(self, websocket):
        try:
            self.cons.remove(websocket)
        finally:
            for i in self.cons:
                await i.send_text(f'Участник вышел')

    async def receive(self, websocket):
        while True:
            data=await websocket.receive_text()
            date=datetime.now()
            for i in self.cons:
                await i.send_text(f'{date.hour}:{date.minute} '+data)
            self.history.append(data)
    