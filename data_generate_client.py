from multiprocessing import Process
from multiprocessing import Queue
import random
import websockets
import time 
import asyncio

class SendData:
    def __init__(self, q):
        self.queue = q
        self.data = 0
        # self.connect()

    # def connect(self):
    #     self.ws = websockets.connect('ws://localhost:8765')
    #     print(self.ws)

    async def send(self):
        while True:
            self.data = self.queue.get()
            print("sonProcess:", self.data)
            async with websockets.connect('ws://localhost:8765') as websocket:
                await websocket.send(str(self.data))
                print("send:", self.data)
                # await asyncio.sleep(1)

                msg = await websocket.recv()
                print("recv:", msg)
                # await asyncio.sleep(1)

    async def recv(self):
        while True:
            print('-----------')
            await asyncio.sleep(0.01)
            # async with websockets.connect('ws://localhost:8765') as websocket:
            #     msg = await websocket.recv()
            #     print("recv:", msg)
            #     await asyncio.sleep(1)

async def start_com(q):
    messager = SendData(q)
    time.sleep(1)

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(messager.send())
        task2 = tg.create_task(messager.recv())

    '''
    method 2
    task1 = asyncio.create_task(messager.send())
    task2 = asyncio.create_task(messager.recv())
    await task1
    await task2
    '''

    # asyncio.get_event_loop().run_until_complete(messager.send())
    # asyncio.get_event_loop().run_until_complete(messager.recv())
    # print('-----------------------------------------------------------')

    # print("child: waiting for data")
    # while True:
    #     _data = q.get()
    #     print("child:", _data)

def main(q):
    asyncio.run(start_com(q))

if __name__ == "__main__":
    q = Queue()
    
    com_process = Process(target = main, args = (q,), daemon = True)
    com_process.start()

    time.sleep(1)   # wait for child process to start

    for i in range(3):
        time.sleep(0.5)
        data = random.randint(0, 1000)
        q.put(data)   
        print("parent:", data)
    isEmpty = q.empty()

    # 加锁保证最后一个数据正常发送
    while not isEmpty:
        time.sleep(2)
        isEmpty = q.empty()