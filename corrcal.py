import numpy as np
import array as arr
import glob
import sys
import os, shutil
import click


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



#Dispersiyon fonksiyonu f(x)=a+bx+cx^2+dx^3
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



def wavelength_lag(fwave, pixel_lag):

#	first_wave=3650.64

	if pixel_lag > 0:
		for i in range(pixel_lag):
			fwave = fwave - disp_function(fwave)
	else :
		for i in range(abs(pixel_lag)):
			fwave = fwave + disp_function(fwave)

	return fwave

#Bu program calibrasyonu doğru yapılamayan dosyaları düzeltmek için kullanılıyor

file_number = sys.argv[1]

print("\nŞimdi Calib dosyaları ile FeAr dosyalarını CCF ile eşleştiriyorum.\n")

ccf_lag_data=np.empty(2049, dtype=int)
ccf_coef_data=np.empty(2049, dtype=float)

print("Kaba CCF yapıyorum...\n")

os.system("python dcf.py fear"+str(file_number)+".1dspec calib"+str(file_number)+".1dspec -1024 1024 10. -v -np -w=slot -p=0 -o")

os.system("cp dcf_output.csv dcf_output_"+str(file_number)+".csv")

ccf_file = open("dcf_output_"+str(file_number)+".csv", "r")
ccf_info_file = open("dcf_output_"+str(file_number)+".info", "w")
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
print("\nKayma miktarı, CCF katsayısı")
print(max_lag_value, max_coef_value)
print("\n")

ccf_file.close()
ccf_info_file.close()

if not click.confirm('CCF eğrisini görmek ister misiniz?', default=True):
	sys.exit()
print('\nGrafik çizimiyle devam ediyoruz...')

gnuplot_dosya = open("plot_ccf_corrcal.gnu", "w")
gnuplot_dosya.write("reset\n")
gnuplot_dosya.write("clear\n")
gnuplot_dosya.write("set multiplot layout 2, 1 title 'Calibration Overview' font ',14'\n")
gnuplot_dosya.write("set datafile separator ','\n")
gnuplot_dosya.write("set xlabel "+"'Lags(pixel)'"+"\n")
gnuplot_dosya.write("set ylabel "+"'CCF Coefficient'"+"\n")
gnuplot_dosya.write("plot 'dcf_output_"+str(file_number)+".csv' using 1:2 w l title 'CCF "+str(file_number)+"\n")

gnuplot_dosya.write("set xlabel "+"'Line (Pixel)'"+"\n")
gnuplot_dosya.write("set ylabel "+"'Relative Flux'"+"\n")
gnuplot_dosya.write("set datafile separator ' '\n")
gnuplot_dosya.write("plot 'calib"+str(file_number)+".1dspec' u ($1-" + str(max_lag_value) + "):($2-8000) w l lc 7 lw 2 ti 'Calib', 'fear"+str(file_number)+".1dspec' u ($1+" + str(0) + "):($2/10) w l  ti 'FeAr'\n")
gnuplot_dosya.write("unset multiplot\n")
gnuplot_dosya.write("\tpause mouse any\n")

gnuplot_dosya.close()

os.system("gnuplot plot_ccf_corrcal.gnu")

new_lag = input("Yeni kayma miktarını girin: ")
print("Yeni girilen " + new_lag + " piksel civarında CCF yapıyoruz...\n")

print("Hassas CCF yapıyorum...\n")

os.system("python dcf.py fear"+str(file_number)+".1dspec calib"+str(file_number)+".1dspec "+str(int(new_lag)-50)+" "+ str(int(new_lag)+50) + " .5 -v -np -w=gauss -p=0 -o")


os.system("cp dcf_output.csv dcf_output_"+str(file_number)+".csv")

ccf_file = open("dcf_output_"+str(file_number)+".csv", "r")
ccf_info_file = open("dcf_output_"+str(file_number)+".info", "w")
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
print("\nKayma miktarı, CCF katsayısı")
print(max_lag_value, max_coef_value)
print("\n")

ccf_info_file.write("#Wave lag at first pixel, Pixel lag, Maximum CCF\n")

max_wave_lag_value = first_wave - wavelength_lag(first_wave, int(max_lag_value))

if (max_lag_value > 0):
	ccf_info_file.write(str(max_wave_lag_value)+","+str(max_lag_value)+","+str(max_coef_value))
		
else :
	ccf_info_file.write(str(-max_wave_lag_value)+","+str(max_lag_value)+","+str(max_coef_value))

ccf_file.close()
ccf_info_file.close()


gnuplot_dosya = open("plot_ccf_corrcal.gnu", "w")
gnuplot_dosya.write("reset\n")
gnuplot_dosya.write("clear\n")
gnuplot_dosya.write("set multiplot layout 2, 1 title 'Calibration Overview' font ',14'\n")
gnuplot_dosya.write("set datafile separator ','\n")
gnuplot_dosya.write("set xlabel "+"'Lags(pixel)'"+"\n")
gnuplot_dosya.write("set ylabel "+"'CCF Coefficient'"+"\n")
gnuplot_dosya.write("plot 'dcf_output_"+str(file_number)+".csv' using 1:2 w l title 'CCF "+str(file_number)+"\n")

gnuplot_dosya.write("set xlabel "+"'Line (Pixel)'"+"\n")
gnuplot_dosya.write("set ylabel "+"'Relative Flux'"+"\n")
gnuplot_dosya.write("set datafile separator ' '\n")
gnuplot_dosya.write("plot 'calib"+str(file_number)+".1dspec' u ($1-" + str(max_lag_value) + "):($2-8000) w l lc 7 lw 2 ti 'Calib', 'fear"+str(file_number)+".1dspec' u ($1+" + str(0) + "):($2/5) w l  ti 'FeAr'\n")
gnuplot_dosya.write("unset multiplot\n")
gnuplot_dosya.write("\tpause mouse any\n")

gnuplot_dosya.close()
os.system("gnuplot plot_ccf_corrcal.gnu")


if not click.confirm('Devam edelim mi?', default=True):
	sys.exit()
print('\nCCF sonucunda elde edilen bilgiler ışığında dosyalar kalibre ediliyor ...\n')

spec_file = open("science"+str(file_number)+".1dspec", "r")
spec_calib_file = open("science_calibrated"+str(file_number)+".1dspecw", "w")

k=0
wave = wavelength_lag(first_wave, int(max_lag_value))
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

flat_file = open("halo"+str(file_number)+".1dspec", "r")
spec_file = open("science_calibrated"+str(file_number)+".1dspecw", "r")
final_file = open("science"+str(file_number)+".1dspecwf", "w")

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

print('\nYeniden kalibrasyon tamamlandı.\n')
