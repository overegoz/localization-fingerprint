import socket
import os, sys
from my_utils import build_radio_map
import pickle

USE_INTERNET_CONN = False

if __name__=="__main__":
    sys.path.append('../')
    import common

    if USE_INTERNET_CONN:  # 클라이언트로 부터 직접 데이터를 전달받음

        # 소켓 통신 준비
        svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #host = socket.gethostname()
        host = common.server_ip
        port = common.server_port
        svr_sock.bind((host, port))
        print('Waiting for connection ...')
        svr_sock.listen(5)
        cli_sock, addr = svr_sock.accept()
        print('Got connection from ...', addr)

        # 클라이언트로 부터 tar로 압축된 rss 측정 데이터 파일 받기
        with open(common.tar_name, 'wb') as fp:
            while True:
                print('Receiving data ...')            
                recv = cli_sock.recv(common.BUF_SIZE)
                if not recv:
                    break
                else:
                    fp.write(recv)

        cli_sock.close()  # 클라이언트 소켓 답기
        print('File receive... done')

        tar_uncompress_cmd = 'tar -xvf ' + common.tar_name
        os.system(tar_uncompress_cmd)  # 클라이언트로 부터 받은 압축파일 압축풀기
        print('RSS data files are ready')

        svr_sock.close()  # 서버 소켓 닫기

    else:  # 클라이언트로 부터 받지 않고, 서버 로컬에 저장된 데이터 사용
        pass

    radio_map, ap_list = build_radio_map(common.dir_name)  # radio map 만들기

    with open(common.dir_name + '/' + common.radio_map_filename, 'wb') as fp:
        pickle.dump(radio_map, fp)  # radio map을 저장하기

    print('Radio Map... dumped to file:', common.radio_map_filename)

    with open(common.dir_name + '/' + common.ap_name_filename, 'wb') as fp:
        pickle.dump(ap_list, fp)  # ap list를 저장하기

    print('AP List... dumped to file:', common.ap_name_filename)
