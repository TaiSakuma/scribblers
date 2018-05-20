# Tai Sakuma <tai.sakuma@gmail.com>
import copy

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.delphes import JetAddMatchedObjects
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
              Object([('PT', 26.454), ('Eta', 0.550), ('Phi', 0.424), ('Mass', 0.000),
                      ('Px', 24.114), ('Py', 10.877), ('Pz', 15.295), ('E', 30.557)]),
              Object([('PT', 12.695), ('Eta', 0.782), ('Phi', 0.269), ('Mass', 0.000),
                      ('Px', 12.238), ('Py', 3.377), ('Pz', 10.968), ('E', 16.777)]),
              Object([('PT', 10.472), ('Eta', 0.982), ('Phi', -0.222), ('Mass', 0.000),
                      ('Px', 10.214), ('Py', -2.310), ('Pz', 12.026), ('E', 15.947)]),
              Object([('PT', 32.270), ('Eta', 0.783), ('Phi', -2.794), ('Mass', 0.000),
                      ('Px', -30.336), ('Py', -11.004), ('Pz', 27.937), ('E', 42.683)]),
              Object([('PT', 1.646), ('Eta', 0.547), ('Phi', -0.112), ('Mass', 0.000),
                      ('Px', 1.635), ('Py', -0.184), ('Pz', 0.946), ('E', 1.899)]),
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
              Object([('PT', 26.454), ('Eta', 0.550), ('Phi', 0.424), ('Mass', 0.000),
                      ('Px', 24.114), ('Py', 10.877), ('Pz', 15.295), ('E', 30.557)]),
              Object([('PT', 12.695), ('Eta', 0.782), ('Phi', 0.269), ('Mass', 0.000),
                      ('Px', 12.238), ('Py', 3.377), ('Pz', 10.968), ('E', 16.777)]),
              Object([('PT', 10.472), ('Eta', 0.982), ('Phi', -0.222), ('Mass', 0.000),
                      ('Px', 10.214), ('Py', -2.310), ('Pz', 12.026), ('E', 15.947)]),
              Object([('PT', 32.270), ('Eta', 0.783), ('Phi', -2.794), ('Mass', 0.000),
                      ('Px', -30.336), ('Py', -11.004), ('Pz', 27.937), ('E', 42.683)]),
              Object([('PT', 1.646), ('Eta', 0.547), ('Phi', -0.112), ('Mass', 0.000),
                      ('Px', 1.635), ('Py', -0.184), ('Pz', 0.946), ('E', 1.899)]),
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
def test_event(obj, mockevent, in_obj1, in_obj2, expected):

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
