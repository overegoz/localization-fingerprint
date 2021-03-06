import numpy as np

"""
========================
=========(y,x)============
(y,x)   (y,x)  (0,2)  (0,3)
(1,0)  (y,x)   (1,2)  (1,3)
(2,0)  (2,1)  (2,2)  (y,x)
(3,0)  (3,1)  (3,2)  (y,x)
(4,0)  (4,1)  (y,x)   (y,x)
======================
=========(y,x)============
(0,2) ==> 세로: 8440    가로: 19384
(0,3) ==> 세로: 8440    가로: 26715

(1,0) ==> 세로: 13840   가로: 3850
(1,2) ==> 세로: 13840   가로: 19384
(1,3) ==> 세로: 13840   가로: 26715

(2,0) ==> 세로: 18590   가로: 3850
(2,1) ==> 세로: 18590   가로: 10934
(2,2) ==> 세로: 18590   가로: 19384

(3,0) ==> 세로: 22194   가로: 3850
(3,1) ==> 세로: 22194   가로: 10934
(3,2) ==> 세로: 22194   가로: 19384

(4,0) ==> 세로: 26842   가로: 3850
(4,1) ==> 세로: 26842   가로: 10934
(4,2) ==> 세로: 26842   가로: 19384

========================
왼쪽 상단이 원점
0         3850 10930 19384 26715
8440                         
13840
18590
22194
26842  
"""


def get_real_coord_YX(y, x):
    """
	(y,x)를 입력으로 받고 (real_y, real_x)를 출력한다
	입력: y 좌표 먼저, x 는 그 다음이다
	리턴값: y 좌표 먼저, x 는 그 다음이다
    """

    max_y_index = 4
    max_x_index = 3

    if y < 0 or y > max_y_index:
        assert False, 'incorrect index of y'

    if x < 0 or x > max_x_index:
        assert False, 'incorrect index of x'

    if y == 0:
		if x == 2:
			return -, -
		elif x == 3:
			return -, -

    if y == 1: 
		if x == 0: 
			return -, - 
		elif x == 2:
			return -, -
		elif x == 3:
			return -, -

    if y == 2:
		if x == 0:
			return -, - 
		elif x == 1:
			return -, -
		elif x == 2: 
			return -, -

    if y == 3:
		if x == 0: 
			return -, - 
		elif x == 1: 
			return -, -
		elif x == 2: 
			return -, -

    if y == 4:
		if x == 0: 
			return -, - 
		elif x == 1: 
			return -, -
		elif x == 2: 
			return -, -        

    # 그 외의 경우
    return -1, -1

