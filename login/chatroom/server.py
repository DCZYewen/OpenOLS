from websocket_server import WebsocketServer

# Called for every client connecting (after handshake)
def new_client(client, server):
        print("New client connected and was given id %d" % client['id'])
        #server.send_message_to_all("a new client...")
        server.send_message(client,"欢迎来到OpenOLS聊天室。")

# Called for every client disconnecting
def client_left(client, server):
        print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
        if len(message) > 200:
                message = message[:200]+'..'
        print("Client(%d)_address%s said: %s" % (client['id'],client['address'], message))
        server.send_message(client,'学生编号'+str(client['id'])+':'+message)


PORT=9005
server = WebsocketServer(PORT,host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()