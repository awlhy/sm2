import hashlib
import math
from random import randint
import math
import random
import time
# 去掉比特串前面的0
def remove_0b_at_beginning(a):
	if(a[0:2] == '0b'):
		a = a[2:len(a)]
	return a

def padding_0_to_length(S, length):
	temp = S
	S = ''
	if(temp[0:2] == '0b'):
		S = S + '0b'
		temp = temp[2:len(temp)]
	for i in range(0, length-len(temp)):
		S = S + '0'
	for i in range(0, len(temp)):
		S = S + temp[i]
	return 


class Point(object):
    def __init__(self,x=0,y=0):
        self._x=x
        self._y=y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'



def int_to_bytes(x, k):
	M = []
	for i in range(0, k):
		M.append(x >> (i*8) & 0xff)
	M.reverse()
	return M


# 4.2.2 字节串到整数
def bytes_to_int(M):
	x = 0
	for b in M:
		x = x * 256 + int(b)
	return x

# 4.2.3 比特串到字节串
def bits_to_bytes(s):
	#print("--- 比特串到字节串的转换 ---")
	if s[0:2] == '0b':
		s = s.replace('0b', '')
		m = len(s)
		k = math.ceil(m/8)
		M = []
		for i in range(0, k):
			temp = ''
			j = 0
			while j < 8:
				if(8*i+j >= m):
					#M.append(s >> 0 & 0xff)
					temp = temp + '0'
				else:
					#M.append(s >> (i*8) & 0xff)
					temp = temp + s[m-(8*i+j)-1:m-(8*i+j)]
					#print(i , "-", j, "-", m-(8*i+j)-1, "-", temp)
				j = j + 1
			temp = temp[::-1]
			temp = int(temp, 2)
			M.append(temp)
			#M = M + temp
		M.reverse()
	else:
		print("*** ERROR: 输入必须为比特串 *** function：bits_to_bytes(s) ***")
		return -1;
	return M

# 4.2.4 字节串到比特串
def bytes_to_bits(M):
	k = len(M)
	m = 8*k
	temp = ''
	s = 0
	M.reverse()
	j = 0
	for i in M:
		s = s + i*(256**j)
		j = j + 1
	s = bin(s)
	s = padding_0_to_length(s, m)
	M.reverse()
	return s
# 4.2.5 域元素到字节串
def ele_to_bytes(a):
	#print("--- 域元素到字节串的转换 ---")
	S = []
	q = get_q()
	if (is_q_prime() and q%2 ==1):   # q为奇素数
		if (a>=0 and a<=q-1):
			t = math.ceil(math.log(q,2))
			l = math.ceil(t/8)
			S = int_to_bytes(a, l)
		else:
			print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：ele_to_bytes(a) ***")
			return -1;
	elif is_q_power_of_two():    # q为2的幂
		if type(a)==str and a[0:2] == '0b':
			m = math.ceil(math.log(q, 2))
			a = padding_0_to_length(a, m)
			if len(a)-2 == m:
				S = bits_to_bytes(a)
			else:
				print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_bytes(a)")
				return -1;
		else:
			print("*** ERROR: 输入必须为比特串 *** function：ele_to_bytes(a) ***")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_bytes(a) ***")
		return -1;
	return S

# 4.2.6 字节串到域元素
def bytes_to_ele(q, S):
	a = ''
	if (is_q_prime() and q%2 ==1):   # q为奇素数
		a = 0
		t = math.ceil(math.log(q,2))
		l = math.ceil(t/8)
		a = bytes_to_int(S)
		if not (a>=0 and a<=q-1):
			print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：bytes_to_ele(q, S) ***")
			return -1;
	elif is_q_power_of_two():    # q为2的幂
		m = math.ceil(math.log(q, 2))
		a = padding_0_to_length(a, m)
		if not len(a)-2 == m:
			print("*** ERROR: 域元素必须为长度为m的比特串 *** function：bytes_to_ele(q, S)")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：bytes_to_ele(q, S) ***")
		return -1;
	return a


# 4.2.7 域元素到整数

def ele_to_int(a):
	#print("--- 域元素到字节串的转换 ---")
	x = 0
	q = get_q()
	if (is_q_prime() and q%2 ==1):   # q为奇素数
		x = a
	elif is_q_power_of_two():    # q为2的幂
		if type(a)==str and a[0:2] == '0b':
			m = math.log(q, 2)
			if len(a)-2 == m:
				#a = a.replace('0b', '')
				a = remove_0b_at_beginning(a)
				for i in a:
					x = x * 2 + int(i)
			else:
				print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)")
				return -1;
		else:
			print("*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***")
			return -1;
	else:
		print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_int(a, q) ***")
		return -1;
	return x


# 4.2.8 点到字符串
def point_to_bytes(point):
	q = get_q()
	l = math.ceil(math.log(q, 2)/8)
	x = point.x
	y = point.y
	S = []
	PC = ''
	# a. 将域元素x转换成长度为l的字节串X
	X = ele_to_bytes(x)
	temp = X
	X = []
	for i in range(0, l-len(temp)):
		X.append(0)
	for i in range(0, len(temp)):
		X.append(temp[i])
	
	##### d. 混合表示形式 #####
	# d.1 将域元素y转换成长度为l的字节串Y
	Y = ele_to_bytes(y)
	temp = Y
	Y = []
	for i in range(0, l-len(temp)):
		Y.append(0)
	for i in range(0, len(temp)):
		Y.append(temp[i])
	# d.2 计算比特y1
	y1_temp = bytes_to_bits(Y)#[math.ceil(math.log(q,2)/8)*8-1:math.ceil(math.log(q,2)/8)*8]
	y1 = y1_temp[len(y1_temp)-1:len(y1_temp)]
	# d.3 若y1=0，则令PC=06；若y1=1，则令PC=07
	if y1 == '0':
		PC = 6
	elif y1 == '1':
		PC = 7
	else:
		print('*** ERROR: PC值不对 function: point_to_bytes ***')
	# d.4 字节串S=PC||X||Y
	S.append(PC)
	for m in X:
		S.append(m)
	for n in Y:
		S.append(n)
	return S

# 4.2.9 字符串到点
def bytes_to_point(a, b, S):
	q = get_q()
	l = math.ceil(math.log(q, 2)/8)
	PC = ''
	X = []
	Y = []
	# a. 
	if len(S) == 2*l+1: #为压缩表示形式或者混合表示形式
		PC = S[0]
		for i in range(1,l+1):
			X.append(S[i])
		for i in range(l+1, 2*l+1):
			Y.append(S[i])
	elif len(S) == l+1: #压缩表示形式
		PC = S[0]
		for i in range(1,l):
			X.append(S[i])
	else:
		print('*** ERROR: wrong size  function: bytes_to_point ***')

	# b. 将X转换成与元素x
	x = bytes_to_ele(q, X)
	##### c. 压缩表示形式 #####
	y1 = ''
	# c.1 and c.2
	if PC == 2:
		y1 = '0'
	elif PC == 3:
		y1 = '1'
	##### d. 未压缩表示形式 #####
	elif PC == 4:
		y = bytes_to_ele(q, Y)
	##### e. 混合表示形式 #####
	# e.1 and e.2
	elif PC == 6 or 7:
		y = bytes_to_ele(q, Y)
	else:
		print('ERROR in bytes_to_point')
	# f. 
	result = 0
	if(type(x) != type(1)):
		x = int(x,2)
	if(type(y) != type(1)):
		y = int(y,2)
	if (is_q_prime() and q%2 ==1):   # q为奇素数
		if (y**2)%q != (x**3 + a*x + b)%q:
			return -1
	elif is_q_power_of_two():
		if (y**2 + x*y) != (x**3 + a*x + b):
			return -1
	# g. 
	point = Point(x,y)
	return point

def bytes_to_str(S):
	temp = ''
	string = ''
	temp = remove_0b_at_beginning(bytes_to_bits(S))
	temp = padding_0_to_length(temp, 8*math.ceil(len(temp)/8))
	for i in range(0, math.ceil(len(temp)/8)):
		string = string + chr(int(temp[i*8:(i+1)*8],2))
	return string

def str_to_bytes(x):
	S = []
	for i in x:
		S.append(ord(i))
	return 





# 多项式加法单位元 #
def polynomial_zero():
    return '0b0'
# 多项式乘法单位元 #
def polynomial_one():
    return '0b1'

# 多项式乘法 #
def polynomial_times(a, b):
    #print("--- 多项式 乘法 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)

    # max result length
    m = len(a) - 2 + len(b) - 2
    m_bytes = math.ceil(float(m) / 8.0)

    # counter
    i = 0
    # result
    c = 0
    while a_int != 0:
        if a_int%2 == 1:
            c = c ^ (b_int << i)
        a_int = a_int // 2
        i += 1
    return bytes_to_bits(int_to_bytes(c, m_bytes))

# 多项式除法 #
def polynomial_a_devide_b(a, b):
    #print("--- 多项式 除法 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)

    # max result length
    m = len(a) - 2
    m_bytes = math.ceil(float(m) / 8.0)

    c = 0
    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ (b_int << i)
        c += (1 << i)
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) \
            - len(bytes_to_bits(int_to_bytes(b_int, b_len)))
    return bytes_to_bits(int_to_bytes(c, m_bytes))


# 多项式取模 #
def polynomial_a_mod_b(a, b):
    #print("--- 多项式 取模 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)

    # max result length
    m = len(b) - 1
    m_bytes = math.ceil(float(m) / 8.0)

    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ (b_int << i)
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) \
            - len(bytes_to_bits(int_to_bytes(b_int, b_len)))
    
    return bytes_to_bits(int_to_bytes(a_int, m_bytes))




# hash函数
def hash_function(m):
	sha256 = hashlib.sha256()
	sha256.update(m.encode("utf8"))
	sha256 = bin(int(sha256.hexdigest(), 16))
	sha256 = padding_0_to_length(sha256, 32*8)
	return sha256

# 密钥派生函数
def KDF(Z, klen):
	v = get_v()
	if(klen < (2**32-1)*v):
		ct=0x00000001
		H = []
		H_ = []
		for i in range(0, math.ceil(klen/v)):
			H.append(remove_0b_at_beginning(hash_function(Z+str(ct))))
			ct = ct + 1
		if (klen/v == math.ceil(klen/v)):
			H_ = remove_0b_at_beginning(H[math.ceil(klen/v)-1])
		else:
			H_ = remove_0b_at_beginning(H[math.ceil(klen/v)-1][0:(klen-(v*math.floor(klen/v)))])
		K = ''
		for i in range(0, math.ceil(klen/v)):
			if(i != math.ceil(klen/v)-1):
				K = K + H[i]
			else:
				K = K + H_
	else:
		print("*** ERROR: klen要小于(2^32-1)*v *** function: KDF(Z, klen) ***")
	return K
def PRG_function(a, b):
	return randint(a, b)

def get_Z(ID, PA):
	a = get_a()
	a = bytes_to_bits(ele_to_bytes(a))
	b = get_b()
	b = bytes_to_bits(ele_to_bytes(b))
	n = get_n()
	Gx = get_Gx()
	Gx_ = bytes_to_bits(ele_to_bytes(Gx))
	Gy = get_Gy()
	Gy_ = bytes_to_bits(ele_to_bytes(Gy))

	ID = bytes_to_bits(str_to_bytes(ID))
	ENTL = int_to_bytes(math.ceil((len(ID)-2)/8)*8, 2)
	ENTL = bytes_to_bits(ENTL)
	xA = bytes_to_bits(ele_to_bytes(PA.x))
	yA = bytes_to_bits(ele_to_bytes(PA.y))
	ZA = hash_function(ENTL+ID+a+b+Gx_+Gy_+xA+yA)
	return ZA

def M_to_bits(input):
	M = ''
	if (type(input) == type('a')):
		for i in input:
			temp = int.from_bytes(i.encode('ascii'), byteorder='big', signed=True)
			temp = int_to_bytes(temp, 1)
			temp = remove_0b_at_beginning(bytes_to_bits(temp))
			temp = padding_0_to_length(temp, 8)
			M = M + temp
	if(type(input) == type([])):
		for i in input:
			if (type(i) == type('a')):
				for j in i:
					temp = int.from_bytes(i.encode('ascii'), byteorder='big', signed=True)
					temp = int_to_bytes(temp, 1)
					temp = remove_0b_at_beginning(bytes_to_bits(temp))
					temp = padding_0_to_length(temp, 8)
					M = M + temp
			elif (type(i) == type(0)):
				M = remove_0b_at_beginning(bytes_to_bits(input))
				M = padding_0_to_length(M, 8*math.ceil(len(M)/8))
			else:
				print('*** ERROR: 字节串中类型不为str或者int *** function：M_to_bits(input) ***')
	return M

def bits_to_M(M):
	output = []
	M = '0b'+M
	M = bits_to_bytes(M)
	output = bytes_to_str(M)
	return output


# 有限域参数 q #
q = 0
q_prime = False
q_2m = False
def is_q_prime():
    return q_prime
def is_q_power_of_two():
    return q_2m

def set_q(a):
    global q
    global q_prime
    global q_2m
    if isPrime_MR(a, 15):
        q = a
        q_prime = True
        if is_Power_of_two(q):
            q_2m = True
        else:
            q_2m = False
    elif is_Power_of_two(a):
        q = a
        q_2m = True
        if isPrime_MR(q, 15):
            q_prime = True
        else:
            q_prime = False
    else:
        print("*** ERROR: q必须为奇素数或2的幂 *** function: set_q")

def get_q():
    return q

# 二元阔域中做模数的素多项式 #
fx = '0b0'

def set_fx(a):
    global fx
    if a[0:2] != '0b':
        print("*** ERROR: 参数必须是比特串 *** function: set_fx")
    else:
        for i in range(2, len(a)):
            if a[i] != '0' and a[i] != '1':
                print("*** ERROR: 参数必须是比特串 *** function: set_fx ***")
        fx = a

def get_fx():
    return fx

# 椭圆曲线参数 #
a = 0
b = 0

def set_a(ia):
    global a
    a = ia

def get_a():
    return a

def set_b(ib):
    global b
    b = ib

def get_b():
    return b

n = 0
def set_n(a):
    global n
    n = a
def get_n():
    return n

Gx = 0
def set_Gx(a):
    global Gx
    Gx = a
def get_Gx():
    return Gx

Gy = 0
def set_Gy(a):
    global Gy
    Gy = a
def get_Gy():
    return Gy

h = -1
def set_h(a):
    global h
    h = a
def get_h():
    return h

# 设置参数 #
def set_parameters(parameters):
    set_q(parameters['q'])
    if  is_q_power_of_two():
        set_fx(parameters['f(x)'])
    set_a(parameters['a'])
    set_b(parameters['b'])
    set_n(parameters['n'])
    set_Gx(parameters['Gx'])
    set_Gy(parameters['Gy'])
    set_h(parameters['h'])

def get_parameters():
    param = {
        'q' : get_q(), 
        'a' : get_a(), 
        'b' : get_b(), 
        'n' : get_n(), 
        'Gx' : get_Gx(), 
        'Gy' : get_Gy(), 
        'h' : get_h()
    }
    if is_Power_of_two(get_q()):
        dict_f = { 'f(x)' : get_fx() }
        param.update(dict_f)
    return param

# 从读配置文件 #
def read_config_file(filename):
    fo = open(filename, "ab+")
    fl = fo.tell()
    fo.seek(0, 0)
    config = eval(fo.read(fl))
    fo.close()
    return config

# 设置为默认参数 #

def default_config():
    # Fp-256
    parameters = {# 'q': 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3,
                  'q': 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
                    'f(x)': 'NULL',
                    # 'a': 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498,
                    'a': 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
                    # 'b': 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A,
                    'b': 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
                    'h' : 1, 
                    # 'Gx': 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
                    'Gx': 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7,
                    # 'Gy': 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2,
                    'Gy': 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0,
                    # 'n': 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
                    'n': 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
                    }
    set_parameters(parameters)

def get_v():
    return 256




# 快速模指数算法 #
def fast_pow(g, a, p):
	e = int(a % (p - 1))
	if e == 0:
		return 1
	r = int(math.log2(e))# + 1 - 1
	x = g
	for i in range(0, r):
		x = int((x**2) % p)
		if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
			x = (g * x) % p
	return int(x)

def isPrime_MR(u, T):    
	# 计算 v 和 w ，使得 u - 1 = w * 2^v
	v = 0
	w = u - 1
	while w%2 == 0:
		v += 1
		w = w // 2
	for j in range(1, T + 1):
		nextj = False
		a = random.randint(2, u - 1)
		b = fast_pow(a, w, u)
		if b == 1 or b == u - 1:
			nextj = True
			continue
		for i in range(1, v):
			b = (b**2)%u
			if b == u - 1:
				nextj = True
				break
			if b == 1:
				return False
		if not nextj:
			return False
	return True

# 判断是否为2的幂
def is_Power_of_two(n):
	if n>0:
		if (n&(n-1))==0 :
			return True
	return False
#if is_Power_of_two(45):
#	print('true')

# 求逆元
def inverse(a, n):
	a_ = fast_pow(a, n-2, n)%n
	return a_
# 判断是否为有限域元素 #
def in_field(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是有限域中元素 *** function: in_field ***")
            return False
        else:
            return True
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = math.log2(q)
        if (len(a)-2) > m:
            print("*** ERROR: a 不是有限域元素 *** function: in_field ***")
            return False
        else:
            for i in range(2, len(a)):
                if a[i] != '0' and a[i] != '1':
                    print("*** ERROR: a 不是有限域元素 *** function: in_field ***")
                    return False
            return True
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***")
        return -1


# 有限域加法单位元 #
def field_ele_zero():
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        return 0
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = int(math.log2(q))
        zero = '0b'
        for i in range(0, m):
            zero += '0'
        return zero
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_zero ***")
        return -1

# 有限域乘法单位元 #
def field_ele_one():
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        return 1
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = int(math.log2(q))
        one = '0b'
        for i in range(0, m - 1):
            one += '0'
        one += '1'
        return one
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_one ***")
        return -1

# 3.1 有限域计算 #
# 有限域加法 #
def field_ele_add(a, b):
    #print("--- 有限域 加法 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是素域中元素 *** function: field_ele_add ***")
            return -1
        elif not in_field(b):
            print("*** ERROR: b不是素域中元素 *** function: field_ele_add ***")
            return -1
        else:
            return((a + b) % q)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not (in_field(a) and in_field(b)):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_add ***")
            return -1
        else:
            c_int = ele_to_int(a) ^ (ele_to_int(b))
            c_bytes = int_to_bytes(c_int, 2)
            c_ele = bytes_to_ele(q, c_bytes)
            return c_ele
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***")
        return -1
# 有限域加法逆元 #
def field_ele_inverse_add(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_inverse_add ***")
            return -1
        else:
            return (q - a) % q
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(a):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_add ***")
            return -1
        else:
            return a
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_add ***")
        return -1

# 有限域减法 #
def field_ele_sub(a, b):
    return field_ele_add(a, field_ele_inverse_add(b))

# 有限域乘法 #
def field_ele_times(a, b):
    #print("--- 有限域 乘法 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_times ***")
            return -1
        elif not in_field(b):
            print("*** ERROR: b不是域中元素 *** function: field_ele_times ***")
            return -1
        else:
            return((a * b) % q)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not (in_field(a) and in_field(b)):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_times ***")
            return -1
        else:
            result_bits = polynomial_a_mod_b(polynomial_times(a, b), get_fx())
            return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_times ***")
        return -1

# 有限域幂运算 #
def field_ele_g_pow_a(g, a):
    #print("--- 有限域 幂运算 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(g):
            print("*** ERROR: a不是域中元素 *** function: field_ele_g_pow_a ***")
            return -1
        else:
            e = a % (q - 1)
            if e == 0:
                return 1
            r = int(math.log2(e))# + 1 - 1
            x = g
            for i in range(0, r):
                x = field_ele_times(x, x)
                if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
                    x = field_ele_times(x, g)
            return x
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(g):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_g_pow_a ***")
            return -1
        else:
            e = a % (q -1)
            if e == 0:
                return polynomial_one()
            r = int(math.log2(e))# + 1 - 1
            x = g
            for i in range(0, r):
                x = field_ele_times(x, x)
                if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
                    x = field_ele_times(x, g)
            return x
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_g_pow_a ***")
        return -1

# 有限域逆元素 #
def field_ele_inverse_times(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_inverse_times ***")
            return -1
        else:
            return field_ele_g_pow_a(a, get_q() - 2)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(a):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_times ***")
            return -1
        else:
            return field_ele_g_pow_a(a, get_q() - 2)
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_times ***")
        return -1

# 有限域除法 #
def field_ele_a_devide_b(a, b):
    #print("--- 有限域 除法 ---")
    return field_ele_times(a, field_ele_inverse_times(b))

# 3.2.3 椭圆曲线群 #

# 椭圆曲线无穷远点 #
def ECG_ele_zero():
    return Point(field_ele_zero(), field_ele_zero())

# 椭圆曲线元素判断 #
# 元素为零 #
def ECG_ele_is_zero(p):
    if p.x == field_ele_zero() and p.y == field_ele_zero():
        return True
    else:
        return False
# 元素互为逆元素 #
def ECG_is_inverse_ele(p1, p2):
    q = get_q()
    # q 为素数
    if is_q_prime():
        if p1.x == p2.x and p1.y == field_ele_inverse_add(p2.y):
            return True
        else:
            return False
    elif is_q_power_of_two():
        if p1.x == p2.x and p2.y == field_ele_add(p1.x, p1.y):
            return True
        else:
            return False
    else:
        print("*** ERROR: q 不是素数或者 2 的幂 *** function: ECG_is_inverse_ele ***")
        return False
# 元素相等 #
def ECG_ele_equal(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return True
    else:
        return False

# 椭圆曲线加法 #
def ECG_ele_add(p1, p2):
    # Fp 上的椭圆曲线群
    if is_q_prime():
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return ECG_ele_zero()
        elif ECG_ele_equal(p1, p2):
            #lam = (3 * (p1.x**2) + config.get_a()) / (2 * p1.y)
            t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p1.x, 2)), get_a())
            t2 = field_ele_times(2, p1.y)
            lam = field_ele_a_devide_b(t1, t2)
            #x = lam**2 - 2 * p1.x
            x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p1.x))
            #y = lam * (p1.x - x) - p1.y
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
            return Point(x, y)
        else:
            #lam = (p2.y - p1.y) / (p2.x - p1.x)
            lam = field_ele_a_devide_b(field_ele_sub(p2.y, p1.y), field_ele_sub(p2.x, p1.x))
            #x = lam * lam - p1.x - p2.x
            x = field_ele_sub(field_ele_sub(field_ele_g_pow_a(lam, 2), p1.x), p2.x)
            #y = lam * (p1.x - x) - p1.y
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
            return Point(x, y)

    # F2^m 上的椭圆曲线
    if is_q_power_of_two():
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return ECG_ele_zero()
        elif ECG_ele_equal(p1, p2):
            #lam = p1.x + (p1.y / p1.x)
            lam = field_ele_add(p1.x, field_ele_a_devide_b(p1.y, p1.x))
            #x = lam**2 + lam + config.get_a()
            x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
            #y = p1.x**2 + (lam + 1) * x
            y = field_ele_add(field_ele_g_pow_a(p1.x, 2), \
                field_ele_times(field_ele_add(lam, field_ele_one()), x))
            return Point(x, y)
        else:
            #lam = (p1.y + p2.y) / (p1.x + p2.x)
            lam = field_ele_a_devide_b(field_ele_add(p1.y, p2.y), \
                field_ele_add(p1.x, p2.x))
            #x = lam**2 + lam + p1.x + p2.x + config.get_a()
            t1 = field_ele_add(field_ele_g_pow_a(lam, 2), lam)
            t2 = field_ele_add(field_ele_add(p1.x, p2.x),get_a())
            x = field_ele_add(t1, t2)
            #y = lam * (p1.x + x) + x + p1.y
            t1 = field_ele_times(lam, field_ele_add(p1.x, x))
            t2 = field_ele_add(x, p1.y)
            y = field_ele_add(t1, t2)
            return Point(x, y)

# 椭圆曲线求 2 倍点 #
def ECG_double_point(p):
    # Fp 上的椭圆曲线群
    if is_q_prime():
        if ECG_ele_is_zero(p):
            return p
        else:
            t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p.x, 2)), get_a())
            t2 = field_ele_times(2, p.y)
            lam = field_ele_a_devide_b(t1, t2)
            x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p.x))
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p.x, x)), p.y)
            return Point(x, y)
    # F2^m 上的椭圆曲线
    if is_q_power_of_two():
        if ECG_ele_is_zero(p):
            return p
        else:
            lam = field_ele_add(p.x, field_ele_a_devide_b(p.y, p.x))
            x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
            y = field_ele_add(field_ele_g_pow_a(p.x, 2), \
                field_ele_times(field_ele_add(lam, field_ele_one()), x))
            return Point(x, y)


# 椭圆曲线求 k 倍点 #
def ECG_k_point(k, p):
    #print('[' + str(k) + ']P')
    l = int(math.log2(k)) + 1# - 1
    #print(l)
    point_q = ECG_ele_zero()
    for i in range(0, l):
        #print('i = ' + str(i))
        j = l - 1 - i
        #t_start = time.time()
        point_q = ECG_double_point(point_q)
        #t_end = time.time()
        #print('double:' + str(t_end - t_start))
        if (k & (1 << j)) == (1 << j):
            #t_start = time.time()
            point_q = ECG_ele_add(point_q, p)
            #t_end = time.time()
            #print('add:' + str(t_end - t_start))
    return point_q
def key_pair_generation(parameters):
    set_parameters(parameters)
    point_g = Point(get_Gx(), get_Gy())
    n = get_n()

    d = random.randint(1, n - 2)
    p = ECG_k_point(d, point_g)
    keypair = []
    keypair.append(d)
    keypair.append(p)
    return keypair

# 6.2 公钥的认证 #

def public_key_verification(parameters, public_key):
    set_parameters(parameters)
    n = get_n()
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 3:
        if ECG_ele_is_zero(public_key):
            print("*** ERROR: 公钥为无穷远点 *** function: public_key_verification")
            #print("无效")
            return False
        if not (in_field(public_key.x) and in_field(public_key.y)):
            print("*** ERROR: 公钥坐标不是素域中元素 *** function: public_key_verification")
            #print("无效")
            return False
        t1 = field_ele_g_pow_a(public_key.y, 2)
        t2 = field_ele_add(field_ele_add(field_ele_g_pow_a(public_key.x, 3), 
                            field_ele_times(get_a(), public_key.x)), get_b())
        if t1 != t2:
            print("*** ERROR: 公钥坐标不符合椭圆曲线方程 *** function: public_key_verification")
            #print("无效")
            return False
        if not(ECG_ele_is_zero(ECG_k_point(n, public_key))):
            print("*** ERROR: n 不是公钥的阶 *** function: public_key_verification")
            #print("无效")
            return False
        #print("有效")
        return True
    # q 为 2 的幂
    elif is_q_power_of_two():
        if ECG_ele_is_zero(public_key):
            print("*** ERROR: 公钥为无穷远点 *** function: public_key_verification")
            #print("无效")
            return False
        #m = math.log2(q)
        if not (in_field(public_key.x) and in_field(public_key.y)):
            print("*** ERROR: 公钥坐标不是素域中元素 *** function: public_key_verification")
            #print("无效")
            return False
        t1 = field_ele_add(field_ele_g_pow_a(public_key.y, 2), 
                            field_ele_times(public_key.x, public_key.y))
        t2 = field_ele_add(field_ele_add(field_ele_g_pow_a(public_key.x, 
                                                            3), 
                                        field_ele_times(get_a(), 
                                                        field_ele_g_pow_a(public_key.x, 2))), 
                            get_b())
        if t1 != t2:
            print("*** ERROR: 公钥坐标不符合椭圆曲线方程 *** function: public_key_verification")
            #print("无效")
            return False
        if not(ECG_ele_is_zero(ECG_k_point(n, public_key))):
            print("*** ERROR: n 不是公钥的阶 *** function: public_key_verification")
            #print("无效")
            return False
        #print("有效")
        return True
    else:
        print("*** ERROR: q 不是奇素数或者 2 的幂 *** function: public_key_verification")
        #print("无效")
        return False




def Signature(M, IDA, dA, PA, d1, d2):
	a = get_a()
	b = get_b()
	n = get_n()
	Gx = get_Gx()
	Gy = get_Gy()
	ZA = get_Z(IDA, PA)
	M_ = ZA + M
	M1 = M_ + M_  # Z1+M
	e1 = hash_function(M1)
	e1 = bytes_to_int(bits_to_bytes(e1))
	# print("e1:", e1)
	r = 0
	k = 0

	k1 = 0
	k2 = 0
	k3 = 0
	while (r == 0) or (r+k == n):
		# A3：用随机数发生器产生随机数k ∈[1,n-1]
		k = PRG_function(1, n-1)
		# A4：计算椭圆曲线点(x1,y1)=[k]G，按本文本第1部分4.2.7给出的细节将x1的数据类型转换为整 数

		k1 = PRG_function(1, n - 1)
		print("1:随机选取k1:",k1)
		k2 = PRG_function(1, n - 1)
		k3 = PRG_function(1, n - 1)
		Q1 = ECG_k_point(k1, Point(Gx, Gy))
		print("1:计算Q1=k1*G，并把Q1发送给用户2")
		print("2:Q1:",Q1)
		print("2:随机选取k2，k3:",k2,k3)
		Q2 = ECG_k_point(k2, Point(Gx, Gy))
		print("2:计算Q2=k2*G，Q2:",Q2)
		temp = k1*k3 + k2
		rx = ECG_k_point(temp, Point(Gx, Gy)).x  # (k1*k3 + k2)*G
		rx = bytes_to_int(ele_to_bytes(rx))
		print("2:利用k3,Q1,Q2计算得到rx:",rx)

		r = (rx + e1) % n
		print("2:利用rx和待签名文件的哈希值计算r")
	s2 = (d2 * k3) % n
	s3 = (d2 * (r + k2)) % n
	print("2:根据d2,k2,k3计算得到s2,s3,并将r,s2,s3发送给用户1")
	print("1:r:",r)
	print("1:s2:",s2)
	print("1:s3:",s3)
	s = (d1*k1*s2+d1*s3-r) % n
	print("1:根据d1,k1,r,s2,s3计算s:",s)
	r = int_to_bytes(r, math.ceil(math.log(n, 2)/8))
	s = int_to_bytes(s, math.ceil(math.log(n, 2)/8))
	Sig = r
	for i in s:
		Sig.append(i)
	return Sig


### test Signature ###
default_config()
parameters = get_parameters()
point_g = Point(get_Gx(), get_Gy())
n = get_n()
print("请输入待签名的文件:")
f1 = input()
f = open(f1,'r')
M = f.read()
key = key_pair_generation(parameters)
d1 = key[0]
P1 = key[1]
re_d1 = inverse(d1, n)
key = key_pair_generation(parameters)
d2 = key[0]
P2 = key[1]
re_d2 = inverse(d2, n)
print("1:计算P1=d1'*G，把P1发送给用户2:")
print("2:P1:",P1)
dA = re_d1*re_d2 - 1
fd = open("privatekey.txt","w")
fd.write(str(dA))
fd.close()
PA = ECG_k_point(dA, point_g)
fp = open("publickey.txt","w")
fp.write(str(PA))
fp.close()
print("2:计算d2'*P1-G得到公钥PA:",PA)
IDA = 'ALICE123@YAHOO.COM'

Sig = Signature(M, IDA, dA, PA, d1, d2)
print("1:输出的签名(r,s)是:", Sig)
f0 = open("signature.txt","w")
f0.write(str(Sig))
f0.close()
