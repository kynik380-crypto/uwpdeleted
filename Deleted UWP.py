import math
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext


class ModernButton:
  """Custom modern rounded button with hover effect"""

  def __init__(
      self,
      canvas,
      x,
      y,
      width,
      height,
      radius,
      text,
      command,
      bg_color="#ff4757",
      hover_color="#ff6b81",
  ):
    self.canvas = canvas
    self.command = command
    self.bg_color = bg_color
    self.hover_color = hover_color
    self.state = "normal"

    self.rect = self._create_round_rect(
        x, y, x + width, y + height, radius, fill=bg_color, outline=""
    )
    self.text_id = canvas.create_text(
        x + width / 2,
        y + height / 2,
        text=text,
        fill="white",
        font=("Segoe UI", 11, "bold"),
    )

    for item in (self.rect, self.text_id):
      canvas.tag_bind(item, "<Enter>", self.on_enter)
      canvas.tag_bind(item, "<Leave>", self.on_leave)
      canvas.tag_bind(item, "<Button-1>", self.on_click)

  def _create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius,
        y1,
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    return self.canvas.create_polygon(points, **kwargs, smooth=True)

  def on_enter(self, event):
    if self.state == "normal":
      self.canvas.itemconfig(self.rect, fill=self.hover_color)

  def on_leave(self, event):
    if self.state == "normal":
      self.canvas.itemconfig(self.rect, fill=self.bg_color)

  def on_click(self, event):
    if self.state == "normal" and self.command:
      self.command()

  def config(self, state):
    self.state = state
    if state == "disabled":
      self.canvas.itemconfig(self.rect, fill="#4a4a55")
    else:
      self.canvas.itemconfig(self.rect, fill=self.bg_color)


class UWPCleanerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Windows UWP App Cleaner — Modern Edition")
    self.root.geometry("720x540")
    self.root.minsize(600, 450)

    self.angle = 0.0

    # Canvas for background gradient animation
    self.canvas = tk.Canvas(root, highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True)

    self.animate_background()
    self.create_ui_card()

  def animate_background(self):
    """Smooth animated glowing background gradient"""
    self.angle += 0.02
    self.canvas.delete("bg_grad")

    width = self.root.winfo_width()
    height = self.root.winfo_height()
    if width < 10:
      width = 720
    if height < 10:
      height = 540

    steps = 25
    step_h = height / steps
    for i in range(steps):
      f1 = (math.sin(self.angle + i * 0.15) + 1) / 2
      f2 = (math.cos(self.angle * 0.7 + i * 0.1) + 1) / 2

      r = int(12 + f1 * 25)
      g = int(8 + f2 * 20)
      b = int(35 + f1 * 45 + f2 * 25)
      color = f"#{r:02x}{g:02x}{b:02x}"

      self.canvas.create_rectangle(
          0,
          i * step_h,
          width,
          (i + 1) * step_h + 2,
          fill=color,
          outline="",
          tags="bg_grad",
      )

    self.canvas.tag_lower("bg_grad")
    self.root.after(50, self.animate_background)

  def create_ui_card(self):
    # Central card container
    self.card = tk.Frame(
        self.root, bg="#16161e", bd=0, highlightthickness=0
    )
    self.card_window = self.canvas.create_window(
        360, 270, window=self.card, width=660, height=480
    )

    self.root.bind("<Configure>", self.on_resize)

    # Title
    title_label = tk.Label(
        self.card,
        text="Windows UWP Debloater",
        font=("Segoe UI", 16, "bold"),
        bg="#16161e",
        fg="#ffffff",
    )
    title_label.pack(pady=(20, 5))

    # Description
    desc_text = (
        "Click the button below to purge pre-installed UWP bloatware.\n(Essential"
        " apps like Microsoft Store, Calculator, Notepad & Paint will be"
        " kept)."
    )
    desc_label = tk.Label(
        self.card,
        text=desc_text,
        font=("Segoe UI", 10),
        bg="#16161e",
        fg="#9ba1a6",
        justify="center",
    )
    desc_label.pack(pady=(0, 15))

    # Rounded Button Canvas
    self.btn_canvas = tk.Canvas(
        self.card,
        width=260,
        height=45,
        bg="#16161e",
        highlightthickness=0,
        cursor="hand2",
    )
    self.btn_canvas.pack(pady=5)

    self.clean_btn = ModernButton(
        self.btn_canvas,
        x=0,
        y=0,
        width=260,
        height=45,
        radius=22,
        text="Remove All UWP Bloatware",
        command=self.start_cleaning_thread,
        bg_color="#ff4757",
        hover_color="#ff6b81",
    )

    # Output Terminal / Log
    self.log_area = scrolledtext.ScrolledText(
        self.card,
        wrap=tk.WORD,
        font=("Consolas", 9),
        bg="#0f0f13",
        fg="#00ff88",
        insertbackground="white",
        bd=0,
        highlightthickness=0,
    )
    self.log_area.pack(expand=True, fill="both", padx=25, pady=15)
    self.log_area.insert(
        tk.END,
        "[i] Ready. Make sure to run this script as Administrator for full"
        " privileges.\n",
    )

  def on_resize(self, event):
    if event.widget == self.root:
      w = event.width
      h = event.height
      if w > 100 and h > 100:
        self.canvas.coords(self.card_window, w / 2, h / 2)

  def log(self, message):
    self.log_area.insert(tk.END, message + "\n")
    self.log_area.see(tk.END)

  def start_cleaning_thread(self):
    if messagebox.askyesno(
        "Confirmation",
        (
            "Are you sure you want to remove pre-installed UWP bloatware apps?"
            " This action cannot be easily undone."
        ),
    ):
      self.clean_btn.config("disabled")
      threading.Thread(target=self.run_powershell_script, daemon=True).start()

  def run_powershell_script(self):
    self.log("\n[+] Starting UWP bloatware removal process...")

    # Expanded list of target packages to remove
    ps_script = """
        $BloatwarePatterns = @(
            "*3DViewer*", "*BingNews*", "*BingWeather*", "*Clipchamp*", "*Cortana*", 
            "*GetHelp*", "*Getstarted*", "*Messaging*", "*MicrosoftOfficeHub*", 
            "*MicrosoftSolitaireCollection*", "*MicrosoftStickyNotes*", "*MixedReality.Portal*", 
            "*MSTeams*", "*Office.OneNote*", "*People*", "*PhoneLink*", "*Photos*", 
            "*PowerAutomateDesktop*", "*SkypeApp*", "*SoundRecorder*", "*Sway*", 
            "*Todos*", "*Xbox*", "*YourPhone*", "*ZuneMusic*", "*ZuneVideo*", 
            "*FeedbackHub*", "*Maps*", "*Wallet*", "*BingSearch*", "*OneDrive*"
        )

        # 1. Remove targeted UWP bloatware packages for current users
        foreach ($Pattern in $BloatwarePatterns) {
            $Packages = Get-AppxPackage -AllUsers | Where-Object { 
                $_.Name -like $Pattern -and 
                $_.NonRemovable -ne $true -and
                $_.Name -notlike "*Store*" -and
                $_.Name -notlike "*Calculator*" -and
                $_.Name -notlike "*WindowsNotepad*" -and
                $_.Name -notlike "*Paint*"
            }
            
            foreach ($Pkg in $Packages) {
                Write-Host "Removing: $($Pkg.Name)"
                try {
                    Remove-AppxPackage -Package $Pkg.PackageFullName -ErrorAction Stop
                } catch {
                    # Ignore locked or non-removable packages
                }
            }
        }

        # 2. Prevent reinstalling bloatware for newly created users
        Get-AppxProvisionedPackage -Online | Where-Object {
            $Name = $_.DisplayName
            $IsBloat = $false
            foreach ($P in $BloatwarePatterns) {
                if ($Name -like $P.Trim("*")) { $IsBloat = $true; break }
            }
            $IsBloat -and $Name -notlike "*Store*" -and $Name -notlike "*Calculator*"
        } | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue

        Write-Host "[+] Cleaning operation completed successfully!"
        """

    try:
      process = subprocess.Popen(
          ["powershell.exe", "-NoProfile", "-Command", ps_script],
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          text=True,
          encoding="cp866",
      )

      for line in process.stdout:
        self.log(line.strip())

      process.wait()
      self.log("\n[✔] Done! Selected UWP bloatware has been removed.")
      messagebox.showinfo("Success", "UWP bloatware removal is complete!")
    except Exception as e:
      self.log(f"\n[!] Error: {str(e)}")
      messagebox.showerror(
          "Error", f"An error occurred while executing the script:\n{e}"
      )
    finally:
      self.clean_btn.config("normal")


if __name__ == "__main__":
  root = tk.Tk()
  app = UWPCleanerApp(root)
  root.mainloop()