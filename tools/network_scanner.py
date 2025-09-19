
#!/usr/bin/env python3
"""
Образовательный сетевой сканер для изучения методов разведки
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import socket
import threading
import subprocess
import sys
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from scapy.all import *
import nmap
import ipaddress

class NetworkScanner:
    """
    Образовательный сетевой сканер для демонстрации методов разведки
    """
    
    def __init__(self, target_network):
        self.target_network = target_network
        self.open_ports = {}
        self.alive_hosts = []
        self.vulnerabilities = {}
        
        # Проверка безопасности
        if not self._is_safe_network(target_network):
            print("❌ ОШИБКА: Сканирование разрешено только для локальных сетей!")
            print("Разрешенные сети: 127.0.0.0/8, 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12")
            sys.exit(1)
    
    def _is_safe_network(self, network):
        """
        Проверяет, является ли сеть безопасной для сканирования
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            
            # Разрешенные частные сети
            safe_networks = [
                ipaddress.IPv4Network('127.0.0.0/8'),    # localhost
                ipaddress.IPv4Network('192.168.0.0/16'), # частная сеть класса C
                ipaddress.IPv4Network('10.0.0.0/8'),     # частная сеть класса A
                ipaddress.IPv4Network('172.16.0.0/12'),  # частная сеть класса B
            ]
            
            return any(net.subnet_of(safe_net) or net == safe_net for safe_net in safe_networks)
        except:
            return False
    
    def ping_sweep(self, timeout=1):
        """
        Ping sweep для обнаружения живых хостов в сети
        """
        print(f"🔍 Выполняю ping sweep для сети {self.target_network}")
        
        try:
            network = ipaddress.IPv4Network(self.target_network, strict=False)
        except ValueError as e:
            print(f"❌ Неверный формат сети: {e}")
            return []
        
        alive_hosts = []
        
        def ping_host(ip):
            """Пинг отдельного хоста"""
            try:
                # Используем системную команду ping
                if sys.platform.startswith('win'):
                    cmd = ['ping', '-n', '1', '-w', str(timeout * 1000), str(ip)]
                else:
                    cmd = ['ping', '-c', '1', '-W', str(timeout), str(ip)]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+1)
                
                if result.returncode == 0:
                    print(f"✅ {ip} - жив")
                    return str(ip)
                    
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                pass
            
            return None
        
        # Параллельный пинг хостов
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(ping_host, ip): ip for ip in network.hosts()}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    alive_hosts.append(result)
        
        self.alive_hosts = alive_hosts
        print(f"📊 Найдено {len(alive_hosts)} живых хостов")
        return alive_hosts
    
    def arp_scan(self):
        """
        ARP сканирование для обнаружения устройств в локальной сети
        """
        print(f"🔍 Выполняю ARP сканирование для {self.target_network}")
        
        try:
            # Создаем ARP запрос для всей сети
            arp_request = ARP(pdst=self.target_network)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # Отправляем запрос и получаем ответы
            answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
            
            hosts_info = []
            for element in answered_list:
                host_dict = {
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc
                }
                hosts_info.append(host_dict)
                print(f"✅ {element[1].psrc} - {element[1].hwsrc}")
            
            print(f"📊 ARP сканирование завершено. Найдено {len(hosts_info)} устройств")
            return hosts_info
            
        except Exception as e:
            print(f"❌ Ошибка ARP сканирования: {e}")
            return []
    
    def port_scan_host(self, host, ports, timeout=1):
        """
        Сканирование портов на конкретном хосте
        """
        open_ports = []
        
        def scan_port(port):
            """Сканирование отдельного порта"""
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    return port
            except:
                pass
            return None
        
        print(f"🔍 Сканирую порты на {host}")
        
        # Параллельное сканирование портов
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, port): port for port in ports}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"  ✅ Порт {result} открыт")
        
        return sorted(open_ports)
    
    def comprehensive_port_scan(self, common_ports_only=True):
        """
        Комплексное сканирование портов на всех живых хостах
        """
        if not self.alive_hosts:
            print("⚠️  Сначала выполните поиск живых хостов")
            return
        
        # Список наиболее распространенных портов
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080
        ]
        
        # Расширенный список портов для полного сканирования
        extended_ports = list(range(1, 1025)) + [1433, 1521, 2049, 2121, 2375, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017]
        
        ports_to_scan = common_ports if common_ports_only else extended_ports
        
        print(f"🔍 Сканирую {len(ports_to_scan)} портов на {len(self.alive_hosts)} хостах")
        
        for host in self.alive_hosts:
            open_ports = self.port_scan_host(host, ports_to_scan)
            if open_ports:
                self.open_ports[host] = open_ports
        
        return self.open_ports
    
    def service_detection(self, host, port):
        """
        Определение сервиса, работающего на порту
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            
            # Отправляем HTTP запрос для веб-сервисов
            if port in [80, 443, 8080, 8443]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                
            # Для других портов просто читаем баннер
            else:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
            
            sock.close()
            return banner.strip()[:200]  # Ограничиваем длину баннера
            
        except:
            return "Неизвестный сервис"
    
    def vulnerability_scan(self):
        """
        Базовое сканирование уязвимостей
        """
        print("🔍 Выполняю поиск известных уязвимостей...")
        
        for host in self.open_ports:
            host_vulns = []
            
            for port in self.open_ports[host]:
                service_banner = self.service_detection(host, port)
                
                # Проверка на известные уязвимые сервисы
                vulns = self._check_known_vulnerabilities(port, service_banner)
                if vulns:
                    host_vulns.extend(vulns)
                
                print(f"  📋 {host}:{port} - {service_banner[:50]}...")
            
            if host_vulns:
                self.vulnerabilities[host] = host_vulns
        
        return self.vulnerabilities
    
    def _check_known_vulnerabilities(self, port, banner):
        """
        Проверка на известные уязвимости по порту и баннеру
        """
        vulnerabilities = []
        banner_lower = banner.lower()
        
        # Проверка веб-сервисов
        if port in [80, 443, 8080, 8443]:
            if 'apache' in banner_lower:
                if '2.2' in banner_lower or '2.0' in banner_lower:
                    vulnerabilities.append("Устаревшая версия Apache - возможны уязвимости")
            
            if 'nginx' in banner_lower:
                if any(v in banner_lower for v in ['1.0', '1.1', '1.2']):
                    vulnerabilities.append("Устаревшая версия Nginx - возможны уязвимости")
            
            if 'iis' in banner_lower:
                vulnerabilities.append("IIS сервер - проверьте на уязвимости Windows")
        
        # Проверка SSH
        elif port == 22:
            if 'openssh' in banner_lower:
                if any(v in banner_lower for v in ['5.', '6.', '7.0', '7.1', '7.2']):
                    vulnerabilities.append("Устаревшая версия OpenSSH - возможны уязвимости")
        
        # Проверка FTP
        elif port == 21:
            if 'vsftpd' in banner_lower:
                if '2.3.4' in banner_lower:
                    vulnerabilities.append("КРИТИЧНО: vsftpd 2.3.4 - известная backdoor уязвимость!")
        
        # Проверка Telnet
        elif port == 23:
            vulnerabilities.append("ВНИМАНИЕ: Telnet использует незашифрованную передачу данных")
        
        # Проверка MySQL
        elif port == 3306:
            vulnerabilities.append("MySQL сервер - проверьте настройки безопасности")
        
        # Проверка RDP
        elif port == 3389:
            vulnerabilities.append("RDP сервис - уязвим к brute force атакам")
        
        return vulnerabilities
    
    def nmap_scan(self, scan_type='sS'):
        """
        Использование nmap для продвинутого сканирования
        """
        print(f"🔍 Выполняю Nmap сканирование ({scan_type}) для {self.target_network}")
        
        try:
            nm = nmap.PortScanner()
            
            # Различные типы сканирования
            scan_args = {
                'sS': '-sS',  # SYN scan
                'sT': '-sT',  # TCP connect scan
                'sU': '-sU',  # UDP scan
                'sV': '-sV',  # Version detection
                'O': '-O',    # OS detection
                'A': '-A'     # Aggressive scan
            }
            
            result = nm.scan(self.target_network, arguments=scan_args.get(scan_type, '-sS'))
            
            for host in nm.all_hosts():
                print(f"\n🎯 Хост: {host}")
                print(f"   Статус: {nm[host].state()}")
                
                if 'osmatch' in nm[host]:
                    for osmatch in nm[host]['osmatch']:
                        print(f"   ОС: {osmatch['name']} ({osmatch['accuracy']}%)")
                
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port].get('name', 'unknown')
                        version = nm[host][proto][port].get('version', '')
                        
                        print(f"   📡 {port}/{proto}: {state} ({service} {version})")
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка Nmap сканирования: {e}")
            return None
    
    def generate_report(self):
        """
        Генерация отчета о сканировании
        """
        print("\n" + "="*60)
        print("📊 ОТЧЕТ О СКАНИРОВАНИИ СЕТИ")
        print("="*60)
        
        print(f"\n🎯 Целевая сеть: {self.target_network}")
        print(f"📅 Время сканирования: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n🖥️  ЖИВЫЕ ХОСТЫ ({len(self.alive_hosts)}):")
        for host in self.alive_hosts:
            print(f"  • {host}")
        
        print(f"\n🚪 ОТКРЫТЫЕ ПОРТЫ:")
        for host, ports in self.open_ports.items():
            print(f"  🎯 {host}:")
            for port in ports:
                service = self.service_detection(host, port)
                print(f"    • {port}/tcp - {service[:30]}...")
        
        print(f"\n⚠️  ОБНАРУЖЕННЫЕ УЯЗВИМОСТИ:")
        if self.vulnerabilities:
            for host, vulns in self.vulnerabilities.items():
                print(f"  🎯 {host}:")
                for vuln in vulns:
                    print(f"    ❗ {vuln}")
        else:
            print("  ✅ Критических уязвимостей не обнаружено")
        
        print(f"\n🛡️  РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ:")
        print("  • Закройте неиспользуемые порты")
        print("  • Обновите программное обеспечение до последних версий")
        print("  • Используйте сильные пароли и двухфакторную аутентификацию")
        print("  • Настройте файрвол для ограничения доступа")
        print("  • Регулярно мониторьте сетевую активность")

def main():
    """
    Главная функция сетевого сканера
    """
    print("=" * 60)
    print("🔍 ОБРАЗОВАТЕЛЬНЫЙ СЕТЕВОЙ СКАНЕР")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Сканирование чужих сетей без разрешения НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Образовательный сетевой сканер')
    parser.add_argument('network', help='Целевая сеть (например, 192.168.1.0/24)')
    parser.add_argument('--ping', action='store_true', help='Выполнить ping sweep')
    parser.add_argument('--arp', action='store_true', help='Выполнить ARP сканирование')
    parser.add_argument('--ports', action='store_true', help='Сканировать порты')
    parser.add_argument('--full-ports', action='store_true', help='Полное сканирование портов')
    parser.add_argument('--vulns', action='store_true', help='Поиск уязвимостей')
    parser.add_argument('--nmap', choices=['sS', 'sT', 'sU', 'sV', 'O', 'A'], 
                       help='Nmap сканирование')
    parser.add_argument('--all', action='store_true', help='Выполнить все виды сканирования')
    
    args = parser.parse_args()
    
    # Создаем сканер
    scanner = NetworkScanner(args.network)
    
    try:
        if args.all or args.ping:
            scanner.ping_sweep()
        
        if args.all or args.arp:
            scanner.arp_scan()
        
        if args.all or args.ports or args.full_ports:
            if not scanner.alive_hosts:
                scanner.ping_sweep()
            scanner.comprehensive_port_scan(common_ports_only=not args.full_ports)
        
        if args.all or args.vulns:
            if not scanner.open_ports:
                if not scanner.alive_hosts:
                    scanner.ping_sweep()
                scanner.comprehensive_port_scan()
            scanner.vulnerability_scan()
        
        if args.nmap:
            scanner.nmap_scan(args.nmap)
        
        # Генерируем отчет
        scanner.generate_report()
        
    except KeyboardInterrupt:
        print("\n🛑 Сканирование прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
