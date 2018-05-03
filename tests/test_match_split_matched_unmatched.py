# Tai Sakuma <tai.sakuma@gmail.com>
import math
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.match import split_matched_unmatched
from scribblers.obj import Object

##__________________________________________________________________||
@pytest.fixture()
def mock_distance_func():
    ret = mock.Mock()
    ret.side_effect = lambda o1, o2: math.hypot(o1.x - o2.x, o1.y - o2.y)
    return ret

##__________________________________________________________________||
def test_match_empty_AB(mock_distance_func):

    A = [ ]
    B = [ ]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert len(Amatched) == 0
    assert len(BmatchedSorted) == 0
    assert len(Aunmatched) == 0
    assert len(Bunmatched) == 0

def test_match_empty_A(mock_distance_func):

    o1 = Object((('x', 0), ('y', 0)))
    o2 = Object((('x', 1), ('y', 0)))

    A = [ ]
    B = [o1, o2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert Amatched == [ ]
    assert BmatchedSorted == [ ]
    assert Aunmatched == [ ]
    assert Bunmatched == [o1, o2]

def test_match_empty_B(mock_distance_func):

    o1 = Object((('x', 0), ('y', 0)))
    o2 = Object((('x', 1), ('y', 0)))

    A = [o1, o2]
    B = [ ]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert Amatched == [ ]
    assert BmatchedSorted == [ ]
    assert Aunmatched == [o1, o2]
    assert Bunmatched == [ ]

def test_match_simple(mock_distance_func):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 0), ('y', 3)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 3), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert Amatched == [a1]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a2]
    assert Bunmatched == [b2]

def test_match_2A_within_distance(mock_distance_func):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 1.5), ('y', 0)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 5), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert Amatched == [a2]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a1]
    assert Bunmatched == [b2]

def test_match_2B_within_distance(mock_distance_func):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 5), ('y', 0)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 1.5), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = split_matched_unmatched(A, B, mock_distance_func, 2)

    assert Amatched == [a1]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a2]
    assert Bunmatched == [b2]

##__________________________________________________________________||
