def show():
	assert True
	assert not False
	a = True
	b = False
	assert a
	assert not b
	assert a != b
	assert a and not b
	#assert False == 0
	#assert True == 1
	#assert True > 0
	# assert a | b
	# assert not(a & b)
	# assert a ^ b
	#assert True in [True, False]
	# false = 0; true = 1
	#c = [0, 1]

	#assert c[1] == 1
	#assert ["false", "true"][False] == "false"
	c = float(1)
	assert c > 0
	#assert float(True) != 0
	print("OK")
	assert True ^ False
	assert False ^ True
	assert True ^ True
	assert False ^ False

if __name__ == '__main__':
	show()