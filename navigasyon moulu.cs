using System;

public class Boat
{
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public double Heading { get; set; }
}

public class NavigationSystem
{
    private const double BoatSpeedKmPerHour = 10.0; // Assume boat travels at 10 km/h
    private const double MaxRouteDeviationPercentage = 5.0; // 5% deviation allowed

    private Boat _boat;
    private double _targetLatitude;
    private double _targetLongitude;

    public NavigationSystem(double startLat, double startLon, double targetLat, double targetLon)
    {
        _boat = new Boat
        {
            Latitude = startLat,
            Longitude = startLon,
            Heading = CalculateBearing(startLat, startLon, targetLat, targetLon)
        };
        _targetLatitude = targetLat;
        _targetLongitude = targetLon;
    }

    /// <summary>
    /// Simulates the boat's movement for one hour.
    /// </summary>
    public void SimulateMovement()
    {
        Console.WriteLine($"Simulating movement from Lat: {_boat.Latitude:F4}, Lon: {_boat.Longitude:F4}");

        // Calculate distance to travel in one hour
        double distanceKm = BoatSpeedKmPerHour;
        
        // Convert distance to degrees for simplicity (approximate conversion)
        // 1 degree of latitude is roughly 111 km
        double distanceInDegrees = distanceKm / 111.0;

        // Update position based on heading
        _boat.Latitude += distanceInDegrees * Math.Cos(DegreesToRadians(_boat.Heading));
        _boat.Longitude += distanceInDegrees * Math.Sin(DegreesToRadians(_boat.Heading));

        // Add a small random deviation to the heading to simulate real-world conditions
        Random rand = new Random();
        _boat.Heading += rand.NextDouble() * 2 - 1; // +/- 1 degree deviation

        Console.WriteLine($"New Position -> Lat: {_boat.Latitude:F4}, Lon: {_boat.Longitude:F4}, Heading: {_boat.Heading:F2}");

        CheckRouteDeviation();
    }

    /// <summary>
    /// Checks if the boat's current position deviates from the planned route.
    /// </summary>
    public void CheckRouteDeviation()
    {
        // Calculate the ideal heading from current position to target
        double idealHeading = CalculateBearing(_boat.Latitude, _boat.Longitude, _targetLatitude, _targetLongitude);
        double deviation = Math.Abs(_boat.Heading - idealHeading);

        // Normalize the deviation angle to be between 0 and 180 degrees
        if (deviation > 180)
        {
            deviation = 360 - deviation;
        }

        // Calculate the percentage of deviation (this is a simplified approach)
        double deviationPercentage = (deviation / 360.0) * 100;

        Console.WriteLine($"Current Heading: {_boat.Heading:F2}, Ideal Heading: {idealHeading:F2}, Deviation: {deviation:F2} degrees ({deviationPercentage:F2}%)");

        if (deviationPercentage > MaxRouteDeviationPercentage)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("!!! Rota Sapması Uyarısı: Hedeflenen rotadan %5'ten fazla sapma var. !!!");
            Console.ResetColor();
        }
    }

    /// <summary>
    /// Helper method to calculate the bearing (heading) between two points.
    /// This is a simplified calculation and does not account for the Earth's curvature (haversine formula).
    /// </summary>
    private double CalculateBearing(double lat1, double lon1, double lat2, double lon2)
    {
        double lat1Rad = DegreesToRadians(lat1);
        double lon1Rad = DegreesToRadians(lon1);
        double lat2Rad = DegreesToRadians(lat2);
        double lon2Rad = DegreesToRadians(lon2);

        double deltaLon = lon2Rad - lon1Rad;

        double y = Math.Sin(deltaLon) * Math.Cos(lat2Rad);
        double x = Math.Cos(lat1Rad) * Math.Sin(lat2Rad) -
                   Math.Sin(lat1Rad) * Math.Cos(lat2Rad) * Math.Cos(deltaLon);

        double bearing = RadiansToDegrees(Math.Atan2(y, x));
        return (bearing + 360) % 360; // Normalize to 0-360 degrees
    }

    private double DegreesToRadians(double degrees)
    {
        return degrees * Math.PI / 180.0;
    }

    private double RadiansToDegrees(double radians)
    {
        return radians * 180.0 / Math.PI;
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Navigasyon Modülü Başlatılıyor...");
        Console.WriteLine("----------------------------------");

        // Start position: Istanbul, Target position: Izmir (simplified coordinates)
        NavigationSystem navSystem = new NavigationSystem(41.0082, 28.9784, 38.4237, 27.1428);

        for (int i = 0; i < 5; i++)
        {
            Console.WriteLine($"\n--- Saat {i + 1} ---");
            navSystem.SimulateMovement();
        }

        Console.WriteLine("\nSimülasyon Tamamlandı.");
    }
}