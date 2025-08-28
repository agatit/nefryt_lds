import asyncio
import math
import platform
import time
from pymodbus.client import AsyncModbusTcpClient

GENERATION_TIME_SECONDS = 10000
REGISTERS = [1000, 2000]


async def _send_data(client: AsyncModbusTcpClient, addr: int, data: list[int]):
    await client.write_registers(addr, data)


def sinus(amp, freq, offset, t):
    return amp * math.sin(2 * math.pi * freq * t) + offset + amp


def sawtooth(amp, freq, offset, t):
    return amp * (((t % (1/freq)) * freq) % 1) + offset

def const_change(start, change, t):
    return start + change * t


async def main():
    tasks_list = []
    clients = [AsyncModbusTcpClient('localhost', port=502)] * len(REGISTERS)

    for client in clients:
        await client.connect()

    t = time.time()
    for it in range(GENERATION_TIME_SECONDS):
        for client, register in zip(clients, REGISTERS):
            trend_type = (register // 1000) % 4
            if trend_type == 1:
                tasks_list.append(asyncio.create_task(
                    _send_data(client, register,
                               [int(sawtooth(max(REGISTERS)+1000-register, 1/30, 0, it + i * 0.01)) for i in range(100)])
                ))
            elif trend_type == 2:
                tasks_list.append(asyncio.create_task(
                    _send_data(client, register,
                               [int(sinus(max(REGISTERS)+1-register, 1/15, 100, it + i * 0.01)) for i in range(100)])
                ))
            elif trend_type == 3:
                tasks_list.append(asyncio.create_task(
                    _send_data(client, register,
                               [int(const_change(register, 100, it + i * 0.01)) for i in range(100)])
                ))
            else:
                tasks_list.append(asyncio.create_task(
                    _send_data(client, register,
                               [int(const_change(max(REGISTERS) - register, -10, it + i * 0.01)) for i in range(100)])
                ))
        await asyncio.sleep(t - time.time() + 1)
        t = time.time()

    await asyncio.gather(*tasks_list)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
