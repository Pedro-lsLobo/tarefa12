from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Recursos compartilhados
score = 0
score_lock = threading.Lock()

@app.route('/score', methods=['GET'])
def get_score():
    global score
    # Retorna o escore atualizado
    return jsonify({"score": score}), 200

@app.route('/score', methods=['PUT'])
def update_score():
    global score
    data = request.get_json()
    
    if not data or 'score' not in data:
        return jsonify({"error": "Payload inválido"}), 400
    
    new_score = data['score']
    
    # Garantia de atomicidade na validação e escrita interna do servidor
    with score_lock:
        if new_score > score:
            old_score = score
            score = new_score
            return jsonify({
                "status": "success",
                "old_score": old_score,
                "new_score": score
            }), 200
        else:
            return jsonify({
                "status": "rejected",
                "error": f"O escore enviado ({new_score}) não é maior que o atual ({score})."
            }), 400

if __name__ == '__main__':
    # Configurado para ouvir na porta 5678 em todas as interfaces de rede
    app.run(host='0.0.0.0', port=5678, debug=False)
