import math

class BIMGeometryFactory:
    """
    MODULI YA MAUMBO (GEOMETRY MODELS LIBRARY)
    Kazi: Kuzalisha data za kijiometri, miondoko, na maumbo tata.
    Inatoa 'Dictionary' ambayo MorphEngine inaweza kuichora moja kwa moja.
    """

    @staticmethod
    def get_base_template(id_name, dim, pos=[0.0, -1.0, 0.0], color=[0.8, 0.7, 0.5, 1]):
        """Template mama ya mbao/umbo lolote uwanjani."""
        return {
            "id": id_name,
            "parent_id": "",         # Inatumika kwa uhusiano wa Parent-Child
            "dim": [float(d) for d in dim],
            "pos": [float(p) for p in pos],
            "pivot": [0.0, 0.0, 0.0],
            "axis": "Y",             # Mhimili wa mzunguko
            "slide_vec": [0.0, 0.0, 1.0], # Mhimili wa mtembeo (Default: Z)
            "linear_vec": [0.0, 0.0, 1.0], # Mwelekeo wa mtembeo
            "color": color,
            "custom_vertices": None, # Kama ni None, injini inachora box
            "shade": 0.05,
            "anim": {
                "type": "static", 
                "state": "paused_closed",
                "val": 0.0, 
                "ang_val": 0.0, 
                "curr_step": 0, 
                "step_timer": 0.0,
                "timer": 0.0, 
                "loop_mode": "ping-pong",
                "has_custom_back": False,
                "time_before_start": 0.0,
                "time_before_return": 2.0,
                "steps": [],        # Linear Forward
                "r_steps": [],      # Angular Forward
                "back_steps": [],   # Linear Backward
                "back_r_steps": []  # Angular Backward
            }
        }

    # ==========================================
    # 1. MAUMBO YA KAWAIDA (BASIC FORMS)
    # ==========================================
    
    @classmethod
    def create_board(cls, id_name, w, h, d, pos=[0, -1, 0], color=[0.8, 0.7, 0.5, 1]):
        """Mbao/Panel ya mstatili ya kawaida."""
        return cls.get_base_template(id_name, [w, h, d], pos, color)

    @classmethod
    def create_mirror(cls, id_name, w, h, d, pos=[0, -1, 0]):
        """Kioo (Mirror) - Tayari kimeshasetiwa rangi ya kioo na ID inayotambulika na injini."""
        # ID lazima iwe na neno 'kioo' ili MorphEngine ifanye reflection logic
        real_id = f"kioo_{id_name}" if "kioo" not in id_name.lower() else id_name
        data = cls.get_base_template(real_id, [w, h, d], pos, color=[0.9, 0.95, 1.0, 0.6])
        return data

    # ==========================================
    # 2. MAUMBO YA ELEVATION (PROFILE MODELS)
    # ==========================================

    @classmethod
    def create_slope(cls, id_name, w, h, d, side="right", pos=[0, -1, 0]):
        """Mbao yenye mshazari (Diagonal/Slope) - Kwa kabati za chini ya ngazi."""
        v = [
            (-0.5, 0, -0.5), (0.5, 0, -0.5), (0.5, 1, -0.5), (-0.5, 1, -0.5), # Mbele
            (-0.5, 0, 0.5),  (0.5, 0, 0.5),  (0.5, 1, 0.5),  (-0.5, 1, 0.5)   # Nyuma
        ]
        if side == "right":
            v[2] = (0.5, 0, -0.5); v[6] = (0.5, 0, 0.5) # Shusha Top-Right
        else:
            v[3] = (-0.5, 0, -0.5); v[7] = (-0.5, 0, 0.5) # Shusha Top-Left
            
        data = cls.get_base_template(id_name, [w, h, d], pos)
        data["custom_vertices"] = v
        return data

    @classmethod
    def create_triangle_elevation(cls, id_name, w, h, d, pos=[0, -1, 0]):
        """Umbo la pembe tatu kamili (Triangle Profile)."""
        v = [
            (-0.5, 0, -0.5), (0.5, 0, -0.5), (0.0, 1, -0.5), (0.0, 1, -0.5), # Mbele
            (-0.5, 0, 0.5),  (0.5, 0, 0.5),  (0.0, 1, 0.5),  (0.0, 1, 0.5)   # Nyuma
        ]
        data = cls.get_base_template(id_name, [w, h, d], pos)
        data["custom_vertices"] = v
        return data

    @classmethod
    def create_trapezoid(cls, id_name, w, h, d, top_ratio=0.6, pos=[0, -1, 0]):
        """Umbo la Trapezoid (Mstatili uliopungua upana kwa juu)."""
        offset = (1.0 - top_ratio) / 2.0
        v = [
            (-0.5, 0, -0.5), (0.5, 0, -0.5), 
            (0.5 - offset, 1, -0.5), (-0.5 + offset, 1, -0.5), # Mbele
            (-0.5, 0, 0.5),  (0.5, 0, 0.5),  
            (0.5 - offset, 1, 0.5),  (-0.5 + offset, 1, 0.5)   # Nyuma
        ]
        data = cls.get_base_template(id_name, [w, h, d], pos)
        data["custom_vertices"] = v
        return data

    # ==========================================
    # 3. MAUMBO TATA (POLYGONS & ARCS)
    # ==========================================

    @classmethod
    def create_arch_top(cls, id_name, w, h, d, segments=16, pos=[0, -1, 0]):
        """Mbao yenye nusu duara kwa juu (Arch Profile)."""
        v = []
        # Chini (Base)
        v.extend([(-0.5, 0, -0.5), (0.5, 0, -0.5)]) 
        # Arc points (Mbele)
        for i in range(segments + 1):
            theta = math.pi * (i / segments)
            vx = 0.5 * math.cos(theta)
            vy = 1.0 + 0.3 * math.sin(theta)
            v.append((-vx, vy, -0.5))
        
        # (Inahitaji injini iweze ku-render Custom Poly - inatoa data ya vertices)
        data = cls.get_base_template(id_name, [w, h, d], pos)
        data["custom_vertices"] = v
        return data

    # ==========================================
    # 4. COMPONENTS (MIGUU, VISHIKIO, NGUZO)
    # ==========================================

    @classmethod
    def create_table_leg(cls, id_name, h, thickness=0.05, pos=[0, -1, 0], style="square"):
        """Mguu wa meza (Square au Tapered/Unaochongoka)."""
        data = cls.get_base_template(id_name, [thickness, h, thickness], pos)
        if style == "tapered":
            v = [
                (-0.2, 0, -0.2), (0.2, 0, -0.2), (0.5, 1, -0.5), (-0.5, 1, -0.5),
                (-0.2, 0, 0.2),  (0.2, 0, 0.2),  (0.5, 1, 0.5),  (-0.5, 1, 0.5)
            ]
            data["custom_vertices"] = v
        return data

    @classmethod
    def create_cylinder_sim(cls, id_name, r, h, pos=[0, -1, 0], segments=12):
        """Nguzo/Cylinder (Simulation kupitia pointi za mduara)."""
        v = []
        for i in range(segments):
            theta = 2 * math.pi * (i / segments)
            vx, vz = r * math.cos(theta), r * math.sin(theta)
            v.append((vx, 0, vz)) # Bottom
            v.append((vx, 1, vz)) # Top
        data = cls.get_base_template(id_name, [1, h, 1], pos)
        data["custom_vertices"] = v
        return data

    @classmethod
    def create_handle(cls, id_name, length, pos=[0, 0, 0], color=[0.8, 0.7, 0.2, 1]):
        """Kishikio (Handle) cha fenicha (Gold/Silver style)."""
        return cls.get_base_template(id_name, [length, 0.02, 0.03], pos, color)

    # ==========================================
    # 5. MODULAR SETS (RAFU/SHELVES)
    # ==========================================

    @classmethod
    def create_shelf_set(cls, parent_id, w, d, count=3, start_y=-0.8, gap=0.4):
        """Zalisha list ya rafu (Shelves) zinazotegemea parent mmoja."""
        shelves = []
        for i in range(count):
            y_pos = start_y + (i * gap)
            s = cls.create_board(f"{parent_id}_shelf_{i}", w, 0.018, d, pos=[0, y_pos, 0])
            s["parent_id"] = parent_id
            shelves.append(s)
        return shelves

# --- MWISHO WA MODULI ---
