"""packageConfig
-------------

Basic information about the package, used by setup.py to populate package metadata.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__) )

##DOC_DEFAULT_DIR
DOC_DEFAULT_DIR = os.path.join(HERE, '../out')

DOC_DIR = os.environ.get('DRQ_CONFIG_DIR', DOC_DEFAULT_DIR)

__versionComment__ = "Splitting data request content from API"
__version__ = "01.beta.09"
__title__ = "dreqML"
__description__ = "CMIP6 Data Request Document"
__uri__ = "http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/{0}".format(__version__)
__author__ = "Martin Juckes"
__email__ = "martin.juckes@stfc.ac.uk"
__license__ = "BSD"
__copyright__ = "Copyright (c) 2015 Science & Technology Facilities Council (STFC)"
