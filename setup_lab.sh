#!/bin/bash

# Скрипт для настройки лабораторной среды кибербезопасности
# ВНИМАНИЕ: Только для образовательных целей!

echo "🎓 Настройка образовательной лаборатории кибербезопасности"
echo "=========================================================="

# Проверка операционной системы
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✅ Обнаружена Linux система"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "✅ Обнаружена macOS система"
else
    echo "❌ Неподдерживаемая операционная система"
    exit 1
fi

# Проверка прав root (для некоторых операций)
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  Выполняется с правами root"
   ROOT_ACCESS=true
else
   echo "ℹ️  Выполняется без прав root (некоторые функции могут быть недоступны)"
   ROOT_ACCESS=false
fi

# Функция для установки пакетов в Linux
install_linux_packages() {
    echo "📦 Установка системных пакетов для Linux..."
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            nmap \
            netcat-traditional \
            tcpdump \
            wireshark-common \
            git \
            curl \
            wget \
            build-essential \
            libpcap-dev \
            libssl-dev
            
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum update -y
        sudo yum install -y \
            python3 \
            python3-pip \
            nmap \
            nc \
            tcpdump \
            git \
            curl \
            wget \
            gcc \
            openssl-devel \
            libpcap-devel
            
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm \
            python \
            python-pip \
            nmap \
            netcat \
            tcpdump \
            wireshark-cli \
            git \
            curl \
            wget \
            base-devel \
            libpcap \
            openssl
    else
        echo "❌ Неподдерживаемый пакетный менеджер"
        return 1
    fi
}

# Функция для установки пакетов в macOS
install_macos_packages() {
    echo "📦 Установка системных пакетов для macOS..."
    
    # Проверка наличия Homebrew
    if ! command -v brew &> /dev/null; then
        echo "🍺 Установка Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Установка пакетов через Homebrew
    brew update
    brew install \
        python3 \
        nmap \
        netcat \
        tcpdump \
        wireshark \
        git \
        curl \
        wget
}

# Установка системных зависимостей
echo "🔧 Установка системных зависимостей..."
if [[ "$OS" == "linux" ]]; then
    install_linux_packages
elif [[ "$OS" == "macos" ]]; then
    install_macos_packages
fi

# Проверка Python
echo "🐍 Проверка Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $PYTHON_VERSION установлен"
else
    echo "❌ Python 3 не найден"
    exit 1
fi

# Создание виртуального окружения
echo "🏠 Создание виртуального окружения..."
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "ℹ️  Виртуальное окружение уже существует"
fi

# Активация виртуального окружения и установка зависимостей
echo "📚 Установка Python зависимостей..."
source venv/bin/activate

# Обновление pip
pip install --upgrade pip

# Установка зависимостей
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
    echo "✅ Python зависимости установлены"
else
    echo "❌ Файл requirements.txt не найден"
    exit 1
fi

# Проверка установки ключевых библиотек
echo "🔍 Проверка установленных библиотек..."
python3 -c "import scapy; print('✅ Scapy установлен')" 2>/dev/null || echo "❌ Ошибка установки Scapy"
python3 -c "import requests; print('✅ Requests установлен')" 2>/dev/null || echo "❌ Ошибка установки Requests"
python3 -c "import paramiko; print('✅ Paramiko установлен')" 2>/dev/null || echo "❌ Ошибка установки Paramiko"
python3 -c "import nmap; print('✅ Python-nmap установлен')" 2>/dev/null || echo "❌ Ошибка установки python-nmap"

# Создание Docker контейнеров для тестирования (если Docker доступен)
if command -v docker &> /dev/null; then
    echo "🐳 Настройка Docker контейнеров для тестирования..."
    
    # Создание docker-compose.yml для уязвимых сервисов
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  # Уязвимое веб-приложение DVWA
  dvwa:
    image: vulnerables/web-dvwa
    ports:
      - "8080:80"
    environment:
      - MYSQL_DATABASE=dvwa
      - MYSQL_USER=dvwa
      - MYSQL_PASSWORD=password
      - MYSQL_ROOT_PASSWORD=password
    networks:
      - lab-network

  # Уязвимый FTP сервер
  ftp-server:
    image: stilliard/pure-ftpd
    ports:
      - "2121:21"
      - "30000-30009:30000-30009"
    environment:
      - PUBLICHOST=localhost
      - FTP_USER_NAME=testuser
      - FTP_USER_PASS=testpass
      - FTP_USER_HOME=/home/testuser
    networks:
      - lab-network

  # Уязвимый SSH сервер
  ssh-server:
    image: ubuntu:20.04
    ports:
      - "2222:22"
    command: >
      bash -c "apt-get update &&
               apt-get install -y openssh-server &&
               echo 'root:password' | chpasswd &&
               echo 'testuser:testpass' | chpasswd &&
               useradd -m testuser &&
               service ssh start &&
               tail -f /dev/null"
    networks:
      - lab-network

  # Простой веб-сервер для тестирования
  web-server:
    image: nginx:alpine
    ports:
      - "8081:80"
    volumes:
      - ./web-content:/usr/share/nginx/html:ro
    networks:
      - lab-network

networks:
  lab-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
EOF

    # Создание простого веб-контента для тестирования
    mkdir -p web-content
    cat > web-content/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Тестовый веб-сервер</title>
</head>
<body>
    <h1>Добро пожаловать на тестовый сервер</h1>
    <p>Этот сервер предназначен для образовательного тестирования.</p>
    <ul>
        <li><a href="/admin/">Админ панель</a></li>
        <li><a href="/backup/">Резервные копии</a></li>
        <li><a href="/config/">Конфигурация</a></li>
    </ul>
</body>
</html>
EOF

    cat > web-content/login.php << EOF
<?php
// Уязвимая страница входа для тестирования SQL injection
if (\$_GET['username'] && \$_GET['password']) {
    \$username = \$_GET['username'];
    \$password = \$_GET['password'];
    
    // УЯЗВИМЫЙ КОД - НЕ ИСПОЛЬЗУЙТЕ В ПРОДАКШЕНЕ!
    \$query = "SELECT * FROM users WHERE username='\$username' AND password='\$password'";
    echo "SQL Query: " . \$query;
    
    if (strpos(\$username, "'") !== false) {
        echo "<br><font color='red'>SQL Error: syntax error near '\$username'</font>";
    }
}
?>
<html>
<body>
    <h2>Уязвимая форма входа</h2>
    <form method="GET">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
EOF

    echo "✅ Docker конфигурация создана"
    echo "ℹ️  Для запуска тестовых сервисов выполните: docker-compose up -d"
    
else
    echo "⚠️  Docker не установлен - пропускаем создание контейнеров"
fi

# Создание скрипта для быстрого запуска
cat > run_tools.sh << 'EOF'
#!/bin/bash

# Скрипт для быстрого запуска инструментов

echo "🎓 Образовательные инструменты кибербезопасности"
echo "=============================================="
echo "1. DDoS тестирование"
echo "2. Сканирование сети"
echo "3. Инструменты эксплуатации"
echo "4. Запуск тестовых сервисов"
echo "5. Выход"
echo

read -p "Выберите опцию (1-5): " choice

case $choice in
    1)
        echo "🚀 Запуск DDoS инструмента..."
        python3 ddos_educational.py --help
        ;;
    2)
        echo "🔍 Запуск сетевого сканера..."
        python3 network_scanner.py --help
        ;;
    3)
        echo "🔓 Запуск инструментов эксплуатации..."
        python3 exploitation_tools.py --help
        ;;
    4)
        if command -v docker-compose &> /dev/null; then
            echo "🐳 Запуск тестовых сервисов..."
            docker-compose up -d
            echo "✅ Сервисы запущены:"
            echo "  - DVWA: http://localhost:8080"
            echo "  - Веб-сервер: http://localhost:8081"
            echo "  - FTP: localhost:2121"
            echo "  - SSH: localhost:2222"
        else
            echo "❌ Docker не установлен"
        fi
        ;;
    5)
        echo "👋 До свидания!"
        exit 0
        ;;
    *)
        echo "❌ Неверный выбор"
        ;;
esac
EOF

chmod +x run_tools.sh

# Настройка прав доступа для скриптов
chmod +x ddos_educational.py
chmod +x network_scanner.py
chmod +x exploitation_tools.py

echo ""
echo "🎉 НАСТРОЙКА ЗАВЕРШЕНА!"
echo "======================"
echo ""
echo "📋 Что было установлено:"
echo "  ✅ Python виртуальное окружение"
echo "  ✅ Все необходимые Python библиотеки"
echo "  ✅ Системные утилиты (nmap, netcat, etc.)"
echo "  ✅ Docker конфигурация для тестовых сервисов"
echo "  ✅ Скрипт быстрого запуска"
echo ""
echo "🚀 Как начать работу:"
echo "  1. Активируйте виртуальное окружение: source venv/bin/activate"
echo "  2. Запустите тестовые сервисы: docker-compose up -d"
echo "  3. Используйте скрипт быстрого запуска: ./run_tools.sh"
echo ""
echo "📚 Примеры команд:"
echo "  • python3 ddos_educational.py 127.0.0.1 -t http -d 30"
echo "  • python3 network_scanner.py 192.168.1.0/24 --all"
echo "  • python3 exploitation_tools.py 127.0.0.1 --ssh-brute"
echo ""
echo "⚠️  ПОМНИТЕ:"
echo "  • Используйте только в собственной лаборатории!"
echo "  • Тестируйте только на разрешенных системах!"
echo "  • Изучайте для защиты, а не для атак!"
echo ""
echo "📖 Документация: README.md"
