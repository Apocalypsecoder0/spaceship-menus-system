import sys
import tkinter as tk
from tkinter import messagebox
import random
import hashlib

class SpaceShipControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Ship Control Computer")
        self.main_menu()

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
                messagebox.showinfo("Set Course", f"Course set to {sel_planet} in {sel_system}, {sel_sector}, {sel_quad}.\nGPS: {planet_coords}")
                set_win.destroy()
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

    def weapons_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- WEAPONS SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.2 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        for weapon in self.WEAPONS_DATABASE:
            row = tk.Frame(self.root)
            row.pack(anchor="w", padx=20, pady=2)
            tk.Label(row, text=weapon, font=("Arial", 11)).pack(side="left")
            tk.Button(row, text="Core Info", font=("Arial", 8), command=lambda w=weapon: self.weapons_core_lookup(w)).pack(side="left", padx=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def shields_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- DEFENSE SYSTEM (SHIELDS) ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.2 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        for shield in self.SHIELDS_DATABASE:
            row = tk.Frame(self.root)
            row.pack(anchor="w", padx=20, pady=2)
            tk.Label(row, text=shield, font=("Arial", 11)).pack(side="left")
            tk.Button(row, text="Core Info", font=("Arial", 8), command=lambda s=shield: self.shields_core_lookup(s)).pack(side="left", padx=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=10)

    def navigation_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- NAVIGATION SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.1 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Set Course", width=25, command=self.set_course).pack(pady=5)
        tk.Button(self.root, text="Engage Warp Drive", width=25, command=self.engage_warp_drive).pack(pady=5)
        tk.Button(self.root, text="Scan Sector", width=25, command=self.scan_sector).pack(pady=5)
        tk.Button(self.root, text="Plot Star Map", width=25, command=self.plot_star_map).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=5)

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="=== SPACE SHIP CONTROL COMPUTER ===", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.2 | Updated: May 20, 2025", font=("Arial", 10), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Set Universe Seed (No Man's Sky Mode)", width=30, command=self.prompt_for_seed).pack(pady=5)
        tk.Button(self.root, text="Navigation", width=25, command=self.navigation_menu).pack(pady=5)
        tk.Button(self.root, text="Engineering", width=25, command=self.engineering_menu).pack(pady=5)
        tk.Button(self.root, text="Weapons", width=25, command=self.weapons_menu).pack(pady=5)
        tk.Button(self.root, text="Defense (Shields)", width=25, command=self.shields_menu).pack(pady=5)
        tk.Button(self.root, text="Communications", width=25, command=self.communications_menu).pack(pady=5)
        tk.Button(self.root, text="Life Support", width=25, command=self.life_support_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", width=25, command=self.exit_program).pack(pady=5)

    def engineering_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- ENGINEERING SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.1 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Check Reactor Status", width=25, command=self.check_reactor_status).pack(pady=5)
        tk.Button(self.root, text="Divert Power", width=25, command=self.divert_power).pack(pady=5)
        tk.Button(self.root, text="Repair Systems", width=25, command=self.repair_systems).pack(pady=5)
        tk.Button(self.root, text="Monitor Engines", width=25, command=self.monitor_engines).pack(pady=5)
        tk.Button(self.root, text="Weapons System", width=25, command=self.weapons_menu).pack(pady=5)
        tk.Button(self.root, text="Shields System", width=25, command=self.shields_menu).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=5)

    def communications_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- COMMUNICATIONS SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.1 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Send Transmission", width=25, command=self.send_transmission).pack(pady=5)
        tk.Button(self.root, text="Receive Transmission", width=25, command=self.receive_transmission).pack(pady=5)
        tk.Button(self.root, text="Jam Signals", width=25, command=self.jam_signals).pack(pady=5)
        tk.Button(self.root, text="Open Hailing Frequencies", width=25, command=self.open_hailing_frequencies).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=5)

    def life_support_menu(self):
        self.clear_window()
        tk.Label(self.root, text="--- LIFE SUPPORT SYSTEM ---", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Patch Info: v1.1 | Updated: May 20, 2025", font=("Arial", 9), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Check Oxygen Levels", width=25, command=self.check_oxygen_levels).pack(pady=5)
        tk.Button(self.root, text="Adjust Temperature", width=25, command=self.adjust_temperature).pack(pady=5)
        tk.Button(self.root, text="Seal Bulkheads", width=25, command=self.seal_bulkheads).pack(pady=5)
        tk.Button(self.root, text="Monitor CO2 Levels", width=25, command=self.monitor_co2_levels).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", width=25, command=self.main_menu).pack(pady=5)

    def not_implemented(self):
        messagebox.showinfo("Info", "Functionality not implemented yet.")

    def exit_program(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceShipControlGUI(root)
    root.mainloop()