"""Main class create the list of websocket connections and work with them"""
import asyncio
import threading
import time

import websocket


class SyncWebSockets(threading.Thread):
    """Class to handle websockets connection"""

    def __init__(self, url: str, uid: str):
        super().__init__()
        self._running = True
        self.uid = uid
        self.url = url
        self.ws = None
        self.open_connection(url=url)

    def open_connection(self, url: str):
        """open websocket connection"""
        self.ws = websocket.WebSocketApp(
            url=url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def run(self):
        """Run thread from derived Thread class"""
        while self._running:
            self.ws.run_forever()

    def terminate(self):
        """Terminate websocket connection"""
        self._running = False
        self.ws.close()

    def on_message(self, ws, message):
        """All messages are collected here"""
        print(f"Messages for {self.uid}: >>> {message}")

    def on_error(self, ws, error):
        """Any websocket errors"""
        pass

    def on_close(self, ws, close_status_code, close_msg):
        """On close method activities"""
        print(f"Closed connection: {self.uid}")

    def on_open(self, ws):
        """Open websocket event"""
        print(f"A new  connection: for client: {self.uid}")

    def ping(self):
        """Make a ping client"""
        print(f"{self.uid}: make a ping request")
        self.ws.send(f"{self.uid} ping request")

    def send_msg(self, msg: str):
        """send message to websocket server"""
        print(f"{self.uid}: send a message to websocket server")
        self.ws.send(f"{msg}")


class FatherWebSockets:
    """The main father class that handles all created clients"""

    def __init__(self, num_connections: int, url: str):
        print(f"Create the list websocket connections...")
        self._clients = {f"client_{x + 1}": SyncWebSockets(url, f"client_{x + 1}") for x in range(num_connections)}
        print(f"clients: {self._clients}")
        self.start_clients()

    def start_clients(self):
        """Start all active threads"""
        for client_id, client_ws in self._clients.items():
            time.sleep(0.1)
            client_ws.start()

    @property
    def active_clients(self):
        """Return the list of active clients"""
        return self._clients

    def get_client_by_uid(self, uid: str):
        """Return the client by UID"""
        try:
            client = self._clients[uid]
        except KeyError as e:
            client = None

        return client

    def check_active_clients(self):
        """Call ping method to raise answer"""
        for client_id, client_ws in self.active_clients.items():
            time.sleep(0.3)
            try:
                client_ws.ping()
            except websocket.WebSocketConnectionClosedException as e:
                print(f"Error: client: {client_id} is died. Remove from the active list")
                # remove this client from the list
                del self.active_clients[client_id]
                break


if __name__ == "__main__":
    # Using some echo websocket server which return our messages back
    url = "ws://echo.websocket.events/"
    # total number of the clients
    num = 5

    # 1. create the list of websocket clients connected to url
    print(f"\n\n::::::: Make {num} active websocket clients connection")
    father_clients = FatherWebSockets(num, url)

    # 2. take the list of active connection
    print(f"\n\n::::::: Total active clients: {len(father_clients.active_clients)} with objects: {father_clients.active_clients}")

    # need to wait a little bit while all thread will be started
    time.sleep(3)

    # 3. Ping them all \ check
    print(f"\n\n::::::: Try to ping all active clients: {len(father_clients.active_clients)} by calling ping() method")
    father_clients.check_active_clients()

    # 3. Starting from the last one till the first one - let's close one by one to see that they're still fine...
    for cl_num in range(num, 1, -1):
        print(f"\n\n::::::: Try to kill client: {cl_num}")
        # take client
        client: SyncWebSockets = father_clients.get_client_by_uid(f"client_{cl_num}")
        client.terminate()
        print(f"\n\n::::::: Ping\check all clients")
        time.sleep(.2)
        father_clients.check_active_clients()
        print(f"\n\n::::::: Total active clients: {len(father_clients.active_clients)}")
        time.sleep(.2)

    # 4. now we have only 1 active websocket let's push something there....
    print(f"We have the last one websocket - let's ping it")
    father_clients.check_active_clients()

    last_client: SyncWebSockets = father_clients.get_client_by_uid(f"client_1")
    last_client.send_msg("Hey! I'm the last one! Long live!")
    time.sleep(2)
    # close the last session
    last_client.terminate()
    print(f"Thanks, we're done!")
