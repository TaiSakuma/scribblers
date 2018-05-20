# Tai Sakuma <tai.sakuma@gmail.com>
import functools

import numpy as np

import pytest

from scribblers.essentials import FuncOnNumpyArrays
from scribblers.obj import Object
from .mockevent import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def obj():
    ret = FuncOnNumpyArrays(
        src_arrays=['mht', 'met'],
        out_name='mhtOverMet',
        func=np.divide
    )
    return ret

@pytest.fixture()
def event():
    event = MockEvent()
    event.mht = [ ]
    event.met = [ ]
    event.pt = [ ]
    return event

@pytest.fixture()
def obj_divide(event):
    ret = FuncOnNumpyArrays(
        src_arrays=['mht', 'met'],
        out_name='mhtOverMet',
        func=np.divide
    )
    ret.begin(event)
    yield ret
    ret.end()

@pytest.fixture()
def obj_sum(event):
    ret = FuncOnNumpyArrays(
        src_arrays=['pt'],
        out_name='ht',
        func=functools.partial(np.sum)
    )
    ret.begin(event)
    yield ret
    ret.end()

@pytest.fixture()
def obj_sum_keepdims(event):
    ret = FuncOnNumpyArrays(
        src_arrays=['pt'],
        out_name='ht',
        func=functools.partial(np.sum, keepdims=True)
    )
    ret.begin(event)
    yield ret
    ret.end()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin_end(obj, event):
    obj.begin(event)
    assert event.mhtOverMet == [ ]
    assert obj.func is not None
    obj.end()
    assert obj.func is None

def test_event_divide(obj_divide, event):
    obj = obj_divide
    out = event.mhtOverMet
    event.mht[:] = [25.0]
    event.met[:] = [12.0]
    obj.event(event)
    assert event.mhtOverMet == [pytest.approx(2.083333)]
    assert out is event.mhtOverMet

def test_event_sum(obj_sum, event):
    obj = obj_sum
    out = event.ht
    event.pt[:] = [25.0, 12.0]
    obj.event(event)
    assert event.ht == [pytest.approx(37.0)]
    assert out is event.ht

def test_event_sum_keepdims(obj_sum_keepdims, event):
    obj = obj_sum_keepdims
    out = event.ht
    event.pt[:] = [25.0, 12.0]
    obj.event(event)
    assert event.ht == [pytest.approx(37.0)]
    assert out is event.ht

##__________________________________________________________________||
