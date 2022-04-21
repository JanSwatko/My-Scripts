try:
	num = int(input("Enter a number: "))

	while num != 0:
		for i in range(11):
			value = num * i
			print("{} * {} = {}".format(num, i, value))

		num = int(input("Enter a number: "))

except:
	print("That is not a number!")