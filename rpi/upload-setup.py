import os
import sys
import socket

if __name__ == "__main__":

    # RPi 가 측정한 신호세기가 저장한 파일이 들어있는 폴더 전체를 압축
    dir_name = 'measure-1'
    tar_name = 'archieve.tar.gz'
    tar_compress_cmd = 'tar -cvf ' + tar_name + ' ' + dir_name
    os.system(tar_compress_cmd)
    assert os.path.isfile(tar_name), "Tar file does not exist!"

    sys.path.append('../')
    import common

    # 앞축 파일을 서버로 보내기
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to...', common.server_ip, common.server_port)

    try:
        cli_socket.connect((common.server_ip, common.server_port))

    except:
        assert False, 'Stop : socket connect error'

    # 파일 내용 보내기
    print('Sending file now...')
    with open(tar_name, 'rb') as fp:
        while True:
            data_to_send = fp.read(BUF_SIZE)
            if not data_to_send:
                break
            else:
                cli_socket.sendall(chunk_to_send)

    print('Finished...')
    cli_socket.close()

