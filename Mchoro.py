import math
import sqlite3
from kivy.app import App
import os
from kivy.graphics import Line, Color, Mesh, InstructionGroup
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import StringProperty, NumericProperty, Clock
from kivy.utils import get_color_from_hex

class KichoraSamaniInjini(MDGridLayout):
    hali = StringProperty("picha") 
    zoom = NumericProperty(600)
    angle_x = NumericProperty(0) 
    angle_y = NumericProperty(0)
    mtazamo = StringProperty("2-point")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.md_bg_color = [0, 0, 0, 1] 
        self.mwanga_dir = [-0.5, 1, 0.8]
        self._touches = [] 
        self.data_ya_sasa = [] # Hifadhi ya mchoro ili kuzungusha (orbit) ifanye kazi
        self.cx = 400 # Thamani ya muda (itabadilika ikishasoma width/2)
        self.cy = 300 # Thamani ya muda
        Clock.schedule_once(self.anzisha_uwanja)

    def anzisha_uwanja(self, dt):
        self.cx = self.width / 2
        self.cy = self.height / 2
        if self.data_ya_sasa:
            self.tekeleza_mchoro(self.data_ya_sasa)

    # --- INJINI YA DATABASE (Hii ndio iliyokosekana) ---
        # --- INJINI YA DATABASE (Safi na Usalama) ---
    def chora_kutoka_database(self, mteja_namba):
        import sqlite3
        # Hii itapata folder la ndani la programu (Files za ndani)
        user_data_dir = App.get_running_app().user_data_dir
    
        # Tengeneza path inayojielewa yenyewe (OS independent)
        kabati_db_path = os.path.join(user_data_dir, 'Kabati.sqlite')
        try:
            con = sqlite3.connect(kabati_db_path)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Kabati WHERE [Namba ya Mteja]=?", (mteja_namba,))
            rows = cur.fetchall()

            if not rows:
                print(f"Dah! Hakuna data kwa: {mteja_namba}")
                return

            self.data_ya_sasa = []
            for r in rows:
                try:
                    # Helper function kuzuia kero za 'poiuoiui'
                    def to_f(val, default=0):
                        try: return float(val)
                        except: return default

                    x, y, z = to_f(r['umbali x']), to_f(r['umbali y']), to_f(r['umbali z'])
                    w, h = to_f(r['upana'], 100), to_f(r['urefu'], 100)
                    print(h,w)
                    
                    panel = {
                        'ncha': [(x, y, z), (x+w, y, z), (x+w, y+h, z), (x, y+h, z)],
                        'z': z,
                        'rangi': '#8B4513'
                    }
                    self.data_ya_sasa.append(panel)
                except Exception as e:
                    print(f"Ruka data mbovu: {e}")
            
            con.close()
            self.tekeleza_mchoro(self.data_ya_sasa)
        except Exception as e:
            print(f"Kimeumana SQLite: {e}")

    # --- TEKELEZA MCHORO (Bila 'with instr' - Welding safi) ---
    def tekeleza_mchoro(self, orodha_ya_panels):
        self.canvas.clear()
        if not orodha_ya_panels: return
        
        # Z-Sorting
        sorted_panels = sorted(orodha_ya_panels, key=lambda p: p['z'], reverse=True)
        
        for p in sorted_panels:
            ncha_2d = []
            for nx, ny, nz in p['ncha']:
                ncha_2d.extend(self.geuza_3d_2d(nx, ny, nz))
            
            final_color = self.piga_hesabu_ya_shading(p['ncha'], p.get('rangi', '#8B4513'))
            
            instr = InstructionGroup()
            
            # 1. Picha/Rangi
            if self.hali in ["picha", "ramani"]:
                instr.add(Color(*final_color))
                v_data = []
                for i in range(0, len(ncha_2d), 2):
                    v_data.extend([ncha_2d[i], ncha_2d[i+1], 0, 0])
                instr.add(Mesh(vertices=v_data, indices=range(len(p['ncha'])), mode='triangle_fan'))
            
            # 2. Mistari (Mfupa)
            if self.hali in ["mfupa", "ramani"]:
                instr.add(Color(0, 0, 0, 1 if self.hali=="mfupa" else 0.4))
                instr.add(Line(points=ncha_2d + ncha_2d[:2], width=1.1))
            
            # 3. Ongeza kundi moja tu kwenye canvas kwa kila panel
            self.canvas.add(instr)

    # --- INJINI YA PERSPECTIVE NA ROTATION ---
    def geuza_3d_2d(self, x, y, z):
        ax = math.radians(self.angle_x)
        ay = math.radians(self.angle_y)
        # Rotation Matrix (Orbit)
        rx = x * math.cos(ax) - z * math.sin(ax)
        rz = x * math.sin(ax) + z * math.cos(ax)
        ry = y * math.cos(ay) - rz * math.sin(ay)
        fz = y * math.sin(ay) + rz * math.cos(ay)
        # Projection
        f = self.zoom / (max(1, self.zoom + fz))
        return self.cx + rx * f, self.cy + ry * f

    
    def piga_hesabu_ya_shading(self, ncha, rangi_hex):
        try:
            v1 = [ncha[1][0]-ncha[0][0], ncha[1][1]-ncha[0][1], ncha[1][2]-ncha[0][2]]
            v2 = [ncha[2][0]-ncha[0][0], ncha[2][1]-ncha[0][1], ncha[2][2]-ncha[0][2]]
            norm = [v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0]]
            mag = math.sqrt(sum(i**2 for i in norm)) or 1
            norm = [i/mag for i in norm]
            dot = sum(norm[i] * self.mwanga_dir[i] for i in range(3))
            shading = max(0.4, (dot + 1) / 2)
            r, g, b, a = get_color_from_hex(rangi_hex)
            return [r*shading, g*shading, b*shading, a]
        except:
            return get_color_from_hex(rangi_hex)

    # --- MIKONO (TOUCH) ---
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.angle_x += touch.dx * 0.4
            self.angle_y -= touch.dy * 0.4
            self.tekeleza_mchoro(self.data_ya_sasa)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown': self.zoom += 20
            elif touch.button == 'scrollup': self.zoom -= 20
            self.tekeleza_mchoro(self.data_ya_sasa)
