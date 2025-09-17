import json
import datetime
import os

class DataLogger:
    def __init__(self, log_file_name="system_log.json"):
        self.log_file_name = log_file_name
        # Log dosyasını başlatma, eğer yoksa oluşturur
        if not os.path.exists(self.log_file_name):
            with open(self.log_file_name, 'w') as f:
                f.write('[]') # Boş bir JSON listesi olarak başlat

    def log_event(self, module_name, event_data):
        """
        Belirtilen modülden gelen olayı zaman damgasıyla birlikte log dosyasına kaydeder.
        """
        try:
            # Mevcut log dosyasını oku
            with open(self.log_file_name, 'r') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            # Dosya boş veya bozuksa yeni bir liste başlat
            logs = []

        # Yeni log girdisini oluştur
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "module": module_name,
            "event": event_data
        }

        # Yeni girdiyi listeye ekle
        logs.append(log_entry)

        # Güncellenmiş listeyi JSON formatında dosyaya geri yaz
        with open(self.log_file_name, 'w') as f:
            json.dump(logs, f, indent=4)
        
        print(f"Log Kaydedildi: [{module_name}] - {event_data.get('message', 'No message provided')}")

def simulate_system_events(logger):
    """
    Önceki modüllerden gelen olayları simüle eder.
    """
    # Navigasyon Modülü Olayı
    logger.log_event("NavigationModule", {
        "message": "Route deviation detected.",
        "latitude": 38.42,
        "longitude": 27.14,
        "deviation_percentage": 5.5
    })
    
    # Çevre Algılama Modülü Olayı
    logger.log_event("EnvironmentModule", {
        "message": "High severity wave detected.",
        "obstacle": "wave",
        "severity": "high",
        "direction": 60
    })
    
    # Enerji Modülü Olayı
    logger.log_event("EnergyModule", {
        "message": "Power-saving mode activated.",
        "battery_level": 19.5
    })

    # Karar Modülü Olayı
    logger.log_event("DecisionModule", {
        "message": "Decision made to change course due to threat.",
        "action": "ChangeCourse"
    })
    
    # Motor Kontrol Modülü Olayı
    logger.log_event("MotorControlModule", {
        "message": "Executing sharp left turn command.",
        "left_motor_speed": 1750,
        "right_motor_speed": 1350
    })

# --- Simülasyon ---
if __name__ == "__main__":
    logger = DataLogger()
    print("Veri Kaydı Modülü Başlatılıyor...")
    print("-----------------------------------")
    
    # Sistemi simüle et ve olayları logla
    simulate_system_events(logger)

    print(f"\nOlaylar '{logger.log_file_name}' dosyasına başarıyla kaydedildi.")