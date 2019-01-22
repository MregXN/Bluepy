from tbsense_scan import scanThunderboards
from tbsense import manager



if __name__ == "__main__":
    while True:
        print("input 'scan' to get thunderboard devices around you")
        x = input()
        if x == "scan":
            print("the devices are as fellow")
            print(scanThunderboards())
            print("input mac addr to connect the devices")
            x = input()
            print("input addr type of yuor device")
            y= input()
            manager.addBoard(x, y)
            thunderboardData = dict()
            for index, obj in enumerate(manager.list):
                if obj["mac_address"] == x:
                    thunderboardData['Acceleration_x'] = manager.list[index]['handle'].thunderboardData['Acceleration_x']
                    thunderboardData['Acceleration_y'] = manager.list[index]['handle'].thunderboardData['Acceleration_y']
                    thunderboardData['Acceleration_z'] = manager.list[index]['handle'].thunderboardData['Acceleration_z']
                    thunderboardData['Orientation_x'] = manager.list[index]['handle'].thunderboardData['Orientation_x']
                    thunderboardData['Orientation_y'] = manager.list[index]['handle'].thunderboardData['Orientation_y']
                    thunderboardData['Orientation_z'] = manager.list[index]['handle'].thunderboardData['Orientation_z']
            print(thunderboardData)

        else:
            print("please input again")
