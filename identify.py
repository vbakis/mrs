from matplotlib.pyplot import plot, ion, show, ioff, close
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from numpy import arange, sqrt, exp
import matplotlib.pyplot as plt
import numpy as np
import sys
import click
import csv

def dispersiyon(x, a, b, c, d):
	return a + b * x + c * x * x + d * x * x * x

def rms(y, yfit):
    return np.sqrt(np.sum((y-yfit)**2))


def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return array[idx]

def gaus(x,a,x0,sigma):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))

def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 / wid)

def bul_xpix(xval,yval):
	fear_dosya = "fear" + sys.argv[1] + ".1dspec"	
	
	fear_data = np.loadtxt(fear_dosya)
	fear_data_x = fear_data[:, 0]
	fear_data_y = fear_data[:, 1]	

	nearest_x = find_nearest(fear_data_x, xval)
	
	gauss_x = np.empty(9)
	gauss_y = np.empty(9)
	
	for i in range(9):
		gauss_x[i] = fear_data_x[int(nearest_x)-4+i]
		gauss_y[i] = fear_data_y[int(nearest_x)-4+i]

	#print(gauss_y)
	#print(n, mean, sigma)
	
	#başlangıç parametreleri amp, cen, wid
	init_vals = [gauss_y[4]-gauss_y[0], gauss_x[4]-1, 2*(gauss_x[4]-gauss_x[0])]
	print(init_vals)
	popt,pcov = curve_fit(gaussian,gauss_x,gauss_y,p0=init_vals)

	amp, cen, wid = popt

	plt.plot(gauss_x,gauss_y,'b+',label='')
	plt.plot(gauss_x,gaussian(gauss_x,*popt),'r:', linewidth=4, label='')
	plt.ylabel('Relative Flux (ADU)')
	plt.xlabel('Column (pixel)')
	plt.text(cen, gauss_y[5]+200, yval, rotation='vertical')
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(111)
	fig.subplots_adjust(top=0.85)
	plt.plot(gauss_x,gauss_y,'b+',label='')
	plt.plot(gauss_x,gaussian(gauss_x,*popt),'r:',label='')
	plt.ylabel('Relative Flux (ADU)')
	plt.xlabel('Column (pixel)')
	ax.annotate(yval, xy=(cen, gauss_y[4]-10), xytext=(cen, gauss_y[5]-50), arrowprops=dict(facecolor='black', shrink=0.05))
	plt.show()
		
	newx = cen
	
	return newx

xc = np.empty(100)
wc = np.empty(100)

file_name = "fear" + sys.argv[1] + ".1dspec"

data = np.loadtxt(file_name)

fear_x = data[:, 0]
fear_y = data[:, 1]

ion() # interaktif modu aç
plot(fear_x, fear_y)

show()

line_input = input("Piksel, Dalgaboyu: ")
n=0
while line_input != "-1":

	line_data = line_input.split(",", 2)
	xc[n] = float(line_data[0])
	wc[n] = float(line_data[1])
	xc[n] = bul_xpix(xc[n],wc[n])
	print("%d- %.3f, %.1f " % (n+1, xc[n], wc[n]))
	n=n+1
	line_input = input("Piksel, Dalgaboyu: ")

close()


yeni_x = np.empty(n)
yeni_w = np.empty(n)
		
for i in range(n):
	yeni_x[i]=xc[i]
	yeni_w[i]=wc[i]

# curve fit
popt, _ = curve_fit(dispersiyon, yeni_x, yeni_w)
# summarize the parameter values
a, b, c, d = popt

yfit = dispersiyon(yeni_x, *popt)

print('y = %.5f + %.5f * x + %.5E * x * x + %.5E * x * x * x' % (a, b, c, d))
print('rms = %.5f' % rms(yeni_w, yfit))

# define a sequence of inputs between the smallest and largest known inputs
x_line = arange(min(yeni_x), max(yeni_x), 1)
# calculate the output for the range
y_line = dispersiyon(x_line, a, b, c, d)


with open('cizgiler.dat', mode='w') as line_file:
	yazici = csv.writer(line_file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for i in range(n):
		yazici.writerow([xc[i],wc[i]])
	
line_file.close()
	
secim = 'E'

while (secim == 'E' or secim == 'e'):

	close()
	
	fig, axs = plt.subplots(2, sharex=True)
	fig.suptitle('Dispersion Solution')
	axs[0].set_ylabel('Wavelength')
	axs[0].scatter(yeni_x, yeni_w)
	axs[0].plot(x_line, y_line)
	axs[1].set_ylabel('Residuals')
	axs[1].set_xlabel('Column')
	axs[1].scatter(yeni_x, yeni_w-yfit)

	secim = input('Dispersiyon çözümünü cizgiler.dat dosyasından tekrar yapmak ister misin? (E/H)')

	dosya = open("cizgiler.dat", "r")
	line_count = 0
	for line in dosya:
		if line != "\n":
			line_count += 1
	dosya.close()


	x = np.empty(line_count)
	y = np.empty(line_count)

	if secim == 'E' or secim == 'e':
		with open('cizgiler.dat') as f:
			i=0
			for line in f:	
				x[i], y[i] = line.split()
				i=i+1
		f.close()

		yeni_x = np.empty(line_count)
		yeni_w = np.empty(line_count)
		
		for i in range(line_count):
			yeni_x[i]=x[i]
			yeni_w[i]=y[i]
	
		# curve fit
		popt, _ = curve_fit(dispersiyon, yeni_x, yeni_w)
		# summarize the parameter values
		a, b, c, d = popt

		yfit = dispersiyon(yeni_x, *popt)

		print('y = %.5f + %.5f * x + %.5E * x * x + %.5E * x * x * x' % (a, b, c, d))
		print('rms = %.5f' % rms(yeni_w, yfit))

		# define a sequence of inputs between the smallest and largest known inputs
		x_line = arange(min(yeni_x), max(yeni_x), 1)
		# calculate the output for the range
		y_line = dispersiyon(x_line, a, b, c, d)
		
		disp_file = open("dispersiyon_cozumu.txt", "w")
		disp_file.write("%2.4f %1.9f %.5E %.5E" % (a, b, c, d))
		disp_file.close()
	else:
		if not click.confirm('Çizgi tanımlama ve dispersiyon çözümü tamamlandı. Çözüm parametreleri dispersiyon_cozumu.txt adlı dosyaya yazdırıldı. Devam edelim mi?', default=True):
			print('\nDispersiyon çözümüne ait üçüncü derece fonksiyonun katsayıları dispersiyon_cozumu.txt adlı dosyada yer almaktadır.')
			sys.exit()
		print('\nDevam ediyoruz....')

