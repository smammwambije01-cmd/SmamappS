import math
import json
import sqlite3
import base64
import io

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Mesh
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu, MDMenuItem
from kivymd.uix.dialog import (
    MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldHelperText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

# ==========================================
# 🪵 MASTER BONGO CATALOG (OFFICIAL DATABASE)
# ==========================================
BONGO_WOOD_CATALOG = {
    "Mninga (Bloodwood)": {"color": [0.55, 0.15, 0.08, 1], "shade": 0.09},
    "Mpingo (Ebony)": {"color": [0.05, 0.05, 0.05, 1], "shade": 0.02},
    "Mvule (Iroko)": {"color": [0.72, 0.55, 0.28, 1], "shade": 0.08},
    "Mtiki (Teak)": {"color": [0.48, 0.38, 0.22, 1], "shade": 0.07},
    "Mkongo (Pod Mahogany)": {"color": [0.38, 0.12, 0.08, 1], "shade": 0.10},
    "Mvange": {"color": [0.3, 0.2, 0.15, 1], "shade": 0.07},
    "Marine Board (Waterproof)": {"color": [0.25, 0.1, 0.05, 1], "shade": 0.09},
    "MDF White (Melamine)": {"color": [0.98, 0.98, 0.98, 1], "shade": 0.02},
    "Kioo Clear (Mirror)": {"color": [0.95, 0.98, 1.0, 1], "shade": 0.01},
    "Granite - Black Galaxy": {"color": [0.1, 0.1, 0.1, 1], "shade": 0.02},
    "Msindano (Pine)": {"color": [0.92, 0.85, 0.6, 1], "shade": 0.03},
    "Clear Varnish": {"color": [0.95, 0.9, 0.8, 0.5], "shade": 0.02},
    "Mahogany Stain": {"color": [0.4, 0.1, 0.1, 0.9], "shade": 0.08}
}
class SmamMorphEngine(Widget):
    scene_objects = ListProperty([])
    selected_obj = ObjectProperty(None, allownone=True)
    
    # Camera Positioning & Rotation
    cam_x = NumericProperty(0.0)
    cam_y = NumericProperty(0.0)
    cam_z = NumericProperty(0.0)
    cam_rx = NumericProperty(0.0)
    cam_ry = NumericProperty(-45.0)
    cam_rz = NumericProperty(0.0)
    cam_d = NumericProperty(15.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.touches = {}
        self.ldist = 0.0
        self.f = 950 
        self.light_pos = [10.0, 20.0, 10.0]
        self.cached_menu_items = []
        
        # Menu References
        self.m_wood = None
        self.m_axis = None
        self.m_anim = None
        self.m_loop = None
        
        # Inasubiri App iwe tayari (Ready state)
        Clock.schedule_once(self._preload_catalog, 0.5)
        Clock.schedule_interval(self.run_engine_cycle, 1/60)

    # --- UI GENERATOR (Mmiliki wa TextFields) ---
    def create_field(self, hint, helper, val="0.0", readonly=False):
        """Hii ndiyo inayounda muonekano wa data inputs"""
        f = MDTextField(
            mode="outlined", 
            readonly=readonly
        )
        f.text = str(val)
        f.add_widget(MDTextFieldHintText(text=hint))
        f.add_widget(MDTextFieldHelperText(text=helper, mode="on_focus"))
        return f
    def show_workshop(self, *args):
        """Hapa injini inafungua Karakana yenye ScrollView na Inputs zote"""
        scroll = ScrollView(
            size_hint_y=None, 
            height="500dp", 
            do_scroll_x=False, 
            scroll_timeout=100
        )
        layout = MDBoxLayout(
            orientation="vertical", 
            spacing="15dp", 
            padding=["20dp", "10dp", "20dp", "100dp"], 
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        # 1. TAARIFA ZA MSINGI (Basic Info)
        self.f_id = self.create_field("Jina la Mbao (ID)", "Mfano: Mlango_1", "M1")
        self.f_wood = self.create_field("Aina ya Mbao", "Gusa kuchagua mti", "Mninga (Bloodwood)", readonly=True)
        self.f_wood.bind(on_touch_up=lambda i, t: self.open_wood_menu(i) if i.collide_point(*t.pos) else None)
        
        # 2. VIPIMO (Dimensions)
        self.f_w = self.create_field("Upana (X) - Mita", "Upana wa mbao", "0.6")
        self.f_h = self.create_field("Urefu (Y) - Mita", "Kimo cha mbao", "2.0")
        self.f_d = self.create_field("Unene (Z) - Mita", "Unene wa mbao", "0.02")
        
        # 3. NAFASI (Position)
        self.f_x = self.create_field("Pos X", "Mahali ilipo (L/R)", "0.0")
        self.f_y = self.create_field("Pos Y", "Kimo (Juu/Chini)", "-1.0")
        self.f_z = self.create_field("Pos Z", "Kina (Mbele/Nyuma)", "0.0")
        
        # 4. BAWABA (Pivot Points)
        self.f_px = self.create_field("Pivot X", "Kituo cha mzunguko X", "0.0")
        self.f_py = self.create_field("Pivot Y", "Kituo cha mzunguko Y", "0.0")
        self.f_pz = self.create_field("Pivot Z", "Kituo cha mzunguko Z", "0.0")

        # Ziongeze hizi kwanza kwenye layout
        f_list = [self.f_id, self.f_wood, self.f_w, self.f_h, self.f_d, 
                  self.f_x, self.f_y, self.f_z, self.f_px, self.f_py, self.f_pz]
        for f in f_list: layout.add_widget(f)
        # 5. MIONDOKO NA MHIMILI (Animation Controls)
        self.f_axis = self.create_field("Mhimili (Axis)", "X, Y, au Z", "Y", readonly=True)
        self.f_axis.bind(on_touch_up=self.open_axis_menu)
        
        self.f_anim_type = self.create_field("Aina ya Miondoko", "static/rotate/slide/both", "static", readonly=True)
        self.f_anim_type.bind(on_touch_up=self.open_anim_menu)
        
        # 6. GIA ZA KWENDA (Forward Gears)
        self.f_speed = self.create_field("Kasi Linear (Kwenda)", "Gia: 0.4, 0.8", "0.4")
        self.f_limit = self.create_field("Ukomo Linear (Kwenda)", "Dist: 0.8, 1.2", "0.8")
        self.f_ang_speed = self.create_field("Kasi Angular (Kwenda)", "Gia: 50, 100", "50.0")
        self.f_ang_limit = self.create_field("Ukomo Angular (Kwenda)", "Deg: 90", "90.0")
        
        # 7. MFUMO WA SAFARI (Loop Control)
        self.f_loop = self.create_field("Loop Mode", "once/ping-pong/custom", "ping-pong", readonly=True)
        self.f_loop.bind(on_touch_up=self.open_loop_menu)
        
        # 8. GIA ZA KURUDI (Backward Gears - Optional)
        self.f_back_speed = self.create_field("Kasi Linear (Kurudi)", "Gia za kurudi", "0.0")
        self.f_back_limit = self.create_field("Ukomo Linear (Kurudi)", "Dist za kurudi", "0.0")
        self.f_back_ang_speed = self.create_field("Kasi Angular (Kurudi)", "Gia za kurudi", "0.0")
        self.f_back_ang_limit = self.create_field("Ukomo Angular (Kurudi)", "Deg za kurudi", "0.0")
        
        # 9. MUDA WA KUSUBIRI (Delays)
        self.f_t_start = self.create_field("Muda wa Kuanza (s)", "Delay start", "0.0")
        self.f_t_return = self.create_field("Muda wa Kurudi (s)", "Delay return", "2.0")

        # Ongeza zilizobaki kwenye layout
        adv_fields = [self.f_axis, self.f_anim_type, self.f_speed, self.f_limit, 
                      self.f_ang_speed, self.f_ang_limit, self.f_loop, 
                      self.f_back_speed, self.f_back_limit, self.f_back_ang_speed, 
                      self.f_back_ang_limit, self.f_t_start, self.f_t_return]
        for f in adv_fields: layout.add_widget(f)
        
        scroll.add_widget(layout)
        
        # Fungua Dialog Kuu
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="BIM Karakana Master"),
            MDDialogContentContainer(scroll),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="GHAIRI"), on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="ONGEZA KAZI"), on_release=self.construct)
            )
        )
        self.dialog.open()
    # --- A: MENU YA MBAO (PRE-LOADED) ---
    def _preload_catalog(self, dt):
        """Inatengeneza items mara moja ili kuongeza spidi"""
        for mti in BONGO_WOOD_CATALOG.keys():
            item = MDMenuItem(
                text=str(mti), 
                on_release=lambda x=str(mti): self.set_wood(x)
            )
            self.cached_menu_items.append(item)

    def open_wood_menu(self, caller):
        if not self.m_wood:
            self.m_wood = MDDropdownMenu(
                caller=caller, items=self.cached_menu_items,
                width_mult=5, max_height="400dp", show_duration=0.1
            )
        self.m_wood.caller = caller
        self.m_wood.open()

    def set_wood(self, jina):
        self.f_wood.text = jina
        if self.m_wood: self.m_wood.dismiss()

    # --- B: MENU YA MHIMILI (AXIS) ---
    def open_axis_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            items = [
                {"text": i, "on_release": lambda x=i: self.set_axis(x)} 
                for i in ["X", "Y", "Z"]
            ]
            self.m_axis = MDDropdownMenu(caller=instance, items=items, width_mult=2)
            self.m_axis.open()

    def set_axis(self, x):
        self.f_axis.text = x
        if hasattr(self, 'm_axis'): self.m_axis.dismiss()

    # --- C: MENU YA MIONDOKO (ANIMATION TYPE) ---
    def open_anim_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            chaguzi = ["static", "rotate", "slide", "both"]
            items = [
                {"text": i, "on_release": lambda x=i: self.set_anim(x)} 
                for i in chaguzi
            ]
            self.m_anim = MDDropdownMenu(caller=instance, items=items, width_mult=3)
            self.m_anim.open()

    def set_anim(self, x):
        self.f_anim_type.text = x
        if hasattr(self, 'm_anim'): self.m_anim.dismiss()

    # --- D: MENU YA MFUMO WA SAFARI (LOOP MODE) ---
    def open_loop_menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            mifumo = ["once", "ping-pong", "custom-back"]
            items = [
                {"text": i, "on_release": lambda x=i: self.set_loop(x)} 
                for i in mifumo
            ]
            self.m_loop = MDDropdownMenu(caller=instance, items=items, width_mult=4)
            self.m_loop.open()

    def set_loop(self, x):
        self.f_loop.text = x
        if hasattr(self, 'm_loop'): self.m_loop.dismiss()
    # ==========================================
    # ⚙️ 3D ENGINE CORE (MATH & PHYSICS)
    # ==========================================
    def rotate_3d(self, x, y, z, rx, ry, rz):
        """Hesabu za kugeuza coordinates kitalamu"""
        ax, ay, az = math.radians(rx), math.radians(ry), math.radians(rz)
        # Mzunguko wa X
        ty = y * math.cos(ax) - z * math.sin(ax)
        tz = y * math.sin(ax) + z * math.cos(ax)
        y, z = ty, tz
        # Mzunguko wa Y
        tx = x * math.cos(ay) + z * math.sin(ay)
        tz = -x * math.sin(ay) + z * math.cos(ay)
        x, z = tx, tz
        # Mzunguko wa Z
        tx = x * math.cos(az) - y * math.sin(az)
        ty = x * math.sin(az) + y * math.cos(az)
        x, y = tx, ty
        return x, y, z

    def project(self, x, y, z):
        """Geuza namba za 3D kuwa picha ya 2D kwenye screen"""
        # Hamisha kulingana na camera
        tx, ty, tz = x - self.cam_x, y - self.cam_y, z - self.cam_z
        # Zungusha kulingana na uelekeo wa camera
        rx, ry, rz = self.rotate_3d(tx, ty, tz, self.cam_rx, self.cam_ry, self.cam_rz)
        # Perspective projection logic
        depth = rz + self.cam_d
        if depth < 0.1: return None
        return (rx * self.f / depth + self.width / 2.0, 
                ry * self.f / depth + self.height / 2.0)

    def run_engine_cycle(self, dt):
        """Huu ndio ubongo unaoendesha gia na miondoko yote"""
        for obj in self.scene_objects:
            a = obj.get("anim")
            if not a or a["type"] == "static": continue
            
            # --- 1. LOGIC YA DELAYS (KUSUBIRI) ---
            if a["state"] == "paused_closed":
                a["timer"] += dt
                if a["timer"] >= a.get("time_before_start", 0):
                    a["state"] = "opening"; a["timer"] = 0; a["curr_step"] = 0
                continue
            elif a["state"] == "paused_open":
                a["timer"] += dt
                if a["timer"] >= a.get("time_before_return", 2):
                    a["state"] = "closing"; a["timer"] = 0; a["curr_step"] = 0
                continue

            # --- 2. CHAGUA GIA KULINGANA NA SAFARI ---
            steps = a["steps"]
            r_steps = a["r_steps"]
            master_steps = r_steps if a["type"] == "rotate" else steps
            if a["type"] == "both":
                master_steps = r_steps if len(r_steps) >= len(steps) else steps

            if a["state"] in ["opening", "closing"]:
                if a["curr_step"] < len(master_steps):
                    direction = 1 if a["state"] == "opening" else -1
                    
                    # TAFUTA INDEX (Reverse vs Custom Back)
                    if a["state"] == "opening":
                        idx = a["curr_step"]
                    else:
                        if a.get("has_custom_back"):
                            # Tumia data maalum za kurudi
                            steps = a.get("back_steps", [])
                            r_steps = a.get("back_r_steps", [])
                            master_steps = r_steps if a["type"] == "rotate" else steps
                            idx = a["curr_step"]
                        else:
                            # Reverse order ya gia za mwanzo
                            idx = (len(master_steps) - 1) - a["curr_step"]

                    # A: TEKELEZA MZUNGUKO (ROTATE)
                    if a["type"] in ["rotate", "both"] and idx < len(r_steps):
                        a["ang_val"] += r_steps[idx]['spd'] * dt * direction
                    
                    # B: TEKELEZA MTEMBEO (SLIDE)
                    if a["type"] in ["slide", "both"] and idx < len(steps):
                        a["val"] += steps[idx]['spd'] * dt * direction

                    # C: TRACK MUDA WA GIA
                    a["step_timer"] += dt
                    if a["step_timer"] >= master_steps[idx]['duration']:
                        a["curr_step"] += 1
                        a["step_timer"] = 0.0
                
                # --- 3. HITIMISHO LA SAFARI ---
                else:
                    if a["state"] == "opening":
                        a["state"] = "paused_open" if a.get("loop_mode") != "once" else "finished_open"
                    else:
                        a["state"] = "paused_closed"
                        # Safisha rounding errors
                        a["val"] = 0.0; a["ang_val"] = 0.0
                    a["curr_step"] = 0; a["step_timer"] = 0.0

        self.render_arch_scene()
    # ==========================================
    # 🎨 RENDERING & MIRROR LOGIC
    # ==========================================
    def render_arch_scene(self, *args):
        self.canvas.clear()
        ground = -1.5
        with self.canvas:
            # GRID ILIYOSHIBA (Mita 1 gap)
            Color(0.5, 0.5, 0.5, 0.18)
            for i in range(-25, 26, 1):
                p1, p2 = self.project(i, ground, -25), self.project(i, ground, 25)
                if p1 and p2: Line(points=[*p1, *p2])
                p3, p4 = self.project(-25, ground, i), self.project(25, ground, i)
                if p3 and p4: Line(points=[*p3, *p4])

        v_u = [(-0.5,0,-0.5),(0.5,0,-0.5),(0.5,1,-0.5),(-0.5,1,-0.5),
               (-0.5,0,0.5),(0.5,0,0.5),(0.5,1,0.5),(-0.5,1,0.5)]
        f_map = [(0,1,2,3),(4,5,6,7),(0,4,7,3),(1,5,6,2),(3,2,6,7),(0,1,5,4)]
        
        # Panga objects kulingana na umbali (Painter's Algorithm)
        sorted_objs = sorted(self.scene_objects, key=lambda x: x.get('_depth_sort', 0), reverse=True)
        mirrors = [o for o in sorted_objs if "kioo" in o.get('id', '').lower()]

        for obj in sorted_objs:
            # 1. Chora object halisi
            self.internal_draw(obj, v_u, f_map)
            # 2. Chora reflection perpendicular kama kuna kioo
            for m in mirrors:
                if obj == m: continue
                m_z = m['pos'][2]
                dist_z = obj['pos'][2] - m_z
                ghost = obj.copy()
                ghost['pos'] = [obj['pos'][0], obj['pos'][1], m_z - dist_z]
                # Fifisha rangi ya reflection (Alpha 0.4)
                base_c = obj.get('color', [0.8, 0.7, 0.5, 1])
                ghost['color'] = [c * 0.5 for c in base_c[:3]] + [0.4]
                self.internal_draw(ghost, v_u, f_map, True)

    def internal_draw(self, obj, v_u, f_map, is_reflect=False):
        """Uchoraji wa kitalamu kwa kutumia Mesh na Shading"""
        w,h,d = obj["dim"]; ox,oy,oz = obj["pos"]; px,py,pz = obj["pivot"]
        ax = obj.get("axis", "Y").upper()
        ang, val = obj["anim"]["ang_val"], obj["anim"]["val"]
        typ = obj["anim"]["type"]
        base_color = obj.get("color", [0.8, 0.7, 0.5, 1])

        for face in f_map:
            pts = []
            for i in face:
                vx_r, vy_r, vz_r = v_u[i]
                vx, vy, vz = vx_r * w - px, vy_r * h - py, vz_r * d - pz
                # Rotation based on specific axis (X, Y, Z)
                rx, ry, rz = self.rotate_3d(vx, vy, vz, 
                                            ang if ax == 'X' else 0, 
                                            ang if ax == 'Y' else 0, 
                                            ang if ax == 'Z' else 0)
                tx, ty = rx + ox + px, ry + oy + py
                tz = rz + oz + pz - (val if typ in ["slide", "both"] else 0)
                p = self.project(tx, ty, tz)
                if p: pts.append(p)
            
            if len(pts) == 4:
                v_list = []
                for pt in pts: v_list.extend([pt[0], pt[1], 0, 0])
                with self.canvas:
                    Color(*base_color)
                    Mesh(vertices=v_list, indices=[0, 1, 2, 2, 3, 0], mode="triangles")

    # ==========================================
    # 🏗️ BIM CONSTRUCTION LOGIC
    # ==========================================
    def construct(self, *args):
        mti = BONGO_WOOD_CATALOG.get(self.f_wood.text, BONGO_WOOD_CATALOG["Mninga (Bloodwood)"])
        def t2l(t): 
            try: return [float(x.strip()) for x in t.split(",")] if "," in t else [float(t)]
            except: return [0.0]
        def build_steps(spd_list, lim_list):
            return [{"spd": s, "duration": abs(l/s) if s!=0 else 0} for s,l in zip(spd_list, lim_list)]

        mpya = {
            "id": self.f_id.text, "axis": self.f_axis.text.upper(),
            "dim": [float(self.f_w.text), float(self.f_h.text), float(self.f_d.text)],
            "pos": [float(self.f_x.text), float(self.f_y.text), float(self.f_z.text)],
            "pivot": [float(self.f_px.text), float(self.f_py.text), float(self.f_pz.text)],
            "color": mti["color"],
            "anim": {
                "type": self.f_anim_type.text.lower(), "state": "paused_closed", "val": 0.0, "ang_val": 0.0,
                "curr_step": 0, "step_timer": 0.0, "timer": 0.0, "loop_mode": self.f_loop.text,
                "time_before_start": float(self.f_t_start.text or 0),
                "time_before_return": float(self.f_t_return.text or 2),
                "steps": build_steps(t2l(self.f_speed.text), t2l(self.f_limit.text)),
                "r_steps": build_steps(t2l(self.f_ang_speed.text), t2l(self.f_ang_limit.text)),
                "has_custom_back": any(x > 0 for x in t2l(self.f_back_speed.text) + t2l(self.f_back_ang.text)),
                "back_steps": build_steps(t2l(self.f_back_speed.text), t2l(self.f_limit.text)),
                "back_r_steps": build_steps(t2l(self.f_back_ang.text), t2l(self.f_ang_limit.text))
            }
        }
        self.scene_objects.append(mpya); self.dialog.dismiss()

    # ==========================================
    # 🕹️ NAVIGATION & DPAD
    # ==========================================
    def on_touch_down(self, t):
        if self.collide_point(*t.pos):
            for w in Window.children:
                if isinstance(w, MDDialog) and w.collide_point(*t.pos): return False
            t.grab(self); self.touches[t.id] = t
            t.ud['mode'] = 'look_around' if t.is_double_tap else 'orbit'
            return True
        return super().on_touch_down(t)

    def on_touch_move(self, t):
        if t.grab_current is self and len(self.touches) == 1:
            if abs(t.dx) > 0.5 or abs(t.dy) > 0.5:
                self.cam_ry += t.dx * 0.45; self.cam_rx -= t.dy * 0.45
                self.cam_ry = round(self.cam_ry, 1); self.cam_rx = round(self.cam_rx, 1)
            return True
        return False

    def on_touch_up(self, t):
        if t.grab_current is self:
            t.ungrab(self); self.touches.pop(t.id, None); return True
        return super().on_touch_up(t)

    def walk_site_dpad(self, dir_key):
        v = 0.8
        if dir_key == "up": self.cam_y += v
        elif dir_key == "down": self.cam_y -= v
        elif dir_key == "left": self.cam_x -= v
        elif dir_key == "right": self.cam_x += v
