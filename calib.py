import numpy as np
import array as arr
import glob
import sys
import os, shutil
import click


number_of_files = sys.argv[1]
#number_of_files = "2"

#Bu dosyada piksele karşı dalaboyu değişimini veren 3ncü derece fonksiyon
#çözümüne ait parametreler yer almaktadır.
#y=a1 + a2 * x + a3 * x * x + a4 * x * x * x
disp_file = open('dispersiyon_cozumu.txt', "r")
data = np.loadtxt(disp_file)

#ilk parametre 1nci pikselin dalgaboyu, bu diğer orderların kayma 
#miktarını belirlemede kullanılacak
a1 = data[0]
a2 = data[1]
a3 = data[2]
a4 = data[3]

first_wave = float(a1) + float(a2) + float(a3) + float(a4)
#first_wave=3650.64

print ("İlk pikselin dalgaboyu: ", first_wave)
#sys.exit()

#Dispersiyon değişim fonksiyonu f(x)=a+bx+cx^2+dx^3
#Bu fonksiyon yukarıda parametreleri verilen dispersiyon 
#fonksiyonu kullanılarak oluşturulan dalgaboyu - dispersiyon (A/px)
#değerlerine yapılan fitten elde edilen parametrelerden oluşmaktadır.
#a=1.41185 +/- 0.000498
#b=0.000312139 +/- 2.501e-07
#c=-2.46627e-08 +/- 4.061e-11
#d=5.05286e-13 +/- 2.137e-15

def disp_function(wavelength):
	a=1.41185
	b=0.000312139
	c=-2.46627e-08
	d=5.05286e-13
	return a + b * wavelength + c* wavelength * wavelength + d * wavelength * wavelength * wavelength


def wavelength_lag(f_wave, pixel_lag):

	if pixel_lag > 0:
		for i in range(pixel_lag):
			f_wave = f_wave - disp_function(f_wave)
	else :
		for i in range(abs(pixel_lag)):
			f_wave = f_wave + disp_function(f_wave)

	return f_wave


#fear dosyası referans tayfımız, bu tayf sabit, dispersiyon çözümü var
#calib pinholun yerine göre değişen çizgi tayfı
#Maksimum CCF değerine karşılık gelen LAG değeri fear??.1dspec dosyasından çıkarılarak kalibre edilecek.

print("\nŞimdi Calib dosyaları ile FeAr dosyalarını CCF ile eşleştiriyorum.\n")

os.system("rm -f *.csv")

ccf_lag_data=np.empty(2049, dtype=int)
ccf_coef_data=np.empty(2049, dtype=float)
max_wave_lag_value = np.empty(int(number_of_files)+1, dtype=float)
max_lag_value_array = np.empty(int(number_of_files)+1, dtype=float)

for i in range(1, int(number_of_files)+1):
	os.system("python dcf.py fear"+str(i)+".1dspec calib"+str(i)+".1dspec -1024 1024 10. -v -np -w=slot -p=0 -o")
	os.system("cp dcf_output.csv dcf_output_"+str(i)+".csv")

	ccf_file = open("dcf_output_"+str(i)+".csv", "r")
	ccf_info_file = open("dcf_output_"+str(i)+".info", "w")
	k=0
	for line in ccf_file.readlines():
		if not k==0:
			data = line.split(',', 3)
			ccf_lag_data[k-1]=int(float(data[0]))
			ccf_coef_data[k-1]=float(data[1])
		k=k+1
	
	#print(ccf_lag_data, ccf_coef_data)
	max_coef_value=np.max(ccf_coef_data)
	max_lag_value = ccf_lag_data[ccf_coef_data.argmax()]
	print("Kaba CCF yapıyorum...\n")
	print("Kayma miktarı, CCF karsayısı\n")
	print(max_lag_value, max_coef_value)
	ccf_file.close()
	
	os.system("python dcf.py fear"+str(i)+".1dspec calib"+str(i)+".1dspec "+str(max_lag_value-10)+" " +str(max_lag_value+10)+" .5 -v -np -w=gauss -p=0 -o")
	os.system("cp dcf_output.csv dcf_output_"+str(i)+".csv")

	ccf_file = open("dcf_output_"+str(i)+".csv", "r")
	k=0
	for line in ccf_file.readlines():
		if not k==0:
			data = line.split(',', 3)
			ccf_lag_data[k-1]=int(float(data[0]))
			ccf_coef_data[k-1]=float(data[1])
		k=k+1

	max_coef_value = np.max(ccf_coef_data)
	max_lag_value = ccf_lag_data[ccf_coef_data.argmax()]
	print("Hassas CCF yapıyorum...\n")
	print("Kayma miktarı, CCF karsayısı\n")
	print(max_lag_value, max_coef_value)
	ccf_info_file.write("#Wave lag at first pixel, Pixel lag, Maximum CCF\n")

	max_wave_lag_value[i] = first_wave - wavelength_lag(first_wave, int(max_lag_value))
	
	if (max_lag_value > 0):
		ccf_info_file.write(str(max_wave_lag_value[i])+","+str(max_lag_value)+","+str(max_coef_value))
		
	else :
		ccf_info_file.write(str(-max_wave_lag_value[i])+","+str(max_lag_value)+","+str(max_coef_value))

	#Piksel kayma miktarlarını hafızada tutuyorum
	max_lag_value_array[i] = max_lag_value

	ccf_file.close()
	ccf_info_file.close()			


if not click.confirm('CCF eğrilerini görmek ister misiniz?', default=True):
	sys.exit()
print('\nGrafik çizimiyle devam ediyoruz...')
	
gnuplot_dosya = open("plot_ccf.gnu", "w")
gnuplot_dosya.write("reset\n")
gnuplot_dosya.write("clear\n")
gnuplot_dosya.write("do for [t=1:"+str(number_of_files)+":1] {\n")
gnuplot_dosya.write("\tset multiplot layout 2, 1 title 'Calibration Overview' font ',14'\n")
gnuplot_dosya.write("\tprint t\n")
gnuplot_dosya.write("\tset datafile separator ','\n")
gnuplot_dosya.write("\tset xlabel "+"'Lags(pixel)'"+"\n")
gnuplot_dosya.write("\tset ylabel "+"'CCF Coefficient'"+"\n")
gnuplot_dosya.write("\tplot 'dcf_output_'.t.'.csv' using 1:2 w l title 'CCF '.t\n")

gnuplot_dosya.write("\tset xlabel "+"'Line (Pixel)'"+"\n")
gnuplot_dosya.write("\tset ylabel "+"'Relative Flux'"+"\n")
gnuplot_dosya.write("\tset datafile separator ' '\n")
gnuplot_dosya.write("\tplot 'calib'.t.'.1dspec' u ($1-" + str(0) + "):($2-8000) w l lc 7 lw 2 ti 'Calib', 'fear'.t.'.1dspec' u 1:($2/10) w l  ti 'FeAr'\n")
gnuplot_dosya.write("\tunset multiplot\n")

gnuplot_dosya.write("\tpause mouse any\n")
gnuplot_dosya.write("}")
gnuplot_dosya.close()

os.system("gnuplot plot_ccf.gnu")



if not click.confirm('Devam edelim mi?', default=True):
	sys.exit()
print('\nCCF sonucunda elde edilen bilgiler ışığında dosyalar kalibre ediliyor devam ediyoruz...')


for l in range(1, int(number_of_files)+1):

	spec_file = open("science"+str(l)+".1dspec", "r")
	spec_calib_file = open("science_calibrated"+str(l)+".1dspecw", "w")

#Dispersiyon fonksiyonu f(x)=a+bx+cx^2+dx^3
#a=1.41185 +/- 0.000498
#b=0.000312139 +/- 2.501e-07
#c=-2.46627e-08 +/- 4.061e-11
#d=5.05286e-13 +/- 2.137e-15

	k=0
	wave = wavelength_lag(first_wave, int(max_lag_value_array[l]))
	for line in spec_file.readlines():
		k=k+1
		spectrum = line.split(' ', 2)
		wave = wave + disp_function(wave)
		#print(wave)
		spec_calib_file.write("%4.4f\t%f\n" % (wave, float(spectrum[1])))
		
	spec_file.close()
	spec_calib_file.close()

#FLAT düzeltmesi
flux_adu = np.empty(2049, dtype=float)
flat_adu = np.empty(2049, dtype=float)
flat_flux = np.empty(2049, dtype=float)

l=0
for l in range(1, int(number_of_files)+1):

	flat_file = open("halo"+str(l)+".1dspec", "r")
	spec_file = open("science_calibrated"+str(l)+".1dspecw", "r")
	final_file = open("science"+str(l)+".1dspecwf", "w")

	k=0
	for line in flat_file.readlines():
		k=k+1
		flat = line.split(' ', 2)
		flat_adu[k] = float(flat[1])
	k=0
	for line in spec_file.readlines():
		k=k+1
		spectrum = line.split('\t', 2)
		flux_adu[k] = float(spectrum[1])
		#print(spectrum[0], spectrum[1])
		flat_flux[k] = flux_adu[k] / flat_adu[k]
		
		final_file.write("%4.4f\t%f\n" % (float(spectrum[0]), flat_flux[k]))

	flat_file.close()
	spec_file.close()
	final_file.close()

print('\nHerşey tamam.\n')
