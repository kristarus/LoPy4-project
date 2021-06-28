import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind(('0.0.0.0', 5001))
serv_sock.listen(5)

while True:
    # Бесконечно обрабатываем входящие подключения
    print('acception a connection...')
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        data = client_sock.recv(1024)
        print(data)
        if not data:
            # Клиент отключился
            break
        client_sock.sendall(data)

    client_sock.close()
