# 🎯 KALI LINUX PENETRATION PROJECT

## 📋 Обзор проекта

Этот проект представляет собой комплексный набор инструментов для изучения кибербезопасности и тестирования на проникновение в Kali Linux. Проект создан для образовательных целей и включает в себя все этапы современной кибератаки.

## ⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ

**Эти инструменты предназначены ИСКЛЮЧИТЕЛЬНО для образовательных целей!**

- ✅ **Разрешено**: Использование в собственной лабораторной среде
- ✅ **Разрешено**: Тестирование на виртуальных машинах и контейнерах
- ✅ **Разрешено**: Изучение методов защиты информации
- ❌ **ЗАПРЕЩЕНО**: Использование против чужих систем без письменного разрешения
- ❌ **ЗАПРЕЩЕНО**: Любая незаконная деятельность

**Использование этих инструментов против чужих систем является преступлением!**

## 🛠️ Основные компоненты проекта

### 1. 🎯 Kali Penetration Master (`kali_penetration_master.py`)
**Главный скрипт для полного внедрения в Kali Linux**

- **Фаза 1**: Продвинутая разведка и сканирование
- **Фаза 2**: Оценка уязвимостей
- **Фаза 3**: Эксплуатация уязвимостей
- **Фаза 4**: Повышение привилегий
- **Фаза 5**: Установка постоянного доступа
- **Фаза 6**: Очистка следов и отчетность

```bash
# Полный цикл атаки
python3 kali_penetration_master.py 10.211.55.14

# Только разведка
python3 kali_penetration_master.py 10.211.55.14 --recon-only

# Только сканирование уязвимостей
python3 kali_penetration_master.py 10.211.55.14 --vuln-scan
```

### 2. 🔧 GitHub Tools Integration (`github_tools_integration.py`)
**Интеграция готовых GitHub проектов для упрощения работы**

- Автоматическая установка популярных инструментов пентеста
- Категоризированная установка по типам атак
- Проверка доступности инструментов
- Скачивание словарей для brute force
- Генерация отчетов об инструментах

```bash
# Установить все инструменты
python3 github_tools_integration.py --install-all

# Установить только веб-инструменты
python3 github_tools_integration.py --install-category web

# Проверить доступность инструментов
python3 github_tools_integration.py --check-all
```

### 3. 🔧 Advanced Kali Vulnerable Setup (`kali_vulnerable_setup_advanced.py`)
**Продвинутая настройка уязвимой Kali Linux**

- Создание множественных уязвимых пользователей
- Ослабление SSH безопасности
- Отключение инструментов безопасности
- Настройка уязвимых веб-сервисов
- Создание различных backdoor
- Установка слабых прав доступа

```bash
# Полная настройка уязвимой системы
python3 kali_vulnerable_setup_advanced.py 10.211.55.14

# Только настройка пользователей
python3 kali_vulnerable_setup_advanced.py 10.211.55.14 --users-only

# Только веб-сервисы
python3 kali_vulnerable_setup_advanced.py 10.211.55.14 --web-only
```

### 4. 🎯 Kali Penetration Workflow (`kali_penetration_workflow.py`)
**Единый workflow для полного внедрения в Kali Linux**

- Последовательное выполнение всех фаз атаки
- Детальное логирование каждого этапа
- Автоматическая генерация отчетов
- Возможность запуска отдельных фаз
- Интеграция с существующими инструментами

```bash
# Полный workflow
python3 kali_penetration_workflow.py 10.211.55.14

# Только разведка
python3 kali_penetration_workflow.py 10.211.55.14 --recon-only

# Конкретная фаза
python3 kali_penetration_workflow.py 10.211.55.14 --phase 2
```

### 5. 🌐 Demo Vulnerable Server (`demo_vulnerable_server.py`)
**Демонстрационный уязвимый веб-сервер**

- SQL Injection уязвимости
- XSS (Cross-Site Scripting)
- Directory Traversal
- Command Injection
- Небезопасная загрузка файлов
- Интерактивный интерфейс для обучения

```bash
# Запуск демо-сервера
python3 demo_vulnerable_server.py --port 8080

# Доступ: http://localhost:8080
```

## 🔄 Полный сценарий использования

### Этап 1: Подготовка окружения
```bash
# Активация виртуального окружения
source venv/bin/activate

# Установка всех инструментов
python3 github_tools_integration.py --install-all

# Скачивание словарей
python3 github_tools_integration.py --download-wordlists
```

### Этап 2: Настройка уязвимой цели
```bash
# Настройка уязвимой Kali Linux
python3 kali_vulnerable_setup_advanced.py 10.211.55.14 --all

# Или запуск демо-сервера для локального тестирования
python3 demo_vulnerable_server.py --port 8080
```

### Этап 3: Проведение атаки
```bash
# Полный цикл атаки
python3 kali_penetration_master.py 10.211.55.14

# Или пошаговый workflow
python3 kali_penetration_workflow.py 10.211.55.14
```

### Этап 4: Анализ результатов
- Проверка сгенерированных отчетов
- Анализ найденных уязвимостей
- Изучение методов защиты

## 📊 Типы атак и уязвимостей

### Сетевые атаки
- **DDoS атаки**: TCP SYN Flood, UDP Flood, HTTP Flood, Slowloris
- **Сетевое сканирование**: Ping sweep, ARP scan, Port scanning
- **ARP Spoofing**: Man-in-the-Middle атаки

### Веб-атаки
- **SQL Injection**: Автоматическое тестирование, различные payload
- **XSS**: Reflected, Stored, DOM-based XSS
- **Directory Traversal**: Чтение системных файлов
- **Command Injection**: Выполнение системных команд
- **File Upload**: Небезопасная загрузка файлов

### Атаки на аутентификацию
- **SSH Brute Force**: Перебор паролей с многопоточностью
- **Password Cracking**: John the Ripper, Hashcat
- **Credential Harvesting**: Сбор учетных данных

### Системные атаки
- **Privilege Escalation**: SUID/SGID файлы, sudo права
- **Persistence**: Backdoor, cron jobs, network listeners
- **Lateral Movement**: Перемещение по сети

## 🛡️ Методы защиты

### Сетевая безопасность
- Firewall конфигурация
- Intrusion Detection/Prevention Systems
- Network segmentation
- VPN и шифрование

### Веб-безопасность
- Input validation и sanitization
- Prepared statements для SQL
- Content Security Policy (CSP)
- Web Application Firewall (WAF)

### Системная безопасность
- Сильные пароли и 2FA
- Regular security updates
- Least privilege access
- Monitoring и logging

## 📚 Образовательная ценность

### Изучаемые концепции
- Методология пентеста (OSSTMM, OWASP)
- Жизненный цикл кибератаки
- Типы уязвимостей и их эксплуатация
- Методы защиты и противодействия
- Правовые и этические аспекты

### Практические навыки
- Работа с инструментами пентеста
- Анализ сетевого трафика
- Эксплуатация веб-уязвимостей
- Создание и анализ отчетов
- Планирование и выполнение атак

## 🔧 Требования к системе

### Операционная система
- Linux (рекомендуется Kali Linux)
- macOS
- Windows (с ограниченной функциональностью)

### Python зависимости
```bash
pip3 install -r requirements.txt
```

### Системные инструменты
- nmap
- hydra
- john
- sqlmap
- nikto
- gobuster

## 📖 Дополнительные ресурсы

### Рекомендуемая литература
1. **"The Web Application Hacker's Handbook"** - Dafydd Stuttard
2. **"Metasploit: The Penetration Tester's Guide"** - David Kennedy
3. **"Black Hat Python"** - Justin Seitz
4. **"The Hacker Playbook 3"** - Peter Kim

### Онлайн курсы
- **OSCP** - Offensive Security Certified Professional
- **CEH** - Certified Ethical Hacker
- **CISSP** - Certified Information Systems Security Professional

### Практические платформы
- **TryHackMe** - Интерактивные уроки
- **HackTheBox** - Реальные сценарии
- **OverTheWire** - Wargames
- **PentesterLab** - Практические упражнения

## 🚨 Этические принципы

### Responsible Disclosure
1. Не эксплуатируйте уязвимости для личной выгоды
2. Уведомите владельца системы о проблеме
3. Предоставьте время для исправления
4. Документируйте процесс обнаружения
5. Публикуйте информацию только после исправления

### Правовые аспекты
- Получите письменное разрешение перед тестированием
- Соблюдайте границы тестирования
- Документируйте все действия
- Защищайте конфиденциальную информацию

## 🤝 Вклад в проект

Если вы хотите внести вклад в этот образовательный проект:

1. **Fork** репозиторий
2. **Создайте** feature branch
3. **Добавьте** новые образовательные инструменты
4. **Документируйте** изменения
5. **Создайте** pull request

### Требования к коду
- Подробные комментарии на русском языке
- Проверки безопасности для предотвращения злоупотреблений
- Образовательная ценность
- Соответствие этическим принципам

## 📞 Поддержка

Для вопросов по образовательному использованию:

- Создайте issue в репозитории
- Опишите образовательный контекст
- Приложите скриншоты ошибок (если есть)

## 📄 Лицензия

Этот проект лицензирован для образовательных целей. Любое коммерческое использование или использование в незаконных целях строго запрещено.

---

## 🎯 Быстрый старт

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd pen_test
chmod +x setup_lab.sh
./setup_lab.sh
source venv/bin/activate
```

### 2. Установка инструментов
```bash
python3 github_tools_integration.py --install-all
python3 github_tools_integration.py --download-wordlists
```

### 3. Запуск демо-сервера
```bash
python3 demo_vulnerable_server.py --port 8080
```

### 4. Тестирование атак
```bash
python3 web_attacks_suite.py http://localhost:8080
```

### 5. Полный цикл атаки
```bash
python3 kali_penetration_workflow.py 10.211.55.14
```

---

**Помните: Знание - это сила, но с силой приходит ответственность. Используйте эти знания для защиты, а не для причинения вреда!**

🎓 **Удачного изучения кибербезопасности!**
