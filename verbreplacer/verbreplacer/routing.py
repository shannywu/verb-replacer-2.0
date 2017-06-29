from replacer.consumers import ws_connect, ws_receive

channel_routing = {
    # 'http.request': http_consumer,
    'websocket.connect': ws_connect,
    'websocket.receive': ws_receive,
    # 'websocket.disconnect': ws_disconnect,
}