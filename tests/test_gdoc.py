import subprocess

from gdoc import _CONFIG

def test_version():
    assert _CONFIG['version'] == '0.1.1'


def test_execute_gdoc_dump():
    result = subprocess.run(["python3", "-m", "gdoc", "dump", "-p", "docs/sample_ProjectManagement.md"], capture_output=True)

    assert result.returncode == 0


def test_execute_gdoc_trace():
    result = subprocess.run(["python3", "-m", "gdoc", "trace", "--lower", "3", "OC3", "docs/sample_ProjectManagement.md"], capture_output=True)

    assert result.returncode == 0
