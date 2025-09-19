#!/usr/bin/env python3
"""
🔧 GITHUB TOOLS INTEGRATION
============================

Интеграция готовых GitHub проектов для упрощения работы с Kali Linux
Автоматическая установка и использование популярных инструментов

ВНИМАНИЕ: Только для образовательных целей!

Автор: Образовательный материал для изучения кибербезопасности
"""

import subprocess
import sys
import os
import json
import requests
from pathlib import Path

class GitHubToolsIntegration:
    """
    Класс для интеграции готовых GitHub инструментов
    """
    
    def __init__(self):
        self.tools_dir = Path("github_tools")
        self.tools_dir.mkdir(exist_ok=True)
        
        # Список популярных GitHub проектов для пентеста
        self.github_tools = {
            # Сканирование и разведка
            'nmap': {
                'repo': 'nmap/nmap',
                'description': 'Network Mapper - инструмент для сканирования сети',
                'install_command': 'sudo apt install nmap'
            },
            'masscan': {
                'repo': 'robertdavidgraham/masscan',
                'description': 'Быстрый сканер портов',
                'install_command': 'sudo apt install masscan'
            },
            'zmap': {
                'repo': 'zmap/zmap',
                'description': 'Быстрое сканирование интернета',
                'install_command': 'sudo apt install zmap'
            },
            
            # Веб-тестирование
            'sqlmap': {
                'repo': 'sqlmapproject/sqlmap',
                'description': 'Автоматическое тестирование SQL injection',
                'install_command': 'sudo apt install sqlmap'
            },
            'nikto': {
                'repo': 'sullo/nikto',
                'description': 'Веб-сканер уязвимостей',
                'install_command': 'sudo apt install nikto'
            },
            'gobuster': {
                'repo': 'OJ/gobuster',
                'description': 'Быстрое перечисление директорий и файлов',
                'install_command': 'sudo apt install gobuster'
            },
            'dirb': {
                'repo': 'v0re/dirb',
                'description': 'Сканер веб-директорий',
                'install_command': 'sudo apt install dirb'
            },
            'wfuzz': {
                'repo': 'xmendez/wfuzz',
                'description': 'Веб-фаззер',
                'install_command': 'sudo apt install wfuzz'
            },
            
            # Brute force атаки
            'hydra': {
                'repo': 'vanhauser-thc/thc-hydra',
                'description': 'Быстрый brute force атакер',
                'install_command': 'sudo apt install hydra'
            },
            'john': {
                'repo': 'openwall/john',
                'description': 'John the Ripper - взлом паролей',
                'install_command': 'sudo apt install john'
            },
            'hashcat': {
                'repo': 'hashcat/hashcat',
                'description': 'Быстрый взлом хешей',
                'install_command': 'sudo apt install hashcat'
            },
            
            # Эксплойты и фреймворки
            'metasploit': {
                'repo': 'rapid7/metasploit-framework',
                'description': 'Фреймворк для разработки и выполнения эксплойтов',
                'install_command': 'curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb | sudo bash'
            },
            'exploitdb': {
                'repo': 'offensive-security/exploitdb',
                'description': 'База данных эксплойтов',
                'install_command': 'sudo apt install exploitdb'
            },
            'searchsploit': {
                'repo': 'offensive-security/exploitdb',
                'description': 'Поиск в базе данных эксплойтов',
                'install_command': 'sudo apt install exploitdb'
            },
            
            # Специализированные инструменты
            'burpsuite': {
                'repo': 'PortSwigger/burp-suite-community',
                'description': 'Веб-прокси для тестирования безопасности',
                'install_command': 'sudo apt install burpsuite'
            },
            'wireshark': {
                'repo': 'wireshark/wireshark',
                'description': 'Анализатор сетевого трафика',
                'install_command': 'sudo apt install wireshark'
            },
            'aircrack-ng': {
                'repo': 'aircrack-ng/aircrack-ng',
                'description': 'Набор инструментов для тестирования WiFi',
                'install_command': 'sudo apt install aircrack-ng'
            },
            'reaver': {
                'repo': 't6x/reaver-wps-fork-t6x',
                'description': 'Атака на WPS',
                'install_command': 'sudo apt install reaver'
            },
            
            # Python инструменты
            'scapy': {
                'repo': 'secdev/scapy',
                'description': 'Библиотека для работы с сетевыми пакетами',
                'install_command': 'pip3 install scapy'
            },
            'requests': {
                'repo': 'psf/requests',
                'description': 'HTTP библиотека для Python',
                'install_command': 'pip3 install requests'
            },
            'paramiko': {
                'repo': 'paramiko/paramiko',
                'description': 'SSH2 библиотека для Python',
                'install_command': 'pip3 install paramiko'
            },
            
            # Дополнительные инструменты
            'nuclei': {
                'repo': 'projectdiscovery/nuclei',
                'description': 'Быстрое сканирование уязвимостей',
                'install_command': 'sudo apt install nuclei'
            },
            'subfinder': {
                'repo': 'projectdiscovery/subfinder',
                'description': 'Поиск поддоменов',
                'install_command': 'sudo apt install subfinder'
            },
            'ffuf': {
                'repo': 'ffuf/ffuf',
                'description': 'Быстрый веб-фаззер',
                'install_command': 'sudo apt install ffuf'
            }
        }
    
    def install_tool(self, tool_name):
        """
        Устанавливает указанный инструмент
        """
        if tool_name not in self.github_tools:
            print(f"❌ Инструмент {tool_name} не найден в списке")
            return False
        
        tool_info = self.github_tools[tool_name]
        print(f"🔧 Устанавливаю {tool_name}: {tool_info['description']}")
        
        # Выполняем команду установки
        install_command = tool_info['install_command']
        print(f"💻 Выполняю: {install_command}")
        
        try:
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {tool_name} успешно установлен")
                return True
            else:
                print(f"❌ Ошибка установки {tool_name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Исключение при установке {tool_name}: {e}")
            return False
    
    def install_all_tools(self):
        """
        Устанавливает все доступные инструменты
        """
        print("🔧 УСТАНОВКА ВСЕХ ИНСТРУМЕНТОВ")
        print("="*60)
        
        success_count = 0
        total_count = len(self.github_tools)
        
        for tool_name in self.github_tools:
            if self.install_tool(tool_name):
                success_count += 1
            print()  # Пустая строка для читаемости
        
        print("="*60)
        print(f"📊 РЕЗУЛЬТАТЫ УСТАНОВКИ:")
        print(f"  ✅ Успешно установлено: {success_count}/{total_count}")
        print(f"  ❌ Ошибки установки: {total_count - success_count}/{total_count}")
    
    def install_category(self, category):
        """
        Устанавливает инструменты по категориям
        """
        categories = {
            'scanning': ['nmap', 'masscan', 'zmap', 'nuclei', 'subfinder'],
            'web': ['sqlmap', 'nikto', 'gobuster', 'dirb', 'wfuzz', 'ffuf', 'burpsuite'],
            'bruteforce': ['hydra', 'john', 'hashcat'],
            'exploits': ['metasploit', 'exploitdb', 'searchsploit'],
            'wireless': ['aircrack-ng', 'reaver'],
            'network': ['wireshark', 'scapy'],
            'python': ['scapy', 'requests', 'paramiko']
        }
        
        if category not in categories:
            print(f"❌ Категория {category} не найдена")
            print(f"Доступные категории: {', '.join(categories.keys())}")
            return
        
        tools = categories[category]
        print(f"🔧 Устанавливаю инструменты категории: {category}")
        print("="*60)
        
        for tool in tools:
            self.install_tool(tool)
            print()
    
    def check_tool_availability(self, tool_name):
        """
        Проверяет доступность инструмента в системе
        """
        if tool_name not in self.github_tools:
            print(f"❌ Инструмент {tool_name} не найден в списке")
            return False
        
        tool_info = self.github_tools[tool_name]
        
        # Проверяем, установлен ли инструмент
        try:
            result = subprocess.run(f"which {tool_name}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {tool_name} установлен: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ {tool_name} не установлен")
                return False
        except Exception as e:
            print(f"❌ Ошибка проверки {tool_name}: {e}")
            return False
    
    def check_all_tools(self):
        """
        Проверяет доступность всех инструментов
        """
        print("🔍 ПРОВЕРКА ДОСТУПНОСТИ ИНСТРУМЕНТОВ")
        print("="*60)
        
        available_count = 0
        total_count = len(self.github_tools)
        
        for tool_name in self.github_tools:
            if self.check_tool_availability(tool_name):
                available_count += 1
        
        print("="*60)
        print(f"📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
        print(f"  ✅ Доступно: {available_count}/{total_count}")
        print(f"  ❌ Недоступно: {total_count - available_count}/{total_count}")
    
    def download_wordlists(self):
        """
        Скачивает популярные словари для brute force атак
        """
        print("📚 СКАЧИВАНИЕ СЛОВАРЕЙ ДЛЯ BRUTE FORCE")
        print("="*60)
        
        wordlists_dir = Path("wordlists")
        wordlists_dir.mkdir(exist_ok=True)
        
        # Популярные словари
        wordlists = {
            'rockyou.txt': {
                'url': 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt',
                'description': 'Популярный словарь паролей'
            },
            'common_passwords.txt': {
                'url': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt',
                'description': 'Список распространенных паролей'
            },
            'usernames.txt': {
                'url': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/xato-net-10-million-usernames.txt',
                'description': 'Список имен пользователей'
            },
            'directories.txt': {
                'url': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt',
                'description': 'Список веб-директорий'
            }
        }
        
        for filename, info in wordlists.items():
            filepath = wordlists_dir / filename
            if filepath.exists():
                print(f"⚠️ {filename} уже существует, пропускаю")
                continue
            
            print(f"📥 Скачиваю {filename}: {info['description']}")
            try:
                response = requests.get(info['url'], stream=True)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"✅ {filename} скачан успешно")
                else:
                    print(f"❌ Ошибка скачивания {filename}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Ошибка скачивания {filename}: {e}")
    
    def setup_kali_environment(self):
        """
        Настраивает среду Kali Linux для пентеста
        """
        print("🔧 НАСТРОЙКА СРЕДЫ KALI LINUX")
        print("="*60)
        
        # Обновление системы
        print("🔄 Обновляю систему...")
        subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True)
        
        # Установка дополнительных пакетов
        print("📦 Устанавливаю дополнительные пакеты...")
        additional_packages = [
            'curl', 'wget', 'git', 'python3-pip', 'python3-venv',
            'build-essential', 'libssl-dev', 'libffi-dev',
            'ruby', 'golang', 'nodejs', 'npm'
        ]
        
        for package in additional_packages:
            print(f"  📦 Устанавливаю {package}...")
            subprocess.run(f"sudo apt install -y {package}", shell=True)
        
        # Настройка Python окружения
        print("🐍 Настраиваю Python окружение...")
        subprocess.run("python3 -m pip install --upgrade pip", shell=True)
        subprocess.run("pip3 install virtualenv", shell=True)
        
        print("✅ Среда Kali Linux настроена")
    
    def generate_tool_report(self):
        """
        Генерирует отчет об установленных инструментах
        """
        print("📊 ГЕНЕРАЦИЯ ОТЧЕТА ОБ ИНСТРУМЕНТАХ")
        print("="*60)
        
        report = {
            'timestamp': str(subprocess.run('date', shell=True, capture_output=True, text=True).stdout.strip()),
            'system_info': {
                'os': subprocess.run('uname -a', shell=True, capture_output=True, text=True).stdout.strip(),
                'python_version': subprocess.run('python3 --version', shell=True, capture_output=True, text=True).stdout.strip()
            },
            'tools_status': {}
        }
        
        for tool_name in self.github_tools:
            try:
                result = subprocess.run(f"which {tool_name}", shell=True, capture_output=True, text=True)
                report['tools_status'][tool_name] = {
                    'installed': result.returncode == 0,
                    'path': result.stdout.strip() if result.returncode == 0 else None,
                    'description': self.github_tools[tool_name]['description']
                }
            except:
                report['tools_status'][tool_name] = {
                    'installed': False,
                    'path': None,
                    'description': self.github_tools[tool_name]['description']
                }
        
        # Сохраняем отчет
        report_file = 'tools_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Отчет сохранен в {report_file}")
        
        # Выводим краткую статистику
        installed_count = sum(1 for tool in report['tools_status'].values() if tool['installed'])
        total_count = len(report['tools_status'])
        
        print(f"\n📊 СТАТИСТИКА:")
        print(f"  ✅ Установлено: {installed_count}/{total_count}")
        print(f"  ❌ Не установлено: {total_count - installed_count}/{total_count}")

def main():
    """
    Главная функция
    """
    parser = argparse.ArgumentParser(description='GitHub Tools Integration for Kali Linux')
    parser.add_argument('--install-all', action='store_true', help='Установить все инструменты')
    parser.add_argument('--install-category', help='Установить инструменты по категории')
    parser.add_argument('--install-tool', help='Установить конкретный инструмент')
    parser.add_argument('--check-all', action='store_true', help='Проверить все инструменты')
    parser.add_argument('--download-wordlists', action='store_true', help='Скачать словари')
    parser.add_argument('--setup-kali', action='store_true', help='Настроить среду Kali Linux')
    parser.add_argument('--generate-report', action='store_true', help='Генерировать отчет')
    
    args = parser.parse_args()
    
    integration = GitHubToolsIntegration()
    
    try:
        if args.install_all:
            integration.install_all_tools()
        elif args.install_category:
            integration.install_category(args.install_category)
        elif args.install_tool:
            integration.install_tool(args.install_tool)
        elif args.check_all:
            integration.check_all_tools()
        elif args.download_wordlists:
            integration.download_wordlists()
        elif args.setup_kali:
            integration.setup_kali_environment()
        elif args.generate_report:
            integration.generate_tool_report()
        else:
            print("🔧 GITHUB TOOLS INTEGRATION")
            print("="*60)
            print("Используйте --help для просмотра доступных опций")
            print("\nПримеры использования:")
            print("  python3 github_tools_integration.py --install-all")
            print("  python3 github_tools_integration.py --install-category web")
            print("  python3 github_tools_integration.py --install-tool nmap")
            print("  python3 github_tools_integration.py --check-all")
            print("  python3 github_tools_integration.py --download-wordlists")
            print("  python3 github_tools_integration.py --setup-kali")
            print("  python3 github_tools_integration.py --generate-report")
            
    except KeyboardInterrupt:
        print("\n🛑 Операция прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
