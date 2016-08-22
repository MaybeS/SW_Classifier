#-*- coding: utf-8 -*-

def TEST(title, callback):
	names = open("names.txt", "r")
	imges = open("images.txt", "r")
	retes = open(title, "w")

	while True:
		name = names.readline()
		imge = imges.readline()
		if name == '' or imge == '':
			break
		retes.write(callback(name, imge) + "\n")

	names.close()
	imges.close()
	retes.close()

def DIFF(first, second, third):
	f_ = open(first, "r")
	s_ = open(second, "r")
	r_ = open(third, "w")

	fb = ""
	sb = ""
	i = 0
	while True:
		f = f_.readline()
		s = s_.readline()
		i += 1
		if f == '' or s == '':
			break
		if f != s:
			if fb == sb:
				r_.write("origin: " + fb + ", " + str(i) + " " + f + ", " + str(i) + " " + s)
			else:
				r_.write("nomatc: \n" + ", " + str(i) + " " + f + ", " + str(i) + " " + s)

		fb = f
		sb = s
	f_.close()
	s_.close()
	r_.close()

if __name__ == "__main__":
	DIFF("mymodel.test", "classify.test", "diff.test")