###############################################################################
#   Sage: Open Source Mathematical Software
#           Copyright (C) 2009 William Stein <wstein@gmail.com>
#  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################

import os
try:
    SAGE_VERSION = os.environ['SAGE_VERSION']
except:
    a = os.path.abspath('.')
    i = a.rfind('-')
    SAGE_VERSION = a[i:]
    print "Using SAGE_VERSION=%s"%SAGE_VERSION

from distutils.core import setup
from distutils.extension import Extension

ext_modules = []
include_dirs = []

code = setup(name = 'sagelite',
      description = 'Sagelite: Lowcal Open Source Mathematics Software',
      version     = SAGE_VERSION,
      license     = 'GNU Public License (GPL)',
      author      = 'William Stein et al.',
      author_email= 'http://groups.google.com/group/sage-support',
      url         = 'http://lite.sagemath.org',
      packages    = [
                     'sage',
                     'sage.interfaces',
                     'sage.misc',
                     'sage.server',
                     'sage.server.simple',
                     'sage.server.notebook',
                     'sage.server.notebook.compress',
                     'sage.structure',
                     ],
      ext_modules = ext_modules,
      include_dirs = include_dirs)
