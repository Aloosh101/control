import asyncio
from aiopylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.0.105')
    await client.connect()
    await client.set_volume(volume=0)
    while True:
        volume = await client.get_volume()
        await client.set_volume(volume=volume+1)
        if volume >= 29:
            break
    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
