using System;

// Assume the following classes are defined in your project from previous tasks:
// public class NavigationSystem { ... }
// public class EnvironmentModule { ... } // Formerly named "Füzyon Modülü"
// public class EnergySystem { ... }

public class DecisionModule
{
    private NavigationSystem _navSystem;
    private EnvironmentModule _envModule;
    private EnergySystem _energySystem;

    public DecisionModule(NavigationSystem navSystem, EnvironmentModule envModule, EnergySystem energySystem)
    {
        _navSystem = navSystem;
        _envModule = envModule;
        _energySystem = energySystem;
    }

    /// <summary>
    /// Evaluates the current situation based on data from all modules and makes a decision.
    /// </summary>
    public void EvaluateSituation()
    {
        Console.WriteLine("\n--- Karar Modülü Değerlendirme Başlatıldı ---");

        // Step 1: Check Energy Status
        if (_energySystem.IsPowerSaveMode)
        {
            Console.WriteLine("Karar: Enerji tasarruf modunda, rota düzeltme veya hız artırma yapılmayacak.");
            return; // Energy conservation is the top priority.
        }

        // Step 2: Check for Environmental Threats
        var environmentalThreat = _envModule.GetThreatStatus();
        if (environmentalThreat != null)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"Karar: Çevresel tehdit algılandı: {environmentalThreat.Obstacle} - Şiddet: {environmentalThreat.Severity}.");
            Console.WriteLine("Karar: Rota değiştir veya bekle komutu verilecek.");

            if (environmentalThreat.Severity == "high")
            {
                // Implement a more cautious action for high-severity threats.
                Console.WriteLine("Karar: Yüksek şiddetli tehlike. Acil durum manevrası başlatılıyor.");
                // Here, you would call a function to change the course
                // For example: _navSystem.ChangeCourse(newCourseHeading);
            }
            else
            {
                Console.WriteLine("Karar: Tehlike durumu izleniyor. Gerekirse rota değiştirilecek.");
            }
            Console.ResetColor();
            return;
        }

        // Step 3: Check Navigation Status (if no critical threats or energy issues)
        var deviationStatus = _navSystem.CheckRouteDeviation();
        if (deviationStatus.DeviationPercentage > 5.0)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("Karar: Rota sapması algılandı. Rota düzeltme komutu verilecek.");
            // Here, you would call a function to correct the course
            // For example: _navSystem.CorrectCourse();
            Console.ResetColor();
        }
        else
        {
            Console.WriteLine("Karar: Rota doğru. Seyir devam ediyor.");
        }

        Console.WriteLine("--- Karar Modülü Değerlendirme Tamamlandı ---");
    }
}