import os
import dotenv
import psycopg2
from pySMART import Device
dri = Device('C:\\')
print(dri)

dotenv.load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Drive:
    def __init__(self, serial, model, size, bad):
        self.serial = serial
        self.model = model
        self.size = size
        self.bad = bad
        self.info = {"Serial Number": self.serial,
                     "Model Number": self.model,
                     "Size": self.size,
                     "Bad Drive": self.bad}
    
    def __str__(self):
        return str(self.info)
print(devlist)
while True:
    ans = input("Would you like to (v)iew a drive, (a)dd a drive manually, or (c)ancel?\n> ")
    if ans.lower() == 'v':
        ans = input("Please enter the serial number of the drive.\n> ")
        c.execute(f"SELECT * FROM drives WHERE serial='{ans}'")
        row = c.fetchall()
        drive = Drive(row[0][0], row[0][1], row[0][2], row[0][3])
        print(drive)
    elif ans.lower() == 'a':
        serial = input("Please enter the serial number.\n> ")
        c.execute(f"SELECT * FROM drives WHERE serial='{serial}'")
        row = c.fetchall()
        if row != []:
            print("That drive is already added.", end=' ')
            continue
        model = input("Please enter the model of the drive.\n> ")
        size = input("Please enter the size of the drive in bytes.\n> ")
        bad = input("Is this a bad drive? (Y/N/U)\n> ")
        if bad.lower() == 'y':
            badsec = "True"
        elif bad.lower() == 'n':
            badsec = "False"
        else:
            badsec = "none"
        drive = Drive(serial, model, size, badsec)
        print(drive)
        c.execute(f"INSERT INTO drives (serial, model, size, badsec) VALUES ({drive.serial}, {drive.model}, {drive.size}, {drive.bad})")
        conn.commit()
        print(f"Added drive {drive.serial} to the database.")
    elif ans.lower() == 'c':
        quit()