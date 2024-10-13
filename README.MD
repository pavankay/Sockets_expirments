# WebSocket Experiments

This project contains various experiments using the [websockets](https://websockets.readthedocs.io/en/stable/) package and [pygame](https://www.pygame.org/docs/) with Python.


### What is a socket

A socket is an endpoint for sending or receiving data across a computer network. It allows communication between different processes, either on the same machine or across different machines over a network. Sockets also support BI directional data transfer. Sockets could be used for games and fun fact is used in gmail. Well what's the difference? On a http server, everytime you want to send data you make connection negotiate the terms send the data and then destroy the connection, Sockets leave that connection open for back and forth data Transfer. Sockets are used in various network protocols, including TCP and UDP, to establish connections and transfer data.

## Setup

### Prerequisites

- Python (tested in Python 3.11.9 )

### Installation
- Install the required packages using `pip`:

```sh
 pip install -r requirements.txt 
```
### Clone the Repository

To get started, clone the repository:

```sh
git clone https://github.com/pavankay/Sockets_expirments
cd Sockets_expirments
```
### Running the code
## Run Multiplayer_box

- cd into directory
```sh
 cd Multiplayer_box
```
- Run the server code using the following command:
```sh
python Multiplaye\server.py
```
- Run the client code using the following command:

```sh
python Multiplaye\client.py
```


### Run Multiplayer_box_web

- cd into directory

```sh
 cd Multiplayer_box_web
```
- Run the server code using the following command:
```sh
python Multiplaye\server.py
```
- Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser


### Notes

- You can run multiple clients or browser tabs to see the multiplayer in action.
- "localhost" means on your own computer so it can only be accessed by your own computer. You can make it multiplayer over other computer connect to the internet by changing the uri and on the connecting client, in the Multiplayer_box/network.py file for example, on line 6 (or as a perameter of the class in client.py) you can set that to http://<local IP>:<port>. The port in our case is 8765.
- You can set this up easisly to make it online from anywhere in the world by using cloud deployment like Azure, AWS, GCP.
