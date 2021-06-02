import socket
import threading

from . import api


def send_flows(config: api.Config) -> None:
    src = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    dst = socket.socket(
        socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)
    )

    f = config.flows[0]
    src.bind((f.src_port, 0))

    dst.bind((f.dst_port, 0))

    t = threading.Thread(target=lambda: print(dst.recvfrom(65535)))
    t.start()

    src.send(f.frame_bytes)
    t.join()
