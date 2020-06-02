import pyttsx3
import winsound
import time
import os
import datetime
import sys
import pyowm
import tee
from io import StringIO
import py_compile

file = open('static/bin/voice/comands/opts.txt', 'r', encoding='utf-8')
sets = file.readlines()
file.close()

file2 = open('static/bin/voice/comands/answer.txt', 'r', encoding='utf-8')
com = file2.readlines()
file2.close()


class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def Decide(called):
    name = 0
    # see what user said is in which list or not
    if (called != ""):
        try:

            for x in sets[0].split(","):
                if (x == (called.split()[0])):
                    name = 1

                    cmd = called
                    for x in sets[0].split(","):
                        cmd = cmd.replace(x, "").strip()

                    if (cmd != ""):
                        cmd = recognize_cmd(cmd)
                        execute_cmd(cmd)
                    else:
                        print('Что?')

                    break

            if name == 0:
                print('У меня есть имя')

        except:
            print("Анечка тоже устаёт, она пошла спать")
    else:
        print('Я вас не слышу, вы в заложниках?')


def recognize_cmd(cmd):
    for i in range(len(sets)):
        for j in sets[i].split(","):
            if j == cmd:
                return sets[i].split(",")[0]


def execute_cmd(cmd):
    m = 0
    try:
        for i in range(len(com)):
            if cmd == com[i].split()[0]:
                i += 1
                while com[i][0][0] != ';':
                    exec(com[i])
                    i += 1
                    m = 1
                break
    except:
        print('Произошла ошибка с импортом команд из текстового документа')
        m = 1

    if m == 0:
        print('Команда не распознана')


def anya(comand):
    with OutputInterceptor() as output:
        Decide(comand)
    text = str(output).replace('[', '').replace(']', '').replace("'", '')
    return text

# py_compile.compile('voice_assistant2.py') #создаёт .pyc файл(exe python)
