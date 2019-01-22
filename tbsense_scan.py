from bluepy.btle import *
from bluepy import btle
import struct
from time import sleep
import threading


def scanThunderboards():
    scanner = Scanner(0)
    devices = scanner.scan(3)
    tbsense = []
    for index, dev in enumerate(devices):
        tbsense.append(
            {
                "mac_address": dev.addr,
                "mac_address_type": dev.addrType,
                "state": "disconnected",
                "lock": False,
            }
        )
    return tbsense
