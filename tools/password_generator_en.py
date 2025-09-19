#!/usr/bin/env python3
"""
Personalized password generator based on target information
WARNING: For use only in your own laboratory environment!

Author: Educational material for cybersecurity learning
License: Educational purposes only
"""

import argparse
import itertools
import random
import string
from datetime import datetime, date

class PersonalizedPasswordGenerator:
    """
    Password generator based on personal information about target
    """
    
    def __init__(self):
        self.passwords = set()  # Use set to avoid duplicates
        self.common_words = [
            'password', 'admin', 'root', 'user', 'guest', 'test', 'demo',
            'default', 'system', 'server', 'linux', 'kali', 'ubuntu',
            'windows', 'microsoft', 'oracle', 'mysql', 'apache', 'nginx'
        ]
    
    def add_basic_info(self, name, birth_year=None, birth_month=None, birth_day=None):
        """
        Add basic information about target
        """
        print(f"📝 Adding target information: {name}")
        
        # Basic name variants
        self.passwords.update([
            name.lower(),
            name.upper(),
            name.capitalize(),
            name.title()
        ])
        
        # Name with numbers
        for i in range(10):
            self.passwords.update([
                f"{name.lower()}{i}",
                f"{name.upper()}{i}",
                f"{name.capitalize()}{i}",
                f"{i}{name.lower()}",
                f"{i}{name.upper()}",
                f"{i}{name.capitalize()}"
            ])
        
        # Name with years
        if birth_year:
            self.passwords.update([
                f"{name.lower()}{birth_year}",
                f"{name.upper()}{birth_year}",
                f"{name.capitalize()}{birth_year}",
                f"{birth_year}{name.lower()}",
                f"{birth_year}{name.upper()}",
                f"{birth_year}{name.capitalize()}"
            ])
            
            # Birth year with different formats
            year_short = str(birth_year)[-2:]
            self.passwords.update([
                f"{name.lower()}{year_short}",
                f"{name.upper()}{year_short}",
                f"{name.capitalize()}{year_short}",
                f"{year_short}{name.lower()}",
                f"{year_short}{name.upper()}",
                f"{year_short}{name.capitalize()}"
            ])
        
        # Name with birth date
        if birth_year and birth_month and birth_day:
            # Full date
            full_date = f"{birth_year}{birth_month:02d}{birth_day:02d}"
            self.passwords.update([
                f"{name.lower()}{full_date}",
                f"{name.upper()}{full_date}",
                f"{name.capitalize()}{full_date}",
                f"{full_date}{name.lower()}",
                f"{full_date}{name.upper()}",
                f"{full_date}{name.capitalize()}"
            ])
            
            # Short date
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
        Add additional personal information
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
                print(f"📝 Adding: {info}")
                
                # Basic variants
                self.passwords.update([
                    info.lower(),
                    info.upper(),
                    info.capitalize(),
                    info.title()
                ])
                
                # With numbers
                for i in range(10):
                    self.passwords.update([
                        f"{info.lower()}{i}",
                        f"{info.upper()}{i}",
                        f"{info.capitalize()}{i}",
                        f"{i}{info.lower()}",
                        f"{i}{info.upper()}",
                        f"{i}{info.capitalize()}"
                    ])
                
                # With years
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
        Add common password patterns
        """
        print("📝 Adding common patterns...")
        
        # Simple passwords
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
        
        # Passwords with years
        for year in range(2020, 2025):
            self.passwords.update([
                f"password{year}", f"admin{year}", f"root{year}", f"user{year}",
                f"kali{year}", f"toor{year}", f"linux{year}", f"ubuntu{year}",
                f"{year}password", f"{year}admin", f"{year}root", f"{year}user",
                f"{year}kali", f"{year}toor", f"{year}linux", f"{year}ubuntu"
            ])
        
        # Passwords with symbols
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        
        for symbol in symbols[:15]:  # Take only first 15 symbols
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
        Add keyboard patterns
        """
        print("📝 Adding keyboard patterns...")
        
        # Keyboard sequences
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
        Add number patterns
        """
        print("📝 Adding number patterns...")
        
        # Simple number sequences
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
        
        # Combinations with years
        for year in range(2020, 2025):
            self.passwords.update([
                f"123{year}", f"1234{year}", f"12345{year}", f"123456{year}",
                f"{year}123", f"{year}1234", f"{year}12345", f"{year}123456",
                f"111{year}", f"1111{year}", f"11111{year}", f"111111{year}",
                f"{year}111", f"{year}1111", f"{year}11111", f"{year}111111"
            ])
    
    def add_leet_speak(self, base_word):
        """
        Add leet speak variants
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
        
        # Simple replacements
        leet_word = base_word.lower()
        for char, replacements in leet_dict.items():
            if char in leet_word:
                for replacement in replacements:
                    leet_variations.add(leet_word.replace(char, replacement))
        
        # Combined replacements
        for char, replacements in leet_dict.items():
            if char in base_word.lower():
                for replacement in replacements:
                    new_word = base_word.lower().replace(char, replacement)
                    leet_variations.add(new_word)
                    # Add with numbers
                    for i in range(10):
                        leet_variations.add(f"{new_word}{i}")
                        leet_variations.add(f"{i}{new_word}")
        
        self.passwords.update(leet_variations)
        return leet_variations
    
    def generate_all_passwords(self):
        """
        Generate all possible passwords
        """
        print("🚀 Generating all possible passwords...")
        
        # Add leet speak for all words
        current_passwords = list(self.passwords)
        for password in current_passwords:
            if len(password) > 2 and password.isalpha():
                self.add_leet_speak(password)
        
        # Add combinations
        self.add_combinations()
        
        # Convert to list and sort
        password_list = list(self.passwords)
        password_list.sort()
        
        print(f"✅ Generated {len(password_list)} unique passwords")
        return password_list
    
    def add_combinations(self):
        """
        Add combinations of existing passwords
        """
        print("📝 Adding combinations...")
        
        current_passwords = list(self.passwords)
        
        # Two word combinations
        for i, word1 in enumerate(current_passwords[:50]):  # Limit for performance
            for word2 in current_passwords[i+1:i+51]:
                if len(word1) > 2 and len(word2) > 2:
                    self.passwords.update([
                        f"{word1}{word2}",
                        f"{word1.capitalize()}{word2.capitalize()}",
                        f"{word1.upper()}{word2.upper()}",
                        f"{word1.lower()}{word2.lower()}"
                    ])
        
        # Combinations with symbols
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '.', ',', ';', ':', '?', '/', '|', '\\', '~', '`', '<', '>', '[', ']', '{', '}', '(', ')', '"', "'", ' ']
        
        for password in current_passwords[:100]:  # Limit for performance
            if len(password) > 2:
                for symbol in symbols[:10]:  # Take only first 10 symbols
                    self.passwords.update([
                        f"{password}{symbol}",
                        f"{symbol}{password}",
                        f"{password}{symbol}{password}",
                        f"{symbol}{password}{symbol}"
                    ])
    
    def save_to_file(self, filename):
        """
        Save passwords to file
        """
        password_list = self.generate_all_passwords()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for password in password_list:
                    f.write(f"{password}\n")
            
            print(f"✅ Passwords saved to file: {filename}")
            print(f"📊 Total passwords: {len(password_list)}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None
    
    def print_statistics(self):
        """
        Print statistics for generated passwords
        """
        password_list = list(self.passwords)
        
        print(f"\n📊 PASSWORD STATISTICS:")
        print(f"  • Total passwords: {len(password_list)}")
        
        # Statistics by length
        length_stats = {}
        for password in password_list:
            length = len(password)
            length_stats[length] = length_stats.get(length, 0) + 1
        
        print(f"  • By length:")
        for length in sorted(length_stats.keys()):
            print(f"    - {length} characters: {length_stats[length]} passwords")
        
        # Statistics by type
        alpha_count = sum(1 for p in password_list if p.isalpha())
        numeric_count = sum(1 for p in password_list if p.isdigit())
        alphanumeric_count = sum(1 for p in password_list if p.isalnum())
        special_count = len(password_list) - alphanumeric_count
        
        print(f"  • By type:")
        print(f"    - Letters only: {alpha_count} passwords")
        print(f"    - Numbers only: {numeric_count} passwords")
        print(f"    - Letters + numbers: {alphanumeric_count} passwords")
        print(f"    - With special symbols: {special_count} passwords")

def main():
    """
    Main function of password generator
    """
    print("=" * 60)
    print("🔐 PERSONALIZED PASSWORD GENERATOR")
    print("=" * 60)
    print("⚠️  WARNING: For use only in your own laboratory!")
    print("⚠️  Using against other systems is ILLEGAL!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Personalized password generator')
    parser.add_argument('-n', '--name', required=True, help='Target name')
    parser.add_argument('-y', '--birth-year', type=int, help='Birth year')
    parser.add_argument('-m', '--birth-month', type=int, help='Birth month')
    parser.add_argument('-d', '--birth-day', type=int, help='Birth day')
    parser.add_argument('--nickname', help='Nickname')
    parser.add_argument('--city', help='City')
    parser.add_argument('--company', help='Company')
    parser.add_argument('--hobby', help='Hobby')
    parser.add_argument('--pet', help='Pet name')
    parser.add_argument('-o', '--output', default='personalized_passwords.txt', help='File to save passwords')
    parser.add_argument('--show-stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    # Create generator
    generator = PersonalizedPasswordGenerator()
    
    # Add basic information
    generator.add_basic_info(
        args.name,
        args.birth_year,
        args.birth_month,
        args.birth_day
    )
    
    # Add additional information
    generator.add_personal_info(
        args.nickname,
        args.city,
        args.company,
        args.hobby,
        args.pet
    )
    
    # Add common patterns
    generator.add_common_patterns()
    generator.add_keyboard_patterns()
    generator.add_number_patterns()
    
    # Save to file
    filename = generator.save_to_file(args.output)
    
    if filename and args.show_stats:
        generator.print_statistics()
    
    print(f"\n🎯 Recommendations:")
    print(f"  • Use file {filename} for SSH brute force")
    print(f"  • Command: python3 tools/smart_ssh_bruteforce_en.py <IP> -u <user> -w {filename}")
    print(f"  • Add --github-passwords for additional popular passwords")
    print(f"  • Use --unlimited-attempts for unlimited attempts")

if __name__ == "__main__":
    main()
