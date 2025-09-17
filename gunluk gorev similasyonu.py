import random
import json
import datetime
import os
import time

# Navigasyon Modülü
class NavigationSystem:
    def __init__(self, start_lat, start_lon, target_lat, target_lon):
        self.latitude = start_lat
        self.longitude = start_lon
        self.heading = self.calculate_bearing(start_lat, start_lon, target_lat, target_lon)
        self.target_latitude = target_lat
        self.target_longitude = target_lon
        self.speed_kmh = 10.0
        self.last_deviation = 0.0

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon = math.radians(lon2 - lon1)
        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
        bearing = math.degrees(math.atan2(y, x))
        return (bearing + 360) % 360

    def update_position(self):
        distance_km = self.speed_kmh
        distance_in_degrees = distance_km / 111.0 # Approximate
        self.latitude += distance_in_degrees * math.cos(math.radians(self.heading))
        self.longitude += distance_in_degrees * math.sin(math.radians(self.heading))
        self.heading += random.uniform(-1, 1) # Add slight random deviation

    def get_deviation(self):
        ideal_heading = self.calculate_bearing(self.latitude, self.longitude, self.target_latitude, self.target_longitude)
        deviation = abs(self.heading - ideal_heading)
        if deviation > 180:
            deviation = 360 - deviation
        self.last_deviation = deviation
        return deviation

# Çevre Algılama & Füzyon Modülü
class EnvironmentModule:
    def __init__(self):
        pass

    def simulate_sensors(self):
        radar_data = self._simulate_radar()
        sonar_data = self._simulate_sonar()
        camera_data = self._simulate_camera()

        return self._fuse_data(radar_data, sonar_data, camera_data)

    def _simulate_radar(self):
        if random.random() < 0.2:
            distance = random.uniform(50, 500)
            angle = random.uniform(0, 360)
            return {"distance": distance, "angle": angle, "type": "radar"}
        return None

    def _simulate_sonar(self):
        if random.random() < 0.1:
            distance = random.uniform(10, 100)
            return {"distance": distance, "type": "sonar"}
        return None

    def _simulate_camera(self):
        phenomena = random.choice([None, "wave", "fog", "vessel"])
        if phenomena:
            severity = random.choice(["low", "medium", "high"])
            direction = random.uniform(0, 360)
            return {"object": phenomena, "severity": severity, "direction": direction, "type": "camera"}
        return None

    def _fuse_data(self, radar, sonar, camera):
        if camera and camera["object"] == "vessel" and camera["severity"] == "high":
            return {"threat": "vessel", "severity": "high", "direction": camera["direction"]}
        if camera and camera["object"] == "wave" and camera["severity"] == "high":
            return {"threat": "storm", "severity": "high", "direction": camera["direction"]}
        if radar and radar["distance"] < 200:
            return {"threat": "potential obstacle", "severity": "medium", "direction": radar["angle"]}
        if sonar and sonar["distance"] < 50:
            return {"threat": "underwater object", "severity": "medium", "direction": None}
        return {"threat": "none", "severity": "low", "direction": None}

# Enerji Yönetim Modülü
class EnergySystem:
    def __init__(self, battery_level=100.0):
        self.battery_level = battery_level
        self.power_save_mode = False
        self.solar_output = 0.0
        self.consumption = 5.0

    def update(self, current_hour):
        time_of_day = self.get_time_of_day(current_hour)
        self.simulate_solar_panel(time_of_day)

        net_change = self.solar_output - self.consumption
        self.battery_level += net_change
        self.battery_level = max(0.0, min(100.0, self.battery_level))
        
        # Check for power-saving mode
        if self.battery_level < 20.0 and not self.power_save_mode:
            self.power_save_mode = True
            self.consumption = 2.0
            return "power_save_activated"
        elif self.battery_level > 25.0 and self.power_save_mode:
            self.power_save_mode = False
            self.consumption = 5.0
            return "power_save_deactivated"
        return "normal"

    def get_time_of_day(self, hour):
        if 6 <= hour < 10: return "morning"
        elif 10 <= hour < 16: return "midday"
        elif 16 <= hour < 20: return "evening"
        return "night"

    def simulate_solar_panel(self, time_of_day):
        if time_of_day == "morning":
            self.solar_output = random.uniform(2.0, 5.0)
        elif time_of_day == "midday":
            self.solar_output = random.uniform(8.0, 15.0)
        elif time_of_day == "evening":
            self.solar_output = random.uniform(1.0, 3.0)
        else:
            self.solar_output = 0.0

# Karar Modülü
class DecisionModule:
    def __init__(self):
        pass

    def evaluate(self, battery_level, power_save_mode, deviation, threat_status):
        if power_save_mode:
            return {"action": "wait", "reason": "Energy conservation mode is active."}
        
        if threat_status["severity"] == "high":
            if threat_status["threat"] == "vessel":
                return {"action": "change_course", "reason": "High severity vessel detected."}
            else:
                return {"action": "wait", "reason": "High severity storm detected."}
        
        if deviation > 5.0:
            return {"action": "correct_course", "reason": "Route deviation detected."}
        
        return {"action": "continue_sailing", "reason": "All systems normal."}

# Motor Kontrol Modülü
class MotorControlModule:
    def __init__(self):
        self.stop_signal = 1500

    def send_command(self, action, deviation=0):
        if action == "continue_sailing":
            return {"left": 1600, "right": 1600}
        elif action == "correct_course":
            if deviation > 0:
                return {"left": 1650, "right": 1550}
            else:
                return {"left": 1550, "right": 1650}
        elif action == "change_course":
            return {"left": 1750, "right": 1350}
        elif action == "wait":
            return {"left": self.stop_signal, "right": self.stop_signal}
        return {"left": self.stop_signal, "right": self.stop_signal}

# Veri Kaydı ve Geri Besleme Modülü
class DataLogger:
    def __init__(self, txt_file="mission_log.txt", json_file="mission_log.json"):
        self.txt_file = txt_file
        self.json_file = json_file
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.txt_file):
            os.remove(self.txt_file)

    def log_event(self, module_name, event_data, hour):
        timestamp = datetime.datetime.now().isoformat()
        
        # TXT dosyasına yazma
        txt_entry = f"Saat {hour:02d}:00 - [{module_name}] - {event_data.get('message', 'No message')}\n"
        with open(self.txt_file, 'a') as f:
            f.write(txt_entry)
        
        # JSON dosyasına yazma
        try:
            with open(self.json_file, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        json_entry = {
            "timestamp": timestamp,
            "hour": hour,
            "module": module_name,
            "event_data": event_data
        }
        logs.append(json_entry)
        
        with open(self.json_file, 'w') as f:
            json.dump(logs, f, indent=4)
        
        print(f"[{module_name}] -> {event_data.get('message', 'No message')}")

# --- Görev Simülasyonu ---
if __name__ == "__main__":
    # Modülleri başlatma
    nav_system = NavigationSystem(41.0082, 28.9784, 38.4237, 27.1428) # Istanbul to Izmir
    env_module = EnvironmentModule()
    energy_system = EnergySystem()
    decision_module = DecisionModule()
    motor_control = MotorControlModule()
    logger = DataLogger()

    print("24 Saatlik Görev Simülasyonu Başlatılıyor...")
    print("---------------------------------------------")

    for hour in range(24):
        print(f"\n--- Saat {hour:02d}:00 ---")
        
        # 1. Enerji Modülü
        energy_status = energy_system.update(hour)
        logger.log_event("EnergySystem", {
            "message": f"Battery level: {energy_system.battery_level:.2f}%. Mode: {energy_status}",
            "battery_level": energy_system.battery_level,
            "solar_output": energy_system.solar_output
        }, hour)
        
        # 2. Navigasyon Modülü
        nav_system.update_position()
        deviation = nav_system.get_deviation()
        logger.log_event("NavigationSystem", {
            "message": f"Position updated. Deviation: {deviation:.2f} degrees.",
            "latitude": nav_system.latitude,
            "longitude": nav_system.longitude,
            "deviation": deviation
        }, hour)
        
        # 3. Çevre Modülü
        threat_status = env_module.simulate_sensors()
        logger.log_event("EnvironmentModule", {
            "message": f"Environmental threat detected: {threat_status['threat']}",
            "threat_status": threat_status
        }, hour)

        # 4. Karar Modülü
        decision = decision_module.evaluate(
            energy_system.battery_level, 
            energy_system.power_save_mode, 
            deviation, 
            threat_status
        )
        logger.log_event("DecisionModule", {
            "message": f"Decision: {decision['action']}. Reason: {decision['reason']}",
            "action": decision['action'],
            "reason": decision['reason']
        }, hour)

        # 5. Motor Kontrol Modülü
        motor_command = motor_control.send_command(decision["action"], deviation)
        logger.log_event("MotorControlModule", {
            "message": f"Motor command sent. Action: {decision['action']}",
            "left_motor": motor_command['left'],
            "right_motor": motor_command['right']
        }, hour)
        
        time.sleep(0.5) # Simülasyonu yavaşlatmak için

    print("\nSimülasyon Tamamlandı. Çıktılar 'mission_log.txt' ve 'mission_log.json' dosyalarında.")