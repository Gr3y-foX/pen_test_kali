# 🎓 Образовательный набор инструментов для изучения кибербезопасности

## ⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ

**Эти инструменты предназначены ИСКЛЮЧИТЕЛЬНО для образовательных целей!**

- ✅ Разрешено: Использование в собственной лабораторной среде
- ✅ Разрешено: Тестирование на виртуальных машинах и контейнерах
- ✅ Разрешено: Изучение методов защиты информации
- ❌ ЗАПРЕЩЕНО: Использование против чужих систем без письменного разрешения
- ❌ ЗАПРЕЩЕНО: Любая незаконная деятельность

**Использование этих инструментов против чужих систем является преступлением!**

## 📚 Описание инструментов

### 1. DDoS Educational Tool (`ddos_educational.py`)

Образовательный инструмент для демонстрации различных типов DDoS атак и изучения методов защиты.

#### Поддерживаемые типы атак:

**TCP SYN Flood**
- Отправляет множество TCP SYN пакетов без завершения handshake
- Исчерпывает таблицу соединений на целевом сервере
- Использует спуфинг IP-адресов для усложнения блокировки

**UDP Flood**
- Отправляет случайные UDP пакеты на различные порты
- Перегружает сетевой канал и обработку пакетов
- Эффективен против серверов с UDP сервисами

**HTTP Flood**
- Отправляет множество HTTP запросов для перегрузки веб-сервера
- Использует различные User-Agent для обхода простых фильтров
- Многопоточная реализация для увеличения нагрузки

**Slowloris**
- Медленно отправляет HTTP заголовки, держа соединения открытыми
- Исчерпывает пул доступных соединений сервера
- Эффективен против серверов с ограниченным количеством соединений

#### Использование:

```bash
# TCP SYN Flood на 60 секунд
python3 ddos_educational.py 192.168.1.100 -t tcp -d 60

# HTTP Flood с 100 потоками
python3 ddos_educational.py 192.168.1.100 -t http --threads 100 -d 120

# Slowloris атака
python3 ddos_educational.py 192.168.1.100 -t slowloris -d 300
```

#### Меры защиты от DDoS:

- **Rate Limiting**: Ограничение количества запросов с одного IP
- **DDoS Protection Services**: Использование CloudFlare, AWS Shield
- **Firewall Rules**: Блокировка подозрительного трафика
- **Load Balancing**: Распределение нагрузки между серверами
- **Traffic Analysis**: Мониторинг аномального трафика

### 2. Network Scanner (`network_scanner.py`)

Комплексный сетевой сканер для обнаружения устройств, портов и уязвимостей в сети.

#### Функциональность:

**Ping Sweep**
- Обнаружение живых хостов в сети с помощью ICMP ping
- Параллельное сканирование для ускорения процесса
- Поддержка различных размеров сетей

**ARP Scanning**
- Обнаружение устройств в локальной сети через ARP запросы
- Получение MAC-адресов устройств
- Более надежен в локальных сетях, чем ping

**Port Scanning**
- TCP сканирование открытых портов
- Поддержка как быстрого (топ порты), так и полного сканирования
- Определение сервисов по баннерам

**Vulnerability Detection**
- Базовое определение известных уязвимостей
- Анализ версий сервисов
- Проверка небезопасных конфигураций

**Nmap Integration**
- Использование nmap для продвинутого сканирования
- OS Detection, Service Version Detection
- Различные типы сканирования (SYN, UDP, etc.)

#### Использование:

```bash
# Полное сканирование сети
python3 network_scanner.py 192.168.1.0/24 --all

# Только ping sweep
python3 network_scanner.py 192.168.1.0/24 --ping

# Сканирование портов с поиском уязвимостей
python3 network_scanner.py 192.168.1.0/24 --ports --vulns

# Nmap SYN scan
python3 network_scanner.py 192.168.1.0/24 --nmap sS
```

#### Меры защиты от сканирования:

- **Firewall Configuration**: Блокировка неиспользуемых портов
- **Port Knocking**: Скрытие сервисов за последовательностью портов
- **Intrusion Detection**: Мониторинг попыток сканирования
- **Network Segmentation**: Разделение сети на изолированные сегменты
- **Banner Hiding**: Сокрытие информации о версиях сервисов

### 3. Exploitation Tools (`exploitation_tools.py`)

Набор инструментов для демонстрации эксплуатации найденных уязвимостей.

#### Инструменты атак:

**SSH Brute Force**
- Перебор паролей для SSH доступа
- Использование словарей логинов и паролей
- Многопоточная реализация с контролем скорости

**FTP Brute Force**
- Атака на FTP сервисы
- Проверка анонимного доступа
- Получение списка файлов при успешном входе

**Web Directory Brute Force**
- Поиск скрытых директорий и файлов на веб-сервере
- Использование словарей путей и расширений
- Анализ HTTP кодов ответов

**SQL Injection Testing**
- Автоматическое тестирование параметров на SQL injection
- Различные типы payload'ов
- Определение уязвимостей по ошибкам, времени ответа и изменению содержимого

**XSS Testing**
- Тестирование на Cross-Site Scripting уязвимости
- Reflected и Stored XSS detection
- Различные векторы атак

**Reverse Shell Generator**
- Генерация команд reverse shell для различных платформ
- Поддержка bash, netcat, Python, PHP, PowerShell и других

#### Использование:

```bash
# Brute force SSH
python3 exploitation_tools.py 192.168.1.100 --ssh-brute --port 22

# Поиск скрытых веб-директорий
python3 exploitation_tools.py 192.168.1.100 --web-dirs --port 80

# Тестирование SQL injection
python3 exploitation_tools.py 192.168.1.100 --sql-test "http://192.168.1.100/login.php"

# Генерация reverse shell
python3 exploitation_tools.py 192.168.1.100 --reverse-shell 192.168.1.50 4444
```

#### Меры защиты:

**От Brute Force атак:**
- Сильные пароли и двухфакторная аутентификация
- Account lockout policies
- Rate limiting и fail2ban
- Мониторинг неудачных попыток входа

**От Web атак:**
- Валидация и санитизация входных данных
- Использование prepared statements для SQL
- Content Security Policy (CSP) для XSS
- Web Application Firewall (WAF)

**От Reverse Shell:**
- Мониторинг исходящих соединений
- Application whitelisting
- Sandboxing и контейнеризация
- Network segmentation

## 🛠️ Требования к системе

### Операционная система:
- Linux (рекомендуется Kali Linux)
- macOS
- Windows (с ограниченной функциональностью)

### Python зависимости:

```bash
pip3 install -r requirements.txt
```

### Системные зависимости:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nmap netcat-traditional

# Kali Linux (уже установлено)
# CentOS/RHEL
sudo yum install nmap nc
```

## 🔧 Настройка лабораторной среды

### Виртуальные машины для тестирования:

1. **Metasploitable 2/3** - Намеренно уязвимые Linux системы
2. **DVWA** - Damn Vulnerable Web Application
3. **VulnHub VMs** - Коллекция уязвимых виртуальных машин
4. **HackTheBox** - Онлайн платформа для практики

### Docker контейнеры:

```bash
# Уязвимое веб-приложение
docker run -d -p 80:80 vulnerables/web-dvwa

# Уязвимый SSH сервер
docker run -d -p 2222:22 --name vulnerable-ssh ubuntu:18.04

# FTP сервер для тестирования
docker run -d -p 21:21 stilliard/pure-ftpd
```

### Сетевая изоляция:

- Используйте изолированные виртуальные сети
- Настройте NAT для предотвращения доступа в интернет
- Используйте VirtualBox/VMware host-only сети

## 📖 Образовательные ресурсы

### Рекомендуемая литература:

1. **"The Web Application Hacker's Handbook"** - Dafydd Stuttard
2. **"Metasploit: The Penetration Tester's Guide"** - David Kennedy
3. **"Black Hat Python"** - Justin Seitz
4. **"The Hacker Playbook 3"** - Peter Kim

### Онлайн курсы:

- **OSCP** - Offensive Security Certified Professional
- **CEH** - Certified Ethical Hacker
- **CISSP** - Certified Information Systems Security Professional
- **Security+** - CompTIA Security+

### Практические платформы:

- **TryHackMe** - Интерактивные уроки кибербезопасности
- **HackTheBox** - Реальные сценарии тестирования на проникновение
- **OverTheWire** - Wargames для изучения безопасности
- **PentesterLab** - Практические упражнения по веб-безопасности

## 🚨 Этические принципы

### Responsible Disclosure:

При обнаружении реальных уязвимостей:

1. **Не эксплуатируйте** уязвимость для личной выгоды
2. **Уведомите** владельца системы о проблеме
3. **Предоставьте время** для исправления уязвимости
4. **Документируйте** процесс обнаружения
5. **Публикуйте информацию** только после исправления

### Правовые аспекты:

- **Получите письменное разрешение** перед любым тестированием
- **Соблюдайте границы** тестирования
- **Документируйте все действия** для отчетности
- **Защищайте конфиденциальную информацию**

## 🔍 Методология тестирования на проникновение

### 1. Разведка (Reconnaissance)

**Пассивная разведка:**
- OSINT (Open Source Intelligence)
- DNS enumeration
- Whois lookup
- Social media analysis

**Активная разведка:**
- Network scanning
- Port enumeration
- Service detection
- Banner grabbing

### 2. Сканирование (Scanning)

**Сетевое сканирование:**
- Ping sweep для обнаружения живых хостов
- Port scanning для открытых сервисов
- OS fingerprinting
- Service version detection

**Веб-сканирование:**
- Directory/file enumeration
- Technology stack identification
- SSL/TLS configuration analysis
- Cookie and session analysis

### 3. Перечисление (Enumeration)

**Детальный анализ сервисов:**
- SMB enumeration
- SNMP enumeration
- LDAP enumeration
- Database enumeration

### 4. Эксплуатация (Exploitation)

**Использование уязвимостей:**
- Buffer overflow attacks
- SQL injection
- Cross-site scripting (XSS)
- Authentication bypass

### 5. Пост-эксплуатация (Post-Exploitation)

**После получения доступа:**
- Privilege escalation
- Persistence mechanisms
- Data exfiltration
- Lateral movement

### 6. Отчетность (Reporting)

**Документирование результатов:**
- Executive summary
- Technical findings
- Risk assessment
- Remediation recommendations

## 🛡️ Комплексные меры защиты

### Сетевая безопасность:

1. **Firewall Configuration**
   - Deny by default policy
   - Least privilege access
   - Regular rule reviews

2. **Intrusion Detection/Prevention**
   - Network-based IDS/IPS
   - Host-based IDS/IPS
   - SIEM integration

3. **Network Segmentation**
   - VLANs for different departments
   - DMZ for public services
   - Zero-trust architecture

### Системная безопасность:

1. **Patch Management**
   - Regular security updates
   - Vulnerability scanning
   - Change management process

2. **Access Control**
   - Multi-factor authentication
   - Role-based access control
   - Privileged access management

3. **Monitoring and Logging**
   - Centralized log collection
   - Real-time alerting
   - Forensic capabilities

### Безопасность приложений:

1. **Secure Development**
   - Security by design
   - Code review process
   - Static/dynamic analysis

2. **Runtime Protection**
   - Web Application Firewall
   - Runtime application self-protection
   - Container security

## 📊 Метрики безопасности

### KPIs (Key Performance Indicators):

- **Mean Time to Detection (MTTD)**
- **Mean Time to Response (MTTR)**
- **Number of vulnerabilities detected/fixed**
- **Security awareness training completion rates**
- **Incident response effectiveness**

### Регулярные оценки:

- **Quarterly vulnerability assessments**
- **Annual penetration testing**
- **Security awareness assessments**
- **Business continuity testing**

## 🤝 Вклад в проект

Если вы хотите внести вклад в этот образовательный проект:

1. **Fork** репозиторий
2. **Создайте** feature branch
3. **Добавьте** новые образовательные инструменты
4. **Документируйте** изменения
5. **Создайте** pull request

### Требования к коду:

- Подробные комментарии на русском языке
- Проверки безопасности для предотвращения злоупотреблений
- Образовательная ценность
- Соответствие этическим принципам

## 📞 Поддержка

Для вопросов по образовательному использованию этих инструментов:

- Создайте issue в репозитории
- Опишите образовательный контекст
- Приложите скриншоты ошибок (если есть)

## 📄 Лицензия

Этот проект лицензирован для образовательных целей. Любое коммерческое использование или использование в незаконных целях строго запрещено.

---

**Помните: Знание - это сила, но с силой приходит ответственность. Используйте эти знания для защиты, а не для причинения вреда!**
