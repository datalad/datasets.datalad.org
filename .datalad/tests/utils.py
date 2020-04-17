from datalad.tests.utils import skip_if
from .consts import DATASETS_FULL_INSTALL

skip_if_not_full_install = skip_if(not DATASETS_FULL_INSTALL, msg="Can be ran only on full install. Set datalad.tests.fullinstallation=true")
