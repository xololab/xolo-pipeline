# tests/test_main_project.py

from typer.testing import CliRunner
from xolo.__main__ import app

runner = CliRunner()

def test_project_help():
    result = runner.invoke(app, ["project", "--help"])
    assert result.exit_code == 0
    assert "create-project" in result.output
    assert "delete-project" in result.output
    assert "import-media" in result.output

def test_config_help():
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "set-roots" in result.output
    assert "update-roots" in result.output

