# websocket-thingy
**Команда для запуска**:
uvicorn app:app --ws-ping-interval=2 --ws-ping-timeout=5 --reload 

Для хоста на локальном устройстве необходимо изменить 153 строку файла app.py

"if __name__ == "__main__":
    uvicorn.run(app, host = 'https://notifs-api.herokuapp.com', port = 1337)"
  
на

"if __name__ == "__main__":
    uvicorn.run(app, host = 'localhost', port = <ваш порт>)"
    
