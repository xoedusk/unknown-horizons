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

import os
import shutil

from horizons.constants import PATHS
from tests.gui import gui_test, TEST_FIXTURES_DIR


@gui_test(timeout=60)
def test_editor(gui):
	"""Test that the map editor shows up."""

	def func():
		gui.trigger('load_map_window', 'cancelButton/action/__execute__')
	
	with gui.handler(func):
		gui.trigger('menu', 'editor')


@gui_test(timeout=60)
def test_credits(gui):
	"""Test that the credits page shows up."""

	def func():
		gui.trigger('credits_window', 'okButton/action/__execute__')
	
	with gui.handler(func):
		gui.trigger('menu', 'creditsLink')


@gui_test(timeout=60)
def test_help(gui):
	"""Test that the help page shows up."""

	def func():
		gui.trigger('help_window', 'okButton/action/__execute__')
		
	with gui.handler(func):
		gui.trigger('menu', 'helpLink')


@gui_test(timeout=60)
def test_help_change_key(gui):
	"""Test changing the key assignment in the help dialog."""
	def change_key():
		keys = gui.find('available_keys')
		keys.select('E')
		gui.trigger('popup_window', 'okButton/action/__execute__')

	def func():
		with gui.handler(change_key):
			gui.trigger('help_window', 'lbl_HELP')

		gui.trigger('help_window', 'okButton/action/__execute__')

	with gui.handler(func):
		gui.trigger('menu', 'helpLink')

	# at this point, the key for help was changed

	def close():
		gui.trigger('help_window', 'okButton/action/__execute__')

	with gui.handler(close):
		gui.press_key(gui.Key.E)


# NOTE doesn't work when running under xvfb (no screen resolutions detected)
"""
@gui_test(timeout=60)
def test_settings(gui):
	gui.trigger('menu', 'settingsLink')
	gui.trigger('settings_window', 'cancelButton')
"""

@gui_test(timeout=60, cleanup_userdir=True)
def test_load_game(gui):
	"""Test loading a game from the mainmenu."""

	# copy fixture savegame into user dir, otherwise we'll just get a 'no savegames' popup
	source = os.path.join(TEST_FIXTURES_DIR, 'boatbuilder.sqlite')
	target_dir = os.path.join(PATHS.USER_DIR, 'save')
	shutil.copy(source, target_dir)

	def func():
		gui.trigger('load_game_window', 'cancelButton/action/__execute__')
		
	with gui.handler(func):
		gui.trigger('menu', 'loadgameButton')
