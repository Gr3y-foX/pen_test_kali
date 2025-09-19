#!/usr/bin/env python3
"""
Educational network scanner for learning reconnaissance methods
WARNING: For use only in your own laboratory environment!

Author: Educational material for cybersecurity learning
License: Educational purposes only
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
    Educational network scanner for demonstrating reconnaissance methods
    """
    
    def __init__(self, target_network):
        self.target_network = target_network
        self.open_ports = {}
        self.alive_hosts = []
        self.vulnerabilities = {}
        
        # Security check
        if not self._is_safe_network(target_network):
            print("❌ ERROR: Scanning is only allowed for local networks!")
            print("Allowed networks: 127.0.0.0/8, 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12")
            sys.exit(1)
    
    def _is_safe_network(self, network):
        """
        Checks if network is safe for scanning
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            
            # Allowed private networks
            safe_networks = [
                ipaddress.IPv4Network('127.0.0.0/8'),    # localhost
                ipaddress.IPv4Network('192.168.0.0/16'), # class C private network
                ipaddress.IPv4Network('10.0.0.0/8'),     # class A private network
                ipaddress.IPv4Network('172.16.0.0/12'),  # class B private network
            ]
            
            # Check if network is within safe ranges
            for safe_net in safe_networks:
                if net.subnet_of(safe_net):
                    return True
            
            return False
            
        except ValueError:
            return False
    
    def ping_sweep(self, network):
        """
        Ping sweep to find alive hosts
        """
        print(f"🔍 Performing ping sweep for network {network}")
        
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            hosts = []
            
            # Generate list of hosts to scan
            for host in net.hosts():
                hosts.append(str(host))
            
            print(f"📊 Scanning {len(hosts)} hosts...")
            
            # Use ThreadPoolExecutor for concurrent ping
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(self._ping_host, host): host for host in hosts}
                
                for future in as_completed(futures):
                    host = futures[future]
                    try:
                        result = future.result()
                        if result:
                            self.alive_hosts.append(host)
                            print(f"✅ {host} - alive")
                    except Exception as e:
                        print(f"❌ Error pinging {host}: {e}")
            
            print(f"📊 Found {len(self.alive_hosts)} alive hosts")
            return self.alive_hosts
            
        except Exception as e:
            print(f"❌ Error in ping sweep: {e}")
            return []
    
    def _ping_host(self, host):
        """
        Ping single host
        """
        try:
            # Use system ping command
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1000', host],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def port_scan(self, host, ports=None):
        """
        Port scan for specific host
        """
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080]
        
        print(f"🔍 Scanning {len(ports)} ports on {host}")
        
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"✅ Port {port} is open on {host}")
                    return port
                return None
            except:
                return None
        
        # Use ThreadPoolExecutor for concurrent port scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(scan_port, port): port for port in ports}
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    pass
        
        self.open_ports[host] = open_ports
        return open_ports
    
    def service_detection(self, host, ports):
        """
        Service detection for open ports
        """
        print(f"🔍 Detecting services on {host}")
        
        services = {}
        
        for port in ports:
            try:
                # Try to connect and get banner
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((host, port))
                
                # Try to get banner
                try:
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        services[port] = banner
                        print(f"📋 Port {port}: {banner}")
                except:
                    pass
                
                sock.close()
                
            except:
                pass
        
        return services
    
    def nmap_scan(self, target):
        """
        Advanced scan using Nmap
        """
        print(f"🔍 Running Nmap scan on {target}")
        
        try:
            nm = nmap.PortScanner()
            
            # Basic scan
            nm.scan(target, arguments='-sS -O -sV')
            
            for host in nm.all_hosts():
                print(f"📊 Host: {host}")
                print(f"   State: {nm[host].state()}")
                
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    print(f"   Protocol: {proto}")
                    
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        version = nm[host][proto][port]['version']
                        
                        print(f"   Port {port}: {state} - {service} {version}")
                        
                        if state == 'open':
                            if host not in self.open_ports:
                                self.open_ports[host] = []
                            self.open_ports[host].append(port)
            
            return True
            
        except Exception as e:
            print(f"❌ Nmap scan error: {e}")
            return False
    
    def vulnerability_scan(self, host, ports):
        """
        Basic vulnerability scanning
        """
        print(f"🔍 Scanning for vulnerabilities on {host}")
        
        vulnerabilities = []
        
        # Check for common vulnerabilities
        if 22 in ports:
            vulnerabilities.append("SSH service detected - check for weak passwords")
        
        if 21 in ports:
            vulnerabilities.append("FTP service detected - check for anonymous access")
        
        if 23 in ports:
            vulnerabilities.append("Telnet service detected - unencrypted communication")
        
        if 80 in ports or 8080 in ports:
            vulnerabilities.append("HTTP service detected - check for web vulnerabilities")
        
        if 443 in ports:
            vulnerabilities.append("HTTPS service detected - check SSL/TLS configuration")
        
        if 3389 in ports:
            vulnerabilities.append("RDP service detected - check for weak authentication")
        
        if 1433 in ports:
            vulnerabilities.append("MSSQL service detected - check for weak passwords")
        
        if 3306 in ports:
            vulnerabilities.append("MySQL service detected - check for weak passwords")
        
        if 5432 in ports:
            vulnerabilities.append("PostgreSQL service detected - check for weak passwords")
        
        self.vulnerabilities[host] = vulnerabilities
        
        for vuln in vulnerabilities:
            print(f"⚠️  {vuln}")
        
        return vulnerabilities
    
    def generate_report(self):
        """
        Generate scan report
        """
        print("=" * 60)
        print("📊 NETWORK SCAN REPORT")
        print("=" * 60)
        
        print(f"🎯 Target network: {self.target_network}")
        print(f"📅 Scan time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print(f"🖥️  ALIVE HOSTS ({len(self.alive_hosts)}):")
        for host in self.alive_hosts:
            print(f"  • {host}")
        print()
        
        print(f"🚪 OPEN PORTS:")
        for host, ports in self.open_ports.items():
            print(f"  🎯 {host}:")
            for port in ports:
                print(f"    • {port}/tcp")
        print()
        
        print(f"⚠️  DETECTED VULNERABILITIES:")
        for host, vulns in self.vulnerabilities.items():
            print(f"  🎯 {host}:")
            for vuln in vulns:
                print(f"    • {vuln}")
        print()
        
        print(f"🛡️  SECURITY RECOMMENDATIONS:")
        print(f"  • Close unused ports")
        print(f"  • Update software to latest versions")
        print(f"  • Use strong passwords and two-factor authentication")
        print(f"  • Configure firewall to limit access")
        print(f"  • Regularly monitor network activity")

def main():
    """
    Main function of educational network scanner
    """
    print("=" * 60)
    print("🔍 EDUCATIONAL NETWORK SCANNER")
    print("=" * 60)
    print("⚠️  WARNING: For use only in your own laboratory!")
    print("⚠️  Scanning other networks without permission is ILLEGAL!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Educational network scanner')
    parser.add_argument('target', help='Target network or IP address')
    parser.add_argument('--ping-sweep', action='store_true', help='Perform ping sweep')
    parser.add_argument('--ports', action='store_true', help='Scan common ports')
    parser.add_argument('--services', action='store_true', help='Detect services')
    parser.add_argument('--nmap', action='store_true', help='Use Nmap for advanced scanning')
    parser.add_argument('--vuln-scan', action='store_true', help='Scan for vulnerabilities')
    parser.add_argument('--all', action='store_true', help='Perform all scans')
    
    args = parser.parse_args()
    
    # Create scanner instance
    scanner = NetworkScanner(args.target)
    
    try:
        # Determine scan type
        if args.all:
            # Ping sweep
            scanner.ping_sweep(args.target)
            
            # Port scan for alive hosts
            for host in scanner.alive_hosts:
                ports = scanner.port_scan(host)
                if ports:
                    scanner.service_detection(host, ports)
                    scanner.vulnerability_scan(host, ports)
            
            # Nmap scan
            scanner.nmap_scan(args.target)
            
        else:
            # Individual scans
            if args.ping_sweep:
                scanner.ping_sweep(args.target)
            
            if args.ports:
                if scanner.alive_hosts:
                    for host in scanner.alive_hosts:
                        scanner.port_scan(host)
                else:
                    # If no ping sweep, scan target directly
                    scanner.port_scan(args.target)
            
            if args.services:
                for host, ports in scanner.open_ports.items():
                    scanner.service_detection(host, ports)
            
            if args.nmap:
                scanner.nmap_scan(args.target)
            
            if args.vuln_scan:
                for host, ports in scanner.open_ports.items():
                    scanner.vulnerability_scan(host, ports)
        
        # Generate report
        scanner.generate_report()
        
    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📚 Educational information:")
    print("• Network scanning is the first phase of penetration testing")
    print("• Ping sweep finds alive hosts in the network")
    print("• Port scanning identifies open services")
    print("• Service detection helps identify running software")
    print("• Vulnerability scanning finds potential security issues")
    print("• Always get permission before scanning networks")

if __name__ == "__main__":
    main()
