from db_functions import dbh_request
from urllib import response
from fastapi import FastAPI, Request, Header, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import asyncio
import uvicorn



app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://${location.host}}/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Количество подключенных устройств:", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Количество подключенных устройств:", len(self.active_connections))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.get("/notifications")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text('ping')
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



#------------------API---------------#



@app.get("/api/notifications") #ТЕСТЫ ПРОЙДЕНЫ
async def get_notifications():

    return dbh_request('select * from notifications')


@app.get("/api/notifications/{id}") #ТЕСТЫ ПРОЙДЕНЫ
async def get_notifications(id:int = Header()):

    return dbh_request(f"select * from notifications where id = '{id}'")


@app.post("/api/notifications") #ТЕСТЫ ПРОЙДЕНЫ
async def post_notifications(type: str = Form(), title: str = Form(), content: str = Form()):

    response = dbh_request(f'insert into notifications(type, title, content) values ("{type}", "{title}", "{content}");')

    match response['status']:
        case 'OK':
            return 'Данные успешно вставлены, ', response['data']
        case _:
            return 'Ошибка, ', response['data']


@app.put("/api/notifications/{id}") #ТЕСТЫ ПРОЙДЕНЫ
async def put_notifications(id: int = Header(), type: str = Form(), title: str = Form(), content: str = Form()):

    response = dbh_request(f'update notifications set type = "{type}", title = "{title}", content = "{content}" where id = "{id}"')

    match response['status']:
        case 'OK':
            return 'Данные успешно изменены, ', response['data']
        case _:
            return 'Ошибка, ', response['data']


@app.delete("/api/notifications/{id}") #ТЕСТЫ ПРОЙДЕНЫ
async def delete_notifications(id: int):

    response = dbh_request(f'delete from notifications where id = {id}')

    match response['status']:
        case 'OK':
            return 'Данные успешно удалены, ', response['data']
        case _:
            return 'Ошибка, ', response['data']

@app.post("/api/notifications/{id}/send")
async def post_notifications_send(id: int, time:int = Form(default=0)):

    response = dbh_request(f'select * from notifications where id = {id}')

    await asyncio.sleep(time)
    await manager.broadcast(str(response['data'][0]))

    match response['status']:
        case 'OK':
            return 'Уведомление всем пользователям отправлено'
        case _:
            return 'Ошибка, ', response['data']



if __name__ == "__main__":
    uvicorn.run(app, host = 'https://notifs-api.herokuapp.com', port = 8000)

#--ЗАПУСК--#
# uvicorn app:app --ws-ping-interval=2 --ws-ping-timeout=5 --reload 
