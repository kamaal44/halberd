# -*- coding: iso-8859-1 -*-

# Copyright (C) 2004 Juan M. Bello Rivas <rwx@synnergy.net>
#
# This program is free software; you can redistribute it and/or modify
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""Output module.
"""

__revision__ = '$Id: reportlib.py,v 1.7 2004/02/13 01:16:55 rwx Exp $'


import sys

import hlbd.clues.analysis as analysis


def report(address, clues, outfile=''):
    """Displays detailed report information to the user.

    @param address: Address of the scanned host.
    @type address: C{str}

    @param clues: Clues found and (pressumably) processed by an analyzer.
    @type clues: C{list}
    """
    out = (outfile and open(outfile, 'w')) or sys.stdout

    out.write('\n[ %d ] possibly real server(s) at [ %s ].\n'
              % (len(clues), address))

    hits = sum([clue.getCount() for clue in clues])

    diff_fields = [field for percent, field in analysis.diff_fields(clues)]

    for num, clue in enumerate(clues):
        info = clue.info
        different = [(field, value) for field, value in clue.headers \
                                    if field in diff_fields]

        out.write('\n')
        out.write('server [ %d ]\t\t[ %s ]\n' % (num, info['server'].lstrip()))

        out.write('successful requests\t[ %2d ]\n' % clue.getCount())
        if hits:
            out.write('traffic\t\t\t[ %.2f%% ]\n' \
                      % (clue.getCount() * 100 / float(hits)))

        out.write('difference\t\t[ %d ]\n' % clue.diff)

        if info['contloc']:
            out.write('content-location\t[ %s ]\n' % info['contloc'].lstrip())

        out.write('header fingerprint\t[ %s ]\n' % info['digest'])

        if different:
            out.write('different headers:\n')
            for field, value in different:
                out.write('  %s:%s\n' % (field, value))


# vim: ts=4 sw=4 et
