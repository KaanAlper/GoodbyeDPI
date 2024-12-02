import os
import signal
import subprocess
import psutil
import time
import tkinter as tk
from tkinter import filedialog

# Konfigürasyon dosyası (metin dosyası yolunu saklamak için)
config_dosyasi = "config.txt"

def program_kapat_ve_ac(kapatilacak_program_yolu, acilacak_program_yolu):
    """Belirtilen bir programı kapatıp yeniden başlatır."""
    program_bulundu = False
    kapatilacak_program_adi = os.path.basename(kapatilacak_program_yolu)

    # Çalışan işlemleri kontrol et
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if kapatilacak_program_adi.lower() in proc.info['name'].lower():
                print(f"{kapatilacak_program_adi} programı bulunuyor. PID: {proc.info['pid']}")
                os.kill(proc.info['pid'], signal.SIGTERM)  # Programı kapatır
                program_bulundu = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not program_bulundu:
        print(f"{kapatilacak_program_adi} çalışmıyor, sadece açılıyor.")

    # Kapatma sonrası kısa bir bekleme
    time.sleep(2)

    # Programı yeniden açma (çift tırnak eklenmesi gerekebilir)
    try:
        print(f"{kapatilacak_program_adi} yeniden başlatılıyor...")
        subprocess.Popen(f'"{acilacak_program_yolu}"', shell=True)  # Çift tırnakla yolu ver
        print(f"{acilacak_program_yolu} başarıyla başlatıldı.")
    except Exception as e:
        print(f"{acilacak_program_yolu} yeniden başlatılamadı: {e}")

def config_dosyasini_yukle(config_dosyasi):
    """Konfigürasyon dosyasını yükler (2. ve 3. satırdan)."""
    if os.path.exists(config_dosyasi):
        with open(config_dosyasi, 'r', encoding='utf-8') as config:
            satirlar = config.readlines()
            if len(satirlar) >= 3:
                # 2. ve 3. satırdaki değerleri döndür
                return satirlar[1].strip(), satirlar[2].strip()
    return None, None

def config_dosyasini_kaydet(config_dosyasi, kapatilacak_program_yolu, acilacak_program_yolu):
    """Konfigürasyon dosyasına bilgileri kaydeder (2. ve 3. satır)."""
    with open(config_dosyasi, 'r+', encoding='utf-8') as config:
        satirlar = config.readlines()

        # Eğer dosya 2 satırdan azsa, dosyaya yeni satırlar ekleriz
        while len(satirlar) < 3:
            satirlar.append("\n")

        # 2. ve 3. satırları güncelle
        satirlar[1] = f"{kapatilacak_program_yolu}\n"
        satirlar[2] = f"{acilacak_program_yolu}\n"

        # Dosyayı tekrar yaz
        config.seek(0)  # Başlangıç noktasına git
        config.writelines(satirlar)

def dosya_secici(mesaj,filename,filetype):
    """Explorer kullanarak bir dosya seçtirir."""
    root = tk.Tk()
    root.withdraw() 
    dosya_yolu = filedialog.askopenfilename(
        title=mesaj,
        filetypes=[(filename, filetype)]
    )
    return dosya_yolu

def ilk_ayar():
    """İlk çalıştırmada kullanıcıdan program bilgilerini alır."""
    print("Select Dnsredir-blacklist.cmd file")
    acilacak_program_yolu = dosya_secici("select Dnsredir-blacklist.cmd file.","dnsredir Dosyasi","*.cmd")
    if not acilacak_program_yolu:
        print("Can not selected. Program will exited")
        time.sleep(2)
        exit()
    print("select goodbyedpi.exe file in x64 folder .")
    kapatilacak_program_yolu = dosya_secici("select GoodByeDpi.exe. file","x64 Goodbyedpi.exe","*.exe")
    if not kapatilacak_program_yolu:
        print("Can not selected. Program will exited")
        time.sleep(2)
        exit()


    return kapatilacak_program_yolu, acilacak_program_yolu


def dosya_yolu_sec():
    """Kullanıcıdan bir dosya seçmesini isteyen fonksiyon."""
    root = tk.Tk()
    root.withdraw() 
    dosya_yolu = filedialog.askopenfilename(
        title="select Blacklist.txt file. if doesnt exist create new one or get help from program's creator",
        filetypes=[("blacklist.txt", "*.txt")]
    )
    return dosya_yolu

def config_dosyasini_yukle_blacklist():
    """Konfigürasyon dosyasından metin dosyası yolunu yükler."""
    if os.path.exists(config_dosyasi):      
        with open(config_dosyasi, 'r', encoding='utf-8') as config:
            satirlar = config.readlines()
            return satirlar[0].strip()
    return None

def config_dosyasini_kaydet_blacklist(dosya_yolu):
    """Metin dosyası yolunu konfigürasyon dosyasına kaydeder."""
    with open(config_dosyasi, 'w', encoding='utf-8') as config:
        config.write(dosya_yolu+"\n")

def metin_ekle(dosya_yolu):
    """Metin dosyasına yazı ekleyen fonksiyon."""
    print(f"Domains will saved on file which is located at {dosya_yolu}")
    while True:
        print("Enter site name (Exp:facebook.com)(dont write www or any pre points)")
        yazi = input("(For restart app please enter 'r'): ")
        if yazi.lower() == 'r':
            break

        with open(dosya_yolu, 'a', encoding='utf-8') as dosya:     
            last_dot_index = yazi.rfind(".")
            if last_dot_index != -1:
                extracted_yazi = yazi[last_dot_index:]
                modified_yazi = yazi[:last_dot_index]
            else:
                raise SystemExit("Please enter a true site name")

            # I made it for all domains, because i found just using "*.sitename.com" or "sitename.com" is make it slower to loading times of sites
            new_text = "-cdn"
            new_text2 = "-media"
            new_yazi1=modified_yazi + new_text + extracted_yazi
            new_yazi2=modified_yazi + new_text2 + extracted_yazi
            dosya.write(f"\n{yazi}")
            dosya.write(f"\nwww.{yazi}")
            dosya.write(f"\ni.{yazi}")
            dosya.write(f"\nt.{yazi}")
            dosya.write(f"\nt1.{yazi}")
            dosya.write(f"\nt2.{yazi}")
            dosya.write(f"\nt3.{yazi}")
            dosya.write(f"\nt4.{yazi}")
            dosya.write(f"\nt5.{yazi}")
            dosya.write(f"\ncdn.{yazi}")
            dosya.write(f"\nmedia.{yazi}")
            dosya.write(f"\nstatic.{yazi}")
            dosya.write(f"\nfiles.{yazi}")
            dosya.write(f"\napi.{yazi}")
            dosya.write(f"\nupload.{yazi}")
            dosya.write(f"\ndumps.{yazi}")
            dosya.write(f"\ncommons.{yazi}")
            dosya.write(f"\nstats.{yazi}")
            dosya.write(f"\nmeta.{yazi}")
            dosya.write(f"\n{new_yazi1}")
            dosya.write(f"\n{new_yazi2}")
            dosya.write(f"\n*.{yazi}")

        print(f"'{yazi}' sitesi başarıyla dosyaya eklendi.")



if __name__ == "__main__":
    dosya_yolu = config_dosyasini_yukle_blacklist()
    if not dosya_yolu:
        print("select Blacklist.txt file")
        dosya_yolu = dosya_yolu_sec()
        if dosya_yolu:
            config_dosyasini_kaydet_blacklist(dosya_yolu)
        else:
            print("Can not selected. Program will exited")
            exit()
    kapatilacak_program_yolu, acilacak_program_yolu = config_dosyasini_yukle(config_dosyasi)
    if not kapatilacak_program_yolu or not acilacak_program_yolu:
        kapatilacak_program_yolu, acilacak_program_yolu = ilk_ayar()
        config_dosyasini_kaydet(config_dosyasi, kapatilacak_program_yolu, acilacak_program_yolu)
    metin_ekle(dosya_yolu)
    program_kapat_ve_ac(kapatilacak_program_yolu, acilacak_program_yolu)
