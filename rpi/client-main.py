import sys
import os
import time
import client_utils

if __name__ == "__main__":

    sys.path.append('../')
    import common

    out_dir = 'measure' + common.delimiter + '1'  # 신호세기 측정 결과를 파일로 저장할 건데, 이런 파일들을 모아 둘 폴더 이름
    if os.path.isdir(out_dir) == False:  # 만약, 디렉토리가 존재하지 않으면
        os.mkdir(out_dir)

    out_filename_base = out_dir + '/' + 'client-measure-realtime'
    wifi_dev_name = 'wlan0'
    scan_cmd_base =  "sudo iwlist " + wifi_dev_name + " scan | grep -E 'level|Address' | sed 's/level=//' | awk '{ if ( $1 == \"Cell\" ) { print $5 } if ( $2 == \"Signal\" ) { print $3 } }'"
   
    # 클라이언트 소켓 생성   
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to...', common.server_ip, server_port)

    # 서버에 연결 시도
    try:
        cli_socket.connect((common.server_ip, common.server_port))
        print('Connected to the server...')
    except:
        assert False, 'Stop: socket connection error'

    tx_counter=0  # 서버로 몇번 전송했는지를 계산할 카운터 변수
    try:
        while True:
            print('Counter : ', tx_counter)  # 디버깅을 위한 터미널 출력

            # 근처의 모든 AP의 RSS값을 스캔해서 파일로 저장
            out_filename_now = out_filename_base + common.delimiter + str(tx_counter) + '.txt'
            scan_cmd_now = scan_cmd_base + ' > ' + out_filename_now
            os.system(scan_cmd_now)
    
            # 저장한 파일을 읽어서, 메시지로 변환 후 서버로 전송
            msg2send = get_msg2send(out_filename_now)
            cli_socket.sendall(bytes(msg2send, "utf-8"))
            
            # 1초간 대기
            time.sleep(common.sleep_sec)  # sleep 하는 것이 안정성 면에서 좋다.

    except:  # 클라이언트에서 ctrl+c로 종료하도록 하고, 이때 소켓을 닫도록 코딩함.
        cli_socket.close()
