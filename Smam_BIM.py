from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFabButton, MDIconButton
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer,MDDialogButtonContainer
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
import json
from SmamMorphEngine import SmamMorphEngine
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTertiaryText,
    MDListItemTrailingCheckbox,
)

from kivy.properties import (
    NumericProperty, 
    ListProperty, 
    ObjectProperty, 
    StringProperty, 
    BooleanProperty  # <--- Ongeza hii hapa!
)
from kivy.core.window import Window
import traceback

# ==========================================
# 🏛️ SMAM_BIM - THE STUDIO INTERFACE
# ==========================================
from kivy.uix.screenmanager import Screen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFabButton
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
import math
from Mahesabu_ya_kabati import Chagua_malighafi,MDFLayout
from kivy.app import App
from kivymd.uix.scrollview import MDScrollView

import random
class Smam_BIM(MDFloatLayout):
    active_mode = StringProperty("walk") # "walk", "look", "orbit"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. ANZA INJINI YA 3D (Tabaka la chini kabisa)
        self.painter = SmamMorphEngine()
        self.add_widget(self.painter)
        self.move_event = None

        # --- A: DASHBOARD HUB (Juu Kulia) ---
        # Hapa kuna Calculator, Workshop (+), na Save
        top_spacing = Window.width * 0.02
        self.menu_box = MDBoxLayout(
            orientation="vertical", 
            adaptive_size=True,
            pos_hint={"right": 0.98, "top": 0.98}, 
            spacing=top_spacing
        )
        self.camera=[]
        from kivy.app import App
        app = App.get_running_app()

        self.files=MDFabButton(
            icon="folder", 
            style="small",
            theme_bg_color="Custom",
            md_bg_color=[0, 0.5, 0.9, 1], # Blue
            radius=(7,7,7,7),
            
        )
        self.chora=MDFabButton(
            icon="plus", 
            style="small",
            theme_bg_color="Custom",
            md_bg_color=[0, 0.5, 0.9, 1], # Blue
            radius=(7,7,7,7),
            on_release=self.painter.show_workshop
        )

        self.calculator=MDFabButton(
            icon="calculator", 
            style="small", 
            theme_bg_color="Custom", 
            md_bg_color=[0, 0.7, 0.4, 1], # Green
            on_release=self.onyesha_quotation_kamili
        )
        
        self.save=MDFabButton(
            icon="content-save", 
            style="small", 
            on_release=self.open_
        )

        # 1. Button ya Ongeza Mbao (+)
        for i in  [self.files,self.chora,self.calculator,self.save]:
                
                    self.menu_box.add_widget(i)
                
        
        self.add_widget(self.menu_box)

        # --- B: MEDIA HUB (Juu Kushoto) ---
        media_box = MDBoxLayout(
            orientation="vertical", 
            adaptive_size=True,
            pos_hint={"x": 0.02, "top": 0.98}, 
            spacing=top_spacing
        )
        self.rangi=self.create_media_btn("format-paint", [0.9, 0.2, 0.2, 1], self.anza_kurekodi)
        media_box.add_widget(self.create_media_btn("camera-plus-outline", [0, 0.7, 0.7, 1], self.painter.piga_picha))
        media_box.add_widget(self.rangi)
        media_box.add_widget(self.create_media_btn("label-outline", [1, 1, 1, 0.8], self.maconstants))
        def fungua(e):
            self.onyesha_msimamizi_wa_vifaa()
            try:self.manager_dialog.open()
            except:self.painter.update_status(traceback.format_exc(),True)
        self.add_widget(media_box)
                # Ndani ya __init__ -> Media Hub
        # Badala ya self.onyesha_vitu_vyote, iite hii mpya:
        media_box.add_widget(self.create_media_btn("layers-outline", [1, 0.8, 0.2, 1], fungua))


        # --- C: UNIVERSAL NAVIGATION HUB (Chini Kushoto) ---
        # Inadhibiti Walk, Look, na Orbit
        self.left_hub = MDBoxLayout(
            adaptive_size=True, 
            pos_hint={"x": 0.02, "y": 0.05}, 
            spacing=Window.width * 0.03
        )
        
        # Gia Toggle
        self.btn_mode = MDIconButton(
            icon="shoe-print", 
            icon_color=[0, 1, 0.7, 1], 
            on_release=self.cycle_modes, 
            font_size=Window.width * 0.12
        )
        
        u_pad = MDBoxLayout(orientation="vertical", adaptive_size=True, spacing=2)
        mid__row = MDBoxLayout(adaptive_size=True, spacing=10)
        mid__row.add_widget(MDBoxLayout(adaptive_size=True, spacing=10))
        mid__row.add_widget(self.create_universal_btn("chevron-up", "up"))
        u_pad.add_widget(mid__row)
        mid_row = MDBoxLayout(adaptive_size=True, spacing=10)
        mid_row.add_widget(self.create_universal_btn("chevron-left", "left"))
        mid_row.add_widget(self.create_universal_btn("chevron-down", "down"))
        mid_row.add_widget(self.create_universal_btn("chevron-right", "right"))
        
        u_pad.add_widget(mid_row)
        self.left_hub.add_widget(self.btn_mode)
        self.left_hub.add_widget(u_pad)
        self.add_widget(self.left_hub)

        # --- D: ELEVATION HUB (Chini Kulia) ---
        # Elevation na Sun Control pekee
        right_hub = MDBoxLayout(
            orientation="vertical", 
            adaptive_size=True, 
            pos_hint={"right": 0.98, "y": 0.05}, 
            spacing=Window.height * 0.015
        )
        right_hub.add_widget(MDIconButton(icon="white-balance-sunny", on_release=lambda x:self.move_sun("up") ))#
        right_hub.add_widget(self.create_elev_btn("chevron-double-up", "up"))
        right_hub.add_widget(self.create_elev_btn("chevron-double-down", "down"))
        right_hub.add_widget(MDIconButton(icon="moon-waning-crescent", on_press=lambda x: self.move_sun("down")))
        self.add_widget(right_hub)
        #Clock.schedule_interval(self.onyesha_msimamizi_wa_vifaa,2)
    # ==========================================
    # ⚙️ LOGIC & HELPER METHODS
    # ==========================================

    def open_(self, *args):
        list_ya_mbao = MDBoxLayout(orientation="vertical", spacing=1, size_hint_y=None)
        list_ya_mbao.bind(minimum_height=list_ya_mbao.setter('height'))
        mdf_zilizopangwa=self.painter.mahesabu.mbao_zinazohitajika()['boards']
        print(mdf_zilizopangwa)
        lebo_vipimo0 = MDLabel(text=f"Mpaka sasa kazi hii inahitaji board(s) {len(mdf_zilizopangwa)}", markup=True,theme_height='Custom', size_hint_y=None, height=5,role='small')
            
        for mdf in mdf_zilizopangwa:
            mdf_box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=380)
            
            lebo_vipimo = MDLabel(text=f"{mdf['board_id']} itakatwa kama unavyoona chini hapo", markup=True,theme_height='Custom', size_hint_y=None, height=5,role='small')
            
            # Hapa sasa ndio unaita ile Widget ya kuchora pale unapohitaji ionekane
            visualizer = MDFLayout(mdf_data=mdf, status_label=lebo_vipimo0,id=mdf['board_id'], size_hint_y=None, height=300)
            mdf_box.add_widget(lebo_vipimo)
            
            mdf_box.add_widget(visualizer)
            list_ya_mbao.add_widget(mdf_box)
        self.boards=ScrollView(     
            size_hint=(1, None),
            height="400dp",
            scroll_timeout=500,
            #effect_cls='ScrollEffect',
            #scrollbar_swiping=True
        )
        try:self.boards.add_widget(list_ya_mbao)
        except:
            list_ya_mbao.patrent.remove_widget(list_ya_mbao)
            self.boards.add_widget(list_ya_mbao)
        self.popup = MDDialog(
            MDDialogHeadlineText(text="Mpangilio wa namna panels zitakatwa kutoka kwenye BOARD",role='small'),
            MDDialogContentContainer(
                self.boards,
                orientation='vertical'
            ),
            MDDialogButtonContainer(
                lebo_vipimo0
            ),
            radius=(7,7,7,7),
            theme_height='Custom',
            adaptive_height=True,
            height=0.5*Window.height,
            opacity=0
        )
        self.popup.open()

    def cycle_modes(self, instance, *args):
        #("orbit", [1,0.5,0,1], "orbit"), 
        #         "orbit": 
        modes = {"walk": ("eye-outline", [1,1,1,0.8], "look"), 
                 "look": ("shoe-print", [0,1,0.7,1], "walk")}
        icon, color, next_m = modes[self.active_mode]
        instance.icon, instance.icon_color, self.active_mode = icon, color, next_m
        #self.painter.update_status(f"Camera_man wetu {random.choice(app.fundi)} ame_move hadi :: Mahali: ({round(self.painter.cam_x,0),round(self.painter.cam_y,0),round(self.painter.cam_z)}) | Uelekeo: ({round(self.painter.cam_rx, 0),round(self.painter.cam_ry, 0)})\n\n")
            
    def handle_universal_press(self, direction):
        app=App.get_running_app()
        if self.move_event: self.move_event.cancel()
        def execute(dt):
            m = self.active_mode
            if m == "walk":
                d_map = {"up":"forward","down":"backward","left":"left","right":"right"}
                self.painter.move_eye(d_map[direction])
                #self.painter.update_status(f"Camera_man {random.choice(app.fundi)} wetu ame_move mpaka ::Mahali: ({round(self.painter.cam_x,0),round(self.painter.cam_y,0),round(self.painter.cam_z)}) | Uelekeo: ({round(self.painter.cam_rx, 0),round(self.painter.cam_ry, 0)})\n\n\n")
            elif m == "look":
                spd = 1.8
                if direction=="up": self.painter.cam_rx-=spd
                elif direction=="down": self.painter.cam_rx+=spd
                elif direction=="left": self.painter.cam_ry-=spd
                elif direction=="right": self.painter.cam_ry+=spd
                self.painter.cam_rx = max(-85, min(85, self.painter.cam_rx))
                
            elif m == "orbit":
                spd = 2000
                if direction=="up": self.painter.world_rot_x+=spd
                elif direction=="down": self.painter.world_rot_x-=spd
                elif direction=="left": self.painter.world_rot_y-=spd
                elif direction=="right": self.painter.world_rot_y+=spd
            self.painter.render_arch_scene()
        self.move_event = Clock.schedule_interval(execute, 1/35)

    def create_universal_btn(self, icon, d):
        return MDIconButton(icon=icon, theme_icon_color="Custom", icon_color=[1,1,1,0.7], 
                            font_size=Window.width*0.11, on_press=lambda x: self.handle_universal_press(d), 
                            on_release=self.stop_walking)

    def create_elev_btn(self, icon, d):
        return MDIconButton(icon=icon, theme_icon_color="Custom", icon_color=[1,1,1,0.6], 
                            font_size=Window.width*0.1, on_press=lambda x: self.start_elevation(d), 
                            on_release=self.stop_walking)

    def start_elevation(self, d):
        if self.move_event: self.move_event.cancel()
        self.move_event = Clock.schedule_interval(lambda dt: self.painter.move_eye(d), 1/35)

    def stop_walking(self, *args):
        if self.move_event: self.move_event.cancel(); self.move_event = None

    def move_sun(self, d):
        # Muda unacheza kati ya 0 (Asubuhi) na 10 (Jioni)
        step = 0.2
        if d == "up":
            self.painter.light_y = min(10.0, self.painter.light_y + step)
        else:
            self.painter.light_y = max(0.0, self.painter.light_y - step)
            
        self.painter.canvas.clear()
        self.painter.render_arch_scene()

    def onyesha_quotation_kamili(self, *args):
        objects=[]
        quot_but=MDButton(on_release=self.painter.bonyeza_tengeneza_quotation)
        quot_but.add_widget(MDButtonText(text='Funga_MAHESABU'))
        for i in self.painter.scene_objects:
            if i.get('visible')==True:
                objects.append(i)
        mbao_uwanjani = objects
        if not mbao_uwanjani:
            self.painter.render_arch_scene()
            self.painter.update_status("Chora kwanza!", True)
            return
        
        hesabu_engine = self.painter.mahesabu
        #hesabu_engine.kazi = self 
        hesabu_engine.anza_kuchakata_mita(mbao_uwanjani)
        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
        cont=MDDialogContentContainer()
        lbl=MDDialogButtonContainer()
        try:cont.add_widget(hesabu_engine.scrll)
        except:
            hesabu_engine.scrll.parent.remove_widget(hesabu_engine.scrll)
            cont.add_widget(hesabu_engine.scrll)
            #self.painter.update_status("Nakuja nakuja....!", True)
        try:lbl.add_widget(quot_but)
        except:pass
        try:lbl.add_widget(hesabu_engine.salamu)
        except:
            hesabu_engine.salamu.parent.remove_widget(hesabu_engine.salamu)
            lbl.add_widget(hesabu_engine.salamu)
            #self.painter.update_status("Nakuja nakuja....!", True)
        self.quote_dialog = MDDialog(
            
            MDDialogHeadlineText(text=f"Mahitaji na gharama za kazi ya {self.painter.current_mteja.upper()}\n[{self.painter.project_name}]"),
            cont,
            radius=(7,7,7,7),
        )
        try:self.quote_dialog.add_widget(lbl)
        except:print('ngweee!')
        try:self.quote_dialog.open()
        except:self.painter.update_status(traceback.format_exc(), True)

    def create_media_btn(self, icon, color, action):
        return MDIconButton(icon=icon, theme_icon_color="Custom", icon_color=color, 
                            on_release=action, font_size=Window.width*0.08)

    def piga_picha(self, *args): pass
    def anza_kurekodi(self, *args):
        self.painter.badili_rangi(self.rangi)
    def save_to_database(self, *args):
        self.painter.bonyeza_tengeneza_quotation()
    def rejesha_kumbukumbu(self, mteja_id): pass

    

    def maconstants(self, *args):
        def malizana(e):
            self.settings.dismiss()
            self.painter.malizana()  
            self.painter.render_arch_scene()      
        scrolll = MDScrollView(
            size_hint=(1, None),
            height="400dp",
            scroll_timeout=200,
            #effect_cls='ScrollEffect'
        ) # Urefu wa list
        try:
            scrolll.add_widget(self.painter.constanti)
        except:
            self.painter.constanti.parent.remove_widget(self.painter.constanti)
            scrolll.add_widget(self.painter.constanti)
        self.settings = MDDialog(
            MDDialogHeadlineText(text="Maconstants"),
            MDDialogContentContainer(scrolll, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="UNYAMA"), 
                    style="filled",
                    on_release=malizana
                ),
            ),
            radius=(7,7,7,7)
        )
        self.settings.open()

    def onyesha_msimamizi_wa_vifaa(self, *args):
        """Inafungua Dialog yenye list ya mbao zote na hali zake (Visible/Hidden)"""
        from kivymd.uix.list import MDListItem, MDListItemTrailingCheckbox, MDListItemHeadlineText
        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
        from kivymd.uix.button import MDButton, MDButtonText
        #from kivymd.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout

        container = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing="10dp")
        scroll = ScrollView(
            size_hint=(1, None),
            height="400dp",
            scroll_timeout=500,
            #effect_cls='ScrollEffect'
        )
        
        mbao_uwanjani = self.painter.scene_objects
        if not mbao_uwanjani:
            #self.painter.update_status("Hakuna vifaa uwanjani!", True)
            return
        
        if self.painter.maboresho_sort==1:
            aa,bb=1,0
            mw=1
        else:
            aa,bb=-1,-1
            mw=0

        # 1. JENGA LIST YA MBAO
        for i in range (len(mbao_uwanjani)):
            indx=aa*i+bb*1
            #if i== len(mbao_uwanjani)-1 and self.painter.maboresho_sort != 1:
            #    indx=0
            obj=mbao_uwanjani[indx]
            is_visible = obj.get('visible', True)
            item=edit(obj['id'],self.painter)
            item.add_widget(MDListItemHeadlineText(text=f"{obj['id']}"))
            check = MDListItemTrailingCheckbox(active=is_visible)
            check.bind(active=lambda cb, value, target_obj=obj: self.badili_hali_ya_mbao(target_obj, value))
            
            item.add_widget(check)
            container.add_widget(item)
        
        scroll.add_widget(container)

        

        def close(e):
            self.painter.trigger_auto_save()
            self.manager_dialog.dismiss()
            self.painter.render_arch_scene()

        # 2. DIALOG YA MSIMAMIZI
        self.manager_dialog = MDDialog(
            
            MDDialogHeadlineText(text="Muundo wa fenicha"),
            MDDialogContentContainer(scroll, orientation="vertical"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="ONYESHA ZOTE"), on_release=self.washa_zote_fast),
                MDBoxLayout(), # Spacer
                MDButton(MDButtonText(text="TAYARI"), style="filled", on_release=close ),
            ),
            radius=(5,5,5,5),
        )
        

    def badili_hali_ya_mbao(self, obj, hali):
        """Inabadilisha visibility ya mbao moja kwa moja toka kwenye list"""
        obj['visible'] = hali
        self.painter.trigger_auto_save()
        #

    def washa_zote_fast(self, *args):
        """Quick Action: Washa mbao zote uwanjani"""
        for obj in self.painter.scene_objects:
            obj['visible'] = True
        self.painter.canvas.clear()
        self.painter.render_arch_scene()
        if hasattr(self, 'manager_dialog'): self.manager_dialog.dismiss()

    def auto_save(self, *args):
        """Auto-save yenye ulinzi wa chuma dhidi ya uwanja mweupe"""
        try:
            import sqlite3
            import json
            import os
            from kivy.app import App

            # --- HATUA YA 1: ULINZI (The Guard) ---
            # Tunachukua mbao zilizopo kwenye painter
            mbao_uwanjani = getattr(self.painter, 'scene_objects', [])
            
            # KAMA UWANJA NI MWEUPE, USISAVE CHOCHOTE!
            if not mbao_uwanjani or len(mbao_uwanjani) == 0:
                # Hii inazuia kufuta data za zamani kwenye DB kama uwanja haujapakia
                print("⚠️ Auto-save imesitishwa: Uwanja hauna mbao (Ulinzi wa Overwrite).")
                return

            # --- HATUA YA 2: ANDAA DATA ---
            app = App.get_running_app()
            db_path = os.path.join(app.db_path, "BIM_Factory.sqlite")
            
            m_id = str(getattr(self, 'current_mteja_id', 'N/A'))
            m_jina = str(getattr(self, 'current_mteja', 'Mteja_Mpya'))
            aina_kazi = str(getattr(self, 'project_name', 'Fenicha'))
            
            # Geuza mchoro kuwa maandishi (JSON)
            mchoro_json = json.dumps(mbao_uwanjani)

            # --- HATUA YA 3: HIFADHI KWENYE SQLITE ---
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Hakikisha table ipo
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS miradi_ya_fenicha (
                    mteja_id TEXT PRIMARY KEY,
                    jina_la_mteja TEXT,
                    aina_ya_fenicha TEXT,
                    data_ya_mchoro TEXT,
                    tarehe_ya_kazi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tumia UPSERT (Insert au Update kama ID ipo)
            cursor.execute('''
                INSERT INTO miradi_ya_fenicha (mteja_id, jina_la_mteja, aina_ya_fenicha, data_ya_mchoro) 
                VALUES (?, ?, ?, ?)
                ON CONFLICT(mteja_id) DO UPDATE SET
                    data_ya_mchoro = excluded.data_ya_mchoro,
                    tarehe_ya_kazi = CURRENT_TIMESTAMP
            ''', (m_id, m_jina, aina_kazi, mchoro_json))

            conn.commit()
            conn.close()
            
            print(f"✅ BIM: Mchoro wa {m_jina} umehifadhiwa kitalamu.")

        except Exception as e:
            print(f"BIM Database Error: {e}")



class edit(MDListItem):
    def __init__(self,oid,painter,**kwargs):
        super().__init__(**kwargs)
        #self.dabo=False
        self.painter=painter
        self.oid=oid
        #self.add_widget(ht)
        
    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                try:self.painter.workshop_dialog.dismiss()
                except:
                    print('haina noma')
                try:
                    for obj in self.painter.scene_objects:
                        if obj['id']==self.oid:
                            self.painter.open_edit_workshop(obj)
                            print('unyama!')
                            return super().on_touch_up
                
                except Exception as e:
                    #print(self.id)
                    
                    print(e)
                
                #return True
        #self.double_touch=False
        return super().on_touch_up   
