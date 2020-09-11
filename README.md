# Localization by using the fingerprint approach

실행방법

1. RPi : ./python3 client-setup.py x y n 을 각 cell-block에서 실행
  - (x,y) cell-block의 인덱스 (물리적인 실제 좌표 아님)
  - 동일한 cell-block에서 몇번 반복해서 측정을 할지 (기본값 = 5)

2. Server : ./python receive-setup.py 실행
  - RPi 클라이언트가 보내주는 radio measurement 파일 수신하기
    - USE_INTERNET_CONN=True 이면 실제로 클라이언트로 부터 전송 받은 데이터로 radio map 만들고
    - False 이면, 서버 로컬에 저장된 데이터를 이용해서 radio map 만든다
  - 수신한 파일을 parsing 해서 radio-map 생성하기
  - 생성한 radio-map을 파일로 dump 하기

3. RPi : ./python3 upload-setup.py aaa.bbb.ccc.ddd pppp 실행
  - aaa.bbb.ccc.ddd : 서버 IP
  - pppp : 서버 port number

4. Server : ./python server.py rrrr 실행 : 실시간 위치 추적 및 디스플레이
  - rrrr : radio-map 파일명

5. RPi : ./python3 client.py xxxx 실행: 실시간 위치추적
  - xxxx : 사용자 ID

