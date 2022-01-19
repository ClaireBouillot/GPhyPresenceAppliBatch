import asyncio
from bleak import BleakScanner
from bleak import BleakClient

# async def main():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)
#
# asyncio.run(main())

# address = "80:0C:67:8E:9D:44"
# MODEL_NBR_UUID = "00008030-001104603CA2802E"
#
# async def main(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))
#
# asyncio.run(main(address))

import asyncio
from bleak import BleakClient
address = "80:0C:67:8E:9D:44"
MODEL_NBR_UUID = "00008030-001104603CA2802E"
async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(main(address))