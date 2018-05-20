# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.altdphiw import AltDphiWrapper

from .mockevent import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def event():
    event = MockEvent()
    return event

@pytest.fixture()
def obj(event):
    ret = AltDphiWrapper(
        pt_name='jet_pt', phi_name='jet_phi',
        out_attr_name_dict={'min_chi': 'minChi', 'dphi_star': 'bdphi'}
    )
    ret.begin(event)
    yield ret
    ret.end()

@pytest.fixture()
def obj_met(event):
    ret = AltDphiWrapper(
        pt_name='jet_pt', phi_name='jet_phi', mht_name='met', mht_phi_name='met_phi',
        out_attr_name_dict={'min_chi': 'minChi', 'dphi_star': 'bdphi'}
    )
    ret.begin(event)
    yield ret
    ret.end()

def test_repr(obj):
    repr(obj)

def test_event(obj, event):
    event.jet_pt = [741.630, 498.694, 45.618]
    event.jet_phi = [-1.408, 1.805, 0.922]
    expected_minChi = [0.004707722]
    expected_bdphi = [0.004707722, 0.02484959, 0.66691385]
    obj.event(event)
    assert expected_minChi == pytest.approx(event.minChi)
    assert expected_bdphi == pytest.approx(event.bdphi)

def test_event_met(obj_met, event):
    obj = obj_met
    event.jet_pt = [741.630, 498.694, 45.618]
    event.jet_phi = [-1.408, 1.805, 0.922]
    event.met = [264.165]
    event.met_phi = [1.447]
    expected_minChi = [0.15177252]
    expected_bdphi = [0.15177252, 0.12343115, 0.44984088]
    obj.event(event)
    assert expected_minChi == pytest.approx(event.minChi)
    assert expected_bdphi == pytest.approx(event.bdphi)

##__________________________________________________________________||
