# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Test expected behaviors of search on our super dataset"""


from datalad.api import install, search

from datalad.support import path as op
from datalad.tests.utils import (
	assert_greater,
	assert_in,
	assert_result_count,
	eq_,
    with_tempfile,
)

from .consts import DATASETS_TOPURL


@with_tempfile
def test_our_metadataset_search(tdir):
    # smoke test for basic search operations on our super-megadataset
    # expensive operation but ok
    ds = install(
       path=tdir,
       source=DATASETS_TOPURL,
       result_xfm='datasets', return_type='item-or-list')
    res_haxby = list(ds.search('haxby'))
    assert_greater(len(res_haxby), 10)
    # default search should be case insensitive
    # but somehow it is not fully -- we get 12 here
    #res_Haxby = list(ds.search('Haxby'))
    #eq_(len(res_haxby), len(res_Haxby))

    assert_result_count(
        ds.search('id:873a6eae-7ae6-11e6-a6c8-002590f97d84', mode='textblob'),
        1,
        type='dataset',
        path=op.join(ds.path, 'crcns', 'pfc-2'))

    # there is a problem with argparse not decoding into utf8 in PY2
    from datalad.cmdline.tests.test_main import run_main
    # TODO: make it into an independent lean test
    from datalad.cmd import Runner
    out, err = Runner(cwd=ds.path)('datalad search Buzsáki')
    assert_in('crcns/pfc-2 ', out)  # has it in description
    # and then another aspect: this entry it among multiple authors, need to
    # check if aggregating them into a searchable entity was done correctly
    assert_in('crcns/hc-1 ', out)
