import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import array as arr
from astropy.wcs import WCS
from astropy.nddata.utils import Cutout2D
from specutils import Spectrum1D
from pathlib import Path
from scipy import ndimage
import glob
import sys
import os, shutil
import click
import datetime

aperture = sys.argv[5]
rnoise =  float(sys.argv[6])
gain =  float(sys.argv[7])
angle = float(sys.argv[8]) #Bu orderin derece cinsinden eğikliği

os.system("rm -f halo*.fits calib*.fits science*.fits fear*.fits var_halo*.fits")

if angle != 0:


	hdulist = fits.open(sys.argv[1])
	hdu = hdulist[0].data
	hdr = hdulist[0].header
	hdulist.close()
	halo_file=ndimage.rotate(hdulist[0].data, angle, reshape=False)
	os.system("rm -f halo_mrs.fits")
	fits.writeto("halo_mrs.fits", halo_file, hdr)
	
	hdulist = fits.open(sys.argv[2])
	hdu = hdulist[0].data
	hdr = hdulist[0].header
	hdulist.close()
	calib_file=ndimage.rotate(hdulist[0].data, angle, reshape=False)
	os.system("rm -f calib_mrs.fits")
	fits.writeto("calib_mrs.fits", calib_file, hdr)
	
	hdulist = fits.open(sys.argv[3])
	hdu = hdulist[0].data
	hdr = hdulist[0].header
	hdulist.close()
	science_file=ndimage.rotate(hdulist[0].data, angle, reshape=False)
	os.system("rm -f science_mrs.fits")
	fits.writeto("science_mrs.fits", science_file, hdr)
	
	hdulist = fits.open(sys.argv[4])
	hdu = hdulist[0].data
	hdr = hdulist[0].header
	hdulist.close()
	fear_file=ndimage.rotate(hdulist[0].data, angle, reshape=False)
	os.system("rm -f fear_mrs.fits")
	fits.writeto("fear_mrs.fits", fear_file, hdr)

else :
	os.system("cp "+sys.argv[1]+" "+"halo_mrs.fits")
	os.system("cp "+sys.argv[2]+" "+"calib_mrs.fits")
	os.system("cp "+sys.argv[3]+" "+"science_mrs.fits")
	os.system("cp "+sys.argv[4]+" "+"fear_mrs.fits")

hdulist = fits.open("halo_mrs.fits")
hdu = hdulist[0].data
hdr = hdulist[0].header
hdulist.close()

int_coord_file = open('xycoordinates.dat', "r")

i=0
for line in int_coord_file.readlines():
	i=i+1
	xy = line.split('\n', 2)
	xy = xy[0].split(',',2)
	xc, yc, xbox, ybox = 1024., int(xy[1]), float(aperture), 2048.
	hdu_crop = Cutout2D(hdu, (xc, yc), (xbox, ybox), wcs=WCS(hdr))
	wcs_cropped = hdu_crop.wcs
	hdr.update(wcs_cropped.to_header())
	comment_str = "= Cropped halogen lamp file for aperture #"+ str(i) +"."
	hdr['COMMENT'] = comment_str.format(datetime.date.today())
	filename='halo' + str(i) + '.fits'
	fits.writeto(filename, hdu_crop.data, hdr)
	hdulist = fits.open(filename)
	image=hdulist[0]
	flux=np.empty(2048, dtype=int)
	lam=np.empty(2048, dtype=float)
	txtfilename='halo' + str(i) + '.1dspec'
	halo_file = open(txtfilename, "w")
	for k in range(2048):
		flux[k]=0
		for j in range(int(aperture)):
			flux[k]=flux[k]+image.data[j][k]
			lam[k]=k
	#print(i, flux[i])
		halo_file.write(str(k)+" "+str(flux[k])+"\n")
	halo_file.close()
int_coord_file.close()

dosya_sayisi = i
#print("DOSYA SAYISI= ", i)


hdulist = fits.open("calib_mrs.fits")
hdu = hdulist[0].data
hdr = hdulist[0].header
hdulist.close()

int_coord_file = open('xycoordinates.dat', "r")
i=0
for line in int_coord_file.readlines():
	i=i+1
	xy = line.split('\n', 2)
	xy = xy[0].split(',',2)
	xc, yc, xbox, ybox = 1024., int(xy[1]), float(aperture), 2048.
	hdu_crop = Cutout2D(hdu, (xc, yc), (xbox, ybox), wcs=WCS(hdr))
	wcs_cropped = hdu_crop.wcs
	hdr.update(wcs_cropped.to_header())
	comment_str = "= Cropped calibration file for aperture #"+ str(i) +"."
	hdr['COMMENT'] = comment_str.format(datetime.date.today())
	filename='calib' + str(i) + '.fits'
	fits.writeto(filename, hdu_crop.data, hdr)
	hdulist = fits.open(filename)
	image=hdulist[0]
	flux=np.empty(2048, dtype=int)
	lam=np.empty(2048, dtype=float)
	txtfilename='calib' + str(i) + '.1dspec'
	calib_file = open(txtfilename, "w")
	for k in range(2048):
		flux[k]=0
		for j in range(int(aperture)):
			flux[k]=flux[k]+image.data[j][k]
			#lam[k]=3650.64+2.2468*k+0.000177174*k*k-2.98299e-08*k*k*k
			#lam[k]=k
	#print(i, flux[i])
		calib_file.write(str(k)+" "+str(flux[k])+"\n")
	calib_file.close()
int_coord_file.close()


hdulist = fits.open("science_mrs.fits")
hdu = hdulist[0].data
hdr = hdulist[0].header
hdulist.close()

int_coord_file = open('xycoordinates.dat', "r")
i=0
for line in int_coord_file.readlines():
	i=i+1
	xy = line.split('\n', 2)
	xy = xy[0].split(',',2)
	xc, yc, xbox, ybox = 1024., int(xy[1]), float(aperture), 2048.
	hdu_crop = Cutout2D(hdu, (xc, yc), (xbox, ybox), wcs=WCS(hdr))
	wcs_cropped = hdu_crop.wcs
	hdr.update(wcs_cropped.to_header())
	comment_str = "= Cropped science file for aperture #"+ str(i) +"."
	hdr['COMMENT'] = comment_str.format(datetime.date.today())
	filename='science' + str(i) + '.fits'
	fits.writeto(filename, hdu_crop.data, hdr)
	hdulist = fits.open(filename)
	image=hdulist[0]
	flux=np.empty(2048, dtype=int)
	lam=np.empty(2048, dtype=float)
	txtfilename='science' + str(i) + '.1dspec'
	science_file = open(txtfilename, "w")
	for k in range(2048):
		flux[k]=0
		for j in range(int(aperture)):
			flux[k]=flux[k]+image.data[j][k]
			lam[k]=k
	#print(i, flux[i])
		science_file.write(str(k)+" "+str(flux[k])+"\n")
	science_file.close()
int_coord_file.close()

hdulist = fits.open("fear_mrs.fits")
hdu = hdulist[0].data
hdr = hdulist[0].header
hdulist.close()

int_coord_file = open('xycoordinates.dat', "r")
i=0
for line in int_coord_file.readlines():
	i=i+1
	xy = line.split('\n', 2)
	xy = xy[0].split(',',2)
	xc, yc, xbox, ybox = 1024., int(xy[1]), float(aperture), 2048.
	hdu_crop = Cutout2D(hdu, (xc, yc), (xbox, ybox), wcs=WCS(hdr))
	wcs_cropped = hdu_crop.wcs
	hdr.update(wcs_cropped.to_header())
	comment_str = "= Cropped fear file for aperture #"+ str(i) +"."
	hdr['COMMENT'] = comment_str.format(datetime.date.today())
	filename='fear' + str(i) + '.fits'
	fits.writeto(filename, hdu_crop.data, hdr)
	hdulist = fits.open(filename)
	image=hdulist[0]
	flux=np.empty(2048, dtype=int)
	lam=np.empty(2048, dtype=float)
	txtfilename='fear' + str(i) + '.1dspec'
	fear_file = open(txtfilename, "w")
	for k in range(2048):
		flux[k]=0
		for j in range(int(aperture)):
			flux[k]=flux[k]+image.data[j][k]
			lam[k]=k
	#print(i, flux[i])
		fear_file.write(str(k)+" "+str(flux[k])+"\n")
	fear_file.close()

int_coord_file.close()


if not click.confirm('Grafik çizdirmek ister misiniz?', default=True):
	sys.exit()
print('\nGrafik çizimiyle devam ediyoruz...')

secim1="1"
secim2="0"

while int(secim1) != 5 and int(secim1) < 5:

	secim1 = input("\nHangi objenin grafiğini çizdireceksiniz? 1.Science, 2.FeAr, 3.Halogen, 4.Calib, >=5.Çıkış\t=>\t")
	if not secim1 == "5" and not secim1 > "5":
		secim2 = input("\nKaç numaralı aperture\t=>\t")
		if int(secim1) == 1:
			dosya_adi="science"+secim2+".1dspec"
		elif int(secim1) == 2:
			dosya_adi="fear"+secim2+".1dspec"
		elif int(secim1) == 3:
			dosya_adi="halo"+secim2+".1dspec"
		elif int(secim1) == 4:
			dosya_adi="calib"+secim2+".1dspec"
		
		print(dosya_adi)
		gnuplot_dosya = open("plot.gnu", "w")
		#gnuplot_dosya.write("set xrange [0:2048]\n")
		gnuplot_dosya.write("set xlabel 'pixel number'\n")
		gnuplot_dosya.write("set ylabel 'relative flux (ADU)'\n")
		gnuplot_dosya.write("plot '"+dosya_adi+"' w l\n")
		gnuplot_dosya.write("pause -1")
		gnuplot_dosya.close()

		os.system("gnuplot plot.gnu")



if not click.confirm('\nGüvenilir bir dispersiyon çözümünüz var mı? Hayır cevabı interaktif çizgi tanımlama ve dispersiyon çözümü işlemini başlatacak.', default=True):

	secim3 = input("\nÇizgi tanımlaması yapacağınız FeAr görüntüsünün numarasını girin: ")
	os.system("python identify.py " + secim3)

print('\nOrderların dalgaboyu kalibrasyonu ile devam ediyoruz...')
print('\ndispersiyon_cozumu.txt dosyası denetleniyor...')

if Path('dispersiyon_cozumu.txt').is_file():
	print ("Dosya bulundu. Dispersiyon fonksiyonu katsayıları okunuyor...")
else:
	print ("Dosya bulunamadı! Program burada durduruluyor.")
	sys.exit()

os.system("python calib.py "+str(dosya_sayisi))


if click.confirm('Birleşik gökyüzü tayfı oluşturmak ister misiniz?', default=True):
		os.system("python birlesik_gokyuzu.py")
print('\nDevam ediyoruz...')


if not click.confirm('İndirgenmiş tayfları çizdirmek ister misiniz?', default=True):
	sys.exit()
print('\nGrafik çizimiyle devam ediyoruz...')

os.system("python plot.py "+str(dosya_sayisi))


