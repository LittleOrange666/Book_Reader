import codecs
import os
import subprocess

os.chdir(os.path.dirname(__file__))
with open("data/book_dictionary", encoding="utf8") as f:
    root = f.read()
import win32api
import win32con
import json
import time

ini_str = '''
[.ShellClassInfo]\r\n
IconResource=icon.ico,0\r\n
[ViewState]\r\n
Mode=\r\n
Vid=\r\n
FolderType=Pictures\r\n
'''
Any2Ico_path = 'Quick_Any2Ico.exe'
ext = ["jpg", "jpeg", "png", "gif", "icns", "ico"]
datf = "dat.json"

if True:
    root = root.strip('"').strip("'")
    print('--->', root)
    t = 0
    if os.path.exists(datf):
        with open(datf) as f:
            dat = json.load(f)
        t = time.mktime(tuple(dat["time"]))
    ot = t
    et = t
    count = 0
    for parent, dirnames, filenames in os.walk(root):
        if not dirnames and os.path.getctime(parent)>ot:
            count+=1
            et = max(et,os.path.getctime(parent))
    okc = 0
    for parent, dirnames, filenames in os.walk(root):
        if not dirnames and os.path.getctime(parent)>ot:
            print(parent)
            first = min(p for p in os.listdir(parent) if p.split(".")[-1].lower() in ext)
            cmd = '"{0}" "-img={1}\\{2}" "-icon={1}\\icon.ico"'.format(Any2Ico_path, parent, first)
            subprocess.run(cmd)
            win32api.SetFileAttributes('{0}/icon.ico'.format(parent), win32con.FILE_ATTRIBUTE_HIDDEN)
            desktop_ini = '{0}/desktop.ini'.format(parent)
            if os.path.exists(desktop_ini):
                os.remove(desktop_ini)
            f = codecs.open(desktop_ini, 'w', 'utf-8')
            f.write(ini_str)
            f.close()
            win32api.SetFileAttributes(desktop_ini, win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
            win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY)
            okc += 1
            print(f"{okc}/{count}")
    dat["time"] = time.localtime(et);
    with open(datf, "w") as f:
        json.dump(dat,f)