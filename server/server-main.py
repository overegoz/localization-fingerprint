import os, sys, pickle
import socket
import numpy as np

PRINT_DEBUG=True

class myQueue:
    _qsize = 5
    _list = []
    def __init__(self, qsize=5)
        self._qsize = sz

    def add_value(value):
        if len(self._list) < self_qsize:
            self_list.append(value)
        else:
            # 선입선출 큐와 같이 동작하도록 구현했음. 새로운 값을 추가하면 큐의 크기가 _qsize 보다
            # 더 커질 경우, 기존의 리스트에 저장된 값 중에서 가장 오래된 값을 버리고, 
            # 나머지 값들만 취해서 다시 리스트를 만들고, 그 다음에 새로운 값을 추가한다.
            self._list = self._list[1:]
            self._list.append(value)

    def get_median():
        if len(self._list) > 0:
            return np.median(self._list)
        else:
            return 0

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

    client_radio_map = []
    for ap in range(num_ap):
        client_radio_map.append(myQueue())   

    try:
        while True:
            # 클라이언트로 부터 rss 측정값을 받는다
            msgFromClient = cli_sock.recv(common.BUF_SIZE)
            # 공백문자를 기준으로 분리해 낸다
            msg_split = msgFromClient.split(common.space_delimiter)
            ind = 0  # 분리된 공백문자 리스트에서 인덱스 역할을 할 변수
            while ind < len(msg_split):
                mac_addr = msg_split[ind]
                ap_index = ap_list.index(mac_addr)
                rss = int(msg_split[ind+1])
                ind += 2  # 두개씩 한 쌍이니까, 인덱스도 한번에 두개씩 증가
                client_radio_map[ap_index].add_value(rss)  # 사용자별 radio map에 저장
            
            # 이제부터 사용자 위치추적 코드
            client_radio_map_median = []
            for ap in range(num_ap):
                client_radio_map_median.append(client_radio_map[ap].get_median())

            how_many = 1  # 가장 가까운 셀 블록 몇개를 찾을지?
            cell_blocks, distances = \
                find_closest_cell_blocks(client_radio_map_median, radio_map, how_many)

            print(cell_blocks, distances)

    except:
        print('Finishing up the server program...')
        cli_sock.close()
        svr_sock.close()
        print('Bye~')
