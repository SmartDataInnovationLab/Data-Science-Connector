import uvicorn
import asyncio
from time import sleep

from app.main import main, periodic

app = main()

PERIODIC_TICK = 1

def periodic_task():
    while True:
        sleep(PERIODIC_TICK)
        try:
            periodic()
        except Exception as e:
            print(e)

def server():
    uvicorn.run(app=app, host="0.0.0.0", port=8090)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_in_executor(None, periodic_task)
    loop.run_in_executor(None, server)
    

