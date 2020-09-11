import os, sys, pickle
import socket
import numpy as np
from server_utils import find_closest_cell_blocks

PRINT_DEBUG=True

class myQueue:
    _qsize = 3
    _list = []
    def __init__(self, qsize=3):
        self._qsize = qsize

    def add_value(self, value):
        print('adding...', value)
        if len(self._list) < self._qsize:
            self._list.append(value)
        else:
            # 선입선출 큐와 같이 동작하도록 구현했음. 새로운 값을 추가하면 큐의 크기가 _qsize 보다
            # 더 커질 경우, 기존의 리스트에 저장된 값 중에서 가장 오래된 값을 버리고, 
            # 나머지 값들만 취해서 다시 리스트를 만들고, 그 다음에 새로운 값을 추가한다.
            self._list = self._list[1:]
            self._list.append(value)

        return self.get_median()

    def get_median(self):
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
    pickle_filename = common.dir_name_outcome + '/' + common.radio_map_filename
    radio_map = load_pickle(pickle_filename)
    # shape을 변경해 주자. 그래야 나중에 euc norm 계산할때 문제 안생김
    for y in range(len(radio_map)):
        for x in range(len(radio_map[0])):
            for ap in range(len(radio_map[0][0])):
                radio_map[y][x][ap] = radio_map[y][x][ap][0]
    print('Radio map load...done')


    # AP 목록 불러오기
    pickle_filename = common.dir_name_outcome + '/' + common.ap_name_filename
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
                          % (y, x, ap_mac, int(radio_map[y][x][ap])))

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
        client_radio_map.append(myQueue(5))   
    print('client_radio_map len: ', len(client_radio_map))

    #try:
    while True:
        # 클라이언트로 부터 rss 측정값을 받는다
        msgFromClient = cli_sock.recv(common.BUF_SIZE)
        msgFromClient = str(msgFromClient.decode("utf-8"))
        print('msg received from cli :', msgFromClient)


        # 공백문자를 기준으로 분리해 낸다
        msg_split = msgFromClient.split(common.space_delimiter)
        for i in range(len(msg_split)):
            msg_split[i] = msg_split[i].rstrip()  # 끝에있는 개행문자 제거

        #print('cli msg split ... done')
        ind = 0  # 분리된 공백문자 리스트에서 인덱스 역할을 할 변수

        # 이번에 데이터를 수신한 AP를 표시해 두기 위해서 체크용도의 리스트를 만든다
        ap_check_if_received = np.zeros(num_ap)
        while ind < len(msg_split):
            #print('let us get it done with ', msg_split[ind], msg_split[ind+1])
            mac_addr = msg_split[ind]
            try:
                ap_index = ap_list.index(mac_addr)
                rss = int(msg_split[ind+1])
                #print('mac, ap, rss : ', mac_addr, ap_index, rss)
                new_median = client_radio_map[ap_index].add_value(rss)  # 사용자별 radio map에 저장
                #print('New median for ap(%d) : %d' % (ap_index, new_median))
                ap_check_if_received[ap_index] = 1
            except:
                # 사전측정 과정에서 탐지하지 못한 ap가 실시간으로 측정중에 탐지될 수 있는데
                # 이 경우는 그냥 무시하고 지나가야 함
                pass

            ind += 2  # 두개씩 한 쌍이니까, 인덱스도 한번에 두개씩 증가
        
        # cli가 측정 못한 ap에 대해서는 0 이라는 값을 넣어줘야지
        for ap_index in range(num_ap):
            if ap_check_if_received[ap_index] == 0:
                new_median = client_radio_map[ap_index].add_value(0)  # 사용자별 radio map에 저장
                #print('New median for ap(%d) : %d' % (ap_index, new_median))
                ap_check_if_received[ap_index] = 1

        #print('cli radio map update... done')

        # 이제부터 사용자 위치추적 코드
        client_radio_map_median = []
        for ap in range(num_ap):
            client_radio_map_median.append(client_radio_map[ap].get_median())

        print('cli radio map update...', client_radio_map_median)

        how_many = 1  # 가장 가까운 셀 블록 몇개를 찾을지?
        cell_blocks, distances = \
            find_closest_cell_blocks(client_radio_map_median, radio_map, how_many)

        #print(cell_blocks, distances)
        print('BEST: cell blocks (y,x) :', cell_blocks)
        print('BEST: distances : ', distances)

    #except:
    print('Finishing up the server program...')
    cli_sock.close()
    svr_sock.close()
    print('Bye~')
