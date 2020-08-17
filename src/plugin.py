# -*- coding: utf-8 -*-
#######################################################################
#
#  SmartControl
#  Version 0.3
#
#  Copyright (c) 2020 by Robert Damas
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

from __future__ import unicode_literals

from Plugins.Plugin import PluginDescriptor

import Plugins.Extensions.SmartControl.Devices as Devices
# import Plugins.Extensions.SmartControl.SmartDevice as SmartDevice
# import Plugins.Extensions.SmartControl.SmartAttributes as SmartAttributes

from __init__ import _

import os

def main(session, **kwargs):
    try:
        session.open(Devices.Devices)
    except:
        import traceback
        traceback.print_exc()

def Plugins(**kwargs):
    return PluginDescriptor(
        name="SmartControl", 
        description=_("HDD health monitor"), 
        where = PluginDescriptor.WHERE_PLUGINMENU, 
        fnc=main)
