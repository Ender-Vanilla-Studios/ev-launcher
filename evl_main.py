from tkinter import *
from tkinter import ttk
from uuid import uuid1
from PIL import Image, ImageTk
from dotenv import load_dotenv, set_key
import os
import threading
import sys
import webbrowser
import minecraft_launcher_lib
import subprocess
import re
import platform
# test
evlversion = "0.9.6_PRE2"
env_file = '.env'
news_url = "https://www.minecraft.net/ru-ru/articles"
banned_keywords = ["LGBT", "pride", "rainbow", "queer", "gay", "lesbian", "trans"]
load_dotenv()

if not os.getenv('evlicense') == '1':
    print("Вы отказались от лицензии")
    sys.exit()

if os.getenv('evlstop')== '1':
    sys.exit()

def stop():
    evtk.destroy()
    sys.exit()

print("Главное меню запущенно")
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    if iteration == total:
        print()

def maximum(max_value, value):
    max_value[0] = value

max_value = [0]

callback = {
    "setStatus": lambda text: print(text),
    "setProgress": lambda value: printProgressBar(value, max_value[0]),
    "setMax": lambda value: maximum(max_value, value)
}

def callbackV2():
    pass

fabric_loader_version = minecraft_launcher_lib.fabric.get_latest_loader_version()

def settings_w():
    subprocess.Popen(['python', 'evl_settings.py'])

def sett_thread():
    threadsett = threading.Thread(target=settings_w)
    threadsett.start()

evtk = Tk()
evtk.title("EV Launcher v" + evlversion)
evtk.iconbitmap(default="assets/ev-launcher_a.ico")
evtk.geometry("300x400")

usernameumol = ""

if os.getenv('nickname') in ('', None):
    usernameumol = ""
else:
    usernameumol = os.getenv('nickname')

entusername = Entry()
entusername.insert(0, usernameumol)
entusername.place(x=10, y=275)
entusername.configure(width=46)

versions = ["1.20.1"]
versions_var = StringVar(value=versions[0])

vcombobox = ttk.Combobox(textvariable=versions_var, values=versions)
vcombobox.place(x=10, y=300)
vcombobox.configure(width=43, height=2)

versionc = str(vcombobox.get())
minecraft_directoryc = ".ev-game"

if os.getenv('custDirectory') == "0":
    pass
else:
    minecraft_directoryc = str(os.getenv('Directory'))

prvalue_var = IntVar(value=0)

progressbar = ttk.Progressbar(orient="horizontal", variable=prvalue_var, length=280, maximum=1)
progressbar.place(x=10, y=325)

label = ttk.Label(textvariable=str(prvalue_var) + "%")
label.place(x=270, y=325)

def launch_game():
    if os.getenv('evlicense') == '0':
        print("Вы отказались от лицензии")
        sys.exit()

    minecraft_launcher_lib.fabric.install_fabric(str(versions_var.get()), minecraft_directory=minecraft_directoryc, callback=callback)
    print("Файлы успешно установлены")
    acesstoken = os.getenv('accestoken')
    custRel = os.getenv('custRel')
    custRelB = False
    username = entusername.get()
    ram_for_java = os.getenv('ram_for_java')
    set_key(env_file, 'nickname', username)
    if ram_for_java is not int:
        ram_for_java = 2048

    if entusername.get() == "":
        username = "Player"

    ip_s = ""
    if str(os.getenv('use_ua_dom')) == "1":
        ip_s = "95.216.30.27"
    else:
        ip_s = "je.ender-vanilla.ru"

    access_allowed = True
    for keyword in banned_keywords:
        if re.search(keyword, username.lower()):
            access_allowed = False
            break

    if access_allowed:
        pass
    else:
        print("Доступ запрещен")
        sys.exit()

    if custRel == 1:
        custRelB = True
    else:
        custRelB = False

    options = {
        'username': str(username),
        'uuid': str(uuid1()),
        'token': str(acesstoken),
        "server": str(ip_s),
        "port": "25801",
        "jvm Arguments": ["-Xincgc", "-Xmx" + str(ram_for_java) + "M", "-Xms256M"],
        "launcher Name": "EV-Launcher",
        "launcher Version": evlversion,
        "gameDirectory": minecraft_directoryc,
        "demo": False,
        "customResolution": custRelB,
        "resolutionWidth": os.getenv('custWidth'),
        "resolutionHeight": os.getenv('custHeight')
    }

    print("Запуск Minecraft")
    subprocess.call(
        minecraft_launcher_lib.command.get_minecraft_command(version="fabric-loader-" + fabric_loader_version + "-" + str(versions_var.get()), minecraft_directory=minecraft_directoryc,
                                                             options=options))

def launch_thread():
    threadlau = threading.Thread(target=launch_game)
    threadlau.start()

def open_lasted_log():
    subprocess.call(['python', 'evl_latest_log.py'])

def open_news_mc():
    webbrowser.open_new(news_url)

def open_folder():
    system = platform.system()
    folder_name = ".ev-game"

    if not os.path.exists(folder_name):
        print(f"Папка '{folder_name}' не существует.")
        return

    try:
        if system == "Windows":
            os.startfile(folder_name)
        elif system == "Darwin":
            subprocess.run(["open", folder_name])
        elif system == "Linux":
            subprocess.run(["xdg-open", folder_name])
        else:
            print("Неизвестная операционная система. Папка не может быть открыта.")
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")

btn = Button(text="СТАРТ", command=launch_thread, activebackground="#0a8b2e", background="green")
btn.place(x=10, y=350)
btn.configure(width=35, height=2)

img = PhotoImage(file="assets/mc_title_.png")

original_image = Image.open("assets/folder.png")
resized_image = original_image.resize((35, 35), Image.Resampling.LANCZOS)
imgfolder = ImageTk.PhotoImage(resized_image)

btn3 = Button(command=open_folder, image=imgfolder)
btn3.place(x=250, y=350)
btn3.configure(width=35, height=35)

btnnews = Button(text="НОВОСТИ МАЙНКРАФТА", command=open_news_mc)
btnnews.place(x=0, y=0)
btnnews.configure(width=22, height=1)

btns = Button(text="НАСТРОЙКИ", command=sett_thread, activebackground="#c8c8c8")
btns.place(x=165, y=0)

btnd = Button(text="ВЫЙТИ", command=stop, activebackground="#cd0000", background="red")
btnd.place(x=250, y=0)

evtk.mainloop()