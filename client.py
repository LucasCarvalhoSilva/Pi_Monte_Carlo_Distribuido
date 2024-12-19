import socket

def connect_to_server():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print("=> Cálculo de Pi pelo Método de Monte Carlo <=")
        
        numberOfPoints = input("Digite a quantidade de pontos que devem ser simulados: ")
        client_socket.send(numberOfPoints.encode())
        
        response = client_socket.recv(1024).decode()
        
        if response.startswith("ERRO"):
            print(f"Erro: {response[6:]}")
        else:
            print(f"Com {numberOfPoints} pontos, o valor estimado de Pi é {response}")
            
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se ele está em execução.")
    except Exception as e:
        print(f"Erro: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    connect_to_server() 