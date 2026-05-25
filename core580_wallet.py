import hashlib
import json
import time
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Адрес ноды твоего сервера. Пока тестируем локально, потом заменим на ссылку trycloudflare!
NODE_URL = "http://127.0.0.1:5000"

def init_wallet():
    """Создает ключи кошелька, если их еще нет"""
    try:
        with open("public_key.pem", "r") as f:
            pub_key = f.read()
        print("🔑 Кошелек загружен успешно!")
        return pub_key
    except FileNotFoundError:
        print("⚙️  Создаем новый крипто-кошелек Core580...")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        
        with open("private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("public_key.pem", "wb") as f:
            f.write(pub_bytes)
        return pub_bytes.decode()

def run_miner(wallet_address):
    """Майнер: скачивает блок с сервера, подбирает хэш и отправляет обратно"""
    print(f"\n⛏️  Запуск майнера Core580 на кошелек: {wallet_address[:30]}...")
    difficulty = 3 # Сложность (3 нуля в начале)
    target = "0" * difficulty
    
    while True:
        # 1. Запрашиваем инфу о цепочке с сервера
        try:
            response = requests.get(f"{NODE_URL}/chain")
            chain_data = response.json()
            last_block = chain_data["chain"][-1]
        except Exception as e:
            print("❌ Ошибка подключения к серверу ноды. Переподключение через 5 сек...")
            time.sleep(5)
            continue

        # Имитируем сборку новых транзакций для блока
        transactions = [f"Награда за майнинг для кошелька {wallet_address[:15]}..."]
        new_index = last_block["index"] + 1
        prev_hash = last_block["hash"]
        
        print(f"🔄 Майним Блок №{new_index}... Ищем хэш с {difficulty} нулями...")
        
        nonce = 0
        start_time = time.time()
        
        # Основной цикл перебора хэшей
        while True:
            block_string = json.dumps({
                "index": new_index,
                "previous_hash": prev_hash,
                "transactions": transactions,
                "nonce": nonce
            }, sort_keys=True).encode()
            
            current_hash = hashlib.sha256(block_string).hexdigest()
            
            if current_hash[:difficulty] == target:
                end_time = time.time()
                print(f"🎉 БЛОК НАЙДЕН ЗА {round(end_time - start_time, 3)} сек! Nonce: {nonce}")
                print(f"🔗 Хэш: {current_hash}")
                
                # 2. Отправляем найденный блок обратно на твой веб-сервер
                payload = {"transactions": transactions, "nonce": nonce, "hash": current_hash}
                try:
                    res = requests.post(f"{NODE_URL}/mine", json=payload)
                    print(f"📡 Ответ сервера: {res.json()['message']}\n")
                except:
                    print("❌ Ошибка отправки блока на сервер!")
                break
                
            nonce += 1
            # Небольшая пауза, чтобы не намертво вешать проц перед GPU интеграцией
            if nonce % 500000 == 0:
                print(f"⏳ Перебрано {nonce} хэшей...")

if __name__ == "__main__":
    print("=== КРИПТОСИСТЕМА CORE580 ===")
    my_address = init_wallet()
    
    # Запускаем бесконечный майнинг
    run_miner(my_address)
