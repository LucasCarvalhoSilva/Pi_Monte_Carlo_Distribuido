import socket
import threading
import time
from queue import Queue

def worker(host, port, points_to_calculate, result_queue):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        batch_size = 1000000
        remaining = points_to_calculate
        
        while remaining > 0:
            current_batch = min(batch_size, remaining)
            client_socket.send(str(current_batch).encode())
            response = client_socket.recv(1024).decode()
            
            if response.startswith("ERRO"):
                print(f"Erro: {response[6:]}")
                break
            else:
                dentro, total = map(int, response.split(','))
                result_queue.put((dentro, total))
                remaining -= current_batch
            
    except Exception as e:
        print(f"Erro na thread: {str(e)}")
    finally:
        client_socket.close()

def connect_to_server():
    host = 'localhost'
    port = 5000
    
    try:
        startTime = time.time()
        print("=> Cálculo de Pi pelo Método de Monte Carlo <=")
        total_points = int(input("Digite a quantidade de pontos que devem ser simulados: "))
        
        num_threads = 5
        points_per_thread = total_points // num_threads
        remaining_points = total_points % num_threads

        result_queue = Queue()
        threads = []
        
        for i in range(num_threads):
            points = points_per_thread + (remaining_points if i == num_threads-1 else 0)
            thread = threading.Thread(
                target=worker,
                args=(host, port, points, result_queue)
            )
            threads.append(thread)
            thread.start()
            print(f"Thread {i+1} iniciada com {points} pontos")
        
        pontos_dentro_total = 0
        pontos_totais = 0
        resultados_processados = 0
        
        while resultados_processados < total_points:
            try:
                dentro, total = result_queue.get(timeout=1)
                pontos_dentro_total += dentro
                pontos_totais += total
                resultados_processados += total
                
                pi_parcial = 4 * pontos_dentro_total / pontos_totais
                progresso = (pontos_totais * 100) // total_points
                print(f"Progresso: {progresso}% - Pi estimado atual: {pi_parcial:.6f}")
                
            except Queue.Empty:
                continue
        
        for thread in threads:
            thread.join()
        
        if pontos_totais > 0:
            pi_final = 4 * pontos_dentro_total / pontos_totais
            endTime = time.time()
            print(f"\nResultado final com {pontos_totais} pontos:")
            print(f"Valor estimado de Pi: {pi_final:.6f}")
            executionTime = (endTime - startTime) * 1000
            print("Tempo de execução =>", executionTime)
    
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se ele está em execução.")
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    connect_to_server() 