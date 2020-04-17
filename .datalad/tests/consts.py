import os
from datalad.support import path as op

# top level of this super dataset
# TODO: may be use our "figure out dataset top" helpers?
# TODO: might want to be able to override it so we could run
#  tests against online (remote) superdataset
LOCAL_DATASETS_ROOT = op.dirname(op.dirname(op.dirname(op.realpath(__file__))))
DATASETS_TOPURL = os.environ.get('DATALAD_DATASETS_TOPURL', LOCAL_DATASETS_ROOT)

# We will rely on the configuration of that location to instruct us
# either it is a full installation (e.g. on smaug or falkor) or not
from datalad.api import Dataset
from datalad.utils import assure_bool

DATASETS_FULL_INSTALL = assure_bool(Dataset(DATASETS_TOPURL).config.get('datalad.tests.fullinstallation', False))
print("Full installation: %s" % DATASETS_FULL_INSTALL)
