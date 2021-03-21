import glob
import sys
import os, shutil
import click


print ("\n\tMRS : The MOS Reduction Software\n")
print ("ÖNEMLİ!!!: Fits uzantılı gözlem dosyalarının ön indirgemesi (D=(S-D)/(PRNU-B)) tayfın MRS ile ayıklanmaya başlamasından önce yapılmalı.\n")

if not click.confirm('Devam edelim mi?', default=True):
	sys.exit()
print('\nBaşlıyoruz...')


#Maske dosyası
maske = "mask0000.fit"

#Halojen lamba dosyası
halo = "flat0000.fit"

#Bölgenin görüntü dosyası
sky = "g107empty01.fits"

#Dalgaboyu kalibrasyon dosyası
calib = "fear0001.fit"

#FeAr lamba dosyası
fear = "fear_for_calib.fit"

#Science görüntsü
science = "mosb.fits"

#aperture çapı
aperture = 14

#okuma gürültüsü (readnoise)
rnoise = 1.5

#kazanç (pixel gain)
gain = 1.

#referans FeAr dosya numarası
reFeAr = 20

#order eğikliği
angle= 0

#y-coordinate offset in pixels (+/- number)
#ne yaptığını bilmiyorsan bu değere 0 (sıfır) gir.
# örn. y_offset = -2
y_offset= +2

cmd = "python bolge_hazirla.py " + maske + " " + halo + " " + sky + " " + calib + " " + science + " " + fear + " " + str(aperture) + " " + str(rnoise) + " " + str(gain) + " " + str(reFeAr) + " " + str(angle) + " " + str(y_offset)

os.system(cmd)
