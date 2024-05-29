import zmq


class PoeterAPI:
    """
    Acts as an endpoint for the Poeter microservice
    """

    def __init__(self, host="localhost", port="5557") -> None:
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{host}:{port}")
        print("Poeter API initialized at port {}".format(port))

    def get_poem(self, prompt: str) -> str:
        request_json = {
            "type": "prompt",
            "payload": prompt
        }
        self.socket.send_json(request_json)
        reply = self.socket.recv_json()
        if reply['status'] == 'error':
            raise Exception(reply['payload'])
        return reply['payload']


if __name__ == "__main__":
    papi = PoeterAPI()
    print(papi.get_poem("Cloudy, sunbreaks later, high of 70"))
