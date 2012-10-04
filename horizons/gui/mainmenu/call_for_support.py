# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from fife import fife
from fife.extensions import pychan

import horizons.globals
from horizons.component.ambientsoundcomponent import AmbientSoundComponent
from horizons.gui.widgets.imagebutton import OkButton, CancelButton


class Dialog(object):
	modal = True

	def __init__(self, widget):
		self._widget = widget

	def pre(self):
		pass

	def show(self):
		self.pre()

		if self.modal:
			self._show_modal_background()

		def _on_keypress(event, dlg=self._widget): # rebind to make sure this dlg is used
			from horizons.engine import pychan_util
			if event.getKey().getValue() == fife.Key.ESCAPE: # convention says use cancel action
				btn = dlg.findChild(name=CancelButton.DEFAULT_NAME)
				callback = pychan_util.get_button_event(btn) if btn else None
				if callback:
					pychan.tools.applyOnlySuitable(callback, event=event, widget=btn)
				else:
					# escape should hide the dialog default
					horizons.globals.fife.pychanmanager.breakFromMainLoop(returnValue=False)
					dlg.hide()
			elif event.getKey().getValue() == fife.Key.ENTER: # convention says use ok action
				btn = dlg.findChild(name=OkButton.DEFAULT_NAME)
				callback = pychan_util.get_button_event(btn) if btn else None
				if callback:
					pychan.tools.applyOnlySuitable(callback, event=event, widget=btn)
				# can't guess a default action here

		self._widget.capture(_on_keypress, event_name="keyPressed")
		ret = self._widget.execute(self.return_events)

		if self.modal:
			self._hide_modal_background()

		return ret

	def _show_modal_background(self):
		"""Loads transparent background that de facto prohibits
		access to other gui elements by eating all input events.
		"""
		height = horizons.globals.fife.engine_settings.getScreenHeight()
		width = horizons.globals.fife.engine_settings.getScreenWidth()
		image = horizons.globals.fife.imagemanager.loadBlank(width, height)
		image = fife.GuiImage(image)
		self._modal_widget = pychan.Icon(image=image)
		self._modal_widget.position = (0, 0)
		self._modal_widget.show()

	def _hide_modal_background(self):
		try:
			self._modal_widget.hide()
			del self._modal_widget
		except AttributeError:
			pass


class CallForSupport(Dialog):
	return_events = {OkButton.DEFAULT_NAME: True}

	def pre(self):
		AmbientSoundComponent.play_special("message")