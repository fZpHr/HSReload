import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import time
import numpy as np
import cv2
import pyautogui
import webbrowser
import pygame
import os


class AutoFirewallControl:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("HSReload - Auto Firewall Control")
        self.root.geometry("365x60")
        self.root.iconphoto(False, tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icon.png')))
        self.root.attributes('-alpha', 0.9, '-topmost', True)
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        self.is_running = False
        self.is_monitoring = False
        self.is_semi_auto_running = False
        self.rule_name = "hsreload"
        self.templates = []
        self.file_path = file_path
        self.threshold = 0.8
        self.next_template_to_find = 0
        self.keep_rule = tk.BooleanVar(value=True)

        pygame.mixer.init()
        
        self.frame = tk.Frame(self.root, bg='#2b2b2b')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.full_auto_button = tk.Button(
            self.frame, text="Full Auto", command=self.toggle_monitoring,
            bg='#4CAF50', fg='white', font=('Segoe UI', 10, 'bold'), width=8
        )
        self.full_auto_button.grid(row=0, column=0, pady=7, padx=7)
        
        self.semi_auto_button = tk.Button(
            self.frame, text="Semi Auto", command=self.activate_once,
            bg='#FFB300', fg='white', font=('Segoe UI', 10, 'bold'), width=8
        )
        self.semi_auto_button.grid(row=0, column=1, pady=7, padx=7)
        
        self.manual_button = tk.Button(
            self.frame, text="Manuel", command=self.toggle_firewall_manual,
            bg='#2196F3', fg='white', font=('Segoe UI', 10, 'bold'), width=8
        )
        self.manual_button.grid(row=0, column=2, pady=7, padx=7)

        self.settings_button = tk.Menubutton(
            self.frame, text="Settings", bg='#FF5722', fg='white', font=('Segoe UI', 10, 'bold'), width=8, relief=tk.RAISED
        )

        self.settings_button.grid(row=0, column=3, pady=7, padx=7)
        self.settings_menu = tk.Menu(self.settings_button, tearoff=0)
        self.settings_button.config(menu=self.settings_menu)
        
        self.settings_menu.add_checkbutton(label="Logs", command=self.toggle_logs)
        self.settings_menu.add_checkbutton(label="Save rule", variable=self.keep_rule)
        self.settings_menu.add_checkbutton(label="Music", command=self.toggle_music)
        self.settings_menu.add_command(label="by fZpHr", command=lambda: webbrowser.open_new("https://github.com/fZpHr"))

        self.log_frame = tk.Frame(self.frame, bg='#2b2b2b')
        self.log_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="n")
        self.log_frame.grid_remove()

        self.log_text = tk.Text(self.log_frame, bg='#2b2b2b', fg='white', font=('Segoe UI', 10), width=45, height=7)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_on_exit)

        self.frame.bind('<B1-Motion>', self.move_window)

    def log(self, message):
        """Affiche un message dans le widget Text des logs."""
        print(message)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    def toggle_logs(self):
        """Affiche ou masque la section des logs et ajuste la taille de la fenêtre."""
        if self.log_frame.winfo_ismapped():
            self.log_frame.grid_remove()
            self.root.geometry("365x60")
        else:
            self.log_frame.grid()
            self.root.geometry("365x200")
        
    def toggle_music(self):
        """Joue ou arrête la musique."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.log("Musique arrêtée.")
        else:
            music_file = os.path.join(os.path.dirname(__file__), "music.mp3")
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)
                self.log(f"Lecture de la musique: {music_file}")
            else:
                self.log(f"Erreur: Le fichier {music_file} n'existe pas.")


    def create_rule(self):
        """Crée une règle de pare-feu."""
        try:
            print(self.file_path)
            self.log(f"fichier: {self.file_path}")
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={self.rule_name}', 'dir=out', 'action=block', 'enable=no',
                f'program="{self.file_path.replace("/", "\\")}"'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Règle créée avec succès.")
        except subprocess.CalledProcessError as e:
            self.log(f"Erreur lors de la création de la règle: {e}")

    def delete_rule(self):
        """Supprime la règle de pare-feu."""
        try:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name={self.rule_name}'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("Règle supprimée avec succès.")
        except subprocess.CalledProcessError:
            self.log("Erreur lors de la suppression de la règle.")

    def cleanup_on_exit(self):
        """Supprime la règle avant de quitter, sauf si l'option de garder la règle est activée."""
        self.log("Nettoyage avant la sortie...")
        if not self.keep_rule.get():
            if rule_exists():
                self.log("Suppression de la règle...")
                self.delete_rule()
        else:
            self.log("La règle est conservée.")
        self.root.destroy()

    def load_templates(self, template_paths):
        """Charge plusieurs images de référence."""
        try:
            for path in template_paths:
                template = cv2.imread(path)
                if template is None:
                    self.log(f"Erreur: Impossible de charger l'image {path}")
                    continue
                self.templates.append(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY))
            return len(self.templates) > 0
        except Exception as e:
            self.log(f"Erreur lors du chargement des templates: {e}")
            return False

    def find_image_on_screen(self, template_index):
        """Cherche une image spécifique sur l'écran."""
        try:
            screen = np.array(pyautogui.screenshot())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            
            if not self.templates:
                return False
            
            current_template = self.templates[template_index]
            result = cv2.matchTemplate(screen_gray, current_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            self.log(f"Confiance de détection (template {template_index + 1}): {max_val:.2f}")
            return max_val >= self.threshold
        except Exception as e:
            self.log(f"Erreur lors de la détection: {e}")
            return False

    def monitor_screen(self):
        """Surveille l'écran pour la détection (Full Auto)."""
        while self.is_monitoring:
            if self.find_image_on_screen(self.next_template_to_find):
                self.log(f"Template {self.next_template_to_find + 1} détecté !")
                if self.next_template_to_find == 0:
                    self.log("Activation du firewall... (Full Auto)")
                    self.activate_firewall()
                    self.next_template_to_find = 1
                elif self.next_template_to_find == 1:
                    self.log("Cycle terminé, attente de l'image 1.")
                    self.next_template_to_find = 0
            time.sleep(0.1)

    def semi_auto_cycle(self):
        """Cycle unique pour le mode Semi Auto."""
        self.log("Mode Semi Auto activé, attente de l'image 1...")
        while self.is_semi_auto_running:
            if self.find_image_on_screen(0):
                self.log("Image 1 détectée ! Activation unique...")
                self.activate_firewall()
                self.is_semi_auto_running = False
                self.semi_auto_button.config(bg='#FFC107')
                break
            time.sleep(0.1)
        if not self.is_semi_auto_running:
            self.semi_auto_button.config(bg='#FFC107')

    def activate_once(self):
        """Lance un cycle Semi Auto unique ou l'arrête si déjà actif."""
        if self.is_semi_auto_running:
            self.log("Arrêt du mode Semi Auto...")
            self.is_semi_auto_running = False
            self.semi_auto_button.config(bg='#FFC107')
            return

        self.log("Activation unique en cours (Semi Auto)...")
        self.is_semi_auto_running = True
        threading.Thread(target=self.semi_auto_cycle, daemon=True).start()

    def toggle_monitoring(self):
        """Active/désactive la surveillance (Full Auto)."""
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.log("Surveillance activée... (Full Auto)")
            self.full_auto_button.config(bg='#FF4444')
            threading.Thread(target=self.monitor_screen, daemon=True).start()
        else:
            self.log("Surveillance désactivée (Full Auto)")
            self.full_auto_button.config(bg='#4CAF50')

    def toggle_firewall_manual(self):
        """Active/Désactive manuellement la règle."""
        if self.is_running:
            self.log("Désactivation manuelle...")
            self.disable_rule()
            self.manual_button.config(bg='#2196F3')
        else:
            self.log("Activation manuelle...")
            self.enable_rule()
            self.manual_button.config(bg='#F44336')
        self.is_running = not self.is_running

    def enable_rule(self):
        try:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'set', 'rule',
                f'name="{self.rule_name}"', 'new', 'enable=yes'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except subprocess.CalledProcessError:
            return False

    def disable_rule(self):
        try:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'set', 'rule',
                f'name="{self.rule_name}"', 'new', 'enable=no'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except subprocess.CalledProcessError:
            return False

    def activate_firewall(self):
        if self.is_running:
            return

        self.is_running = True
        self.log("Activation du firewall...")
        
        def rule_timer():
            self.enable_rule()
            time.sleep(2.3)
            self.disable_rule()
            self.is_running = False
        
        threading.Thread(target=rule_timer, daemon=True).start()

    def move_window(self, event):
        x = self.root.winfo_pointerx() - 150
        y = self.root.winfo_pointery() - 50
        self.root.geometry(f'+{x}+{y}')


def rule_exists():
    """Vérifie si la règle de pare-feu existe."""
    try:
        output = subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'show', 'rule',
            'name="hsreload"'
        ], capture_output=True, text=True, check=True).stdout
        return "Nom" in output
    except subprocess.CalledProcessError:
        return False


def main():
    root = tk.Tk()
    root.withdraw()
    file_path = ""
    
    app = AutoFirewallControl(root, file_path)

    if rule_exists():
        app.log("La règle existe déjà, démarrage de l'application...")
        pass
    else:
        file_path = filedialog.askopenfilename(
            title="Sélectionnez le fichier",
            filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        
        if not file_path:
            print("Aucun fichier sélectionné. Fermeture de l'application.")
            return
        
        if not file_path.lower().endswith('.exe'):
            print("Le fichier sélectionné n'est pas un exécutable valide.")
            return
        app.file_path = file_path
        app.create_rule()

    root.deiconify()
    if not app.load_templates([os.path.join(os.path.dirname(__file__), 'combat.png'), os.path.join(os.path.dirname(__file__),'tavern.png')]):
        app.log("ERREUR: Impossible de charger les images templates!")
    else:
        app.log("Images templates chargées avec succès!")
    
    root.mainloop()


if __name__ == "__main__":
    main()