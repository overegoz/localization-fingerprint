# 개발내용

시나리오
  - 방/강의실 등에서 한쪽 끝(A)과, 다른쪽 끝(B)을 각각 좌표로 잡고 위치추적 (take two farthest points in a room)
    - 방이 넓어야지 위치측정 결과가 정확할 것임 (having a large room will yeild a better result)
    - 넓은 방이 없다면, 방 안과 방 바깥, 이렇게 2개 좌표 잡아도 됨 (if the room is not large enough, take one point inside the room, and the other point can be any outside the room)
  - A에 노트북 1번, B에 노트북 2번 설치 (place one notebook 1 at point A, notebook 2 at point B )
    - 뮤직비디오 등 비디오 파일을 하나 구해서 다운받고, 두 대의 노트북 모두에 저장하기 (get a video file, and save it on both notebooks)
    - 파이썬으로 동영상 재생하는 코드 짜고, 동영상 시작 시점을 입력으로 주도록 하면 될듯 (I guess it'll be needed to develop a python program that plays a video file from a given point of time)
  - 사용자 위치가 A로 가면 노트북 1번에서 영상을 플레이 하고, B로 이동하면 노트북 2번에서 영상 플레이 (When the user goes to point A, notebook 1 should play the video. When the user moves to point B, notebook 2 should play the video)
    - 사용자가 마지막까지 시청한 시점부터 동영상 재생 (play the video from the moment user has watched last)
    - 사용자가 A에서 B로 이동할때, 노트북1에서 마지막으로 시청한 시점을 받아오고, B로 이동을 완료하면, 마지막 시청 시점을 노트북2로 전달 해 줘야할듯? (When the user moves from A to B, the user may need to receive the play time so that it can pass it to notebook 2)