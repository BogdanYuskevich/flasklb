import socket
import time

host = '127.0.0.1'
port = 55555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print(f"Server is listening on {host}, {port}")

conn, addr = s.accept()
print(f'Connected with {str(addr)}')

while True:
    data = conn.recv(1024).decode('utf-8')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nReceived from the client: {data}")
    print(f"time: {current_time}")

    if data == "stop":
        conn.close()
        print("\nConnection was closed by client.")
        break
    else:
        time.sleep(5)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        response = conn.send(data.encode('utf-8'))
        print(f"Replied to the client.")
        print(f"time: {current_time}")

        if len(data) == response:
            print("The text was sent successfully!")
        else:
            print("\nSomething went wrong!")

conn.close()
s.close()
