# デバイスから通知を取得してみる
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.uuids import normalize_uuid_str

def print_heart_rate(sender, data: bytearray):
    # データ形式を調べる
    flags = data[0]
    index = 1
    # 心拍数が2バイトのとき
    if flags & 0x01:
        heart_rate = int.from_bytes(data[index:index+2], "little")
        index += 2
    else:
        heart_rate = data[index]
        index += 1
    print(f"Heart rate: {heart_rate}")

    # RR間隔が含まれる時
    if flags & 0x10:
        while index+2 <= len(data):
            raw_rr_interval = int.from_bytes(data[index:index+2], "little")
            index += 2
            ms_rr_interval = raw_rr_interval * 1000/1024
            print(f"RR interval: {ms_rr_interval} ms")



async def get_heart_rate(device, char_uuid):
    # PolarH10に接続するためのクライアントを作る
    async with BleakClient(device) as client:
        if client.is_connected:
            print(f"Connected to {device.name}")
            # Polar H10から通知が届いたら、print_heart_rateを実行
            await client.start_notify(char_uuid, print_heart_rate)

            while True:
                await asyncio.sleep(1)
        else:
            print(f"Failed to connect to {device.name}")

async def find_device():
    device = await BleakScanner.find_device_by_name(
    "Polar H10 01080F31"
    )
    if device is None:
        print("Device not found")
        return None
    return device

async def main():
    device = await find_device()
    if device is None:
        return
    # asyncio.get_event_loop()で実行中のイベントループを取得
    await get_heart_rate(device, char_uuid)

if __name__ == "__main__":
    # 心拍取得用のUUIDを取得
    char_uuid = normalize_uuid_str("2A37")
    # イベントループを用意し、その中でmainを実行
    asyncio.run(main())
