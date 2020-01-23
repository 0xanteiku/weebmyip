import os
import time
import random
from config import del_ipfiles, home_dir

random_one = random.choice(['', '.1'])
random_two = random.choice(['', '.1', '.2'])
random_four = random.choice(['', '.1', '.2', '.3', '.4'])


def WeebGen(IP):
    ip = IP.split('.')
    dot = open(home_dir+'audio/phrases/dot'+random_one+'.mp3', 'rb').read()
    YIPIS = open(home_dir+'audio/phrases/YIPIS'+random_two+'.mp3', 'rb').read()
    senpai = open(home_dir+'audio/phrases/senpai'+random_two+'.mp3', 'rb').read()
    baka = open(home_dir+'audio/phrases/baka'+random_one+'.mp3', 'rb').read()
    uwu = open(home_dir+'audio/phrases/uwu'+random_four+'.mp3', 'rb').read()
    final_ip = bytearray()
    count = 1
    for i in ip:
        final_ip += open(home_dir+'audio/nums/'+i+'.mp3', 'rb').read()
        if count != 4:
            final_ip += dot
            count += 1
    null = bytearray()
    joined = random.choice([senpai, null, baka, uwu]) + YIPIS + final_ip
    open(home_dir+'static/generated/'+IP.replace('.', '-')+'.mp3', 'wb').write(joined)


def WeebDel(IP):
    time.sleep(del_ipfiles)
    os.remove(home_dir+'static/generated/'+IP.replace('.', '-')+'.mp3')
