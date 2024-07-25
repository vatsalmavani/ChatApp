# ChatApp

## Overview

This project implements terminal based, real time chatting application. It follows the client-server architecture in which one central server provides data to all the clients.

## Usage

* Run the server script first
* Run the client script
* Use different bash instances to simulate different users
* User can exit from the chat using `/exit` command
* Server can be stopped running using `exit()` command

## Limitations

* The server can accept maximum of 10 connections.
* Every message must be less than 4096 bytes in size.

## Reference

* https://docs.python.org/3/howto/sockets.html
* https://docs.python.org/3/library/socket.html