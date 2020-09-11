import sys
import os
import time
import shutil

if __name__ == "__main__":

    sys.path.append('../')
    import common

    # 프로그램 실행 시, 인자값이 충분히 들어왔는지 체크
    if len(sys.argv) != 4:
        assert False, '[ERROR] usage : python3 file.name x y n'

    x_coord = sys.argv[1]  # x 값 (현실 좌표 아님)
    y_coord = sys.argv[2]  # y 값 (현실 좌표 아님)
    n_repeat = int(sys.argv[3])  # 신호세기 측정을 몇 번 할 것인지

    # common.dir_name 신호세기 측정 결과를 파일로 저장할 건데, 이런 파일들을 모아 둘 폴더 이름
    if os.path.isdir(common.dir_name_measurement) == False :  # 만약, 디렉토리가 존재하지 않으면
        os.mkdir(common.dir_name_measurement)

    out_filename_base = common.dir_name_measurement + '/' + 'client-measure' + common.delimiter + x_coord + common.delimiter + y_coord
    wifi_dev_name = 'wlan0'
    scan_cmd_base =  "sudo iwlist " + wifi_dev_name + " scan | grep -E 'level|Address' | sed 's/level=//' | awk '{ if ( $1 == \"Cell\" ) { print $5 } if ( $2 == \"Signal\" ) { print $3 } }'"

    for i in range(n_repeat):
        out_filename_now = out_filename_base + common.delimiter + str(i) + '.txt'
        scan_cmd_now = scan_cmd_base + ' > ' + out_filename_now
        print('Working: ', out_filename_now)
        os.system(scan_cmd_now)
        time.sleep(common.sleep_sec)  # sleep 하는 것이 안정성 면에서 좋다.

    print('Client : RSS measure... done')
