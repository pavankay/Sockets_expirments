# WebSocket Experiments

This project contains various experiments using the [websockets](https://websockets.readthedocs.io/en/stable/) package and [pygame](https://www.pygame.org/docs/) with Python.


### What is a socket

A socket is an endpoint for sending or receiving data across a computer network. It allows communication between different processes, either on the same machine or across different machines over a network. Sockets also support BI directional data transfer. Sockets could be used for games and fun fact is used in gmail. Well what's the difference? Imagine that on a http server, everytime you want to send data you make connection negoitatio the terms send the data and then destroy the connection, Sockets leave that connection open for back and forth data Transfer.Sockets are used in various network protocols, including TCP and UDP, to establish connections and transfer data.

## Setup

### Prerequisites

- Python 3.11

### Installation
- Install the required packages using `pip`:

```sh
 pip install pygame weboscket 
```
### Clone the Repository

To get started, clone the repository:

```sh
git clone https://github.com/pavankay/Sockets_expirments
cd Sockets_expirments
```
### Running the code

- Run the server code using the following command:

```sh
python Multiplaye\server.py
```
- Run the client code using the following command:

```sh
python Multiplaye\client.py
```
-Note you can run multiple clients to see the multiplayer in action.