using System;
using System.Threading;

public class MotorControlModule
{
    // Motor sinyal aralıkları (örnek değerler, genellikle 1000-2000 arasıdır)
    private const int StopSignal = 1500;
    private const int MinSpeedSignal = 1200;
    private const int MaxSpeedSignal = 1800;

    private int _leftMotorSpeed;
    private int _rightMotorSpeed;

    public MotorControlModule()
    {
        _leftMotorSpeed = StopSignal;
        _rightMotorSpeed = StopSignal;
    }

    /// <summary>
    /// Karar modülünden gelen komutları işler ve motorlara komut gönderir.
    /// </summary>
    /// <param name="command">Karar modülünden gelen komut metni (örneğin: "CorrectCourse", "ChangeCourse")</param>
    /// <param name="deviationAngle">Eğer varsa, rota düzeltme için gereken sapma açısı (derece cinsinden)</param>
    public void SendMotorCommand(string command, double deviationAngle = 0)
    {
        Console.WriteLine($"\n--- Motor Kontrol Modülü Komut İşleniyor: {command} ---");
        
        switch (command)
        {
            case "ContinueSailing":
                // Normal seyir, iki motor da aynı hızda ileri
                _leftMotorSpeed = 1600;
                _rightMotorSpeed = 1600;
                Console.WriteLine("Komut: Seyir devam ediyor. Hız normal.");
                break;

            case "CorrectCourse":
                // Rota sapmasını düzeltmek için motor hızlarını ayarla
                if (deviationAngle > 0)
                {
                    // Sağa dön
                    _leftMotorSpeed = 1650;
                    _rightMotorSpeed = 1550;
                    Console.WriteLine($"Komut: Sola dönerek rotayı düzelt. Sapma: {deviationAngle}°");
                }
                else if (deviationAngle < 0)
                {
                    // Sola dön
                    _leftMotorSpeed = 1550;
                    _rightMotorSpeed = 1650;
                    Console.WriteLine($"Komut: Sağa dönerek rotayı düzelt. Sapma: {deviationAngle}°");
                }
                else
                {
                    // Sapma yoksa normal seyre dön
                    _leftMotorSpeed = 1600;
                    _rightMotorSpeed = 1600;
                    Console.WriteLine("Komut: Rota sapması yok. Normal seyre dönülüyor.");
                }
                break;

            case "ChangeCourse":
                // Tehlikeden kaçınmak için daha keskin bir manevra
                _leftMotorSpeed = 1750;
                _rightMotorSpeed = 1350; // Örnek olarak hızlı bir sola dönüş
                Console.WriteLine("Komut: Rota değiştiriliyor. Keskin sola dönüş yap.");
                break;

            case "EmergencyStop":
                // Acil durum duruşu
                _leftMotorSpeed = StopSignal;
                _rightMotorSpeed = StopSignal;
                Console.WriteLine("Komut: Acil durum duruşu. Motorlar durduruldu.");
                break;

            default:
                Console.WriteLine("Bilinmeyen komut geldi.");
                break;
        }

        // Simüle edilmiş motor komutlarını göster
        Console.WriteLine($"Motorlara Gönderilen Komut: Sol Motor = {_leftMotorSpeed}, Sağ Motor = {_rightMotorSpeed}");
        // Gerçek bir uygulamada bu sinyaller fiziksel bir donanıma (örneğin bir mikrokontrolcüye) gönderilirdi.
    }
}

// --- Simülasyon ---
class Program
{
    static void Main(string[] args)
    {
        MotorControlModule motorModule = new MotorControlModule();

        // Karar Modülünden gelen komutları simüle edelim
        motorModule.SendMotorCommand("ContinueSailing");
        Thread.Sleep(1000);

        // Rota sapması algılandığında
        motorModule.SendMotorCommand("CorrectCourse", 5.0);
        Thread.Sleep(1000);

        // Diğer yöne rota sapması
        motorModule.SendMotorCommand("CorrectCourse", -3.5);
        Thread.Sleep(1000);

        // Çevresel tehdit algılandığında
        motorModule.SendMotorCommand("ChangeCourse");
        Thread.Sleep(1000);

        // Acil durum komutu
        motorModule.SendMotorCommand("EmergencyStop");
    }
}