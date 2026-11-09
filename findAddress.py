import asyncio
from bleak import BleakScanner

async def main():
    # 10秒でBLEを探索 見つかったデバイスをリストに格納
    devices = await BleakScanner.discover(timeout=10)
    for device in devices:
        print(f"名前: {device.name}")
        print(f"アドレス: {device.address}")
        print("--------------------")
    
    if len(devices) == 0:
        print("見つかりませんでした")

asyncio.run(main())