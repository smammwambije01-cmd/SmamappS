from kivymd.uix.button import MDButton,MDButtonText,MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox,MDSwitch
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem,MDNavigationRailMenuButton,MDNavigationRailItemLabel,MDNavigationRailFabButton,MDNavigationRailItemIcon
from kivy.metrics import dp
import random
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
#from kivymd.uix.loadingindicator import MDLoadingIndicator

from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
    VariableListProperty,
    BooleanProperty
)
import Vipimo
from kivy import Logger
from kivy.animation import Animation, AnimationTransition
from kivy.graphics import PopMatrix, PushMatrix, Scale
from kivy.clock import Clock
import threading
from kivymd.uix.progressindicator import MDLinearProgressIndicator
#from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock           
import os
from kivy.core.window import Window
#Window.softinput_mode = "pan"
#from kivy.core.window import Window

# 'p
# Optional: Add a smooth animation for the movement
#Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}

main_dict={}

lengo=''

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationrail import (
    MDNavigationRail, 
    MDNavigationRailItem, 
    MDNavigationRailMenuButton,
    MDNavigationRailItemIcon,
    MDNavigationRailItemLabel
)
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock

class Rail_box(MDGridLayout):
    def __init__(self, faili, items, chini=ObjectProperty(None, allownone=True), faili1='', **kwargs):
        super().__init__(**kwargs)
        self.faili = faili1
        self.cols = 2
        self.chini = chini
        
        # 1. MFUMO WA DATA (Daraja la kuunganisha na main.py)
        # Hii list ndiyo itaruhusu main.py ku-bind matukio ya uchoraji
        self.rail_items = [] 

        self.nje = MDGridLayout(spacing=5, cols=2)
        self.ndani = MDGridLayout(padding=5, cols=1, spacing=200)
        self.ndani_kabisa = MDGridLayout(cols=2)

        # BOX CLASS YA NDANI
        class Box(MDRelativeLayout):
            def __init__(slf, **kwargs):
                super().__init__(**kwargs)
                slf.pos_hint = {"top": 0}
                slf.spacing = 5
                slf.md_bg_color = 'grey'
        
        self.box = Box()

        # 2. NAVIGATION RAIL SETUP
        self.nav = nav_r = MDNavigationRail(
            anchor='bottom', 
            md_bg_color='grey', 
            type='labeled', 
            size_hint=(0.175, 0.75)
        )
        
        # Menu Button (Mafaili)
        self.files = MDNavigationRailMenuButton(icon="folder-outline")
        label_0 = MDNavigationRailItemLabel(font_size=10, text='Mafaili', text_color='yellow')
        self.files.add_widget(label_0) 
        nav_r.add_widget(self.files)

        # 3. LOOP YA KUTENGENEZA MBAO (Items)
        ktu = {}
        for jina in items:
            # Create the Item
            kitu = MDNavigationRailItem()
            
            # --- UNYAMA WA DATA ---
            # Tunapachika 'key' (mfano: 'Top') ndani ya item ili main.py iidake
            kitu.key = jina 
            
            icon_k = MDNavigationRailItemIcon(
                size_hint=(0.075, 1), 
                icon=items[jina].get('icon', 'hammer-wrench')
            )
            label_k = MDNavigationRailItemLabel(
                font_size=10, 
                text=items[jina].get('jina', jina), 
                text_color='yellow'
            )
            
            # KivyMD Internal Linking
            kitu._navigation_rail = nav_r
            icon_k._navigation_rail = nav_r
            
            kitu.add_widget(icon_k)
            kitu.add_widget(label_k)
            nav_r.add_widget(kitu)
            
            # IJAZIE LIST YA GLOBAL ITEMS
            self.rail_items.append(kitu)
            ktu[jina] = kitu

        # 4. LOGIC YA MAFAILI NA MTEJA
        def mteja(e):
            self.ndani.clear_widgets()
            if self.faili != '':
                self.faili.nav_rail = nav_r
                self.ndani.add_widget(self.faili) 

        if self.faili != '':
            self.faili.rail = self
            self.faili.items = items
            self.faili.ktu = ktu
            self.faili.prnt = self.ndani
            self.faili.ndani_kabisa = self.ndani_kabisa
            self.files.bind(on_release=mteja)
            self.faili.ndani = self.ndani
            self.faili.chini = self.chini
            self.faili.g_prnt = self.nje
        else:
            # Kama hakuna faili, bind vipimo vya kawaida
            for i in items:
                self.vipimo(ktu[i], items[i]['kazi'])

        # 5. ASSEMBLE UI
        self.nje.add_widget(nav_r)
        self.nje.add_widget(self.ndani)
        self.add_widget(self.nje)
        
    def vipimo(self, itm, ftn):
        def dd(e):
            try:
                self.ndani_kabisa.clear_widgets()
                self.ndani.add_widget(self.ndani_kabisa)
            except: pass
            self.ndani_kabisa.add_widget(ftn)
            try:
                if self.chini is not None: 
                    self.ndani.add_widget(self.chini)
            except: pass
        itm.bind(on_release=dd)
        
    def show_popup(self, *args):
        if hasattr(self, 'popup_box'):
            anim = Animation(pos_hint={"center_x": 0.5, "top": 1.2}, duration=0.3)
            anim.start(self.popup_box)
        
    def hide_popup(self, *args):
        if hasattr(self, 'input_field'):
            self.input_field.focus = False
            anim = Animation(pos_hint={"center_x": 0.5, "top": 0}, duration=0.2)
            anim.start(self.popup_box)






