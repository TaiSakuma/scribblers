# Tai Sakuma <tai.sakuma@gmail.com>
import copy

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

if not has_no_ROOT:
    from scribblers.delphes import JetAddMatchedObjects
    from scribblers.delphes import FourVecSum

from scribblers.match import DeltaR
from scribblers.obj import Object

from .mockevent import MockEvent
from .compare_obj import cmp_obj_list_almost_equal

##__________________________________________________________________||
class MockScaleFunc(object):
    def __init__(self):
        self.ret = 1.0
        self.args = None

    def __call__(self, pt, eta):
        self.args = (pt, eta)
        return self.ret

##__________________________________________________________________||
@pytest.fixture()
def mockevent():
    return MockEvent()

@pytest.fixture()
def obj(mockevent):
    ret = JetAddMatchedObjects(
        in_obj1='GenJet20all',
        in_obj2='GenNeutrino',
        out_obj1='GenJet20wNeu',
        distance_func=DeltaR(
            obj1_eta_phi_names=('Eta', 'Phi'),
            obj2_eta_phi_names=('Eta', 'Phi')
        ),
        max_distance=0.4
    )
    ret.begin(mockevent)
    yield ret
    ret.end()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

@pytest.mark.parametrize('in_obj1, in_obj2, expected', [
     pytest.param(
         [ ],
         [ ],
         [ ],
         id='empty'
     ),
     pytest.param(
         [
             Object([('PT', 888.443), ('Eta', 0.659), ('Phi', 0.359), ('Mass', 79.528)]),
             Object([('PT', 808.685), ('Eta', 0.801), ('Phi', -2.717), ('Mass', 102.789)]),
             Object([('PT', 186.931), ('Eta', 0.725), ('Phi', 3.003), ('Mass', 19.412)]),
             Object([('PT', 68.112), ('Eta', 0.985), ('Phi', -0.167), ('Mass', 9.606)]),
         ],
         [
              Object([('PT', 26.454), ('Eta', 0.550), ('Phi', 0.424), ('Mass', 0.000)]),
              Object([('PT', 12.695), ('Eta', 0.782), ('Phi', 0.269), ('Mass', 0.000)]),
              Object([('PT', 10.472), ('Eta', 0.982), ('Phi', -0.222), ('Mass', 0.000)]),
              Object([('PT', 32.270), ('Eta', 0.783), ('Phi', -2.794), ('Mass', 0.000)]),
              Object([('PT', 1.646), ('Eta', 0.547), ('Phi', -0.112), ('Mass', 0.000)]),
         ],
         [
             Object([('PT', 927.485), ('Eta', 0.658), ('Phi', 0.360), ('Mass', 85.244)]),
             Object([('PT', 840.863), ('Eta', 0.800), ('Phi', -2.720), ('Mass', 105.567)]),
             Object([('PT', 186.931), ('Eta', 0.725), ('Phi', 3.003), ('Mass', 19.412)]),
             Object([('PT', 78.570), ('Eta', 0.985), ('Phi', -0.174), ('Mass', 10.419)]),
         ],
         id='2-1-1-match'
     ),
     pytest.param(
         [ ],
         [
              Object([('PT', 26.454), ('Eta', 0.550), ('Phi', 0.424), ('Mass', 0.000)]),
              Object([('PT', 12.695), ('Eta', 0.782), ('Phi', 0.269), ('Mass', 0.000)]),
              Object([('PT', 10.472), ('Eta', 0.982), ('Phi', -0.222), ('Mass', 0.000)]),
              Object([('PT', 32.270), ('Eta', 0.783), ('Phi', -2.794), ('Mass', 0.000)]),
              Object([('PT', 1.646), ('Eta', 0.547), ('Phi', -0.112), ('Mass', 0.000)]),
         ],
         [ ],
         id='empty-obj1'
     ),
     pytest.param(
         [
             Object([('PT', 888.443), ('Eta', 0.659), ('Phi', 0.359), ('Mass', 79.528)]),
             Object([('PT', 808.685), ('Eta', 0.801), ('Phi', -2.717), ('Mass', 102.789)]),
             Object([('PT', 186.931), ('Eta', 0.725), ('Phi', 3.003), ('Mass', 19.412)]),
             Object([('PT', 68.112), ('Eta', 0.985), ('Phi', -0.167), ('Mass', 9.606)]),
         ],
         [ ],
         [
             Object([('PT', 888.443), ('Eta', 0.659), ('Phi', 0.359), ('Mass', 79.528)]),
             Object([('PT', 808.685), ('Eta', 0.801), ('Phi', -2.717), ('Mass', 102.789)]),
             Object([('PT', 186.931), ('Eta', 0.725), ('Phi', 3.003), ('Mass', 19.412)]),
             Object([('PT', 68.112), ('Eta', 0.985), ('Phi', -0.167), ('Mass', 9.606)]),
         ],
         id='empty-obj2'
     ),
   ])
def test_call(obj, mockevent, in_obj1, in_obj2, expected):

    in_obj1_org = copy.deepcopy(in_obj1)
    in_obj2_org = copy.deepcopy(in_obj2)

    mockevent.GenJet20all = in_obj1
    mockevent.GenNeutrino = in_obj2

    obj.event(mockevent)

    assert cmp_obj_list_almost_equal(expected, mockevent.GenJet20wNeu, atol=1e-02)

    # the original not modified
    assert in_obj1_org == in_obj1
    assert in_obj2_org == in_obj2

##__________________________________________________________________||
@pytest.fixture()
def obj2(mockevent):
    ret = JetAddMatchedObjects(
        in_obj1='GenJet20all',
        in_obj2='GenNeutrino',
        out_obj1='GenJet20wNeu',
        distance_func=DeltaR(
            obj1_eta_phi_names=('eta', 'phi'),
            obj2_eta_phi_names=('eta', 'phi')
        ),
        max_distance=0.4,
        add_func=FourVecSum(
            obj1_pt_eta_phi_mass_names=('pt', 'eta', 'phi', 'mass'),
            obj2_pt_eta_phi_mass_names=('pt', 'eta', 'phi', 'mass')
        )
    )
    ret.begin(mockevent)
    yield ret
    ret.end()

@pytest.mark.parametrize('in_obj1, in_obj2, expected', [
     pytest.param(
         [
             Object([('pt', 888.443), ('eta', 0.659), ('phi', 0.359), ('mass', 79.528)]),
             Object([('pt', 808.685), ('eta', 0.801), ('phi', -2.717), ('mass', 102.789)]),
             Object([('pt', 186.931), ('eta', 0.725), ('phi', 3.003), ('mass', 19.412)]),
             Object([('pt', 68.112), ('eta', 0.985), ('phi', -0.167), ('mass', 9.606)]),
         ],
         [
              Object([('pt', 26.454), ('eta', 0.550), ('phi', 0.424), ('mass', 0.000)]),
              Object([('pt', 12.695), ('eta', 0.782), ('phi', 0.269), ('mass', 0.000)]),
              Object([('pt', 10.472), ('eta', 0.982), ('phi', -0.222), ('mass', 0.000)]),
              Object([('pt', 32.270), ('eta', 0.783), ('phi', -2.794), ('mass', 0.000)]),
              Object([('pt', 1.646), ('eta', 0.547), ('phi', -0.112), ('mass', 0.000)]),
         ],
         [
             Object([('pt', 927.485), ('eta', 0.658), ('phi', 0.360), ('mass', 85.244)]),
             Object([('pt', 840.863), ('eta', 0.800), ('phi', -2.720), ('mass', 105.567)]),
             Object([('pt', 186.931), ('eta', 0.725), ('phi', 3.003), ('mass', 19.412)]),
             Object([('pt', 78.570), ('eta', 0.985), ('phi', -0.174), ('mass', 10.419)]),
         ],
         id='2-1-1-match'
     ),
   ])
def test_call_lowercase(obj2, mockevent, in_obj1, in_obj2, expected):

    in_obj1_org = copy.deepcopy(in_obj1)
    in_obj2_org = copy.deepcopy(in_obj2)

    mockevent.GenJet20all = in_obj1
    mockevent.GenNeutrino = in_obj2

    obj2.event(mockevent)

    assert cmp_obj_list_almost_equal(expected, mockevent.GenJet20wNeu, atol=1e-02)

    # the original not modified
    assert in_obj1_org == in_obj1
    assert in_obj2_org == in_obj2

##__________________________________________________________________||
