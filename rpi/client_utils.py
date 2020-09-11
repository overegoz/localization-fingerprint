import os, sys
import time
def get_msg2send(filename):
    sys.path.append('../')
    import common

    #print('Checking file: ', filename)
    #print('file size: ', os.path.getsize(filename))
    msg = ""
    fp = open(filename, 'r')
    lines = fp.readlines()
    #print('Lines read: ', lines)
    for line in lines:
        l = line.rstrip()
        #print('Line read : ', l)
        if len(msg) > 0:
            msg = msg + common.space_delimiter + l
        else:
            msg = l

    fp.close()

    return msg.rstrip()  # 끝에 공백 하나가 더붙어 있을 것이므로, 없애고 리턴하자

