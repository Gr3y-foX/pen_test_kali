#!/usr/bin/env python3
"""
Генератор персонализированных паролей на основе информации о цели
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import argparse
import itertools
import random
import string
from datetime import datetime, date

class PersonalizedPasswordGenerator:
    """
    Генератор паролей на основе персональной информации о цели
    """
    
    def __init__(self):
        self.passwords = set()  # Используем set для избежания дубликатов
        self.common_words = [
            'password', 'admin', 'root', 'user', 'guest', 'test', 'demo',
            'default', 'system', 'server', 'linux', 'kali', 'ubuntu',
            'windows', 'microsoft', 'oracle', 'mysql', 'apache', 'nginx'
        ]
    
    def add_basic_info(self, name, birth_year=None, birth_month=None, birth_day=None):
        """
        Добавление базовой информации о цели
        """
        print(f"📝 Добавляем информацию о цели: {name}")
        
        # Базовые варианты имени
        self.passwords.update([
            name.lower(),
            name.upper(),
            name.capitalize(),
            name.title()
        ])
        
        # Имя с цифрами
        for i in range(10):
            self.passwords.update([
                f"{name.lower()}{i}",
                f"{name.upper()}{i}",
                f"{name.capitalize()}{i}",
                f"{i}{name.lower()}",
                f"{i}{name.upper()}",
                f"{i}{name.capitalize()}"
            ])
        
        # Имя с годами
        if birth_year:
            self.passwords.update([
                f"{name.lower()}{birth_year}",
                f"{name.upper()}{birth_year}",
                f"{name.capitalize()}{birth_year}",
                f"{birth_year}{name.lower()}",
                f"{birth_year}{name.upper()}",
                f"{birth_year}{name.capitalize()}"
            ])
            
            # Год рождения с разными форматами
            year_short = str(birth_year)[-2:]
            self.passwords.update([
                f"{name.lower()}{year_short}",
                f"{name.upper()}{year_short}",
                f"{name.capitalize()}{year_short}",
                f"{year_short}{name.lower()}",
                f"{year_short}{name.upper()}",
                f"{year_short}{name.capitalize()}"
            ])
        
        # Имя с датой рождения
        if birth_year and birth_month and birth_day:
            # Полная дата
            full_date = f"{birth_year}{birth_month:02d}{birth_day:02d}"
            self.passwords.update([
                f"{name.lower()}{full_date}",
                f"{name.upper()}{full_date}",
                f"{name.capitalize()}{full_date}",
                f"{full_date}{name.lower()}",
                f"{full_date}{name.upper()}",
                f"{full_date}{name.capitalize()}"
            ])
            
            # Короткая дата
            short_date = f"{birth_month:02d}{birth_day:02d}"
            self.passwords.update([
                f"{name.lower()}{short_date}",
                f"{name.upper()}{short_date}",
                f"{name.capitalize()}{short_date}",
                f"{short_date}{name.lower()}",
                f"{short_date}{name.upper()}",
                f"{short_date}{name.capitalize()}"
            ])
    
    def add_personal_info(self, nickname=None, city=None, company=None, hobby=None, pet=None):
        """
        Добавление дополнительной персональной информации
        """
        personal_info = []
        
        if nickname:
            personal_info.append(nickname)
        if city:
            personal_info.append(city)
        if company:
            personal_info.append(company)
        if hobby:
            personal_info.append(hobby)
        if pet:
            personal_info.append(pet)
        
        for info in personal_info:
            if info:
                print(f"📝 Добавляем: {info}")
                
                # Базовые варианты
                self.passwords.update([
                    info.lower(),
                    info.upper(),
                    info.capitalize(),
                    info.title()
                ])
                
                # С цифрами
                for i in range(10):
                    self.passwords.update([
                        f"{info.lower()}{i}",
                        f"{info.upper()}{i}",
                        f"{info.capitalize()}{i}",
                        f"{i}{info.lower()}",
                        f"{i}{info.upper()}",
                        f"{i}{info.capitalize()}"
                    ])
                
                # С годами
                for year in range(2020, 2025):
                    self.passwords.update([
                        f"{info.lower()}{year}",
                        f"{info.upper()}{year}",
                        f"{info.capitalize()}{year}",
                        f"{year}{info.lower()}",
                        f"{year}{info.upper()}",
                        f"{year}{info.capitalize()}"
                    ])
    
    def add_common_patterns(self):
        """
        Добавление распространенных паттернов паролей
        """
        print("📝 Добавляем распространенные паттерны...")
        
        # Простые пароли
        simple_passwords = [
            'password', '123456', 'admin', 'root', 'user', 'guest',
            'test', 'demo', 'kali', 'toor', 'ubuntu', 'linux',
            'password123', 'admin123', 'root123', 'user123',
            'password1', 'admin1', 'root1', 'user1',
            'password!', 'admin!', 'root!', 'user!',
            'password@', 'admin@', 'root@', 'user@',
            'password#', 'admin#', 'root#', 'user#',
            'pass', 'Pass', 'PASS', 'pass123', 'Pass123', 'PASS123',
            'hello', 'Hello', 'HELLO', 'hello123', 'Hello123', 'HELLO123',
            'welcome', 'Welcome', 'WELCOME', 'welcome123', 'Welcome123', 'WELCOME123'
        ]
        
        self.passwords.update(simple_passwords)
        
        # Пароли с годами
        for year in range(2020, 2025):
            self.passwords.update([
                f"password{year}", f"admin{year}", f"root{year}", f"user{year}",
                f"kali{year}", f"toor{year}", f"linux{year}", f"ubuntu{year}",
                f"{year}password", f"{year}admin", f"{year}root", f"{year}user",
                f"{year}kali", f"{year}toor", f"{year}linux", f"{year}ubuntu"
            ])
        
        # Пароли с символами
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        
        for symbol in symbols[:15]:  # Берем только первые 15 символов
            for word in ['password', 'admin', 'root', 'user', 'kali', 'toor']:
                self.passwords.update([
                    f"{word}{symbol}",
                    f"{word.capitalize()}{symbol}",
                    f"{word.upper()}{symbol}",
                    f"{symbol}{word}",
                    f"{symbol}{word.capitalize()}",
                    f"{symbol}{word.upper()}"
                ])
    
    def add_keyboard_patterns(self):
        """
        Добавление клавиатурных паттернов
        """
        print("📝 Добавляем клавиатурные паттерны...")
        
        # Клавиатурные последовательности
        keyboard_patterns = [
            'qwerty', 'QWERTY', 'Qwerty', 'qwerty123', 'QWERTY123', 'Qwerty123',
            'asdfgh', 'ASDFGH', 'Asdfgh', 'asdfgh123', 'ASDFGH123', 'Asdfgh123',
            'zxcvbn', 'ZXCVBN', 'Zxcvbn', 'zxcvbn123', 'ZXCVBN123', 'Zxcvbn123',
            '1qaz2wsx', '1QAZ2WSX', '1qaz2wsx123', '1QAZ2WSX123',
            'qazwsx', 'QAZWSX', 'Qazwsx', 'qazwsx123', 'QAZWSX123', 'Qazwsx123',
            '123qwe', '123QWE', '123qwe123', '123QWE123',
            'qwertyui', 'QWERTYUI', 'Qwertyui', 'qwertyui123', 'QWERTYUI123', 'Qwertyui123',
            'asdfghjk', 'ASDFGHJK', 'Asdfghjk', 'asdfghjk123', 'ASDFGHJK123', 'Asdfghjk123',
            'zxcvbnm', 'ZXCVBNM', 'Zxcvbnm', 'zxcvbnm123', 'ZXCVBNM123', 'Zxcvbnm123'
        ]
        
        self.passwords.update(keyboard_patterns)
    
    def add_number_patterns(self):
        """
        Добавление числовых паттернов
        """
        print("📝 Добавляем числовые паттерны...")
        
        # Простые числовые последовательности
        number_patterns = [
            '123', '1234', '12345', '123456', '1234567', '12345678', '123456789', '1234567890',
            '111', '1111', '11111', '111111', '1111111', '11111111',
            '000', '0000', '00000', '000000', '0000000', '00000000',
            '999', '9999', '99999', '999999', '9999999', '99999999',
            '0123', '01234', '012345', '0123456', '01234567', '012345678',
            '9876', '98765', '987654', '9876543', '98765432', '987654321',
            '1357', '13579', '135791', '1357913', '13579135',
            '2468', '24680', '246802', '2468024', '24680246',
            '1122', '112233', '1122334', '11223344',
            '1212', '121212', '1212121', '12121212',
            '1313', '131313', '1313131', '13131313',
            '1414', '141414', '1414141', '14141414',
            '1515', '151515', '1515151', '15151515'
        ]
        
        self.passwords.update(number_patterns)
        
        # Комбинации с годами
        for year in range(2020, 2025):
            self.passwords.update([
                f"123{year}", f"1234{year}", f"12345{year}", f"123456{year}",
                f"{year}123", f"{year}1234", f"{year}12345", f"{year}123456",
                f"111{year}", f"1111{year}", f"11111{year}", f"111111{year}",
                f"{year}111", f"{year}1111", f"{year}11111", f"{year}111111"
            ])
    
    def add_leet_speak(self, base_word):
        """
        Добавление leet speak вариантов
        """
        leet_dict = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'l': ['1'],
            'g': ['9'],
            'b': ['6'],
            'z': ['2']
        }
        
        leet_variations = set()
        
        # Простые замены
        leet_word = base_word.lower()
        for char, replacements in leet_dict.items():
            if char in leet_word:
                for replacement in replacements:
                    leet_variations.add(leet_word.replace(char, replacement))
        
        # Комбинированные замены
        for char, replacements in leet_dict.items():
            if char in base_word.lower():
                for replacement in replacements:
                    new_word = base_word.lower().replace(char, replacement)
                    leet_variations.add(new_word)
                    # Добавляем с цифрами
                    for i in range(10):
                        leet_variations.add(f"{new_word}{i}")
                        leet_variations.add(f"{i}{new_word}")
        
        self.passwords.update(leet_variations)
        return leet_variations
    
    def generate_all_passwords(self):
        """
        Генерация всех возможных паролей
        """
        print("🚀 Генерируем все возможные пароли...")
        
        # Добавляем leet speak для всех слов
        current_passwords = list(self.passwords)
        for password in current_passwords:
            if len(password) > 2 and password.isalpha():
                self.add_leet_speak(password)
        
        # Добавляем комбинации
        self.add_combinations()
        
        # Преобразуем в список и сортируем
        password_list = list(self.passwords)
        password_list.sort()
        
        print(f"✅ Сгенерировано {len(password_list)} уникальных паролей")
        return password_list
    
    def add_combinations(self):
        """
        Добавление комбинаций существующих паролей
        """
        print("📝 Добавляем комбинации...")
        
        current_passwords = list(self.passwords)
        
        # Комбинации двух слов
        for i, word1 in enumerate(current_passwords[:50]):  # Ограничиваем для производительности
            for word2 in current_passwords[i+1:i+51]:
                if len(word1) > 2 and len(word2) > 2:
                    self.passwords.update([
                        f"{word1}{word2}",
                        f"{word1.capitalize()}{word2.capitalize()}",
                        f"{word1.upper()}{word2.upper()}",
                        f"{word1.lower()}{word2.lower()}"
                    ])
        
        # Комбинации с символами
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        
        for password in current_passwords[:100]:  # Ограничиваем для производительности
            if len(password) > 2:
                for symbol in symbols[:10]:  # Берем только первые 10 символов
                    self.passwords.update([
                        f"{password}{symbol}",
                        f"{symbol}{password}",
                        f"{password}{symbol}{password}",
                        f"{symbol}{password}{symbol}"
                    ])
    
    def save_to_file(self, filename):
        """
        Сохранение паролей в файл
        """
        password_list = self.generate_all_passwords()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for password in password_list:
                    f.write(f"{password}\n")
            
            print(f"✅ Пароли сохранены в файл: {filename}")
            print(f"📊 Всего паролей: {len(password_list)}")
            return filename
            
        except Exception as e:
            print(f"❌ Ошибка сохранения файла: {e}")
            return None
    
    def print_statistics(self):
        """
        Вывод статистики по сгенерированным паролям
        """
        password_list = list(self.passwords)
        
        print(f"\n📊 СТАТИСТИКА ПАРОЛЕЙ:")
        print(f"  • Всего паролей: {len(password_list)}")
        
        # Статистика по длине
        length_stats = {}
        for password in password_list:
            length = len(password)
            length_stats[length] = length_stats.get(length, 0) + 1
        
        print(f"  • По длине:")
        for length in sorted(length_stats.keys()):
            print(f"    - {length} символов: {length_stats[length]} паролей")
        
        # Статистика по типам
        alpha_count = sum(1 for p in password_list if p.isalpha())
        numeric_count = sum(1 for p in password_list if p.isdigit())
        alphanumeric_count = sum(1 for p in password_list if p.isalnum())
        special_count = len(password_list) - alphanumeric_count
        
        print(f"  • По типам:")
        print(f"    - Только буквы: {alpha_count} паролей")
        print(f"    - Только цифры: {numeric_count} паролей")
        print(f"    - Буквы + цифры: {alphanumeric_count} паролей")
        print(f"    - Со спец. символами: {special_count} паролей")

def main():
    """
    Главная функция генератора паролей
    """
    print("=" * 60)
    print("🔐 ГЕНЕРАТОР ПЕРСОНАЛИЗИРОВАННЫХ ПАРОЛЕЙ")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Генератор персонализированных паролей')
    parser.add_argument('-n', '--name', required=True, help='Имя цели')
    parser.add_argument('-y', '--birth-year', type=int, help='Год рождения')
    parser.add_argument('-m', '--birth-month', type=int, help='Месяц рождения')
    parser.add_argument('-d', '--birth-day', type=int, help='День рождения')
    parser.add_argument('--nickname', help='Псевдоним')
    parser.add_argument('--city', help='Город')
    parser.add_argument('--company', help='Компания')
    parser.add_argument('--hobby', help='Хобби')
    parser.add_argument('--pet', help='Имя питомца')
    parser.add_argument('-o', '--output', default='personalized_passwords.txt', help='Файл для сохранения паролей')
    parser.add_argument('--show-stats', action='store_true', help='Показать статистику')
    
    args = parser.parse_args()
    
    # Создаем генератор
    generator = PersonalizedPasswordGenerator()
    
    # Добавляем базовую информацию
    generator.add_basic_info(
        args.name,
        args.birth_year,
        args.birth_month,
        args.birth_day
    )
    
    # Добавляем дополнительную информацию
    generator.add_personal_info(
        args.nickname,
        args.city,
        args.company,
        args.hobby,
        args.pet
    )
    
    # Добавляем распространенные паттерны
    generator.add_common_patterns()
    generator.add_keyboard_patterns()
    generator.add_number_patterns()
    
    # Сохраняем в файл
    filename = generator.save_to_file(args.output)
    
    if filename and args.show_stats:
        generator.print_statistics()
    
    print(f"\n🎯 Рекомендации:")
    print(f"  • Используйте файл {filename} для SSH brute force")
    print(f"  • Команда: python3 tools/advanced_ssh_attack.py <IP> -u <user> -w {filename}")
    print(f"  • Добавьте --random-ports для обхода лимитов")
    print(f"  • Используйте --unlimited-attempts для неограниченного количества попыток")

if __name__ == "__main__":
    main()
