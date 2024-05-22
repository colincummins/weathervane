import base64

import zmq


class SkrivenerAPI:
    """
    Acts as an endpoint for the Skrivener microservice
    Adapted from Skrivener README -  https://github.com/bcliden/skrivener?tab=readme-ov-file
    """
    def __init__(self, host="localhost", port="8672") -> None:
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.bind(f"tcp://{host}:{port}")

    def text_to_img(self, text: str, bg_color: str = None, text_color: str = None) -> bytes:
        packet = {"text": text}
        if bg_color and text_color:
            colors: dict[str, str | None] = {"text": text_color, "bg": bg_color}
            packet['colors'] = colors
        self.socket.send_json(packet)
        reply: dict[str, str] = self.socket.recv_json()

        if reply['status'] == 'error':
            raise Exception(reply['message'])

        return base64.b64decode(reply['image'])
