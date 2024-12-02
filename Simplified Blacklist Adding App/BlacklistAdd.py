import os
import signal
import subprocess
import psutil
import time
import tkinter as tk
from tkinter import filedialog

# Configuration file (to store the path of the text file)
config_file = "config.txt"

def file_selector(message, filename, filetype):
    """Allows the user to select a file using Explorer."""
    root = tk.Tk()
    root.withdraw()  # Hides the Tkinter window
    file_path = filedialog.askopenfilename(
        title=message,
        filetypes=[(filename, filetype)]
    )
    return file_path

def close_and_restart_program(v2rayexe, goodbydpiexe, dnsredirblacklist):
    """Closes and restarts the specified program."""
    program_found = False
    program_name_to_close = os.path.basename(goodbydpiexe)
    program_name_to_close2 = os.path.basename(v2rayexe)

    # Check running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if program_name_to_close.lower() in proc.info['name'].lower():
                print(f"{program_name_to_close} program is running. PID: {proc.info['pid']}")
                os.kill(proc.info['pid'], signal.SIGTERM)  # Closes the program
                program_found = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not program_found:
        print(f"{program_name_to_close} is not running, it will only be started.")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if program_name_to_close2.lower() in proc.info['name'].lower():
                print(f"{program_name_to_close2} program is running. PID: {proc.info['pid']}")
                os.kill(proc.info['pid'], signal.SIGTERM)  # Closes the program
                program_found = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not program_found:
        print(f"{program_name_to_close2} is not running, it will only be started.")

    # Short wait after closing
    time.sleep(2)

    # Restart the program (double quotes may be needed)
    try:
        print(f"Restarting {program_name_to_close}...")
        subprocess.Popen(f'"{dnsredirblacklist}"', shell=True)  # Provide the path with double quotes
        print(f"GoodByeDpi started successfully.")
    except Exception as e:
        print(f"Failed to restart GoodByeDpi: {e}")
    try:
        print(f"Restarting {program_name_to_close2}...")
        subprocess.Popen(f'"{v2rayexe}"', shell=True)  # Provide the path with double quotes
        print(f"V2Ray started successfully.")
    except Exception as e:
        print(f"Failed to restart V2Ray: {e}")

def initial_setup():
    """Takes program information from the user during the first run."""
    print("Select the blacklist.txt file. If it doesn't exist, create one.")
    blacklisttxt = file_selector("Select the Blacklist.exe file. If it doesn't exist, create one.", "blacklist.txt", "*.txt")
    if not blacklisttxt:
        print("No file selected. Terminating the program.")
        exit()

    print("Select the Dnsredir.cmd file.")
    dnsredirblacklist = file_selector("Select the Dnsredir.cmd file.", "dnsredir File", "*.cmd")
    if not dnsredirblacklist:
        print("No file selected. Terminating the program.")
        exit()

    print("Select the v2ray.exe file.")
    v2rayexe = file_selector("Select the v2ray.exe file.", "v2ray.exe", "*.exe")
    if not v2rayexe:
        print("No file selected. Terminating the program.")
        exit()

    print("Select the goodbyedpi.exe file.")
    goodbydpiexe = file_selector("Select the GoodByeDpi.exe file.", "x64 Goodbyedpi.exe", "*.exe")
    if not goodbydpiexe:
        print("No file selected. Terminating the program.")
        exit()

    return blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist

def load_config_file(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as config:
            lines = config.readlines()
            if len(lines) >= 4:
                # Return the values from the 1st, 2nd, 3rd, and 4th lines
                return lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[3].strip()
    return None, None, None, None

def save_config_file(config_file, blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist):
    with open(config_file, 'w+', encoding='utf-8') as config:
        lines = config.readlines()
        # If the file has fewer than 4 lines, add new lines
        while len(lines) < 4:
            lines.append("\n")

        # Update the 2nd, 3rd, and 4th lines
        lines[0] = f"{blacklisttxt}\n"
        lines[1] = f"{v2rayexe}\n"
        lines[2] = f"{goodbydpiexe}\n"
        lines[3] = f"{dnsredirblacklist}\n"

        config.seek(0)  # Move to the start of the file
        config.writelines(lines)

def add_text(file_path):
    """Function to add text to a text file."""
    print(f"Sites will be saved to the {file_path} file.")
    while True:
        text = input("Enter the site name (e.g., facebook.com) (type 'q' to quit): ")
        if text.lower() == 'q':
            break

        with open(file_path, 'a', encoding='utf-8') as file:
            # Get the part up to the last dot
            last_dot_index = text.rfind(".")
            if last_dot_index != -1:
                # Get the part including the dot
                extracted_text = text[last_dot_index:]
                # Remove this part from the original text
                modified_text = text[:last_dot_index]
            else:
                raise SystemExit("Please enter a valid site name!")

            # Add new text
            new_text = "-cdn"
            new_text2 = "-media"
            new_text1 = modified_text + new_text + extracted_text
            new_text2 = modified_text + new_text2 + extracted_text
            file.write(f"\n{text}")
            file.write(f"\nwww.{text}")
            file.write(f"\ni.{text}")
            file.write(f"\ni1.{text}")
            file.write(f"\ni2.{text}")
            file.write(f"\ni3.{text}")
            file.write(f"\ni4.{text}")
            file.write(f"\ni5.{text}")            
            file.write(f"\nt.{text}")
            file.write(f"\nt1.{text}")
            file.write(f"\nt2.{text}")
            file.write(f"\nt3.{text}")
            file.write(f"\nt4.{text}")
            file.write(f"\nt5.{text}")
            file.write(f"\ncdn.{text}")
            file.write(f"\nmedia.{text}")
            file.write(f"\nstatic.{text}")
            file.write(f"\nfiles.{text}")
            file.write(f"\napi.{text}")
            file.write(f"\nupload.{text}")
            file.write(f"\ndumps.{text}")
            file.write(f"\ncommons.{text}")
            file.write(f"\nstats.{text}")
            file.write(f"\nmeta.{text}")
            file.write(f"\n{new_text1}")
            file.write(f"\n{new_text2}")
            file.write(f"\nupload.{text}")
            file.write(f"\ndumps.{text}")
            file.write(f"\ncommons.{text}")
            file.write(f"\nstats.{text}")
            file.write(f"\nmeta.{text}")
            file.write(f"\n{new_text1}")
            file.write(f"\n{new_text2}")
            file.write(f"\n*.{text}")

        print(f"'{text}' added successfully.")



if __name__ == "__main__":
    blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist = load_config_file(config_file)
    # If the configration file doesn't exist, get information from user and save it
    if not goodbydpiexe or not dnsredirblacklist or not v2rayexe or not blacklisttxt:
        blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist = initial_setup()
        save_config_file(config_dosyasi, blacklisttxt, v2rayexe, goodbydpiexe, dnsredirblacklist)
    add_text(blacklisttxt)
    close_and_restart_program(v2rayexe, goodbydpiexe, dnsredirblacklist)