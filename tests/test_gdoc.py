from gdoc import _CONFIG

def test_version():
    assert _CONFIG['version'] == '0.1.1'
