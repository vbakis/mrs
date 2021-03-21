import numpy as np
import array as arr
import glob
import sys
import os, shutil
import click

secim1="1"
secim2="0"

while int(secim1) != 5 and int(secim1) < 5:

	secim1 = input("\nHangi objenin grafiğini çizdireceksiniz? 1.Science Calibraeted, 2.FeAr, 3.Halogen, 4.Calib, >=5.Çıkış\t=>\t")
	if not secim1 == "5" and not secim1 > "5":
		secim2 = input("\nKaç numaralı aperture\t=>\t")
		if int(secim1) == 1:
			dosya_adi="science_calibrated"+secim2+".1dspecw"
		elif int(secim1) == 2:
			dosya_adi="fear"+secim2+".1dspec"
		elif int(secim1) == 3:
			dosya_adi="halo"+secim2+".1dspec"
		elif int(secim1) == 4:
			dosya_adi="calib"+secim2+".1dspec"
		
		print(dosya_adi)
		gnuplot_dosya = open("plot_final.gnu", "w")
		#gnuplot_dosya.write("set xrange [0:2048]\n")
		if int(secim1) == 1:
			gnuplot_dosya.write("set xlabel 'Angström'\n")
		else :
			gnuplot_dosya.write("set xlabel 'pixel number'\n")
		gnuplot_dosya.write("set ylabel 'relative flux (ADU)'\n")
		gnuplot_dosya.write("plot '"+dosya_adi+"' w l\n")
		gnuplot_dosya.write("pause -1")
		gnuplot_dosya.close()

		os.system("gnuplot plot_final.gnu")
