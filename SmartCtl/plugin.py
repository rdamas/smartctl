# -*- coding: utf-8 -*-
#######################################################################
#
#  SmartCtl
#  Version 0.2.1
#  Support: www.vuplus-support.org
#
#  Copyright (c) 2016 by Robert Damas
#  All rights reserved.
#
#  Permission to use, copy, modify, and distribute this software for any
#  purpose, without fee, and without a written agreement is hereby granted,
#  provided that the above copyright notice and this paragraph and the
#  following two paragraphs appear in all copies.
#
#  IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
#  SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
#  ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
#  THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS"
#  BASIS, AND THE AUTHOR HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT,
#  UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
#######################################################################M

from Plugins.Plugin import PluginDescriptor
import Plugins.Extensions.SmartCtl.SmartCtl as SmartCtl

from __init__ import _

def main(session, **kwargs):
	# reload(SmartCtl)
	try:
		session.open(SmartCtl.SmartCtl)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	return PluginDescriptor(
		name="SmartCtl", 
		description=_("Display HDD Health Information"), 
		where = PluginDescriptor.WHERE_PLUGINMENU, 
		fnc=main)
