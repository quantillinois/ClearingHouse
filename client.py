import zmq

def main():
    context = zmq.Context()

    # Socket to talk to the server
    print("Connecting to the authentication server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Get username and password from user
    mpid = input("Enter MPID: ")
    password = input("Enter password: ")

    # Send authentication request
    socket.send_json({"mpid": mpid, "password": password})

    # Get the reply from the server
    message = socket.recv()
    print(f"Received reply: {message.decode('utf-8')}")

if __name__ == "__main__":
    main()