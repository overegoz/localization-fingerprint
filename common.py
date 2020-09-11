"""
Define some commonly-used values

"""

server_ip = "192.168.0.2"
server_port = 9999
BUF_SIZE = 4096
tar_name = 'archieve.tar.gz'
delimiter = '-'
version='1'
dir_name_measurement = 'measure' + delimiter + version  # radio map을 만들기 위해 사전작업할때 측정한 데이터 저장공간
dir_name_realtime = 'measure-realtime' + delimiter + version  # radio map, ap list를 저장할 폴더
dir_name_outcome = 'measure-outcome' + delimiter + version # rpi가 실시간으로 측정하는 rss 저장할 폴더
radio_map_filename = 'radio-map.pickle'
ap_name_filename = 'ap-name.pickle'
space_delimiter = ' '
sleep_sec = 1

# THE END
