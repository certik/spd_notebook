"""
Expect Interfaces Compatibility Module

This module provides some classes that are used by expect.py when the 
rest of Sage is not present.
"""
#*****************************************************************************
#       Copyright (C) 2009 Mike Hansen <mhansen@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

SageObject = object

class ParentWithBase(object):
    def __repr__(self):
        """
        Returns a string representation of this Expect interface.
        
        EXAMPLES:

            sage: S = Sage(python=True, preparse=False)
            sage: S
            Sage
        """
        return self.name().capitalize()

class RingElement(object):
    def __init__(self, parent):
        self._parent = parent

    def parent(self):
        """
        Returns the parent of this ExpectElement.

        EXAMPLES::
        
             sage: S = Sage(python=True, preparse=False)
             sage: a = S(2); a
             2
             sage: a.parent()
             Sage
        """
        return self._parent

    def __add__(self, right):
        """
        EXAMPLES::
        
            sage: S = maxima
            sage: S(2) + 3
            5
        """
        return self._add_(self._parent(right))

    __radd__ = __add__
        
    def __sub__(self, right):
        """
        EXAMPLES::
        
            sage: S = maxima
            sage: S(2) - 3
            -1
        """
        return self._sub_(self._parent(right))

    def __mul__(self, right):
        """
        EXAMPLES::
        
            sage: S = maxima
            sage: S(2) * 3
            6
        """
        return self._mul_(self._parent(right))

    __rmul__ = __mul__

    def __div__(self, right):
        """  
        EXAMPLES::
        
            sage: S = maxima
            sage: S(4) / 2
            2

        """
        return self._div_(self._parent(right))
    
