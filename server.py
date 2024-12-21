import socket
from src.utils.generator import generateRandomPoints

def calculate_pi_points(num_points):
    points_inside = 0
    total_points = num_points
    
    batch_size = 1000000
    remaining_points = num_points
    
    while remaining_points > 0:
        current_batch = min(batch_size, remaining_points)
        
        for x, y in generateRandomPoints(current_batch):
            if x**2 + y**2 <= 1:
                points_inside += 1
        
        remaining_points -= current_batch
    
    return points_inside, total_points

def start_server():
    host = 'localhost'
    port = 5000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Servidor iniciado. Aguardando conexões...")
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Cliente conectado: {address}")
            
            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    
                    try:
                        num_points = int(data)
                        points_inside, total_points = calculate_pi_points(num_points)
                        response = f"{points_inside},{total_points}"
                        client_socket.send(response.encode())
                        
                    except ValueError:
                        error_msg = "ERRO: Número de pontos inválido"
                        client_socket.send(error_msg.encode())
                    except Exception as e:
                        error_msg = f"ERRO: {str(e)}"
                        client_socket.send(error_msg.encode())
                        
            except Exception as e:
                print(f"Erro na comunicação com o cliente: {str(e)}")
            finally:
                client_socket.close()
                print(f"Cliente desconectado: {address}")
                
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")
    except Exception as e:
        print(f"Erro no servidor: {str(e)}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server() 