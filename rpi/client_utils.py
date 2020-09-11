import os, sys

def get_msg2send(filename):
    sys.path.append('../')
    import common

    msg = ""
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline().rstrip()
            if not line:
                break

            msg = msg + common.space_delim + line

    return msg.rstrip()  # 끝에 공백 하나가 더붙어 있을 것이므로, 없애고 리턴하자

