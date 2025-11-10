import re
import sys
import time
import os
import random

def final_tape(s):
	return ''.join(filter(lambda x: x in '|O', s))

def to(x, y):
    return f"\033[{y};{x}H"

def digits_to_subscripts(s):
	for i in range(10):
		s = s.replace(str(i),chr(0x2080 + i))
	return s

def cleaned(t):
	return digits_to_subscripts(t.replace(' ',''))

def load_prog_from(filename):
	sep_re  = re.compile('[^a-zA-Z0-9| ]+')
	words =	sep_re.split(cleaned(open(filename).read()))
	return list(zip(words[::2],words[1::2]))

def load_prog_from_str(s):
	sep_re  = re.compile('[^a-zA-Z0-9| ]+')
	words =	sep_re.split(cleaned(s))
	return list(zip(words[::2],words[1::2]))

def random_tape_input(L):
	return ''.join(random.choice('O|') for _ in range(L))

def pr_prog(f):
	for p in f: print(p[0] + " ⟶  " + p[1])

def next_prod(f, t):
	for p in f:
		if p[0] in t:
			return p
	return ['','']

def step(f,t):
	for p in f:
		if p[0] in t:
			t = t.replace(p[0],p[1],1)
			return t
	return t

def step_sim(f, t):
	f = load_prog_from(f)
	t = cleaned(t)
	init_t = t
	print('press ENTER to continue\nenter Q to quit')
	tape_y_pos = 3
	os.system('clear')
	response = ''
	while response != 'Q':
		os.system('clear')
		print(to(0,tape_y_pos) + t)
		p = next_prod(f,t)
		print(to(0,tape_y_pos + 1) + p[0] + ' ⟶  ' + p[1] )
		print(to(0,tape_y_pos + 3)  + 'Press ENTER to continue or Q to quit.')
		response = input()
		if p[0] == '':
			response = 'Q'
			print(to(0,tape_y_pos + 4) + init_t + ' ⟶ ⟶  ' + t)
		t = step(f,t)

def report_sim(f, t, detail):
	f = load_prog_from(f)
	t = cleaned(t)
	init_t = t
	check_t = ''
	os.system('clear')
	p = next_prod(f,t)
	while t != check_t:
		print(t)
		if detail:
			p = next_prod(f,t)
			if p[0] != '':
				print(p[0] + ' ⟶  ' + p[1] )
			else:
				print('<halt>')
		check_t = t
		t = step(f,t)
	print('\n' + init_t + ' ⟶ ⟶  ' + t)

def min_sim(f, t):
	f = load_prog_from(f)
	t = cleaned(t)
	init_t = t
	check_t = ''
	while t != check_t:
		check_t = t
		t = step(f,t)
	print('\n' + init_t + ' ⟶ ⟶  ' + t)

def min_sim_f_loaded(f, t):
	t = cleaned(t)
	init_t = t
	check_t = ''
	while t != check_t:
		check_t = t
		t = step(f,t)
	print('\n' + init_t + ' ⟶ ⟶  ' + t)

def tape_compute(f, t):
	t = cleaned(t)
	init_t = t
	check_t = ''
	while t != check_t:
		check_t = t
		t = step(f,t)
	return final_tape(t)

#min_sim('30.txt', 'f' + random_tape_input(11))

