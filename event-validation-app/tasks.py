import os
import time

from invoke import task


def wait_port_is_open(host, port): # nosec
    import socket
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            sock.close()
            print(result, "host: ", host, " port: ", port)
            if result == 0:
                return
            time.sleep(1)
        except Exception:
            continue


@task
def devStart(ctx):
    wait_port_is_open("db", 5432)

    ctx.run("python3 manage.py runserver 0.0.0.0:8000")
