import random
import time

class EnergySystem:
    def __init__(self, battery_level=100.0):
        self.battery_level = battery_level
        self.power_save_mode = False
        self.solar_panel_output = 0.0
        self.consumption_rate = 5.0  # Saatlik enerji tüketimi (örneğin %5)

    def get_time_of_day(self, hour):
        """Saat dilimine göre günün zamanını belirler."""
        if 6 <= hour < 10:
            return "morning"
        elif 10 <= hour < 16:
            return "midday"
        elif 16 <= hour < 20:
            return "evening"
        else:
            return "night"

    def simulate_solar_panel(self, time_of_day):
        """Günün zamanına göre sahte güneş paneli verisi üretir."""
        if time_of_day == "morning":
            # Sabah saatlerinde düşük verimlilik
            self.solar_panel_output = random.uniform(2.0, 5.0)
        elif time_of_day == "midday":
            # Öğle saatlerinde en yüksek verimlilik
            self.solar_panel_output = random.uniform(8.0, 15.0)
        elif time_of_day == "evening":
            # Akşam saatlerinde verimlilik düşüşü
            self.solar_panel_output = random.uniform(1.0, 3.0)
        else: # "night"
            # Gece güneş enerjisi üretimi yok
            self.solar_panel_output = 0.0

    def update_energy_state(self, current_hour):
        """Enerji durumunu günceller ve tasarruf modunu yönetir."""
        
        # 1. Güneş paneli verisini simüle etme
        time_of_day = self.get_time_of_day(current_hour)
        self.simulate_solar_panel(time_of_day)

        # 2. Batarya seviyesini güncelleme
        # Üretim (solar_panel_output) ile tüketim (consumption_rate) arasındaki farkı hesapla
        net_change = self.solar_panel_output - self.consumption_rate
        self.battery_level += net_change

        # Batarya seviyesinin %0 ile %100 arasında kalmasını sağla
        self.battery_level = max(0.0, min(100.0, self.battery_level))
        
        # 3. Tasarruf modunu kontrol etme ve yönetme
        if self.battery_level < 20.0 and not self.power_save_mode:
            self.power_save_mode = True
            self.consumption_rate = 2.0  # Tasarruf modunda tüketimi azalt
            print("!!! Enerji Tasarruf Modu Aktif: Batarya seviyesi %20'nin altında.")
        elif self.battery_level > 25.0 and self.power_save_mode:
            # Batarya seviyesi %25 üzerine çıktığında normal moda dön (tasarruf modundan çıkış için buffer eklemek iyi bir pratik)
            self.power_save_mode = False
            self.consumption_rate = 5.0  # Normal tüketim oranına dön
            print("Enerji Tasarruf Modu Devre Dışı: Batarya seviyesi yeterli.")

        print(f"Saat: {current_hour}:00, Günün Zamanı: {time_of_day}, Güneş Paneli Üretimi: {self.solar_panel_output:.2f}%, Batarya Seviyesi: {self.battery_level:.2f}%")

# --- Simülasyon ---
if __name__ == "__main__":
    energy_system = EnergySystem()
    print("Enerji Yönetim Sistemi Başlatılıyor...")
    print("---------------------------------------")

    # 24 saatlik bir döngü simüle etme
    for hour in range(24):
        energy_system.update_energy_state(hour)
        time.sleep(0.5) # Simülasyonu daha yavaş çalıştırmak için bekleme ekledik
    
    print("\nSimülasyon Tamamlandı.")