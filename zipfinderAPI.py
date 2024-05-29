import zmq


class ZipfinderAPI:
    """
    Acts as an endpoint for the Zipfinder microservice
    """

    def __init__(self, host="localhost", port="5556") -> None:
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{host}:{port}")
        print("Zipfinder API initialized at port {}".format(port))

    def get_location(self, geodata:str):
        request_json = {
            "type": "location",
            "payload": geodata
        }
        self.socket.send_json(request_json)
        reply = self.socket.recv_json()
        if reply['status'] == 'Error':
            raise Exception(reply['message'])

        return reply['payload']
