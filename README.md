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
