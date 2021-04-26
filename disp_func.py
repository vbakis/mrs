

#Dispersiyon fonksiyonu f(x)=a+bx+cx^2+dx^3
#a=1.41185 +/- 0.000498
#b=0.000312139 +/- 2.501e-07
#c=-2.46627e-08 +/- 4.061e-11
#d=5.05286e-13 +/- 2.137e-15

def disp_function(wavelength):

	return 1.41185 + 0.000312139 * wavelength + -2.46627e-08* wavelength * wavelength + 5.05286e-13 * wavelength * wavelength * wavelength


def wavelength_lag(pixel_lag):

	first_wave=3650.64

	if pixel_lag > 0:
		for i in range(pixel_lag):
			first_wave = first_wave - disp_function(first_wave)
#			print (first_wave)
	elif pixel_lag < 0:
		for i in range(abs(pixel_lag)):
			first_wave = first_wave + disp_function(first_wave)
			print (first_wave)

	return first_wave


#print (wavelength_lag(-19))
wavelength_lag(-19)

#wave = wavelength_lag(562)

#for i in range(10):
#	wave = wave + disp_function(wave)
#	print(wave)


