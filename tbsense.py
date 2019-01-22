from bluepy import btle
from flask import jsonify
from bluepy.btle import *
import struct
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler


class Thunderboard:

    def __init__(self, addr, addrType):
        self.addr = addr
        self.addrType = addrType
        self.char = dict()
        self.session = ''
        self.coinCell = False
        self.bleService = None
        self.senseData = dict()
        self.motionData = dict()
        self.thunderboardData = dict()
        self.bleService = Peripheral()
        self.schedulers = BackgroundScheduler()

        self.bleService.connect(self.addr, self.addrType)
        self.delegate = MyDelegate(self)
        self.bleService.setDelegate(self.delegate)
        self.enableNotification()

        self.characteristics = self.bleService.getCharacteristics()

        for k in self.characteristics:
            if k.uuid == '2a6e':
                self.char['temperature'] = k

            elif k.uuid == '2a6f':
                self.char['humidity'] = k

            elif k.uuid == '2a19':
                self.char['batterylevel'] = k

            elif k.uuid == 'ec61a454-ed01-a5e8-b8f9-de9ec026ec51':
                self.char['powertype'] = k

        self.job0 = self.schedulers.add_job(self.senseDataUpdate, replace_existing=True, trigger='interval', seconds=(
            300 / 1000))
        self.job1 = self.schedulers.add_job(self.motionDataUpdate, replace_existing=True, trigger='interval', seconds=(
            300 / 1000))

        self.schedulers.start()
        self.job0.pause()
        self.job1.pause()

    def jobInit(self, sense_interval, sense_interval_unit, motion_interval, motion_interval_unit):

        self.schedulers.pause()
        self.job0.remove()
        self.job1.remove()

        if sense_interval_unit == "seconds":
            self.job0 = self.schedulers.add_job(
                self.senseDataUpdate, replace_existing=True, trigger='interval', seconds=sense_interval)
        elif sense_interval_unit == "minutes":
            self.job0 = self.schedulers.add_job(
                self.senseDataUpdate, replace_existing=True, trigger='interval', minutes=sense_interval)
        elif sense_interval_unit == "days":
            self.job0 = self.schedulers.add_job(
                self.senseDataUpdate, replace_existing=True, trigger='interval', days=sense_interval)
        elif sense_interval_unit == "weeks":
            self.job0 = self.schedulers.add_job(
                self.senseDataUpdate, replace_existing=True, trigger='interval', weeks=sense_interval)

        if motion_interval_unit == "seconds":
            self.job1 = self.schedulers.add_job(
                self.motionDataUpdate, replace_existing=True, trigger='interval', seconds=motion_interval)
        elif motion_interval_unit == "minutes":
            self.job1 = self.schedulers.add_job(
                self.motionDataUpdate, replace_existing=True, trigger='interval', minutes=motion_interval)
        elif motion_interval_unit == "days":
            self.job1 = self.schedulers.add_job(
                self.motionDataUpdate, replace_existing=True, trigger='interval', days=motion_interval)
        elif motion_interval_unit == "weeks":
            self.job1 = self.schedulers.add_job(
                self.motionDataUpdate, replace_existing=True, trigger='interval', weeks=motion_interval)

        self.schedulers.resume()

    def senseDataUpdate(self):
        self.senseUpdate()
        self.thunderboardData['powertype'] = self.senseData['powertype']
        self.thunderboardData['batterylevel'] = self.senseData['batterylevel']
        self.thunderboardData['temperature'] = self.senseData['temperature']
        self.thunderboardData['humidity'] = self.senseData['humidity']

        # self.disconnect()

    def motionDataUpdate(self):
        self.thunderboardData['Orientation_x'] = self.motionData['Orientation']['x']
        self.thunderboardData['Orientation_y'] = self.motionData['Orientation']['y']
        self.thunderboardData['Orientation_z'] = self.motionData['Orientation']['z']
        self.thunderboardData['Acceleration_x'] = self.motionData['Acceleration']['x']
        self.thunderboardData['Acceleration_y'] = self.motionData['Acceleration']['y']
        self.thunderboardData['Acceleration_z'] = self.motionData['Acceleration']['z']
        # self.disconnect()

    def readTemperature(self):
        value = self.char['temperature'].read()
        value = struct.unpack('<H', value)
        value = value[0] / 100
        return value

    def readHumidity(self):
        value = self.char['humidity'].read()
        value = struct.unpack('<H', value)
        value = value[0] / 100
        return value

    def readBatteryLevel(self):
        value = self.char['batterylevel'].read()
        value = struct.unpack('B', value)
        value = value[0]
        return value

    def waitForNotification(self):
        if self.bleService.waitForNotifications(1.0):
            print("Waiting...")

    def enableNotification(self):
        self.bleService.writeCharacteristic(
            79, (1).to_bytes(2, byteorder='little'))
        self.bleService.writeCharacteristic(
            82, (1).to_bytes(2, byteorder='little'))

    def disableNotification(self):
        self.bleService.writeCharacteristic(
            79, (0).to_bytes(2, byteorder='little'))
        self.bleService.writeCharacteristic(
            82, (0).to_bytes(2, byteorder='little'))

    def connect(self):
        self.bleService.connect(self.addr, self.addrType)
        self.delegate = MyDelegate(self)
        self.bleService.setDelegate(self.delegate)
        self.enableNotification()

        self.job0.resume()
        self.job1.resume()

    def disconnect(self):

        self.job0.pause()
        self.job1.pause()
        sleep(0.5)
        del self.delegate
        self.bleService.disconnect()

    def senseUpdate(self):
        value = self.char['powertype'].read()
        if ord(value) == 0x04:
            self.coinCell = "coinCell"
        else:
            self.coinCell = "externalPower"
        self.senseData['powertype'] = self.coinCell

        for key in self.char.keys():
            if key == 'batterylevel':
                self.senseData['batterylevel'] = self.readBatteryLevel()

            elif key == 'temperature':
                self.senseData['temperature'] = self.readTemperature()

            elif key == 'humidity':
                self.senseData['humidity'] = self.readHumidity()


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, bledevice):
        btle.DefaultDelegate.__init__(self)
        self.data = dict()
        self.bledevice = bledevice

    def handleNotification(self, cHandle, data):
        if cHandle == 81:
            result = list(struct.unpack('hhh', data))
            self.data['x'] = result[0] / float(100)
            self.data['y'] = result[1] / float(100)
            self.data['z'] = result[2] / float(100)
            self.bledevice.motionData['Orientation'] = self.data
        elif cHandle == 78:
            result = list(struct.unpack('hhh', data))
            self.data['x'] = result[0] / float(1000)
            self.data['y'] = result[1] / float(1000)
            self.data['z'] = result[2] / float(1000)
            self.bledevice.motionData['Acceleration'] = self.data
        self.data = dict()


class ThunderboardsManager:
    def __init__(self):
        self.list = []

    # template = [
    # {
    #     "mac_address": "00:00:00:00:00"
    #     "mac_address_type" : "public"
    #     "handle" : Thunderboard( , )
    #     "state" : "connected" / "disconnected"
    #     "sense_interval" :
    #     "motion_interval" :
    #     "motion_interval_unit" :
    #     "sense_interval_unit"  :
    # }
    #  .......
    # ]

    def addBoard(self, addr, addrType):
        for index, obj in enumerate(self.list):
            if obj["mac_address"] == addr:
                self.delBoard(addr)
        self.list.append({
            "mac_address": addr,
            "mac_address_type": addrType,
            "handle": Thunderboard(addr, addrType),
            "state": "connected",
            "sense_interval": 300,
            "motion_interval": 300,
            "sense_interval_unit": 'seconds',
            "motion_interval_unit": 'seconds',
        })

        return True

    def delBoard(self, addr):
        for index, obj in enumerate(self.list):
            if obj["mac_address"] == addr:
                if self.list[index]["state"] == "connected":
                    self.list[index]["handle"].disconnect()
                del self.list[index]["handle"]
                del self.list[index]
                return True
        return False

    def getBoard(self, addr):
        for index, obj in enumerate(self.list):
            if obj["mac_address"] == addr:
                return jsonify({
                    "mac_address": self.list[index]['mac_address'],
                    "state": self.list[index]['state'],
                    "sense_interval": self.list[index]['sense_interval'],
                    "motion_interval": self.list[index]['motion_interval'],
                    "sense_interval_unit": self.list[index]['sense_interval_unit'],
                    "motion_interval_unit": self.list[index]['motion_interval_unit'],
                })
        return False

    def modifyBoard(self, addr, parameter):
        interval = [0, 0, 0, 0]
        for index, obj in enumerate(self.list):
            if obj["mac_address"] == addr:
                for (key, value) in parameter.items():

                    if key == "state":
                        if value == "connected":
                            self.list[index]["handle"].connect()
                        elif value == "disconnected":
                            self.list[index]["handle"].disconnect()
                    if key == "sense_interval":
                        interval[0] = value
                    if key == "sense_interval_unit":
                        interval[1] = value
                    if key == "motion_interval":
                        interval[2] = value
                    if key == "motion_interval_unit":
                        interval[3] = value

                    self.list[index][key] = value

                if interval[0] and interval[2]:
                    self.list[index]["handle"].jobInit(
                        interval[0], interval[1], interval[2], interval[3])

                return True
        return False


manager = ThunderboardsManager()
