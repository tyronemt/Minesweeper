row = int(input("Insert Num of rows: "))
col = int(input("Insert Num of cols: "))
print()
b = [['N' for i in range(col)] for j in range(row)]
for r in b[::-1]:
	print('  '.join(r))
print()
b[0][1] = str(1)
print("Changing coor (0,1)")
for r in b[::-1]:
	temp = [str(i) for i in r]
	print('  '.join(temp))
input("Cont...")