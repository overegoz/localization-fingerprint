import os, sys
import glob
import numpy as np

def build_radio_map(dir_name):
    sys.path.append('../')
    import common

    ap_list = get_ap_list(dir_name)  # 전체 AP 목록 가져오기
    num_ap = len(ap_list)  # AP의 갯수 파악하기
    print('Number of APs: ', num_ap)
    max_x_index, max_y_index = get_max_xy(dir_name)  # (x,y) 좌표값 중에서 각각 최대값 구하기
    print('Max X: %d, max Y: %d' % (max_x_index, max_y_index))

    # radio_map은 (y,x)로 접근해야 한다
    radio_map = []
    for y in range(max_y_index+1):
        radio_map.append([])
        for x in range(max_x_index+1):
            radio_map[y].append([])
            for ap in range(num_ap):
                radio_map[y][x].append([])

    print('a', os.getcwd())
    os.chdir(dir_name)
    print('b', os.getcwd())

    for fname in glob.glob('*.txt'):
        word_bag = fname.split(common.delimiter)
        x = int(word_bag[2])
        assert x >= 0
        y = int(word_bag[3])
        assert y >= 0

        fp = open(fname, 'r')
        while True:
            mac_addr = fp.readline().rstrip()
            if not mac_addr:
                break  # 파일을 모두 다 읽었으니, while 루프 탈출

            # 한번에 두줄 씩 읽어야 한다. 첫줄은 mac 주소, 둘째줄은 rss값
            rss = int(fp.readline())

            mac_addr_index = ap_list.index(mac_addr)
            print('(%d,%d) MAC addr index : %d' %(y,x,mac_addr_index))
            radio_map[y][x][mac_addr_index].append(rss)

        fp.close()

    # median 값으로 대체하자
    for y in range(max_y_index+1):
        for x in range(max_x_index+1):
            for ap in range(num_ap):
                rss_list = radio_map[y][x][ap]
                median_value = 0
                if len(rss_list) > 0:
                    median_value = int(np.median(rss_list))

                radio_map[y][x][ap].clear()
                radio_map[y][x][ap].append(median_value)

    print('c', os.getcwd())
    os.chdir('../')
    print('d', os.getcwd())

    return radio_map, ap_list

# 총 AP의 갯수를 카운트 하고, 각각의 MAC 주소에 인덱스 번호를 할당하자
def get_ap_list(dir_name):
    print('e', os.getcwd())
    os.chdir(dir_name)
    print('f', os.getcwd())

    ap_list = []

    # 총 AP의 갯수를 카운트 하고, 각각의 MAC 주소에 인덱스 번호를 할당하자
    for fname in glob.glob('*.txt'):
        fp = open(fname, 'r')
        while True:
            line = fp.readline()
            if not line:
                break  # 파일을 모두 다 읽었으니, while 루프 탈출
            
            if line[0] != '-':  # MAC 주소를 발견했다
                mac_addr = line.rstrip()
                print(mac_addr)
                try:
                    ap_list.index(mac_addr)

                except ValueError:
                    # ap_list에 없던, 새로운 MAC 주소다 => 추가하자
                    ap_list.append(mac_addr)
            else:
                pass  # RSS 값이다.

        fp.close()

    print('g', os.getcwd())
    os.chdir('../')
    print('h', os.getcwd())

    return ap_list

# (x,y) 좌표값 중에서 각각 최대값 구하기
def get_max_xy(dir_name):
    sys.path.append('../')
    import common

    print('i', os.getcwd())
    os.chdir(dir_name)
    print('j', os.getcwd())

    max_x, max_y = -1, -1
    # 총 AP의 갯수를 카운트 하고, 각각의 MAC 주소에 인덱스 번호를 할당하자
    for fname in glob.glob('*.txt'):
        word_bag = fname.split(common.delimiter)
        x = int(word_bag[2])
        assert x >= 0
        y = int(word_bag[3])
        assert y >= 0
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    
    print('k', os.getcwd())
    os.chdir('../')
    print('l', os.getcwd())

    assert max_x >= 0
    assert max_y >= 0

    return max_x, max_y 

#how_many = 1  # 가장 가까운 셀 블록 몇개를 찾을지?
def find_closest_cell_blocks(client_radio_map, radio_map, how_many):
    max_y, max_x = len(radio_map)-1, len(radio_map[0])-1

    # 검색을 빠르게 하기 위해 아래와 같이 추가로 3개의 list를 더 사용
    coord = []
    dist = []

    for y in range(max_y+1):
        for x in range(max_x+1):
            coord.append([y,x])
            print('at y=%d, x=%d' % (y, x))
            print('cli radio map : ', client_radio_map)
            print('this_coord_radio_map : ', radio_map[y][x])
            d = round(np.linalg.norm(np.array(client_radio_map) - np.array(radio_map[y][x])))
            print('dist : ', d)

            dist.append(d)

    # 결과 저장
    cell_blocks, distances = [], []
    for _ in range(how_many):
        min_dist = min(dist)  # 최단거리 값 구하기
        min_dist_index = dist.index(min_dist)  # 최단거리가 어느 인덱스에 저장되어 있는지?
        cell_blocks.append(coord[min_dist_index])  # 해당 인덱스의 좌표값 가져오기
        distances.append(dist[min_dist_index])  # 해당 인덱스와의 거리값 가져오기
        # 큰 값으로 바꿔놓으면, 다음 iteration에서는 두번째로 작은 거리값을 찾을 수 있지
        dist[min_dist_index] = sys.maxsize  

    return cell_blocks, distances