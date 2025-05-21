import sys
import tkinter as tk
from tkinter import messagebox
import random
import hashlib
import threading
import time

class SpaceShipControlGUI:
    def __init__(self, root):
        self.root = root
        self.show_splash_screen()

    def show_splash_screen(self):
        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.geometry("400x250+500+250")
        tk.Label(splash, text="STARFLEET COMPUTER", font=("Arial", 20, "bold"), fg="#00bfff").pack(pady=30)
        tk.Label(splash, text="Loading Space Ship Control System...", font=("Arial", 12)).pack(pady=10)
        progress = tk.Label(splash, text="Initializing...", font=("Arial", 10), fg="gray")
        progress.pack(pady=10)
        self.root.withdraw()
        def load():
            for i, msg in enumerate(["Loading Core Modules...", "Loading Navigation...", "Loading Engineering...", "Loading Weapons...", "Loading Shields...", "Loading UI...", "Ready!"]):
                progress.config(text=msg)
                splash.update()
                time.sleep(0.5)
            splash.destroy()
            self.root.deiconify()
            self.root.title("Space Ship Control Computer")
            self.main_menu()
        threading.Thread(target=load).start()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_seeded_galaxy(self, seed):
        random.seed(seed)
        quadrants = [f"Quadrant {chr(65+i)}" for i in range(4)]
        galaxy = {}
        for q in quadrants:
            galaxy[q] = {}
            for s in range(1, 4):
                sector_name = f"Sector {s:03d}"
                galaxy[q][sector_name] = {}
                for sys in range(1, 4):
                    sys_x = round(random.uniform(0, 200), 2)
                    sys_y = round(random.uniform(0, 50), 2)
                    sys_z = round(random.uniform(0, 20), 2)
                    sys_name = f"System-{hashlib.md5(f'{q}{sector_name}{sys}{seed}'.encode()).hexdigest()[:6]}"
                    galaxy[q][sector_name][sys_name] = {
                        "coords": (sys_x, sys_y, sys_z),
                        "planets": {}
                    }
                    for p in range(random.randint(2, 5)):
                        planet_x = sys_x + round(random.uniform(-0.5, 0.5), 2)
                        planet_y = sys_y + round(random.uniform(-0.5, 0.5), 2)
                        planet_z = sys_z + round(random.uniform(-0.5, 0.5), 2)
                        pname = f"Planet-{hashlib.md5(f'{q}{sector_name}{sys}{p}{seed}'.encode()).hexdigest()[:5]}"
                        galaxy[q][sector_name][sys_name]["planets"][pname] = (planet_x, planet_y, planet_z)
        return galaxy

    def prompt_for_seed(self):
        def set_seed():
            seed = seed_var.get()
            if not seed:
                messagebox.showwarning("Seed Required", "Please enter a seed value.")
                return
            self.GALAXY_MAP = self.generate_seeded_galaxy(seed)
            messagebox.showinfo("Universe Seeded", f"Universe generated with seed: {seed}")
            seed_win.destroy()
        seed_win = tk.Toplevel(self.root)
        seed_win.title("Set Universe Seed")
        tk.Label(seed_win, text="Enter Universe Seed:", font=("Arial", 12)).pack(pady=5)
        seed_var = tk.StringVar(seed_win)
        tk.Entry(seed_win, textvariable=seed_var).pack(pady=5)
        tk.Button(seed_win, text="Generate Universe", command=set_seed).pack(pady=10)
        tk.Button(seed_win, text="Cancel", command=seed_win.destroy).pack()

    # --- Galaxy Data with GPS Coordinates ---
    GALAXY_MAP = {
        "Alpha Quadrant": {
            "Sector 001": {
                "Sol System": {
                    "coords": (0, 0, 0),
                    "planets": {
                        "Earth": (0, 0, 1),
                        "Mars": (0, 0, 1.5),
                        "Jupiter": (0, 0, 5.2)
                    }
                },
                "Alpha Centauri System": {
                    "coords": (4.37, 0, 0),
                    "planets": {
                        "Alpha Centauri A": (4.37, 0, 0.1),
                        "Alpha Centauri B": (4.37, 0, 0.2),
                        "Proxima Centauri": (4.24, 0, 0.01)
                    }
                }
            },
            "Sector 002": {
                "Vega System": {
                    "coords": (25, 0, 0),
                    "planets": {
                        "Vega IV": (25, 0, 0.4),
                        "Vega V": (25, 0, 0.5)
                    }
                },
                "Sirius System": {
                    "coords": (8.6, 0, 0),
                    "planets": {
                        "Sirius A": (8.6, 0, 0.1),
                        "Sirius B": (8.6, 0, 0.2)
                    }
                }
            }
        },
        "Beta Quadrant": {
            "Sector 101": {
                "Qo'noS System": {
                    "coords": (90, 10, 5),
                    "planets": {
                        "Qo'noS": (90, 10, 5.1)
                    }
                },
                "Rura Penthe System": {
                    "coords": (95, 12, 6),
                    "planets": {
                        "Rura Penthe": (95, 12, 6.1)
                    }
                }
            },
            "Sector 102": {
                "Romulus System": {
                    "coords": (120, 20, 10),
                    "planets": {
                        "Romulus": (120, 20, 10.1),
                        "Remus": (120, 20, 10.2)
                    }
                },
                "Nimbus System": {
                    "coords": (130, 22, 11),
                    "planets": {
                        "Nimbus III": (130, 22, 11.1)
                    }
                }
            }
        }
    }

    # --- Star Trek Planets Database ---
    PLANET_DATABASE = {
        "Earth": {"class": "M", "type": "Terrestrial", "desc": "Homeworld of humanity, Federation capital."},
        "Qo'noS": {"class": "M", "type": "Terrestrial", "desc": "Klingon homeworld."},
        "Romulus": {"class": "M", "type": "Terrestrial", "desc": "Romulan homeworld."},
        "Remus": {"class": "M", "type": "Terrestrial", "desc": "Twin planet to Romulus."},
        "Mars": {"class": "M", "type": "Terrestrial", "desc": "Federation shipyards."},
        "Jupiter": {"class": "J", "type": "Gas Giant", "desc": "Largest planet in Sol system."},
        "Vega IV": {"class": "M", "type": "Terrestrial", "desc": "Colony world."},
        "Nimbus III": {"class": "M", "type": "Desert", "desc": "Planet of Galactic Peace."},
        "Rura Penthe": {"class": "H", "type": "Penal Colony", "desc": "Klingon penal asteroid."},
        "Alpha Centauri A": {"class": "M", "type": "Terrestrial", "desc": "Colony world."},
        "Alpha Centauri B": {"class": "M", "type": "Terrestrial", "desc": "Colony world."},
        "Proxima Centauri": {"class": "M", "type": "Terrestrial", "desc": "Colony world."},
        "Sirius A": {"class": "A", "type": "Star", "desc": "Primary star in Sirius system."},
        "Sirius B": {"class": "D", "type": "White Dwarf", "desc": "Companion star in Sirius system."},
        # Add more as needed
    }

    # --- Weapons and Defense Database ---
    WEAPONS_DATABASE = {
        "Phaser Array": {"class": "X", "type": "Energy", "desc": "Standard Starfleet shipboard phaser array."},
        "Photon Torpedo": {"class": "X", "type": "Explosive", "desc": "Matter/antimatter warhead torpedo."},
        "Disruptor Cannon": {"class": "X", "type": "Energy", "desc": "Klingon and Romulan ship disruptor weapon."},
        "Quantum Torpedo": {"class": "X", "type": "Explosive", "desc": "Advanced Starfleet torpedo."},
        # Add more as needed
    }
    SHIELDS_DATABASE = {
        "Deflector Shield": {"class": "A", "type": "Energy", "desc": "Standard starship defensive shield."},
        "Ablative Armor": {"class": "B", "type": "Material", "desc": "Physical armor for additional protection."},
        "Regenerative Shield": {"class": "S", "type": "Energy", "desc": "Advanced shield with self-repair capability."},
        # Add more as needed
    }

    # --- Settings State ---
    SETTINGS = {
        'theme': 'light',
        'audio': True
    }

    def apply_theme(self):
        # Simple theme switch (light/dark)
        bg = 'white' if self.SETTINGS['theme'] == 'light' else '#222'
        fg = 'black' if self.SETTINGS['theme'] == 'light' else 'white'
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

    def computer_core_lookup(self, planet_name):
        info = self.PLANET_DATABASE.get(planet_name)
        if info:
            messagebox.showinfo(
                f"Computer Core: {planet_name}",
                f"Class: {info['class']}\nType: {info['type']}\nDescription: {info['desc']}"
            )
        else:
            messagebox.showinfo(
                "Computer Core",
                f"No database entry for {planet_name}."
            )

    def plot_star_map(self):
        # Show a simple galaxy map in a new window
        map_win = tk.Toplevel(self.root)
        map_win.title("Galaxy Star Map")
        tk.Label(map_win, text="Galaxy Star Map", font=("Arial", 14)).pack(pady=5)
        for quadrant, sectors in self.GALAXY_MAP.items():
            tk.Label(map_win, text=quadrant, font=("Arial", 12, "bold"), fg="blue").pack(anchor="w", padx=10)
            for sector, systems in sectors.items():
                tk.Label(map_win, text=f"  {sector}", font=("Arial", 11, "italic"), fg="darkgreen").pack(anchor="w", padx=20)
                for system, sysdata in systems.items():
                    sys_coords = sysdata["coords"]
                    sys_label = f"    {system} (GPS: {sys_coords})"
                    tk.Label(map_win, text=sys_label, font=("Arial", 10, "bold")).pack(anchor="w", padx=30)
                    for planet, p_coords in sysdata["planets"].items():
                        planet_row = tk.Frame(map_win)
                        planet_row.pack(anchor="w", padx=50)
                        tk.Label(planet_row, text=f"{planet} (GPS: {p_coords})", font=("Arial", 10)).pack(side="left")
                        tk.Button(planet_row, text="Core Info", font=("Arial", 8), command=lambda p=planet: self.computer_core_lookup(p)).pack(side="left", padx=5)
        tk.Button(map_win, text="Close", command=map_win.destroy).pack(pady=10)

    def viewscreen(self):
        vs_win = tk.Toplevel(self.root)
        vs_win.title("Main Viewscreen")
        vs_win.geometry("600x400")
        tk.Label(vs_win, text="STARSHIP MAIN VIEWSCREEN", font=("Arial", 16, "bold"), fg="#00bfff").pack(pady=10)
        self.view_label = tk.Label(vs_win, text="Awaiting course...", font=("Arial", 12), wraplength=550, justify="center")
        self.view_label.pack(pady=20)
        tk.Button(vs_win, text="Show Current Destination", command=self.update_viewscreen).pack(pady=5)
        tk.Button(vs_win, text="Close", command=vs_win.destroy).pack(pady=10)
        self.current_destination = None
        self.vs_win = vs_win

    def update_viewscreen(self):
        if hasattr(self, 'current_destination') and self.current_destination:
            dest = self.current_destination
            self.view_label.config(text=f"Destination: {dest['planet']}\nSystem: {dest['system']}\nSector: {dest['sector']}\nQuadrant: {dest['quadrant']}\nGPS: {dest['coords']}")
        else:
            self.view_label.config(text="No destination set. Use Navigation > Set Course.")

    def set_course(self):
        # Let user pick a system and planet from the galaxy map
        def select_planet():
            sel_quad = quadrant_var.get()
            sel_sector = sector_var.get()
            sel_system = system_var.get()
            sel_planet = planet_var.get()
            if sel_planet:
                sysdata = self.GALAXY_MAP[sel_quad][sel_sector][sel_system]
                planet_coords = sysdata["planets"][sel_planet]
                self.current_destination = {
                    'quadrant': sel_quad,
                    'sector': sel_sector,
                    'system': sel_system,
                    'planet': sel_planet,
                    'coords': planet_coords
                }
                messagebox.showinfo("Set Course", f"Course set to {sel_planet} in {sel_system}, {sel_sector}, {sel_quad}.\nGPS: {planet_coords}")
                set_win.destroy()
                # If viewscreen is open, update it
                if hasattr(self, 'vs_win') and self.vs_win.winfo_exists():
                    self.update_viewscreen()
            else:
                messagebox.showwarning("Set Course", "Please select a planet.")

        set_win = tk.Toplevel(self.root)
        set_win.title("Set Course")
        tk.Label(set_win, text="Set Course to:", font=("Arial", 12)).pack(pady=5)
        quadrant_var = tk.StringVar(set_win)
        sector_var = tk.StringVar(set_win)
        system_var = tk.StringVar(set_win)
        planet_var = tk.StringVar(set_win)

        # Quadrant dropdown
        tk.Label(set_win, text="Quadrant:").pack(anchor="w", padx=10)
        quad_menu = tk.OptionMenu(set_win, quadrant_var, *self.GALAXY_MAP.keys())
        quad_menu.pack(fill="x", padx=10)

        # Sector dropdown
        tk.Label(set_win, text="Sector:").pack(anchor="w", padx=10)
        sector_menu = tk.OptionMenu(set_win, sector_var, "")
        sector_menu.pack(fill="x", padx=10)

        # System dropdown
        tk.Label(set_win, text="System:").pack(anchor="w", padx=10)
        system_menu = tk.OptionMenu(set_win, system_var, "")
        system_menu.pack(fill="x", padx=10)

        # Planet dropdown
        tk.Label(set_win, text="Planet:").pack(anchor="w", padx=10)
        planet_menu = tk.OptionMenu(set_win, planet_var, "")
        planet_menu.pack(fill="x", padx=10)

        # Update dropdowns dynamically
        def update_sectors(*_):
            sectors = list(self.GALAXY_MAP.get(quadrant_var.get(), {}).keys())
            sector_var.set("")
            menu = sector_menu["menu"]
            menu.delete(0, "end")
            for s in sectors:
                menu.add_command(label=s, command=lambda v=s: sector_var.set(v))
            update_systems()
        def update_systems(*_):
            systems = list(self.GALAXY_MAP.get(quadrant_var.get(), {}).get(sector_var.get(), {}).keys())
            system_var.set("")
            menu = system_menu["menu"]
            menu.delete(0, "end")
            for s in systems:
                menu.add_command(label=s, command=lambda v=s: system_var.set(v))
            update_planets()
        def update_planets(*_):
            planets = []
            sysdata = self.GALAXY_MAP.get(quadrant_var.get(), {}).get(sector_var.get(), {}).get(system_var.get(), None)
            if sysdata:
                planets = list(sysdata["planets"].keys())
            planet_var.set("")
            menu = planet_menu["menu"]
            menu.delete(0, "end")
            for p in planets:
                menu.add_command(label=p, command=lambda v=p: planet_var.set(v))
        quadrant_var.trace_add('write', update_sectors)
        sector_var.trace_add('write', update_systems)
        system_var.trace_add('write', update_planets)

        tk.Button(set_win, text="Set Course", command=select_planet).pack(pady=10)
        tk.Button(set_win, text="Planet Core Info", command=lambda: self.computer_core_lookup(planet_var.get())).pack(pady=2)
        tk.Button(set_win, text="Cancel", command=set_win.destroy).pack()

    def engage_warp_drive(self):
        messagebox.showinfo("Engage Warp Drive", "Warp drive engaged! Hold on tight.")

    def scan_sector(self):
        messagebox.showinfo("Scan Sector", "Sector scan complete. No threats detected.")

    def check_reactor_status(self):
        messagebox.showinfo("Reactor Status", "Reactor stable. Output at 98% efficiency.")

    def divert_power(self):
        messagebox.showinfo("Divert Power", "Power successfully diverted to shields.")

    def repair_systems(self):
        messagebox.showinfo("Repair Systems", "All critical systems repaired.")

    def monitor_engines(self):
        messagebox.showinfo("Monitor Engines", "Engines running within normal parameters.")

    def send_transmission(self):
        messagebox.showinfo("Send Transmission", "Transmission sent to Starfleet Command.")

    def receive_transmission(self):
        messagebox.showinfo("Receive Transmission", "New message received: 'Safe travels, Captain!'")

    def jam_signals(self):
        messagebox.showinfo("Jam Signals", "All external signals are now jammed.")

    def open_hailing_frequencies(self):
        messagebox.showinfo("Hailing Frequencies", "Hailing frequencies open.")

    def check_oxygen_levels(self):
        messagebox.showinfo("Oxygen Levels", "O2 levels at 21%. All normal.")

    def adjust_temperature(self):
        messagebox.showinfo("Adjust Temperature", "Temperature set to 22°C.")

    def seal_bulkheads(self):
        messagebox.showinfo("Seal Bulkheads", "All bulkheads sealed.")

    def monitor_co2_levels(self):
        messagebox.showinfo("CO2 Levels", "CO2 levels at 0.04%. Safe for crew.")

    def weapons_core_lookup(self, weapon_name):
        info = self.WEAPONS_DATABASE.get(weapon_name)
        if info:
            messagebox.showinfo(
                f"Weapons Core: {weapon_name}",
                f"Class: {info['class']}\nType: {info['type']}\nDescription: {info['desc']}"
            )
        else:
            messagebox.showinfo(
                "Weapons Core",
                f"No database entry for {weapon_name}."
            )

    def shields_core_lookup(self, shield_name):
        info = self.SHIELDS_DATABASE.get(shield_name)
        if info:
            messagebox.showinfo(
                f"Shields Core: {shield_name}",
                f"Class: {info['class']}\nType: {info['type']}\nDescription: {info['desc']}"
            )
        else:
            messagebox.showinfo(
                "Shields Core",
                f"No database entry for {shield_name}."
            )

    def power_source_gui(self):
        self.clear_window()
        tk.Label(self.root, text="--- STARSHIP POWER SOURCES ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Label(self.root, text="Starship power sources are critical for all major systems, including propulsion, shields, and weapons.", font=("Arial", 10), wraplength=500, justify="left").pack(pady=5)
        tk.Label(self.root, text="Common Power Sources:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        sources = [
            ("Matter-Antimatter Reactor (M/AM)", "Primary power source for most advanced starships. Produces immense energy via matter-antimatter annihilation."),
            ("Fusion Reactor", "Used for impulse engines and auxiliary power. Safer but less powerful than M/AM."),
            ("Quantum Singularity Core", "Romulan technology. Harnesses a miniature black hole for power."),
            ("Solar Collector", "Used by some civilian or planetary installations. Not suitable for starships."),
        ]
        for name, desc in sources:
            tk.Label(self.root, text=f"- {name}", font=("Arial", 11, "bold")).pack(anchor="w", padx=30)
            tk.Label(self.root, text=desc, font=("Arial", 10), wraplength=480, justify="left").pack(anchor="w", padx=50)
        tk.Label(self.root, text="\nMatter-Antimatter Reaction:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(self.root, text="The matter-antimatter reaction is the most critical process in starship engineering. Mixing deuterium (matter) and anti-deuterium (antimatter) in the reaction chamber produces pure energy, regulated by dilithium crystals. Any imbalance can cause catastrophic failure.", font=("Arial", 10), wraplength=500, justify="left", fg="red").pack(anchor="w", padx=20)
        tk.Label(self.root, text="\nCritical Importance:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(self.root, text="- Power source integrity is vital for ship survival.\n- Failure of the M/AM reactor can result in total loss of ship.\n- Redundant systems and containment fields are mandatory.", font=("Arial", 10), wraplength=500, justify="left").pack(anchor="w", padx=20)
        tk.Label(self.root, text="\nVariants:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(self.root, text="- Federation: Standard M/AM reactor with dilithium regulation.\n- Klingon: M/AM core, less redundancy, more raw output.\n- Romulan: Quantum Singularity core, unique failure modes.\n- Civilian: Fusion or fission reactors, lower output.", font=("Arial", 10), wraplength=500, justify="left").pack(anchor="w", padx=20)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def warp_drive_gui(self):
        self.clear_window()
        tk.Label(self.root, text="--- WARP DRIVE SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Label(self.root, text="The warp drive enables faster-than-light travel by warping space around the ship.", font=("Arial", 10), wraplength=500, justify="left").pack(pady=5)
        tk.Label(self.root, text="\nCore Components:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        tk.Label(self.root, text="- Matter-Antimatter Reactor: Provides energy for the warp coils.\n- Warp Coils: Generate the warp field.\n- Dilithium Crystals: Regulate the M/AM reaction.", font=("Arial", 10), wraplength=500, justify="left").pack(anchor="w", padx=20)
        tk.Label(self.root, text="\nCritical Importance:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(self.root, text="- Warp drive failure can strand a ship light-years from help.\n- Overloading the warp core can cause a breach (catastrophic).\n- Regular maintenance and monitoring are essential.", font=("Arial", 10), wraplength=500, justify="left").pack(anchor="w", padx=20)
        tk.Label(self.root, text="\nVariants:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(self.root, text="- Federation: Standard warp drive, high safety.\n- Klingon: High-output, less redundancy.\n- Romulan: Quantum singularity-powered warp.\n- Civilian: Limited to warp 5 or below.", font=("Arial", 10), wraplength=500, justify="left").pack(anchor="w", padx=20)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def navigation_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- NAVIGATION SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        nav_items = [
            ("Set Course", self.set_course),
            ("View Star Map", self.plot_star_map),
            ("Open Viewscreen", self.viewscreen),
            ("Return to Main Menu", self.main_menu)
        ]
        for label, cmd in nav_items:
            tk.Button(self.root, text=label, width=25, command=cmd).pack(pady=5)

    def weapons_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- WEAPONS SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        for weapon in self.WEAPONS_DATABASE:
            tk.Button(self.root, text=weapon, width=30, command=lambda w=weapon: self.weapons_core_lookup(w)).pack(pady=2)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def shields_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- DEFENSE SYSTEM (SHIELDS) ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        for shield in self.SHIELDS_DATABASE:
            tk.Button(self.root, text=shield, width=30, command=lambda s=shield: self.shields_core_lookup(s)).pack(pady=2)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def settings_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- SETTINGS & OPTIONS ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        settings_items = [
            ("Display Settings", self.display_settings_menu),
            ("Audio Settings", self.audio_settings_menu),
            ("Return to Main Menu", self.main_menu)
        ]
        for label, cmd in settings_items:
            tk.Button(self.root, text=label, width=25, command=cmd).pack(pady=5)

    def display_settings_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- DISPLAY SETTINGS ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Theme:").pack(pady=2)
        theme_var = tk.StringVar(value=self.SETTINGS['theme'])
        def set_theme():
            self.SETTINGS['theme'] = theme_var.get()
            self.apply_theme()
        tk.Radiobutton(self.root, text="Light", variable=theme_var, value='light', command=set_theme).pack()
        tk.Radiobutton(self.root, text="Dark", variable=theme_var, value='dark', command=set_theme).pack()
        tk.Button(self.root, text="Return to Settings", width=25, command=self.settings_menu).pack(pady=10)

    def audio_settings_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- AUDIO SETTINGS ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Audio:").pack(pady=2)
        audio_var = tk.BooleanVar(value=self.SETTINGS['audio'])
        def set_audio():
            self.SETTINGS['audio'] = audio_var.get()
        tk.Checkbutton(self.root, text="Enable Audio", variable=audio_var, command=set_audio).pack()
        tk.Button(self.root, text="Return to Settings", width=25, command=self.settings_menu).pack(pady=10)

    def starship_class_type_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- STARSHIP CLASSES & TYPES ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        starship_classes = [
            ("Constitution Class", "Federation heavy cruiser, e.g., USS Enterprise NCC-1701"),
            ("Galaxy Class", "Federation explorer, e.g., USS Enterprise NCC-1701-D"),
            ("Intrepid Class", "Federation science vessel, e.g., USS Voyager"),
            ("D'deridex Class", "Romulan warbird"),
            ("Bird-of-Prey", "Klingon light attack ship"),
            ("Vor'cha Class", "Klingon attack cruiser"),
            ("Warbird", "Romulan capital ship"),
            ("Defiant Class", "Federation escort"),
            ("Sovereign Class", "Federation flagship, e.g., USS Enterprise NCC-1701-E"),
        ]
        for name, desc in starship_classes:
            tk.Label(self.root, text=f"- {name}", font=("Arial", 11, "bold")).pack(anchor="w", padx=30)
            tk.Label(self.root, text=desc, font=("Arial", 10), wraplength=480, justify="left").pack(anchor="w", padx=50)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def interstellar_travel_calculator(self):
        self.clear_window()
        tk.Label(self.root, text="--- INTERSTELLAR TRAVEL CALCULATOR ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Label(self.root, text="Enter distance (light years) and speed (warp or c, or km/s):").pack(pady=5)
        dist_var = tk.DoubleVar()
        speed_var = tk.StringVar()
        tk.Label(self.root, text="Distance (ly):").pack()
        tk.Entry(self.root, textvariable=dist_var).pack()
        tk.Label(self.root, text="Speed (e.g., Warp 5, 0.5c, 100000 km/s):").pack()
        tk.Entry(self.root, textvariable=speed_var).pack()
        result_label = tk.Label(self.root, text="")
        result_label.pack(pady=5)
        def calculate():
            try:
                d_ly = dist_var.get()
                s = speed_var.get().strip().lower()
                c_kms = 299792.458
                if s.startswith("warp"):
                    warp = float(s.replace("warp", "").strip())
                    # Star Trek TNG warp formula: v/c = warp^(10/3)
                    v_c = warp ** (10/3)
                    v_kms = v_c * c_kms
                elif s.endswith("c"):
                    v_c = float(s.replace("c", "").strip())
                    v_kms = v_c * c_kms
                elif "km/s" in s:
                    v_kms = float(s.replace("km/s", "").strip())
                    v_c = v_kms / c_kms
                else:
                    result_label.config(text="Invalid speed format.")
                    return
                # Time in years
                t_yrs = d_ly / v_c if v_c else float('inf')
                # Kinetic energy (non-relativistic)
                mass_kg = 4.5e6  # Assume 4.5 million kg (small starship)
                v_ms = v_kms * 1000
                ke_joules = 0.5 * mass_kg * v_ms ** 2
                result = f"Travel Time: {t_yrs:.2f} years\nSpeed: {v_kms:,.0f} km/s ({v_c:.2f}c)\nKinetic Energy: {ke_joules:,.2e} J"
                result_label.config(text=result)
            except Exception as e:
                result_label.config(text=f"Error: {e}")
        tk.Button(self.root, text="Calculate", command=calculate).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def telemetry_overlay(self):
        # Overlay window for real-time ship telemetry
        overlay = tk.Toplevel(self.root)
        overlay.title("Telemetry System Overlay")
        overlay.geometry("350x320+1000+100")
        overlay.attributes('-topmost', True)
        tk.Label(overlay, text="--- SHIP TELEMETRY ---", font=("Arial", 13, "bold")).pack(pady=5)
        tk.Label(overlay, text="Patch Info: v1.5 | Updated: May 20, 2025", font=("Arial", 8), fg="gray").pack()
        # Simulated telemetry values
        hull_var = tk.StringVar(value="100% (Optimal)")
        shields_var = tk.StringVar(value="100% (Active)")
        warp_var = tk.StringVar(value="Offline")
        reactor_var = tk.StringVar(value="98% Output")
        speed_var = tk.StringVar(value="0.00c (Stationary)")
        coords_var = tk.StringVar(value="(0, 0, 0)")
        tk.Label(overlay, text="Hull Integrity:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=hull_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        tk.Label(overlay, text="Shields:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=shields_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        tk.Label(overlay, text="Warp Core Status:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=warp_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        tk.Label(overlay, text="Reactor Output:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=reactor_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        tk.Label(overlay, text="Current Speed:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=speed_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        tk.Label(overlay, text="Current Coordinates:").pack(anchor="w", padx=15)
        tk.Label(overlay, textvariable=coords_var, font=("Arial", 10)).pack(anchor="w", padx=30)
        # Simulate telemetry updates
        def update_telemetry():
            import random
            hull = max(0, 100 - random.randint(0, 2))
            shields = max(0, 100 - random.randint(0, 5))
            warp = random.choice(["Online", "Offline", "Standby"])
            reactor = f"{random.randint(95, 100)}% Output"
            speed = random.choice(["0.00c (Stationary)", "0.25c (Impulse)", "1.00c (Warp 1)", "9.00c (Warp 4.5)"])
            coords = (round(random.uniform(0,200),2), round(random.uniform(0,50),2), round(random.uniform(0,20),2))
            hull_var.set(f"{hull}% ({'Optimal' if hull>90 else 'Damaged'})")
            shields_var.set(f"{shields}% ({'Active' if shields>0 else 'Down'})")
            warp_var.set(warp)
            reactor_var.set(reactor)
            speed_var.set(speed)
            coords_var.set(str(coords))
            if overlay.winfo_exists():
                overlay.after(2000, update_telemetry)
        update_telemetry()
        tk.Button(overlay, text="Close", command=overlay.destroy).pack(pady=10)

    # --- Main Menu ---
    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- MAIN MENU ---", font=("Arial", 16, "bold")).pack(pady=10)
        menu_items = [
            ("Navigation System", self.navigation_menu),
            ("Weapons System", self.weapons_menu),
            ("Defense System (Shields)", self.shields_menu),
            ("Settings", self.settings_menu),
            ("Starship Classes & Types", self.starship_class_type_menu),
            ("Power Source Info", self.power_source_gui),
            ("Warp Drive Info", self.warp_drive_gui),
            ("Interstellar Travel Calculator", self.interstellar_travel_calculator),
            ("Telemetry Overlay", self.telemetry_overlay),
            ("Exit", sys.exit)
        ]
        for label, cmd in menu_items:
            tk.Button(self.root, text=label, width=25, command=cmd).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceShipControlGUI(root)
    root.mainloop()