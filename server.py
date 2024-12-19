import socket
from src.calculator import calculatePi

def start_server():
    host = 'localhost'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Servidor iniciado. Aguardando conexões...")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexão estabelecida com: {address}")
        
        try:
            data = client_socket.recv(1024).decode()
            numberOfPoints = int(data)
            
            if numberOfPoints <= 0:
                response = "ERRO: O número de pontos deve ser maior que 0"
            else:
                estimatedPi = calculatePi(numberOfPoints)
                response = f"{estimatedPi:.6f}"
                
            client_socket.send(response.encode())
            
        except Exception as e:
            client_socket.send(f"ERRO: {str(e)}".encode())
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server() 