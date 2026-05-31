import requests
import time
import random
import threading

# Configuração do endpoint do servidor AWS
SERVER_IP = "3.227.138.6"
SERVER_PORT = "5678"
URL = f"http://{SERVER_IP}:{SERVER_PORT}/score"

def worker_client(client_name, iterations=5):
    """Função que simula o comportamento de um único cliente"""
    print(f"[INFO] {client_name} conectado e jogando...")
    
    for i in range(iterations):
        try:
            # 1. Consulta o escore atual
            response = requests.get(URL, timeout=5)
            if response.status_code == 200:
                current_score = response.json()['score']
                
                # Pequeno atraso randômico para induzir a condição de corrida
                time.sleep(random.uniform(0.05, 0.2))
                
                # 2. Calcula a nova pontuação
                points_to_add = random.randint(1, 10)
                new_score = current_score + points_to_add
                
                # 3. Tenta atualizar o escore
                payload = {"score": new_score}
                update_response = requests.put(URL, json=payload, timeout=5)
                
                if update_response.status_code == 200:
                    res_data = update_response.json()
                    print(f" -> [SUCESSO] {client_name} subiu o placar de {res_data['old_score']} para {res_data['new_score']} (+{points_to_add})")
                else:
                    res_data = update_response.json()
                    print(f" -> [REJEITADO] {client_name} tentou enviar {new_score}, mas o servidor barrou: {res_data.get('error')}")
            else:
                print(f"[ERRO] {client_name} falhou na consulta: Status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[FALHA DE REDE] {client_name}: {e}")
            
        # Espera um pouco antes da próxima jogada
        time.sleep(random.uniform(0.3, 0.8))

def run_simulation(num_clients=5, iterations_per_client=5):
    """Dispara os clientes de forma concorrente"""
    print(f"=== Iniciando simulação com {num_clients} clientes concorrentes ===")
    threads = []
    
    # Cria e inicia as threads dos clientes
    for i in range(num_clients):
        client_name = f"Cliente_{i+1:02d}"
        t = threading.Thread(target=worker_client, args=(client_name, iterations_per_client))
        threads.append(t)
        t.start()
        
    # Aguarda todas as threads terminarem antes de encerrar o script
    for t in threads:
        t.join()
        
    print("=== Simulação finalizada ===")

if __name__ == '__main__':
    # Define quantos clientes você quer rodar de uma vez só (ex: 5 clientes, 5 rodadas cada)
    run_simulation(num_clients=5, iterations_per_client=5)
