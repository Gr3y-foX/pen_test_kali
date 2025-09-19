# 🎯 Kali Linux Penetration Toolkit

## 📋  Project Overview

A comprehensive toolkit for cybersecurity learning and penetration testing in Kali Linux. The project includes all stages of modern cyberattacks from reconnaissance to backdoor installation.

## ⚠️ IMPORTANT WARNING

**These tools are intended EXCLUSIVELY for educational purposes!!**

- ✅ **Allowed**: ИUse in your own laboratory environment
- ✅ **Allowed**: Testing on virtual machines and containers
- ✅ **Allowed**: Studying information security defense methods
- ❌ **PROHIBITED**: Use against third-party systems without 


## 📁 Project Structureа

```
pen_test/
├── core/                    # Core scripts
│   ├── kali_penetration_master.py      # Main script for full penetration
│   ├── kali_penetration_workflow.py    # Unified attack workflow
│   └── github_tools_integration.py     # GitHub tools integration
├── tools/                   # Attack tools
│   ├── web_attacks_suite.py            # Web attacks (SQL, XSS, etc.)
│   ├── network_scanner.py              # Network scanning
│   ├── ddos_educational.py             # DDoS attacks
│   ├── advanced_ssh_attack.py          # SSH brute force
│   ├── arp_spoofing.py                 # ARP spoofing
│   └── john_attacks.py                 # Password cracking
├── demos/                   # Demonstration scripts
│   ├── demo_vulnerable_server.py       # Vulnerable web server
│   └── kali_vulnerable_setup_advanced.py # Vulnerable Kali setup
├── wordlists/               # Dictionaries for brute force
│   ├── passwords.txt
│   ├── passwords_extended.txt
│   ├── hashes.txt
│   └── hashes_only.txt
├── docs/                    # Documentation
│   ├── README.md
│   ├── QUICK_START.md
│   ├── KALI_PENETRATION_PROJECT.md
│   └── PROJECT_SUMMARY.md
├── reports/                 # Reports (created automatically)
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
└── setup_lab.sh            # Laboratory setup script

```

## 🚀 Quick Start

### 1. Installing Dependencies
```bash
chmod +x setup_lab.sh
./setup_lab.sh
source venv/bin/activate
```

### 2. Installing Tools
```bash
python3 core/github_tools_integration.py --install-all
```

### 3. Running Demo Server
```bash
python3 demos/demo_vulnerable_server.py --port 8080
```

### 4. Testing Web Attacks
```bash
python3 tools/web_attacks_suite.py http://localhost:8080
```

### 5. Full Attack Cycle
```bash
python3 core/kali_penetration_workflow.py (your ip)
```

## 🎯  Main Components

### Core (Main Scripts)
- **`kali_penetration_master.py` - Main script for full penetration
- **`kali_penetration_workflow.py` - Unified attack workflow
- **`github_tools_integration.py` - GitHub tools integration

### Tools (Инструменты атак)
- **`web_attacks_suite.py`** - SQL Injection, XSS, Directory Traversal, Command Injection
- **`network_scanner.py`** - Сетевое сканирование, порты, сервисы
- **`ddos_educational.py`** - TCP SYN Flood, UDP Flood, HTTP Flood, Slowloris
- **`advanced_ssh_attack.py`** - Multi-threaded SSH brute force
- **`arp_spoofing.py`** - ARP spoofing attacl
- **`john_attacks.py`** - Password cracking with John the Ripper

### Demos (Демонстрационные скрипты)
- **`demo_vulnerable_server.py`** - Vulnerable web server for learning
- **`kali_vulnerable_setup_advanced.py`** - Vulnerable Kali Linux setup 

## 📚 Attack Types

### 🌐 Веб-атаки
- SQL Injection
- XSS (Cross-Site Scripting)
- Directory Traversal
- Command Injection
- File Upload

### 🔐 Authentication Attacks
- SSH Brute Force
- Password Cracking
- Credential Harvesting

### 🌐 Network Attacks
- DDoS атаки
- Сетевое сканирование
- ARP Spoofing

### 💻 System Attacks
- Privilege Escalation
- Backdoor установка
- Persistence

## 🛡️ Defense Methods

### Web-security
- Input validation и sanitization
- Prepared statements для SQL
- Content Security Policy (CSP)
- Web Application Firewall (WAF)

### Network-security
- Firewall конфигурация
- Intrusion Detection Systems
- Network segmentation

### System Security
- Сильные пароли и 2FA
- Regular security updates
- Least privilege access
- Monitoring и logging

## 📖 Documentation

Detailed documentation is located in the `docs/` folder:
- **`QUICK_START.md`** -  Quick start guide
- **`KALI_PENETRATION_PROJECT.md`** - Complete project description
- **`PROJECT_SUMMARY.md`** - Project summary

## 🎓 Educational Value

### Covered Concepts
- Penetration testing methodology
- Cyberattack lifecycle
- Types of vulnerabilities and their exploitation
- Defense and countermeasure techniques

### Practical Skills
- Working with penetration testing tools
- Network traffic analysis
- Exploitation of web vulnerabilities
- Report creation and analysis

## 🚨 Ethical Principles

### Responsible Disclosure
1. Do not exploit vulnerabilities for personal gain
2.	Notify the system owner about the issue
3.	Allow time for remediation
4.	Document the discovery process

### Legal Aspects
- Obtain written permission before testing
- Respect the testing scope boundaries
- Document all actions
- Protect confidential information

## 🤝 Contributing

If you want to contribute:
1.	Fork the repository
2.	Create a feature branch
3.	Add new tools
4.	Document the changes
5.	Create a pull request

## 📄 License

This project is licensed for educational purposes. Any commercial use or use for illegal purposes is strictly prohibited.

---

**🎓 Happy cybersecurity learning!**

**⚠️ Remember: Use only in your own lab environment!**

# 🎯 Kali Linux Penetration Toolkit

## 📋 Обзор проекта

Комплексный набор инструментов для изучения кибербезопасности и тестирования на проникновение в Kali Linux. Проект включает все этапы современной кибератаки от разведки до установки backdoor.

## ⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ

**Эти инструменты предназначены ИСКЛЮЧИТЕЛЬНО для образовательных целей!**

- ✅ **Разрешено**: Использование в собственной лабораторной среде
- ✅ **Разрешено**: Тестирование на виртуальных машинах и контейнерах
- ✅ **Разрешено**: Изучение методов защиты информации
- ❌ **ЗАПРЕЩЕНО**: Использование против чужих систем без письменного разрешения
- ❌ **ЗАПРЕЩЕНО**: Любая незаконная деятельность

## 📁 Структура проекта

```
pen_test/
├── core/                    # Основные скрипты
│   ├── kali_penetration_master.py      # Главный скрипт для полного внедрения
│   ├── kali_penetration_workflow.py    # Единый workflow атак
│   └── github_tools_integration.py     # Интеграция GitHub инструментов
├── tools/                   # Инструменты атак
│   ├── web_attacks_suite.py            # Веб-атаки (SQL, XSS, etc.)
│   ├── network_scanner.py              # Сетевое сканирование
│   ├── ddos_educational.py             # DDoS атаки
│   ├── advanced_ssh_attack.py          # SSH brute force
│   ├── arp_spoofing.py                 # ARP spoofing
│   └── john_attacks.py                 # Взлом паролей
├── demos/                   # Демонстрационные скрипты
│   ├── demo_vulnerable_server.py       # Уязвимый веб-сервер
│   └── kali_vulnerable_setup_advanced.py # Настройка уязвимой Kali
├── wordlists/               # Словари для brute force
│   ├── passwords.txt
│   ├── passwords_extended.txt
│   ├── hashes.txt
│   └── hashes_only.txt
├── docs/                    # Документация
│   ├── README.md
│   ├── QUICK_START.md
│   ├── KALI_PENETRATION_PROJECT.md
│   └── PROJECT_SUMMARY.md
├── reports/                 # Отчеты (создаются автоматически)
├── venv/                    # Виртуальное окружение Python
├── requirements.txt         # Python зависимости
└── setup_lab.sh            # Скрипт настройки лаборатории
```

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
chmod +x setup_lab.sh
./setup_lab.sh
source venv/bin/activate
```

### 2. Установка инструментов
```bash
python3 core/github_tools_integration.py --install-all
```

### 3. Запуск демо-сервера
```bash
python3 demos/demo_vulnerable_server.py --port 8080
```

### 4. Тестирование веб-атак
```bash
python3 tools/web_attacks_suite.py http://localhost:8080
```

### 5. Полный цикл атаки
```bash
python3 core/kali_penetration_workflow.py 10.211.55.14
```

## 🎯 Основные компоненты

### Core (Основные скрипты)
- **`kali_penetration_master.py`** - Главный скрипт для полного внедрения
- **`kali_penetration_workflow.py`** - Единый workflow атак
- **`github_tools_integration.py`** - Интеграция GitHub инструментов

### Tools (Инструменты атак)
- **`web_attacks_suite.py`** - SQL Injection, XSS, Directory Traversal, Command Injection
- **`network_scanner.py`** - Сетевое сканирование, порты, сервисы
- **`ddos_educational.py`** - TCP SYN Flood, UDP Flood, HTTP Flood, Slowloris
- **`advanced_ssh_attack.py`** - SSH brute force с многопоточностью
- **`arp_spoofing.py`** - ARP spoofing атаки
- **`john_attacks.py`** - Взлом паролей с John the Ripper

### Demos (Демонстрационные скрипты)
- **`demo_vulnerable_server.py`** - Уязвимый веб-сервер для обучения
- **`kali_vulnerable_setup_advanced.py`** - Настройка уязвимой Kali Linux

## 📚 Типы атак

### 🌐 Веб-атаки
- SQL Injection
- XSS (Cross-Site Scripting)
- Directory Traversal
- Command Injection
- File Upload

### 🔐 Атаки на аутентификацию
- SSH Brute Force
- Password Cracking
- Credential Harvesting

### 🌐 Сетевые атаки
- DDoS атаки
- Сетевое сканирование
- ARP Spoofing

### 💻 Системные атаки
- Privilege Escalation
- Backdoor установка
- Persistence

## 🛡️ Методы защиты

### Веб-безопасность
- Input validation и sanitization
- Prepared statements для SQL
- Content Security Policy (CSP)
- Web Application Firewall (WAF)

### Сетевая безопасность
- Firewall конфигурация
- Intrusion Detection Systems
- Network segmentation

### Системная безопасность
- Сильные пароли и 2FA
- Regular security updates
- Least privilege access
- Monitoring и logging

## 📖 Документация

Подробная документация находится в папке `docs/`:
- **`QUICK_START.md`** - Быстрый старт
- **`KALI_PENETRATION_PROJECT.md`** - Полное описание проекта
- **`PROJECT_SUMMARY.md`** - Резюме проекта

## 🎓 Образовательная ценность

### Изучаемые концепции
- Методология пентеста
- Жизненный цикл кибератаки
- Типы уязвимостей и их эксплуатация
- Методы защиты и противодействия

### Практические навыки
- Работа с инструментами пентеста
- Анализ сетевого трафика
- Эксплуатация веб-уязвимостей
- Создание и анализ отчетов

## 🚨 Этические принципы

### Responsible Disclosure
1. Не эксплуатируйте уязвимости для личной выгоды
2. Уведомите владельца системы о проблеме
3. Предоставьте время для исправления
4. Документируйте процесс обнаружения

### Правовые аспекты
- Получите письменное разрешение перед тестированием
- Соблюдайте границы тестирования
- Документируйте все действия
- Защищайте конфиденциальную информацию

## 🤝 Вклад в проект

Если вы хотите внести вклад:
1. Fork репозиторий
2. Создайте feature branch
3. Добавьте новые инструменты
4. Документируйте изменения
5. Создайте pull request

## 📄 Лицензия

Этот проект лицензирован для образовательных целей. Любое коммерческое использование или использование в незаконных целях строго запрещено.

---

**🎓 Удачного изучения кибербезопасности!**

**⚠️ Помните: Используйте только в собственной лабораторной среде!**