import random
import re

def random_tape(L):
	return ''.join(random.choice('O|') for _ in range(L))

def str_to_bin(s):
	return int(s.replace('|','1').replace('O','0'), 2)

def bin_to_str_8(b):
	return f"{b:08b}".replace('1','|').replace('0','O')

def bin_to_str_3(b):
	return f"{b:03b}".replace('1','|').replace('0','O')

def digits_to_subscripts(s):
	for i in range(10):
		s = s.replace(str(i),chr(0x2080 + i))
	return s

def cleaned(t):
	return digits_to_subscripts(t.replace(' ',''))

def final_tape(s):
	return ''.join(filter(lambda x: x in '|O', s))

def load_prog_from_str(s):
	sep_re  = re.compile('[^a-zA-Z0-9| ]+')
	words =	sep_re.split(cleaned(s))
	return list(zip(words[::2],words[1::2]))

def step(f,t):
	for p in f:
		if p[0] in t:
			t = t.replace(p[0],p[1],1)
			return t
	return t

def tape_compute(f, t):
	t = cleaned(t)
	init_t = t
	check_t = ''
	while t != check_t:
		check_t = t
		t = step(f,t)
	return final_tape(t)

def eca(r, s):
	S = len(s)
	r = bin_to_str_8(r)[::-1]
	y = ''
	for i in range(S):
		v = str_to_bin(s[(i-1)%S] + s[i%S] + s[(i+1)%S])
		y += r[v]
	return y

def prog_for_ECA(n):
	r = bin_to_str_8(n)[::-1]
	p = 'fO > Og\nf| > |k\ngO > Og\ng| > |g\nOg > hOO\n'
	p += '|g > j|O\nkO > Ok\nk| > |k\nOk > hO|\n|k > j||\n'
	p += 'Oj > jO\n|j > j|\nOh > hO\n|h > h|\nj > p|\nh > pO\n'
	for i in range(8):
		p += 'p'+bin_to_str_3(i) + ' > ' + r[i] + 'p' + bin_to_str_3(i)[1:] + '\n'
	p += 'pOO > q\npO| > q\np|O > q\np|| > q\nOq > qO\n|q > q|'
	return p

def eca_tape_test(n):
	for i in range(n):
		t = random_tape(20)
		rn = random.randint(0, 255)
		r = bin_to_str_8(rn)
		print('r = '+ r)
		f = load_prog_from_str(prog_for_ECA(rn))
		print("ECA gives  " + eca(rn, t))
		print("tape gives " + tape_compute(f, 'f'+t))
		if eca(rn, t) == tape_compute(f, 'f'+t):
			print('success')

for i in range(256):
	print('tape program for ECA rule ' + str(i) + '\n')
	print(prog_for_ECA(i))
	print('\n\n')









