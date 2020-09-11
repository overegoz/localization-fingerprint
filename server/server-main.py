import os, sys, pickle
import socket

PRINT_DEBUG=True

def load_pickle(pickle_filename):
    with open(pickle_filename,'rb') as fp:
        data = pickle.load(fp)
    return data
    

if __name__=="__main__":
    sys.path.append('../')
    import common

    # radio map 정보 불러오기
    pickle_filename = common.dir_name + '/' + common.radio_map_filename
    radio_map = load_pickle(pickle_filename)
    print('Radio map load...done')


    # AP 목록 불러오기
    pickle_filename = common.dir_name + '/' + common.ap_name_filename
    ap_list = load_pickle(pickle_filename)
    print('AP list load...done')

    # 디버깅을 위해서 화면에 출력
    max_y, max_x = len(radio_map)-1, len(radio_map[0])-1
    num_ap = len(radio_map[0][0])
    if PRINT_DEBUG:
        print('Max-Y: %d, Max-X: %d, N_AP: %d' % (max_y, max_x, num_ap))

        for y in range(max_y+1):
            for x in range(max_x+1):
                for ap in range(num_ap):
                    ap_mac = ap_list[ap]
                    print('y=%d, x=%d, ap=%s, rss=%d' \
                          % (y, x, ap_mac, int(radio_map[y][x][ap][0])))

    # 클라이언트와의 소켓 통신 준비
    svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = common.server_ip
    port = common.server_port
    svr_sock.bind((host, port))
    print('Waiting for connection ...')
    svr_sock.listen(5)
    cli_sock, addr = svr_sock.accept()
    print('Got connection from ...', addr)
    
