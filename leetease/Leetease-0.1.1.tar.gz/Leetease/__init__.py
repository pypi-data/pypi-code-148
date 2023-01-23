def Int_to_Roman(s):
	res = 0; prev = 0
	save = {
	"I" : 1,
	"V" : 5,
	"X" : 10,
	"L" : 50,
	"C" : 100,
	"M" : 1000
	}
	for i in reversed(s):
		if save[i] >= prev:
			res += save[i]
		else:
			res -= save[i]
		prev = save[i]

	print(f"The number you entered in roman form is {res}")