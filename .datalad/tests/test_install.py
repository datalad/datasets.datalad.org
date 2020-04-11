# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Test that things install and look good (no detached heads etc)"""

import os
import random

from datalad.api import install, search

from datalad.tests.utils import (
    assert_equal,
    assert_greater,
    eq_,
    with_tempfile,
)
from .consts import DATASETS_TOPURL

import logging
lgr = logging.getLogger('datalad.tests')


@with_tempfile
def test_install_top(tdir):
    # installs one level of subdatasets only
    ds = install(
        path=tdir,
        source=DATASETS_TOPURL,
        recursive=True,
        recursion_limit=1,
    )
    subdss = ds.subdatasets(fulfilled=True, result_xfm='datasets')
    assert_greater(len(subdss), 25)  # we have a good number on top
    assert_equal(ds.subdatasets(fulfilled=False), [])   # and none is left behind

    detached = [s.path for s in subdss if not s.repo.get_active_branch()]
    assert_equal(detached, [])


@with_tempfile
def test_install_random_deep(tdir):
    seed = os.environ.get('DATALAD_SEED', str(random.randint(0, 10000)))
    lgr.info("Random seed: %r", seed)
    random.seed(seed)
    # installs top one
    ds = install(path=tdir, source=DATASETS_TOPURL)
    depth = 0
    while True:
        depth += 1
        # and dig in (randomly) until no more sub datasets left
        subdss = ds.subdatasets(result_xfm='datasets')
        if not subdss:
            break
        pds = ds
        ds = random.choice(subdss)
        pds.install(ds.path)
    lgr.info("Stopped at depth %s at %s", depth, ds)
