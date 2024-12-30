import os
import signal
import subprocess
import psutil
import time
import tkinter as tk
from tkinter import filedialog

# Konfigürasyon dosyası (metin dosyası yolunu saklamak için)
config_dosyasi = "config.txt"
if not os.path.exists(config_dosyasi):
    # Create the file if it doesn't exist
    with open(config_dosyasi, 'w') as file:
        pass


def dosya_secici(mesaj,filename,filetype):
    """Explorer kullanarak bir dosya seÃ§tirir."""
    root = tk.Tk()
    root.withdraw()  # Tkinter pencereyi gizler
    dosya_yolu = filedialog.askopenfilename(
        title=mesaj,
        filetypes=[(filename, filetype)]
    )
    return dosya_yolu


def program_kapat_ve_ac(v2rayexe, goodbydpiexe, dnsredirblacklist,secim,forall):
    """Belirtilen bir programı kapatıp yeniden başlatır."""
    program_bulundu1 = False
    program_bulundu2 = False
    kapatilacak_program_adi = os.path.basename(goodbydpiexe)
    kapatilacak_program_adi2 = os.path.basename(v2rayexe)


    # Çalışan işlemleri kontrol et
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if kapatilacak_program_adi.lower() in proc.info['name'].lower():
                print(f"{kapatilacak_program_adi} programı bulunuyor. PID: {proc.info['pid']}")
                os.kill(proc.info['pid'], signal.SIGTERM)  # Programı kapatır
                program_bulundu1 = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    if not program_bulundu1:
        print(f"{kapatilacak_program_adi} çalışmıyor, sadece açılıyor.")
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if kapatilacak_program_adi2.lower() in proc.info['name'].lower():
                print(f"{kapatilacak_program_adi2} programı bulunuyor. PID: {proc.info['pid']}")
                os.kill(proc.info['pid'], signal.SIGTERM)  # Programı kapatır
                program_bulundu2 = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not program_bulundu2:
        print(f"{kapatilacak_program_adi2} çalışmıyor, sadece açılıyor.")

    # Kapatma sonrası kısa bir bekleme
    time.sleep(2)

    # Programı yeniden açma (çift tırnak eklenmesi gerekebilir)
    print (secim)
    if secim=="1":
        try:
            print(f"{kapatilacak_program_adi} yeniden başlatılıyor...")
            subprocess.Popen(f'"{forall}"', shell=True)  # Çift tırnakla yolu ver
            print(f"GoodByeDpi başarıyla başlatıldı.")
        except Exception as e:
            print(f"GoodByeDpi yeniden başlatılamadı: {e}")
    elif secim=="2":
        try:
            print(f"{kapatilacak_program_adi} yeniden başlatılıyor...")
            subprocess.Popen(f'"{dnsredirblacklist}"', shell=True)  # Çift tırnakla yolu ver
            print(f"GoodByeDpi başarıyla başlatıldı.")
        except Exception as e:
            print(f"GoodByeDpi yeniden başlatılamadı: {e}")   
            
    try:
        print(f"{kapatilacak_program_adi2} yeniden başlatılıyor...")
        subprocess.run(['cmd', '/c', f'{v2rayexe} run'])
        print(f"V2Ray başarıyla başlatıldı.")
    except Exception as e:
        print(f"V2Ray yeniden başlatılamadı: {e}")


def ilk_ayar(v2rayexe, goodbydpiexe, dnsredirblacklist,forall,blacklisttxt):
    """İlk çalıştırmada kullanıcıdan program bilgilerini alır."""
    if blacklisttxt==None:
        print("blacklist.txt dosyasını seçin. Eger yoksa olusturun.")
        blacklisttxt = dosya_secici("Blacklist.exe dosyasını seçin. Eger yoksa olusturun.","blacklist.txt","*.txt")
        if not blacklisttxt:
            print("Herhangi bir dosya seçilmedi. Program sonlandırılıyor.")
            exit()
    if forall==None:
        print("forall.cmd dosyasını seçin.")
        forall = dosya_secici("forall.cmd dosyasını seçin.","forall.cmd","*.cmd")
        if not forall:
            print("Herhangi bir dosya seçilmedi. Program sonlandırılıyor.")
            exit()
    if dnsredirblacklist==None:    
        print("Dnsredir.cmd dosyasını seçin.")
        dnsredirblacklist = dosya_secici("Dnsredir.cmd dosyasını seçin.","dnsredir Dosyasi","*.cmd")
        if not dnsredirblacklist:
            print("Herhangi bir dosya seçilmedi. Program sonlandırılıyor.")
            exit()
    if v2rayexe==None:    
        print("v2ray.exe dosyasını seçin.")
        v2rayexe = dosya_secici("v2ray.exe dosyasını seçin.","v2ray.exe","*.exe")
        if not v2rayexe:
            print("Herhangi bir dosya seçilmedi. Program sonlandırılıyor.")
            exit()
    if goodbydpiexe==None:
        print("goodbyedpi.exe dosyasını seçin.")
        goodbydpiexe = dosya_secici("GoodByeDpi.exe dosyasını seçin.","x64 Goodbyedpi.exe","*.exe")
        if not goodbydpiexe:
            print("Herhangi bir dosya seçilmedi. Program sonlandırılıyor.")
            exit()

        
    return blacklisttxt,forall, v2rayexe, goodbydpiexe, dnsredirblacklist
    
    
def config_dosyasini_yukle(config_dosyasi):
    if os.path.exists(config_dosyasi):
        with open(config_dosyasi, 'r', encoding='utf-8') as config:
            lines = []
            for i, line in enumerate(config):
                if i >= 5:  # Sadece ilk 5 satırı işle
                    break
                line = line.strip()  # Satırdaki gereksiz boşlukları temizle
                lines.append(line if line else None)  # Satır boşsa None ekle

            # İlk 5 değeri döndür, eksik olanları None ile doldur
            while len(lines) < 5:
                lines.append(None)
            return tuple(lines)  # 5 değer olarak döndür
    else:
        raise FileNotFoundError(f"{config_dosyasi} dosyası bulunamadı!")

    
    
def config_dosyasini_kaydet(config_dosyasi, blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist, forall):
    with open(config_dosyasi, 'w+', encoding='utf-8') as config:
        satirlar = config.readlines()
        # Eğer dosya 4 satırdan azsa, dosyaya yeni satırlar ekler
        while len(satirlar) < 5:
            satirlar.append("\n")
            
        # 2. 3. ve 4.satırları güncelle
        satirlar[0] = f"{blacklisttxt}\n"
        satirlar[1] = f"{forall}\n"
        satirlar[2] = f"{v2rayexe}\n"
        satirlar[3] = f"{goodbydpiexe}\n"
        satirlar[4] = f"{dnsredirblacklist}\n"
        

        config.seek(0)  # Başlangıç noktasına git
        config.writelines(satirlar)

def metin_ekle(dosya_yolu):
    """Metin dosyasına yazı ekleyen fonksiyon."""
    print(f"Siteler {dosya_yolu} dosyasına kaydedilecektir.")
    while True:
        yazi = input("Site ismini girin (Ör:facebook.com) (çıkmak için 'q' yazın): ")
        if yazi.lower() == 'q':
            secim=input("Forall: 1 \nBlacklist: 2\n---> ") 
            break

        with open(dosya_yolu, 'a', encoding='utf-8') as dosya:
            # Son noktaya kadar olan kısmı al
            last_dot_index = yazi.rfind(".")
            if last_dot_index != -1:
                # Nokta dahil kısmı al
                extracted_yazi = yazi[last_dot_index:]
                # Orijinal metinden bu kısmı sil
                modified_yazi = yazi[:last_dot_index]
            else:
                raise SystemExit("Lutfen dogru bir site adi girin!")

            # Yeni metni ekle
            new_text = "-cdn"
            new_text2 = "-media"
            new_yazi1=modified_yazi + new_text + extracted_yazi
            new_yazi2=modified_yazi + new_text2 + extracted_yazi
            dosya.write(f"\n{yazi}")
            dosya.write(f"\nwww.{yazi}")
            dosya.write(f"\ni.{yazi}")
            dosya.write(f"\ni1.{yazi}")
            dosya.write(f"\ni2.{yazi}")
            dosya.write(f"\ni3.{yazi}")
            dosya.write(f"\ni4.{yazi}")
            dosya.write(f"\ni5.{yazi}")            
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
    return(secim)

if __name__ == "__main__":
    blacklisttxt,forall, v2rayexe, goodbydpiexe, dnsredirblacklist = config_dosyasini_yukle(config_dosyasi)
    # Eğer konfigürasyon dosyası yoksa, kullanıcıdan bilgi al ve kaydet
    if not goodbydpiexe or not dnsredirblacklist or not v2rayexe or not blacklisttxt or not forall:
        blacklisttxt,forall, v2rayexe, goodbydpiexe, dnsredirblacklist = ilk_ayar(v2rayexe, goodbydpiexe, dnsredirblacklist,forall,blacklisttxt)
        config_dosyasini_kaydet(config_dosyasi, blacklisttxt,forall, v2rayexe, goodbydpiexe, dnsredirblacklist)
    secim=metin_ekle(blacklisttxt)
    program_kapat_ve_ac(v2rayexe, goodbydpiexe, dnsredirblacklist,secim,forall)