import asyncio
from aiopylgtv import WebOsClient

async def runloop():
    client = await WebOsClient.create('192.168.0.105')
    await client.connect()
    # Get the current volume level
    #volume = await client.get_volume()
    #await client.set_volume(15)
    a=await client.get_apps()
    print(a.json)
    await client.disconnect()

asyncio.get_event_loop().run_until_complete(runloop())
