'''
    Copyright (C) 2014-2016 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

#
#
import logging
#
from resources.modules import log
class mediaurl:
    # CloudService v0.2.4

    ##
    ##
    def __init__(self, url, qualityDesc, quality, order, title=''):
        log.warning('ININT')
        self.url = url
        self.qualityDesc = qualityDesc
        self.quality = quality
        self.order = order
        self.title = title
        self.offline = False


    def __repr__(self):
        log.warning('__repr__')
        log.warning(self.__class__.__name__)
        log.warning(self.order)
        return '{}: {} '.format(self.__class__.__name__,
                                  self.order)

    def __cmp__(self, other):
        log.warning('__cmp__')
        if hasattr(other, 'order'):
            log.warning('__cmp2__')
            return self.order.__cmp__(other.order)

    def getKey(self):
        log.warning('getKey')
        return self.order

