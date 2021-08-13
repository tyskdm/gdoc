import subprocess

from gdoc import _CONFIG

def test_version():
    assert _CONFIG['version'] == '0.1.1'


def test_execute_gdoc_dump(datadir):
    result = subprocess.run(["python3", "-m", "gdoc", "dump", "-p", "docs/sample_ProjectManagement.md"], capture_output=True)
    contents = (datadir / 'data_ProjectManagement.dump.out.txt').read_bytes()

    assert result.returncode == 0
    assert result.stdout == contents



def test_execute_gdoc_trace(datadir):
    result = subprocess.run(["python3", "-m", "gdoc", "trace", "--lower", "3", "OC3", "docs/sample_ProjectManagement.md"], capture_output=True)
    contents = (datadir / 'data_ProjectManagement.trace.out.txt').read_bytes()

    assert result.returncode == 0
    assert result.stdout == contents
