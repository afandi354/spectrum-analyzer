# spektrum.py
# Setting warna background dan ukuran


import os
import time

import pygame

import controller
import model
import ui


# Konfigurasi Aplikasi.
SDR_SAMPLE_SIZE = 1024 # Jumlah sampel yang diambil
					   # Harus lebih besar dari lebar maksimal layar

CLICK_DEBOUNCE  = 0.4	# Waktu yang digunakan untuk menunggu proses
						# saat dilakukan double click program

# Konfigurasi ukuran font.
MAIN_FONT = 25
NUM_FONT  = 50

# Konfigurasi warna (RGB tuples, 0 to 255).
MAIN_BG        = (255, 255, 255) # Putih
INPUT_BG       = ( 60, 255, 255) # Cyan-ish
INPUT_FG       = ( 0,   0,   0)  # Black
CANCEL_BG      = (128,  45,  45) # merah gelap
ACCEPT_BG      = ( 45, 128,  45) # hijau gelap
BUTTON_BG      = ( 60,  60,  60) # light gray
BUTTON_FG      = (255, 255 ,255) # Putih
TULISAN        = (0, 0 ,0)
BUTTON_BORDER  = (128, 128, 128) # abu-abu
INSTANT_LINE   = (0, 0, 128)     # Hijau terang.
PEMBATAS       = (0, 0, 0) 
BATAS_TENGAH   = (190,190,190)
BATAS	       = (70,55,65)

# Gradien warna untuk waterfall spektrum
# hijau ke cyan ke merah.
WATERFALL_GRAD = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]

# Configure default UI and button values.
ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color     = BUTTON_FG
ui.Button.bg_color     = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px   = 2
ui.Button.border_px    = 2


if __name__ == '__main__':
	# Initialize pygame and SDL to use the PiTFT display and touchscreen.
	os.putenv('SDL_VIDEODRIVER', 'fbcon')
	os.putenv('SDL_FBDEV'      , '/dev/fb1')
	os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
	os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
	pygame.display.init()
	pygame.font.init()
	pygame.mouse.set_visible(False)
	# Mendapatkan ukuran dan membuat permukaan render.
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	# Menampilkan splash screen.
	splash = pygame.image.load('/home/pi/Desktop/.Splash1.png')
	screen.fill(MAIN_BG)
	screen.blit(splash, ui.align(splash.get_rect(), (0, 0, size[0], size[1])))
	pygame.display.update()
	splash_start = time.time()
	# Membuat model dan controller.
	fsmodel = model.SpektrumModel(size[0], size[1])
	fscontroller = controller.SpektrumController(fsmodel)
	time.sleep(5.0)
	# Loop utama untuk proses events dan render.
	lastclick = 0
	while True:
		# Proses dari events (hanya untuk mouse events).
		for event in pygame.event.get():
			if event.type is pygame.MOUSEBUTTONDOWN \
				and (time.time() - lastclick) >= CLICK_DEBOUNCE:
				lastclick = time.time()
				fscontroller.current().click(pygame.mouse.get_pos())
		# Update dan render tampilan.
		fscontroller.current().render(screen)
		pygame.display.update()
