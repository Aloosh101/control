
import socket
import threading


host = "0.0.0.0"
port = 8080


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.bind((host, port))


s.listen()


def handle_connection(conn, addr):
    
    print("Connected by", addr)

    
    file_name = None

    
    file_size = None

    
    file_data = b""

    
    file_offset = 0

    
    while True:
        
        data = conn.recv(1024)

        
        if not data:
            
            break

        
        if file_name is None and file_size is None:
            
            message = data.decode("utf-8")

            
            fields = message.split(",\n")

            
            if len(fields) == 2:
                
                file_name = fields[0]
                file_size = int(fields[1])

                
                conn.sendall(b"OK\n")
            else:
                
                conn.sendall(b"ERROR\n")
                conn.close()
                return

        else:
            
            file_data += data

            
            file_offset += len(data)

            
            if file_offset >= file_size:
                
                with open(file_name, "wb") as f:
                    f.write(file_data)

                
                print(f"File received: {file_name}")

                
                conn.sendall(b"OK\n")
                conn.close()
                return



while True:
    
    conn, addr = s.accept()

    
    threading.Thread(target=handle_connection, args=(conn, addr)).start()
