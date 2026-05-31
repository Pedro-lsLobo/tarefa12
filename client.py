import requests
import time
import random
import sys

# Configuração do endpoint do servidor
SERVER_IP = "3.227.138.6"
SERVER_PORT = "5678"
URL = f"http://{SERVER_IP}:{SERVER_PORT}/score"

def run_client(client_id, iterations=10):
    print(f"--- Cliente {client_id} Iniciado ---")
    
    for i in range(iterations):
        try:
            # Passo 1: Consultar o escore atual
            response = requests.get(URL)
            if response.status_code == 200:
                current_score = response.json()['score']
                print(f"[Reg {i}] Cliente {client_id} leu escore: {current_score}")
                
                # Simula atraso de processamento/rede local para favorecer a concorrência
                time.sleep(random.uniform(0.1, 0.4))
                
                # Calcular o novo escore (Regra 1)
                points_to_add = random.randint(1, 10)
                new_score = current_score + points_to_add
                print(f"[Reg {i}] Cliente {client_id} calculou novo escore: {new_score} (+{points_to_add})")
                
                # Passo 2: Enviar a atualização
                payload = {"score": new_score}
                update_response = requests.put(URL, json=payload)
                
                if update_response.status_code == 200:
                    res_data = update_response.json()
                    print(f" -> [SUCESSO] Cliente {client_id} atualizou de {res_data['old_score']} para {res_data['new_score']}")
                else:
                    res_data = update_response.json()
                    print(f" -> [REJEITADO] Servidor barrou Cliente {client_id}: {res_data.get('error')}")
            else:
                print(f"Erro ao consultar o servidor: Código {response.status_code}")
                
        except Exception as e:
            print(f"Falha de comunicação: {e}")
            
        # Intervalo randômico entre requisições de jogo
        time.sleep(random.uniform(0.5, 1.5))

if __name__ == '__main__':
    # Permite passar o ID do cliente via linha de comando (ex: python3 client.py C1)
    cid = sys.argv[1] if len(sys.argv) > 1 else "Inominado"
    run_client(cid)
