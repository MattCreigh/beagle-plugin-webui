"""beagle-plugin-webui tests — the security invariants survive the move (WP-5)."""

from __future__ import annotations

import typer
from typer.testing import CliRunner


def test_plugin_exports_app() -> None:
    """The plugin contract: the entry-point module exports ``app``."""
    import beagle_plugin_webui.cli as cli_mod

    assert isinstance(cli_mod.app, typer.Typer)


def test_path_traversal_guard_present() -> None:
    """The audit-correct guard must survive byte-identical in the port."""
    import inspect

    from beagle_plugin_webui import server

    src = inspect.getsource(server)
    assert "relative_to" in src, "path-traversal guard lost in the move"
    assert "resolve(" in src


def test_webui_help_renders() -> None:
    from beagle_plugin_webui.cli import app

    r = CliRunner().invoke(app, ["--help"])
    assert r.exit_code == 0


def test_non_loopback_bind_without_token_refuses() -> None:
    """D-02: the refusal logic must be in the ported server."""
    import inspect
    import os

    from beagle_plugin_webui import server

    os.environ.pop("BEAGLE_WEBUI_TOKEN", None)
    assert server._is_loopback("127.0.0.1")
    assert not server._is_loopback("0.0.0.0")
    src = inspect.getsource(server.main)
    assert "BEAGLE_WEBUI_TOKEN" in src
