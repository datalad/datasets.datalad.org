import os
from datalad.support import path as op

# top level of this super dataset
# TODO: may be use our "figure out dataset top" helpers?
# TODO: might want to be able to override it so we could run
#  tests against online (remote) superdataset
LOCAL_DATASETS_ROOT = op.dirname(op.dirname(op.dirname(op.realpath(__file__))))
DATASETS_TOPURL = os.environ.get('DATALAD_DATASETS_TOPURL', LOCAL_DATASETS_ROOT)
