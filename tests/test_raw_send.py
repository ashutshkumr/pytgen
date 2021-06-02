def test_raw_send(src_port: str, dst_port: str):
    from pytgen.api import Config, Flow
    from pytgen.transport import send_flows

    c = Config(
        "c", flows=[Flow(name="f1", src_port=src_port, dst_port=dst_port)]
    )
    send_flows(c)
