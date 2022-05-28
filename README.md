# Websockets 
Create the list of websockets and work with them: ping and close one by one

# Prepare environment
1. python -m venv venv
2. python -m pip install -r requirements.txt
3. .\venv\Scripts\activate

# Run script
python .\client_websocket.py

# Task description 

We have the class **SyncWebSockets** which is derived from the Thread class and using run() method allows us to run the class instance in the thread.
So basically we describe the object (SyncWebSockets) that will be run separately in the thread.

**FatherWebSockets** main class helps to create and handle the list (actually dict with id and object memory reference) of SyncWebSockets instances. 
By default we run 5 websockets clients (threads) that are connected to default echo webserver -> "ws://echo.websocket.events/"

# FatherWebSockets methods:
  - **active_clients**: property that has the ref to the dict of our active websocket clients\thread
  - **check_active_clients**(): have a trick that verify our webcoket clients and in case we already kill some of them, we just remove this client from the dict in case we raise _WebSocketConnectionClosedException_ exception during ping() call
  - **get_client_by_uid**(): help to return the instance of the created SyncWebSockets class to work with the client
  -  **start_clients**(): call the default threads method to statr the thread 

# SyncWebSockets methods:
  - classic websocket methods with one termination to close the websocket...
# Task time:
Ovetall task time is about 2 hours.
