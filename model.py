# model.py
# setting default center frekuensi & sample rate
# Coding algoritma FFT

import numpy as np
from rtlsdr import *

import spektrum


class SpektrumModel(object):
	def __init__(self, width, height):
		"""Membuat aplikasi model utama. Harus memuat panjang
		dan tinggi layar dalam piksel.
		"""
		# Set properties yang akan digunakan oleh view.
		self.width = width
		self.height = height
		# Inisialisasi auto scaling dari min and max intensity (Y axis of plots).
		self.min_auto_scale = True
		self.max_auto_scale = True
		self.set_min_intensity('AUTO')
		self.set_max_intensity('AUTO')
		# Inisialisasi library RTL-SDR.
		self.sdr = RtlSdr()
		self.set_center_freq(96.2)
		self.set_sample_rate(1.0)
		self.set_gain('AUTO')

	def _clear_intensity(self):
		if self.min_auto_scale:
			self.min_intensity = None
		if self.max_auto_scale:
			self.max_intensity = None
		self.range = None

	def get_center_freq(self):
		"""Mengembalikan nilai frekuensi tengah dari tuner ke Megahertz."""
		return self.sdr.get_center_freq()/1000000.0

	def set_center_freq(self, freq_mhz):
		"""Set frekuensi tengah tuner untuk mendapatkan nilai megahertz."""
		try:
			self.sdr.set_center_freq(freq_mhz*1000000.0)
			self._clear_intensity()
		except IOError:
			
			pass

	def get_sample_rate(self):
		"""Mengembalikan nilai sample rate dari tuner ke megahertz."""
		return self.sdr.get_sample_rate()/1000000.0

	def set_sample_rate(self, sample_rate_mhz):
		"""Set tuner sample rate untuk menghasilkan frequency dalam megahertz."""
		try:
			self.sdr.set_sample_rate(sample_rate_mhz*1000000.0)
		except IOError:
			
			pass

	def get_gain(self):
		"""Mengembalikan gain dari  tuner.  Dapat berisi nilai string 'AUTO' atau 
		nilai angka yang mewakili nilai desible.
		"""
		if self.auto_gain:
			return 'AUTO'
		else:
			return '{0:0.1f}'.format(self.sdr.get_gain())

	def set_gain(self, gain_db):
		"""Set gain of tuner.  Can be the string 'AUTO' for automatic gain
		or a numeric value in decibels for fixed gain.
		"""
		if gain_db == 'AUTO':
			self.sdr.set_manual_gain_enabled(False)
			self.auto_gain = True
			self._clear_intensity()
		else:
			try:
				self.sdr.set_gain(float(gain_db))
				self.auto_gain = False
				self._clear_intensity()
			except IOError:
				
				pass

	def get_min_string(self):
		
		if self.min_auto_scale:
			return 'AUTO'
		else:
			return '{0:0.0f}'.format(self.min_intensity)

	def set_min_intensity(self, intensity):
		"""Set nilai Y dalam desible sebagai nilai minimum 
		dapat juga memilih 'AUTO' untuk membuat enable auto scaling .
		"""
		if intensity == 'AUTO':
			self.min_auto_scale = True
		else:
			self.min_auto_scale = False
			self.min_intensity = float(intensity)
		self._clear_intensity()

	def get_max_string(self):
		"""Return string with the appropriate maximum intensity value, either
		'AUTO' or the min intensity in decibels (rounded to no decimals).
		"""
		if self.max_auto_scale:
			return 'AUTO'
		else:
			return '{0:0.0f}'.format(self.max_intensity)

	def set_max_intensity(self, intensity):
		"""Set Y axis maximum intensity in decibels (i.e. dB value at top of 
		spectrograms).  Can also pass 'AUTO' to enable auto scaling of value.
		"""
		if intensity == 'AUTO':
			self.max_auto_scale = True
		else:
			self.max_auto_scale = False
			self.max_intensity = float(intensity)
		self._clear_intensity()

	def get_data(self):
		"""Memdapatkan nilai spectrogram data dari the tuner.  
		data yang dicuplik adalah sinyal radio
		"""
		samples = self.sdr.read_samples(spektrum.SDR_SAMPLE_SIZE)[0:self.width+4]
		# Menjalankan FFT dan membuat nilai absolute untuk mendapatkan nilai magnitude frekuensi.
		freqs = np.absolute(np.fft.fft(samples))
		freqs = freqs[1:-1]
		# Menukar hasil posisi FFT agar nilai frekuensi tengah berada di tengah.
		freqs = np.fft.fftshift(freqs)
		# Convert ke decibels.
		freqs = 10.0*np.log10(freqs/100000)
		# Update nilai min and max ketika auto scaling.
		if self.min_auto_scale:
			min_intensity = np.min(freqs)
			self.min_intensity = min_intensity if self.min_intensity is None \
				else min(min_intensity, self.min_intensity)
		if self.max_auto_scale:
			max_intensity = np.max(freqs)
			self.max_intensity = max_intensity if self.max_intensity is None \
				else max(max_intensity, self.max_intensity)
		# Update intensity range (panjang antara min and max intensity).
		self.range = self.max_intensity - self.min_intensity
		# Mengembalikan nilai intensitas frekuensi.
		return freqs
