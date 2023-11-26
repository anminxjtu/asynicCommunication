import asyncio
import websockets
from multiprocessing import Process

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

def server_run():
    asyncio.run(main())

if __name__ == "__main__":
    com_process = Process(target = server_run, daemon = False)
    com_process.start()

    print("------------------")

