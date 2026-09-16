"""beagle-plugin-webui — the dashboard as a discovered Beagle plugin."""

from __future__ import annotations

import os

import typer

webui_app = typer.Typer(help="Serve the Beagle web dashboard (real Beagle-backed).")


@webui_app.command("webui")
def webui(
    port: int = typer.Option(
        int(os.environ.get("BEAGLE_WEBUI_PORT", "8080")),
        "--port",
        "-p",
        help="Port to bind the web dashboard on.",
    ),
    host: str = typer.Option(
        os.environ.get("BEAGLE_WEBUI_HOST", "127.0.0.1"),
        "--host",
        help=(
            "Host interface to bind. Defaults to 127.0.0.1 (loopback only); "
            "set BEAGLE_WEBUI_TOKEN when binding to a non-loopback address."
        ),
    ),
) -> None:
    """Serve the Beagle web dashboard."""
    from beagle_plugin_webui import server as _server

    # The server's main() reads BEAGLE_WEBUI_PORT/HOST from the environment;
    # pass explicit overrides so CLI flags win (same precedence as before the
    # extraction — CLI args > env > default).
    os.environ["BEAGLE_WEBUI_PORT"] = str(port)
    os.environ["BEAGLE_WEBUI_HOST"] = host
    raise typer.Exit(_server.main())


app = webui_app