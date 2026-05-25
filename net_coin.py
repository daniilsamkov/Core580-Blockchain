from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time

app = Flask(__name__)

blockchain = [
    {
        "index": 0,
        "timestamp": time.time(),
        "transactions": ["Genesis Block Network"],
        "previous_hash": "0",
        "nonce": 0,
        "hash": "000"
    }
]

# КРАСИВЫЙ HTML-ШАБЛОН ДЛЯ САЙТА
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Панель управления Криптосети CORE580</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px; }
        h1 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
        .status-box { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 6px; margin-top: 20px; }
        .neon-text { color: #7fee1d; font-weight: bold; }
        .block-card { background-color: #21262d; border: 1px solid #30363d; padding: 15px; margin-top: 10px; border-radius: 6px; }
        .hash { color: #8b949e; font-size: 12px; }
    </style>
</head>
<body>
    <h1>🚀 Добро пожаловать в децентрализованную сеть CORE580</h1>
    <p>Это полностью независимый блокчейн, запущенный на домашнем сервере Даниила.</p>
    
    <div class="status-box">
        <h3>📊 Статус ноды: <span class="neon-text">ОНЛАЙН (СЛУШАЕТ ПОРТ 5000)</span></h3>
        <p>Всего блоков в сети: <strong>{{ blocks_count }}</strong></p>
        <p>Алгоритм хэширования: <strong>SHA-256 (Оптимизация под GPU RX 580)</strong></p>
        <p>Награда за блок: <strong>50 монет CR580</strong></p>
    </div>

    <h2>⛓️ Последний смайненный блок в сети:</h2>
    <div class="block-card">
        <h3>Блок №{{ last_block.index }}</h3>
        <p>📋 Данные: <strong>{{ last_block.transactions }}</strong></p>
        <p class="hash">🔒 Хэш блока: {{ last_block.hash }}</p>
        <p class="hash">🔑 Nonce (Попыток): {{ last_block.nonce }}</p>
    </div>
</body>
</html>
"""

# 1. ГЛАВНАЯ СТРАНИЦА САЙТА (Теперь вместо 404 ошибки будет красота)
@app.route('/', methods=['GET'])
def index():
    return render_template_string(
        HTML_TEMPLATE, 
        blocks_count=len(blockchain), 
        last_block=blockchain[-1]
    )

# 2. Показать сырой блокчейн (для кошельков)
@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"chain": blockchain, "length": len(blockchain)}), 200

# 3. Принять новый блок от майнера
@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.get_json()
    if not data or 'transactions' not in data or 'nonce' not in data or 'hash' not in data:
        return jsonify({"message": "❌ Ошибка в данных"}), 400
    
    new_block = {
        "index": len(blockchain),
        "timestamp": time.time(),
        "transactions": data['transactions'],
        "previous_hash": blockchain[-1]['hash'],
        "nonce": data['nonce'],
        "hash": data['hash']
    }
    blockchain.append(new_block)
    return jsonify({"message": "🎉 Блок успешно принят глобальной сетью!", "block": new_block}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
