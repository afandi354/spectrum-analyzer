# controller.py
# mengontrol tampilan waterfall

from views import *


class SpektrumController(object):
	"""Class which controls the views shown in the application and mediates
	changing between views.
	"""
	def __init__(self, model):
		"""Initialize controller with specified Spektrum model."""
		self.model = model
		# Create instantaneous and waterfall spectrogram views once because they
		# hold state and have a lot of data.
		self.instant = InstantSpectrogram(model, self)
		self.waterfall = WaterfallSpectrogram(model, self)
		# Start with instantaneous spectrogram.
		self._current_view = None
		self.change_to_instant()

	def change_view(self, view):
		"""Change to specified view."""
		self._prev_view = self._current_view
		self._current_view = view

	def current(self):
		"""Return current view."""
		return self._current_view

	def message_dialog(self, text, **kwargs):
		"""Open a message dialog which goes back to the previous view when
		canceled.
		"""
		self.change_view(MessageDialog(self.model, text, 
			cancel=self._change_to_previous, **kwargs))

	def number_dialog(self, label_text, unit_text, **kwargs):
		"""Open a number dialog which goes back to the previous view when
		canceled.
		"""
		self.change_view(NumberDialog(self.model, label_text, unit_text,
			cancel=self._change_to_previous, **kwargs))

	def _change_to_previous(self, *args):
		# Change to previous view, note can only go back one level.
		self.change_view(self._prev_view)

	# Functions that switch between views and are able to work as a click handler
	# because they ignore any arguments passed in (like clicked button).
	def change_to_main(self, *args):
		"""Change to main spectrogram view (either instant or waterfall depending
		on what was the last main view).
		"""
		self.change_view(self._main_view)

	def toggle_main(self, *args):
		"""Switch between instantaneous and waterfall spectrogram views."""
		if self._current_view == self.waterfall:
			self.change_to_instant()
		else:
			self.change_to_waterfall()

	def change_to_instant(self, *args):
		"""Change to instantaneous spectrogram view."""
		self._main_view = self.instant
		self.change_view(self.instant)

	def change_to_waterfall(self, *args):
		"""Change to waterfall spectrogram view."""
		self._main_view = self.waterfall
		self.change_view(self.waterfall)

	def change_to_settings(self, *args):
		"""Change to settings list view."""
		# Create a new settings list view object because the setting values might
		# change and need to be rendered with different values.
		self.change_view(SettingsList(self.model, self))
