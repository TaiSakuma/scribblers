# Tai Sakuma <tai.sakuma@gmail.com>
import io
import textwrap
import json

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.cmscertlumi import InCertifiedLumiSections

from .mockevent import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def mock_open(monkeypatch):
    ret = mock.MagicMock()
    try:
        import __builtin__
        monkeypatch.setattr(__builtin__, 'open', ret)
    except ImportError:
        import builtins
        monkeypatch.setattr(builtins, 'open', ret)
    return ret

@pytest.fixture()
def io_from_txt(txt):
    txt = textwrap.dedent(txt[1:])
    try:
        io_ = io.StringIO(txt)
    except TypeError:
        io_ = io.BytesIO(txt.encode())
    return io_

@pytest.fixture()
def json_file_io():
    file_content = """
    {"273158": [[1, 1279]],
    "273302": [[1, 459]],
    "273425": [[62, 352], [354, 733]]}
    """
    return io_from_txt(file_content)

@pytest.fixture(autouse=True)
def mock_open_for_json(mock_open, json_file_io):
    mock_open.return_value = json_file_io
    return mock_open

@pytest.fixture()
def event():
    event = MockEvent()
    return event

@pytest.fixture()
def obj(event):
    ret = InCertifiedLumiSections(
        json_path='Cert_JSON.txt'
    )
    return ret

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
params = [
    (273158, 1, True), (273158, 2, True),
    (273158, 1279, True), (273158, 1280, False),
    (273425, 1, False), (273425, 61, False),
    (273425, 62, True), (273425, 352, True),
    (273425, 353, False), (273425, 354, True),
    (273425, 733, True), (273425, 734, False),
]

@pytest.mark.parametrize('run, lumi, expected', params)
def test_event_in(obj, event, run, lumi, expected):
    obj.begin(event)
    event.run = [run]
    event.lumi = [lumi]
    obj.event(event)
    assert expected == event.inCertifiedLumiSections[0]

@pytest.mark.parametrize('run, lumi, expected', params)
def test_event_attrs(event, run, lumi, expected):
    obj = InCertifiedLumiSections(
        json_path='Cert_JSON.txt',
        run_attr_name='runNumber',
        lumi_attr_name='luminosityBlock',
        out_attr_name='certified'
    )
    obj.begin(event)
    event.runNumber = [run]
    event.luminosityBlock = [lumi]
    obj.event(event)
    assert expected == event.certified[0]

def test_event_end(obj, event):
    obj.begin(event)
    obj.end()
    assert obj.run_lumi_pairs is None
    assert obj.json_dict is None

##__________________________________________________________________||
