# ExergyUtilities
# Copyright (c) 2010, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`xx` module 
"""


from __future__ import print_function

import inspect

def get_self():
    return inspect.stack()[1][3]

def get_parent():
    return inspect.stack()[2][3]

def list_attrs(obj):
    attrs = vars(obj)
    attr_list  = ["{} : {}".format(*item) for item in attrs.items()]
    print(attr_list)
    
def list_object(theObject,cols = 5):
    print("********")
    print(type(theObject))
    items = dir(theObject)
    while(items):
        for i in range(cols):
            if items:
                print("{:<30}".format(items.pop(0)),end='')
        print()