def biggest_power_of2(n):
	res = 0
	for i in range(n, 0, -1):
		
		# If i is a power of 2
		if ((i & (i - 1)) == 0):
		
			res = i
			break
		
	return res