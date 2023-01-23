def Roman_to_Int(s):
	res = 0; prev = 0
	save = {
	"I" : 1,
	"V" : 5,
	"X" : 10,
	"L" : 50,
	"C" : 100,
	"D" : 500,
	"M" : 1000
	}
	for i in reversed(s):
		if save[i] >= prev:
			res += save[i]
		else:
			res -= save[i]
		prev = save[i]

	print(f"The number you entered in roman form is {res}")
def Two_Sum(num, target):
	int_num = []
	try:
		for i in range(len(num)):
			int_num.append(int(num[i]))
	except:
		print("The list may only have integers")
		return
	for i in range(0, len(int_num)):
		for j in range(i+1, len(int_num)):
			res = int_num[i] + int_num[j]
			if res == target:
				print(f"[{i}, {j}],")