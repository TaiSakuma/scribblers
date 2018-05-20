# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from scribblers.obj import Object
from .compare_obj import cmp_obj_list_almost_equal
from .compare_obj import cmp_obj_almost_equal

##__________________________________________________________________||
@pytest.mark.parametrize('list1, list2, expected', [
    pytest.param(
        [ ], [ ],
        True, id='empty'),
    pytest.param(
        [Object([('i', 3)]), Object([('i', 5)])],
        [Object([('i', 3)]), Object([('i', 5)])],
        True, id='same-1'),
    pytest.param(
        [Object([('i', 3)]), Object([('i', 5)])],
        [Object([('i', 3)]), Object([('i', 8)])],
        False, id='different-content'),
    pytest.param(
        [Object([('i', 3)]), Object([('i', 5)])],
        [Object([('i', 3)])],
        False, id='list1-longer'),
    pytest.param(
        [Object([('i', 3)])],
        [Object([('i', 3)]), Object([('i', 5)])],
        False, id='list2-longer'),
    pytest.param(
        [Object([('i', 3), ('x', 10.1)]), Object([('i', 5), ('x', 32.5)])],
        [Object([('i', 3), ('x', 10.1)]), Object([('i', 5), ('x', 32.5)])],
        True, id='float'),
    pytest.param(
        [Object([('i', 3), ('x', 10.1)]), Object([('i', 5), ('x', 32.5)])],
        [Object([('i', 3), ('x', 10.1)]), Object([('i', 5), ('x', 32.50001)])],
        True, id='float-almost-equal'),
    ])
def test_cmp_obj_list_almost_equal(list1, list2, expected):
    assert expected == cmp_obj_list_almost_equal(list1, list2)

@pytest.mark.parametrize('obj1, obj2, expected', [
    pytest.param(
        Object([('i', 3)]),
        Object([('i', 3)]),
        True, id='same-int'),
    pytest.param(
        Object([('i', 3)]),
        Object([('i', 5)]),
        False, id='diff-int'),
    pytest.param(
        Object([('i', 3)]),
        Object([('j', 5)]),
        False, id='diff-attrs'),
    pytest.param(
        Object([('x', 32.5)]),
        Object([('x', 32.5000001)]),
        True, id='same-float-almost'),
    pytest.param(
        Object([('x', 32.5)]),
        Object([('x', 32.501)]),
        False, id='diff-float-almost'),
    pytest.param(
        Object([('n', 'abc')]),
        Object([('n', 'abc')]),
        True, id='str'),
    ])
def test_cmp_obj_almost_equal(obj1, obj2, expected):
    assert expected == cmp_obj_almost_equal(obj1, obj2)

##__________________________________________________________________||
