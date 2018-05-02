# Tai Sakuma <tai.sakuma@gmail.com>
import math
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.match import ObjectMatch
from scribblers.obj import Object
from .mockevent import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def mock_distance_func():
    ret = mock.Mock()
    ret.side_effect = lambda o1, o2: math.hypot(o1.x - o2.x, o1.y - o2.y)
    return ret

@pytest.fixture()
def obj(mock_distance_func):
    return ObjectMatch(
        in_obj1='A',
        in_obj2='B',
        out_obj1_matched='Amatched',
        out_obj2_matched_sorted='BmatchedSorted',
        out_obj1_unmatched='Aunmatched',
        out_obj2_unmatched='Bunmatched',
        distance_func=mock_distance_func,
        max_distance=2
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.A = [ ]
    event.B = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, event):

    obj.begin(event)
    assert event.Amatched == [ ]
    assert event.BmatchedSorted == [ ]
    assert event.Aunmatched == [ ]
    assert event.Bunmatched == [ ]

def test_end(obj, event):

    obj.begin(event)
    obj.end()
    assert obj.obj1_matched is None
    assert obj.obj2_matched_sorted is None
    assert obj.obj1_unmatched is None
    assert obj.obj2_unmatched is None

def test_event_simple(obj, event):

    obj.begin(event)

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 3), ('y', 0)))
    a3 = Object((('x', 6), ('y', 0)))
    a4 = Object((('x', 9), ('y', 0)))
    b1 = Object((('x', 13), ('y', 0)))
    b2 = Object((('x', 6.5), ('y', 0)))
    b3 = Object((('x', 5), ('y', 0)))
    b4 = Object((('x', 2), ('y', 0)))
    b5 = Object((('x', 1), ('y', 0)))

    event.A[:] = [a1, a2, a3, a4]
    event.B[:] = [b1, b2, b3, b4, b5]
    obj.event(event)

    assert event.Amatched == [a1, a2, a3]
    assert event.BmatchedSorted == [b5, b4, b2]
    assert event.Aunmatched == [a4]
    assert event.Bunmatched == [b1, b3]

##__________________________________________________________________||
