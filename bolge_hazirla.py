from astropy.io import fits
import glob
import sys
import os, shutil
import click

#arguman #1 maske dosyası
#arguman #2 halojen dosyası
#arguman #3 ccd_field dosyası
#arguman #4 calib dosyası
#arguman #5 science dosyası
#arguman #6 order açısı
#arguman #7 aperture diameter
#arguman #12 y-coordinate offset

angle = sys.argv[11]
aperture_radii = float(sys.argv[7])/2
y_offset = int(sys.argv[12])

#source extractor ile pinhole deliklerinin koordinatları belirleniyor
cmd1="source-extractor " + sys.argv[1] + " -c default.sex"

os.system(cmd1)

#Koordinat dosyaları
cat_file = open('mosmask.cat', "r")
int_coord_file = open('xycoordinates.dat', "w")
reg_file = open('circcoords.reg', "w")
reg_file2 = open('boxcoords.reg', "w")
reg_file3 = open('textcoords.reg', "w")


i=0
for line in cat_file.readlines():
	koordinatlar1 = line.split('\n', 2)[0]
	koordinatlar2 = koordinatlar1.split('   ')
	int_koordinat = koordinatlar2
	if (koordinatlar2[0] == "") :
		koordinatlar2[0]=koordinatlar2[1]
		koordinatlar2[1]=koordinatlar2[2]
		int_koordinat[0]=int(float(koordinatlar2[0]))
		int_koordinat[1]=int(float(koordinatlar2[1]))
		#print (int_koordinat[0], int_koordinat[1])
	i=i+1
	int_koordinat[0]=int(float(koordinatlar2[0]))
	int_koordinat[1]=int(float(koordinatlar2[1]))		
	satir="circle("+str(float(koordinatlar2[0]))+","+str(float(koordinatlar2[1])+y_offset)+"," + str(aperture_radii) + ") # text={"+str(i)+"}\n"
	satir2="box(" + str("1024") + "," + str(int_koordinat[1]+y_offset) + ",2048," + sys.argv[7] + "," + angle + ")\n"
	satir3="text("+str("5")+","+str(int_koordinat[1])+") # text={"+str(i)+"}\n"
	satir4=str(int(float(koordinatlar2[0])))+","+str(int(float(koordinatlar2[1]))+y_offset)+"\n"
	reg_file.write (satir)
	reg_file2.write (satir2)
	reg_file3.write (satir3)
	int_coord_file.write (satir4)

cat_file.close()
reg_file.close()
reg_file2.close()
reg_file3.close()
int_coord_file.close()

cmd2="ds9 " + sys.argv[1] + " -zscale -zoom to fit -regions circcoords.reg"

os.system(cmd2)

if not click.confirm('Maskedeki pinhole deliklerini gösterdim. Devam edelim mi?', default=True):
	sys.exit()
print('\nDevam ediyoruz...')
	
cmd3="ds9 "+ sys.argv[2] + " -zscale -zoom to fit -regions boxcoords.reg -regions textcoords.reg"
	
os.system(cmd3)
	
if not click.confirm('Ayıklayacağımız bölgeleri gösterdim. Devam edelim mi?', default=True):
	sys.exit()
print('\nDevam ediyoruz...')

cmd4="ds9 "+ sys.argv[3] + " -zscale -zoom to fit -regions circcoords.reg"
	
os.system(cmd4)

if not click.confirm('Pinhole deliklerinin gökyüzünde baktığı yerleri gösterdim. Devam edelim mi?', default=True):
	sys.exit()
print('\nDevam ediyoruz...')
print('\nBölgeleri ayıklıyorum...')

os.system("python3 spextract.py " + sys.argv[2] + " " + sys.argv[4] + " " + sys.argv[5] + " " + sys.argv[6] + " " + sys.argv[7] + " " + sys.argv[8] + " " + sys.argv[9] + " " + angle)

