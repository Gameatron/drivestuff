import os
import dotenv
import psycopg2

dotenv.load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()
os.system("wmic diskdrive get Model, SerialNumber, Size >file.txt")

def split(word):
    return [char for char in word]

skip = 1
keys = ["Model", "SerialNumber", "Size", "BadSectors"]
fi = open("file.txt")
for line in fi:
    if skip == 1:
        skip += 1
    else:
        line = split(line)
        for i in line:
            if i == '\x00':
                line.remove(i)
        word = []
        info = []
        for i in range(len(line)):
            if line[i] == ' ':
                if line[i-1] != ' ' and line[i+1] == ' ':
                    word = ''.join(word)
                    info.append(word)
                    word = []
                continue
            word.append(line[i])
        # remove_space = [x.strip(' ') for x in info]
        # delete_empty = [ele for ele in info if ele.strip()]
        res = {}
        for k in keys:
            for v in info:
                res[k] = v
                info.remove(v)
                break
        if res != {}:
            if res["SerialNumber"] != 'S0NFNEAB400506':
                try:
                    c.execute(f"INSERT INTO drives (serial, model, size, badsec) VALUES ('{res['SerialNumber']}', '{res['Model']}', '{res['Size']}', 'none')")
                    conn.commit()
                except:
                    continue
                print(f"Added drive {res['SerialNumber']} to the drive list!")
                conn.commit()
fi.close()