from datetime import datetime

class Connections:
    def __init__(self,name, cons, history, id,creator):
        self.name=name
        self.id=int(id)
        self.creator=creator
        self.cons=list()
        self.nicklist=list()
        self.history=list()

    async def connect(self, websocket, nickname):
        await websocket.accept()
        date=datetime.now()
        jointext=f'{date.hour}:{date.minute if date.minute>9 else f'0{date.minute}'} {nickname} присоединился'
        for i in self.cons:
            await i.send_text(jointext)
        self.history.append(jointext)
        active=''
        for i in self.nicklist:
            active+=f'<button style="padding: 0px; background-color: transparent;" onclick="appeal(`{i}`)">{i}</button><br>'
        self.cons.append(websocket)
        self.nicklist.append(nickname)
        for i in self.history:
            await websocket.send_text(i)
        await websocket.send_text(
            f'''
            Добро пожаловать в чат, {nickname}!<br>
            Список активных пользователей:
            {active if active else 'Пользователей пока нет!'}
            '''
        )

    async def disconnect(self, websocket, nickname):
        date=datetime.now()
        try:
            self.cons.remove(websocket)
            self.nicklist.remove(nickname)
        finally:
            for i in self.cons:
                await i.send_text(f'{date.hour}:{date.minute if date.minute>9 else f'0{date.minute}'} {nickname} вышел')
            self.history.append(f'{date.hour}:{date.minute if date.minute>9 else f'0{date.minute}'} {nickname} вышел')

    async def receive(self, websocket, nickname):
        while True:
            data=await websocket.receive_text()
            date=datetime.now()
            txt=''
            for index,i in enumerate(data):
                if index%50==0 and index!=0:
                    txt+='<br>'+i
                else: txt+=i
            txt+=f'<br>{date.hour}:{date.minute if date.minute>9 else f'0{date.minute}'}'
            txt=f'<button style="padding: 0px; background-color: transparent;" onclick="appeal(`{nickname}`)">{nickname}</button><br>'+txt
            for i in self.cons:
                await i.send_text(txt)
            self.history.append(txt)
    