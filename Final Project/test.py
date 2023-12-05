# grabbed from https://github.com/hbldh/bleak/blob/develop/examples/uart_service.py
import asyncio
import sys

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

states = [b'[1,2]',b'[1,2]',b'[1,2]', b'[1,2]', b'[1,2]']

async def uart(name = 'Fred'):
    """This sends info back and forth"""
    names = []
    def match_name(device, adv):
        if not adv.local_name in names:
            names.append(adv.local_name) #make a list of all BLE devices seen
            print(adv.local_name)
        return adv.local_name == name #is this the right one?

    device = await BleakScanner.find_device_by_filter(match_name)

    if device is None:
        print("no matching device found, check the name.")
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        print("received:", data)

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        loop = asyncio.get_running_loop()
        service = client.services.get_service(UART_SERVICE_UUID)
        rx_char = service.get_characteristic(UART_RX_CHAR_UUID)
        
        i = 0
        while True:  # cycle through all 5 possible states
            data = states[i]
            await client.write_gatt_char(rx_char, data, response=False)
            i = i+1 if i<4 else 0
            print("sent:", data)
            await asyncio.sleep(3)


if __name__ == "__main__":
    try:
        asyncio.run(uart('Fred'))
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
    