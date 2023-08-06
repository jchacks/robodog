import click


@click.command()
@click.option("--ip", help="IP of host to stream to.")
@click.option("--port", default=5000, type=int, help="Port to stream to.")
def camera(ip, port):
    """Run camera."""
    from robodog.server import camera

    camera.udp_stream(ip, port)


if __name__ == "__main__":
    camera()
