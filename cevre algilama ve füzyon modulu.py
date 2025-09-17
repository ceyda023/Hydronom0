import random
import math

def simulate_radar():
    """Simulates radar data: distance and angle of potential objects."""
    if random.random() < 0.3:  # 30% chance of detecting something
        distance = random.uniform(50, 500)  # Distance in meters
        angle = random.uniform(0, 360)  # Angle in degrees relative to the boat's heading
        return {"distance": distance, "angle": angle, "type": "radar"}
    else:
        return None

def simulate_sonar():
    """Simulates sonar data: presence of underwater objects."""
    if random.random() < 0.5:  # 50% chance of detecting something underwater
        distance = random.uniform(10, 100)  # Distance in meters
        return {"distance": distance, "type": "sonar"}
    else:
        return None

def simulate_camera():
    """Simulates camera data: detects visual phenomena like waves or fog."""
    phenomena = random.choice([None, "wave", "fog"])
    if phenomena:
        severity = random.choice(["low", "medium", "high"])
        direction = random.uniform(0, 360)  # Approximate direction
        return {"object": phenomena, "severity": severity, "direction": direction, "type": "camera"}
    else:
        return None

def fuse_sensors():
    """Fuses data from radar, sonar, and camera to detect obstacles or storms."""
    radar_data = simulate_radar()
    sonar_data = simulate_sonar()
    camera_data = simulate_camera()

    fused_detection = {"obstacle": None, "severity": "low", "direction": None}

    # Simple fusion logic: prioritize camera for object identification
    if camera_data and camera_data["object"] == "wave" and camera_data["severity"] == "high":
        fused_detection["obstacle"] = "wave"
        fused_detection["severity"] = camera_data["severity"]
        fused_detection["direction"] = camera_data["direction"]
    elif camera_data and camera_data["object"] == "fog" and camera_data["severity"] == "high":
        fused_detection["obstacle"] = "fog"
        fused_detection["severity"] = camera_data["severity"]
        fused_detection["direction"] = camera_data["direction"]
    elif radar_data and radar_data["distance"] < 100:
        fused_detection["obstacle"] = "potential obstacle (radar)"
        fused_detection["severity"] = "medium"
        fused_detection["direction"] = radar_data["angle"]
    elif sonar_data and sonar_data["distance"] < 30:
        fused_detection["obstacle"] = "underwater object (sonar)"
        fused_detection["severity"] = "medium"
        fused_detection["direction"] = None  # Sonar typically doesn't give a precise angle

    return fused_detection

if __name__ == "__main__":
    print("Çevre Algılama & Füzyon Modülü Başlatılıyor...")
    print("-------------------------------------------")

    for _ in range(5):  # Simulate 5 sensing cycles
        detection_result = fuse_sensors()
        print(f"Tespit Sonucu: {detection_result}")

    print("\nÇevre Algılama Tamamlandı.")