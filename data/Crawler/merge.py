#-*- coding: utf-8 -*-

def main():
	r = open('result.txt', 'w')
	f = open('out1.txt', 'r')
	s = open('out2.txt', 'r')
	fl = f.readlines()
	sl = s.readlines()
	print len(fl), len(sl)
	for each in fl:
		r.write(each)
	for each in sl:
		r.write(each)
	r.close()
	f.close()
	s.close()

if __name__ == '__main__':
	main()