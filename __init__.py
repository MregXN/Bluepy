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
        else:
            print("please input again")
