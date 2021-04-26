import numpy as np
import statistics

secim = input("Birleştirmek istediğiniz gökyüzü görüntülerinin numarasını girin (örn. 1,2,3) (Minimum 6 tane önerilir): ")

dosya_sayilari = secim.split(",")

first_x = np.empty(len(dosya_sayilari), dtype=float)
last_x = np.empty(len(dosya_sayilari), dtype=float)
dosya_baslangic = np.empty(len(dosya_sayilari), dtype=int)
dosya_bitis = np.empty(len(dosya_sayilari), dtype=int)

#print(len(dosya_sayilari))

for i in range(len(dosya_sayilari)):
	sky_file = open('science_calibrated'+str(dosya_sayilari[i])+'.1dspecw', "r")
	
	lines = sky_file.readlines()

#	print(len(lines))
	first_line=lines[0].split("\t")
	first_x[i] = float(first_line[0])
	last_line=lines[2047].split("\t")
	last_x[i] = float(last_line[0])

	print(i+1, ". dosya, dalgaboyu ilk-son: ", first_x[i], " - ", last_x[i])

	sky_file.close()

#min_x=min(first_x)

print("Birleşik gökyüzü dalgaboyu aralığı: ", first_x.max(), " - ", last_x.min())

for i in range(len(dosya_sayilari)):
	sky_file = open('science_calibrated'+str(dosya_sayilari[i])+'.1dspecw', "r")
	j=0

	for line in sky_file.readlines():
		xy = line.split('\n', 2)
		xy = xy[0].split('.',2)
		if(int(xy[0]) == int(first_x.max())):
			dosya_baslangic[i]=j
			print(i+1,". dosya için başlangıç index: ", j)
		if(int(xy[0]) == int(last_x.min())):
			dosya_bitis[i]=j
			print(i+1,". dosya için bitiş index: ", j)
		j=j+1
	
	print(i+1,". dosya için satır sayısı: ", dosya_bitis[i]-dosya_baslangic[i])

	sky_file.close()
	
npiksel = np.empty(dosya_bitis[0]-dosya_baslangic[0], dtype=int)	

sky_x_array=np.empty([len(npiksel)+2, len(dosya_sayilari)], dtype=float)
sky_y_array=np.empty([len(npiksel)+2, len(dosya_sayilari)], dtype=float)


#print(len(dosya_sayilari), len(npiksel))

for i in range(len(dosya_sayilari)):
	
	science_file = open('science_calibrated'+str(dosya_sayilari[i])+'.1dspecw', "r")
	sky_file = open('sky'+str(dosya_sayilari[i])+'.1dspecw', "w")
	#lines = sky_file.readlines()

#	print(lines)
	j=0
	k=0
	for lines in science_file.readlines():
		xy = lines.split('\n', 2)
		xy = xy[0].split('\t',2)
		if(j>=dosya_baslangic[i] and j<=dosya_bitis[i]):
			sky_x_array[k][i]=float(xy[0])
			sky_y_array[k][i]=float(xy[1])
			#print (dosya_baslangic[i], dosya_bitis[i], i, j, k)
#			print (k, i, sky_x_array[k][i], sky_y_array[k][i])
			sky_file.write(str(sky_x_array[k][i]) + " " + str(sky_y_array[k][i])+"\n")
			k=k+1
		j=j+1
	science_file.close()
	sky_file.close()


sigma_sky_array = np.empty(len(dosya_sayilari), dtype=float)
wave_array = np.empty(len(dosya_sayilari), dtype=float)

sky_final = open('sky_final.1dspec', "w")
sky_final_draft = open('sky_final.draft', "w")

sky_final_draft.write("#Sıra\tDalgaboyu\t[OrtalananDeğerler]\tMean\tSigma\n")

for j in range(len(npiksel)):
	sky_final_draft.write("%d " % (j))
	for i in range(len(dosya_sayilari)):
		sigma_sky_array[i]= sky_y_array[j][i]
#		print(j,i, sigma_sky_array, np.average(sigma_sky_array), np.std(sigma_sky_array))
#		print(sigma_sky_array)
		sigma_sky = np.std(sigma_sky_array)
		mean_sky = np.mean(sigma_sky_array)
	final_sky = [x for x in sigma_sky_array if (x > mean_sky - 2 * sigma_sky)]
	final_sky = [x for x in final_sky if (x < mean_sky + 2 * sigma_sky)]
#	print(j, final_sky, mean_sky, sigma_sky)
	sky_final.write("%.4f %.2f\n" % (sky_x_array[j][0], np.mean(final_sky)))
	sky_final_draft.write("%.4f %s %.2f %.2f\n" % (sky_x_array[j][0], final_sky, mean_sky, sigma_sky))

sky_final.close()
sky_final_draft.close()
