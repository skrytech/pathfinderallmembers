# coding: utf8
import os
import zipfile as zf
import tempfile
import shutil

back = 1
RC = 'RemoteCompanions'
PC = 'PartyCharacters'
# defpath = os.getcwd()
with open('path.txt') as p:
    defpath = p.read()
os.chdir(defpath)
fn = 'player.json'
files = os.listdir(defpath)
# создание папки бекапов
if 'backup' not in files:
    os.mkdir('backup')
# выбор самого нового сохранения по дате
p = 0
while p == 0:
    p = 1
    for k in files:
        if not k.endswith(".zks"):
            files.remove(k)
            p = 0
fp = max(files, key=os.path.getctime)
fpp = fp[0:len(fp) - 4]

with tempfile.TemporaryDirectory() as lol:
    os.mkdir(lol + '/1')
    # print('Создана временная директория %s' % lol)
    # разархивирование сохранения во временную директурию
    z = zf.ZipFile(fp, mode='r')
    z.extractall(lol + '/1')
    z.close()
    # создание бекапа
    files = os.listdir('backup/')
    if files == []:
        shutil.copy(fp, 'backup/' + fp + '.backup' + str(back))
    # print(files)
    # нумерация бекапа
    for k in files:
        if back <= int(k[(k.rfind('backup') + 6):]):
            back = int(k[(k.rfind('backup') + 6):]) + 1
    shutil.copy(fp, 'backup/' + fp + '.backup' + str(back))
    files = os.listdir('backup/')
    # удаление старого шестого бекапа
    if len(files) == 6:
        b = int(files[1][(files[1].rfind('backup') + 6):])
        for k in files:
            if b >= int(k[(k.rfind('backup') + 6):]):
                j = k
                b = int(k[(k.rfind('backup') + 6):])
        os.remove('backup/' + j)
        os.remove(fp)
    os.chdir(lol)
    # print(os.listdir(lol + '/1'))
    # редактирование файла со спутниками
    with open(lol + '/1/' + fn, 'r', encoding="utf8") as party:
        a = party.read()
        f = a.find(PC)
        d = a[f:]
        ff = d.find(RC)
        fff = d.find(']', ff)
        if d[fff - 1] == '[':
            # ничего не делать, если нет спутников в запасе
            pass
        else:
            a = a[0:f]
            g = d[ff + 19:fff]
            d = d[0:ff + 19] + d[fff:]
            fff = d.find(']')
            d = d[0:fff] + ',' + g + d[fff:]
            a = a[0:f] + d
    # запись в файл
    with open(lol + '/1/' + fn, 'w', encoding="utf8") as party:
        party.write(a)
    # архивация файлов сохранения
    z = zf.ZipFile(fp, mode='w')
    files = os.listdir('1')
    # print(files)
    for k in files:
        z.write('1/' + k, k)
    z.close()
    # print(os.listdir())
    with open(lol + '/1/' + fn, 'r', encoding="utf8") as party:
        print(party.read())
    # копирование архива в папку сохранения
    shutil.copy(fp, defpath + '/' + fp)
    os.chdir(defpath)
