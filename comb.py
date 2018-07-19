
import itertools
import csv



while True:
	try:
		x = int(input("Toplam değişken adedini giriniz: "))
		y = int(input("Kaçlı kombinasyon olacak: "))
	except ValueError:
		print("lütfen sayı giriniz...")
	else: 
		if y>=x:
			print("sayı sıralaması yanlış..")
		else:
			break



indices = list(range(1,x+1))
print(indices)
print("----------------------------------")
sayılar = itertools.combinations(indices,y)
a=list(sayılar)
print(a)
print(len(a))
j=1
b=[]
adet=len(a)
print("adet",adet)
sabit=a[0]
b.append(sabit)

for i in a:
	sayi=0
	j = 0
	i_2 = list(i)
	sabit_2 = list(sabit)
	print("i2......", i_2)
	print("sabit_2.....", sabit_2)
	while j < y:
		if i_2[j] in sabit_2:
			sayi = sayi + 1
		j = j +1
	print("işte sayı.....", sayi)
	if sayi > 4:
		pass
	else: 
		sabit = i
		b.append(sabit)
	
print(b)
print(len(b))


with open('test.csv','w') as out:
    csv_out=csv.writer(out)
    for row in b:
        csv_out.writerow(row)


