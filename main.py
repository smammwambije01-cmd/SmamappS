import sys 
sys.path.append('/home/smam_mwambije/SmamappS/stanvirt/lib/python3.10/site-packages')
from kivy.config import Config
from kivy.animation import Animation
from kivy.utils import get_color_from_hex 
from kivy.uix.scrollview import ScrollView
# --- Kivy & KivyMD Base Imports ---
#from kivymd.uix.scrollview import ScrollView
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTrailingSupportingText,
    MDList
)
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText

import sqlite3
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.stacklayout import MDStackLayout

from kivy.utils import platform
from kivymd.uix.navigationrail import MDNavigationRailItem, MDNavigationRailItemIcon
if platform not in ['android', 'ios']:
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '750')
    Config.set('graphics', 'resizable', '1')
    # Hii inasaidia sana WSL isigande (Disable anti-aliasing)
    Config.set('graphics', 'multisamples', '0') 
# 1. Define the fix. Use 'self' so Python treats it as a method.
def anim_complete(self, *args):
    # Safely get the rail. If it's missing, 'rail' will be None.
    rail = getattr(self, "_navigation_rail", None)
    
    # If this is an Icon, we need the actual Item it belongs to.
    item = getattr(self, "_navigation_item", self)
    
    # Only call the method if the rail still exists in memory.
    if rail and hasattr(rail, "set_active_item"):
        rail.set_active_item(item)

# 2. Overwrite the methods in both classes using the original name.
MDNavigationRailItem.anim_complete = anim_complete
MDNavigationRailItemIcon.anim_complete = anim_complete
import random,re
from kivy.clock import Clock     
import os
os.environ['KIVY_NO_CONFIG'] = '1'
os.environ['KIVY_NO_FILELOG'] = '1'
import os
import os
import sys
import estimator_widget as e_w
from Smam_BIM import Smam_BIM
from Smam_FORMS import BIMGeometryFactory
import traceback

try:
    from fpdf import FPDF
    print("FPDF imepatikana!")
except ImportError:
    print("Bado haionekani, cheki kama folder lipo hapa!")
# Hii inaiambia Python iangalie kwanza folder la project yako
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Path for your database or files
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_SECURE_SETTINGS])
    
    # This is the safe private internal folder on Android
    user_data_dir = os.getenv('PYTHON_EGGS', '/data/user/0/org.test.karakana/files/app')
    # Or even simpler:
    internal_path = os.path.dirname(os.path.abspath(__file__))
else:
    internal_path = os.getcwd()

print(f"App is using path: {internal_path}")
from kivy.metrics import dp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.navigationdrawer import (
    MDNavigationLayout, MDNavigationDrawer, MDNavigationDrawerMenu, 
    MDNavigationDrawerLabel, MDNavigationDrawerItem, MDNavigationDrawerItemLeadingIcon, 
    MDNavigationDrawerItemText, MDNavigationDrawerItemTrailingText, 
    MDNavigationDrawerDivider
)
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

import mbaompya as mmpy
import MisumariGui,Misumari,Kabati
from kivy.core.window import Window
import Vipimo,Rail_box,Maelezo,Mahesabu_ya_kabati
# 'pan' moves the entire window up so the focused text field is visible
#.softinput_mode = "pan"

# Optional: Add a smooth animation for the movement
#Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
# A specialized mode that tries to keep the keyboard strictly below the text input.
#Window.softinput_mode = "below_target"
#: Resizes your layout to fit the remaining space; use this if your popup is inside a ScrollView
#Window.softinput_mode = "resize"

import sys
from kivy.logger import Logger

class LogStream:
    def __init__(self, painter):
        self.painter = painter
    def write(self, s):
        if s.strip():
            # Tuma kosa moja kwa moja kwenye ule ubao wako wa Status
            self.painter.update_status(f"Err: {s[:40]}", is_error=True)
        Logger.error(f"Console: {s}")
    def flush(self): pass

# Ndani ya KarakanaApp kwenye on_start au build:
# sys.stderr = LogStream(self.engine_3d.painter)


class KarakanaApp(MDApp):
    def on_start(self):
        print(">>> WINDOW TAYARI! Kama huioni, basi imejificha nyuma ya terminal.")
        sys.stderr = LogStream(self.engine_3d.painter)
        #self.update_status=self.painter.update_status

    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_SECURE_SETTINGS
            ])
        # 1. Setup the Content Area (Screen Manager)
        self.m_id=0
        
        self.manager = MDScreenManager()
        self.bidhaa_list=[]
        self.bidhaa_jina=StringProperty()
        self.bidhaa_jina1=StringProperty()
        self.bidhaa_jina4=StringProperty()
        self.bidhaa_jina5=ObjectProperty()
        self.uchoraji_rail=MDLabel()
        self.mteja=StringProperty()
        self.bidhaa_jina2=[]
        self.bidhaa_jina3=[]
        self.bidhaa_itm=ObjectProperty()
        self.drop_menu=ObjectProperty()
        self.content_screen = MDScreen()
        self.manager.add_widget(self.content_screen)
        self.engine_3d = Smam_BIM()
        sys.stderr = LogStream(self.engine_3d.painter)
        #Clock.schedule_once(self.lete_mzigo , 1)
        self.fundi=['Stany_BABE','Stany_MAMBAO','Fundi_KIBUKTA','Mr_Mambao','Mr_SMAM','Mr_MIMI','Mr_MWAMBIJE']
        def pp(q):
            print(self.nav_drawer)
            self.nav_drawer.set_state("open")
        btn_open = MDButton(
            MDButtonText(text="Fungua Menu"),
            on_release=pp,
            pos_hint={"center_x": .5, "center_y": .5}
            
        )
        self.content_screen.add_widget(btn_open)
        #return self.manager
        
        
        #def lete_mzigo(self,dt):
        self.db_path = self.get_database_path()   
        #self.db_path=self.db_path
        print(">>> Naandaa mizigo mizito sasa...")
        self.bidhaa_mradi_dct = {
            # --- MILANGO & FREMU ---
            'Fremu': {'jina': 'Fremu', 'icon': 'door-frame', 'parts': {'Side-L': {'jina': 'Side Jamb (L)', 'icon': 'format-vertical-align-left', 'dim': [2.4, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Jamb (R)', 'icon': 'format-vertical-align-right', 'dim': [2.4, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Head': {'jina': 'Head Jamb', 'icon': 'format-horizontal-align-top', 'dim': [1.0, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Sill': {'jina': 'Sill (Chini)', 'icon': 'border-bottom', 'dim': [1.0, 0.15, 0.02], 'kazi': 'kuchora()'}}},
            'Mlango': {'jina': 'Mlango', 'icon': 'door-closed', 'parts': {'Stile-L': {'jina': 'Stile (Kushoto)', 'icon': 'format-vertical-align-left', 'dim': [2.1, 0.12, 0.045], 'kazi': 'kuchora()'}, 'Stile-R': {'jina': 'Stile (Kulia)', 'icon': 'format-vertical-align-right', 'dim': [2.1, 0.12, 0.045], 'kazi': 'kuchora()'}, 'Rail-T': {'jina': 'Top Rail', 'icon': 'format-horizontal-align-top', 'dim': [0.66, 0.12, 0.045], 'kazi': 'kuchora()'}, 'Rail-M': {'jina': 'Mid Rail', 'icon': 'format-horizontal-align-center', 'dim': [0.66, 0.12, 0.045], 'kazi': 'kuchora()'}, 'Rail-B': {'jina': 'Bottom Rail', 'icon': 'format-horizontal-align-bottom', 'dim': [0.66, 0.18, 0.045], 'kazi': 'kuchora()'}, 'Panel-T': {'jina': 'Panel ya Juu', 'icon': 'texture-box', 'dim': [0.66, 0.85, 0.02], 'kazi': 'kuchora()'}, 'Panel-B': {'jina': 'Panel ya Chini', 'icon': 'texture-box', 'dim': [0.66, 0.85, 0.02], 'kazi': 'kuchora()'}}},
            'Dirisha': {'jina': 'Dirisha', 'icon': 'window-closed-variant', 'parts': {'Frame-V': {'jina': 'Outer Stile', 'icon': 'border-vertical', 'dim': [1.2, 0.1, 0.1], 'kazi': 'kuchora()'}, 'Frame-H': {'jina': 'Outer Rail', 'icon': 'border-horizontal', 'dim': [1.2, 0.1, 0.1], 'kazi': 'kuchora()'}, 'Sash-V': {'jina': 'Sash Stile', 'icon': 'format-vertical-align-center', 'dim': [1.1, 0.06, 0.035], 'kazi': 'kuchora()'}, 'Sash-H': {'jina': 'Sash Rail', 'icon': 'format-horizontal-align-center', 'dim': [0.55, 0.06, 0.035], 'kazi': 'kuchora()'}, 'Glass': {'jina': 'Kioo', 'icon': 'mirror', 'dim': [0.5, 1.0, 0.005], 'kazi': 'kuchora()'}}},
            
            # --- SEBULE ---
            'TV-Stand': {'jina': 'TV Stand', 'icon': 'television-guide', 'parts': {'Top': {'jina': 'Top Board', 'icon': 'table-top', 'dim': [1.8, 0.4, 0.02], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Bottom Board', 'icon': 'table-bottom', 'dim': [1.8, 0.4, 0.02], 'kazi': 'kuchora()'}, 'Side-L': {'jina': 'Side Panel (L)', 'icon': 'border-left', 'dim': [0.4, 0.48, 0.02], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Panel (R)', 'icon': 'border-right', 'dim': [0.4, 0.48, 0.02], 'kazi': 'kuchora()'}, 'Divider': {'jina': 'Vertical Divider', 'icon': 'border-vertical', 'dim': [0.38, 0.48, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Open Shelf', 'icon': 'reorder-horizontal', 'dim': [0.85, 0.35, 0.018], 'kazi': 'kuchora()'}, 'Back': {'jina': 'Back Panel', 'icon': 'texture-box', 'dim': [1.8, 0.48, 0.003], 'kazi': 'kuchora()'}}},
            'Sofa': {'jina': 'Sofa', 'icon': 'sofa-single-outline', 'parts': {'Base-F': {'jina': 'Seat Frame', 'icon': 'floor-plan', 'dim': [2.4, 0.8, 0.1], 'kazi': 'kuchora()'}, 'Back-F': {'jina': 'Backrest Frame', 'icon': 'backburger', 'dim': [2.4, 0.4, 0.05], 'kazi': 'kuchora()'}, 'Arm-L': {'jina': 'Armrest (L)', 'icon': 'border-left', 'dim': [0.15, 0.8, 0.6], 'kazi': 'kuchora()'}, 'Arm-R': {'jina': 'Armrest (R)', 'icon': 'border-right', 'dim': [0.15, 0.8, 0.6], 'kazi': 'kuchora()'}, 'Leg': {'jina': 'Mguu (4pcs)', 'icon': 'arrow-down-thick', 'dim': [0.05, 0.05, 0.15], 'kazi': 'kuchora()'}}},
            'Kiti': {'jina': 'Kiti', 'icon': 'chair-school', 'parts': {'Seat': {'jina': 'Seat Board', 'icon': 'chair-school', 'dim': [0.45, 0.45, 0.02], 'kazi': 'kuchora()'}, 'Leg-F': {'jina': 'Mguu Mbele', 'icon': 'format-vertical-align-bottom', 'dim': [0.04, 0.04, 0.45], 'kazi': 'kuchora()'}, 'Leg-B': {'jina': 'Mguu Nyuma (Long)', 'icon': 'format-vertical-align-top', 'dim': [0.04, 0.04, 0.9], 'kazi': 'kuchora()'}, 'Back-R': {'jina': 'Back Rail', 'icon': 'reorder-horizontal', 'dim': [0.4, 0.08, 0.02], 'kazi': 'kuchora()'}, 'Slat': {'jina': 'Back Slat', 'icon': 'reorder-vertical', 'dim': [0.05, 0.4, 0.02], 'kazi': 'kuchora()'}}},
            'Meza': {'jina': 'Meza', 'icon': 'table-furniture', 'parts': {'Top': {'jina': 'Top Board', 'icon': 'table-top', 'dim': [1.2, 0.6, 0.025], 'kazi': 'kuchora()'}, 'Leg': {'jina': 'Mguu (4pcs)', 'icon': 'ray-start-vertex', 'dim': [0.05, 0.05, 0.725], 'kazi': 'kuchora()'}, 'Apron-L': {'jina': 'Apron Ndefu', 'icon': 'border-top-variant', 'dim': [1.0, 0.08, 0.02], 'kazi': 'kuchora()'}, 'Apron-S': {'jina': 'Apron Fupi', 'icon': 'border-left-variant', 'dim': [0.4, 0.08, 0.02], 'kazi': 'kuchora()'}, 'Support': {'jina': 'Center Support', 'icon': 'ray-vertex', 'dim': [0.5, 0.05, 0.02], 'kazi': 'kuchora()'}}},
            
            # --- CHUMBANI ---
            'Kitanda': {'jina': 'Kitanda', 'icon': 'bed-double-outline', 'parts': {'Head-P': {'jina': 'Head Post', 'icon': 'format-vertical-align-top', 'dim': [0.1, 0.1, 1.2], 'kazi': 'kuchora()'}, 'Head-B': {'jina': 'Headboard Panel', 'icon': 'view-agenda-outline', 'dim': [1.8, 0.6, 0.03], 'kazi': 'kuchora()'}, 'Foot-P': {'jina': 'Foot Post', 'icon': 'format-vertical-align-bottom', 'dim': [0.1, 0.1, 0.5], 'kazi': 'kuchora()'}, 'Side': {'jina': 'Side Rail', 'icon': 'distribute-horizontal-center', 'dim': [1.9, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Slat': {'jina': 'Rungu (Slat)', 'icon': 'reorder-horizontal', 'dim': [1.8, 0.05, 0.02], 'kazi': 'kuchora()'}, 'Mid': {'jina': 'Center Support', 'icon': 'ray-vertex', 'dim': [1.9, 0.05, 0.05], 'kazi': 'kuchora()'}}},
            'Kabati': {'jina': 'Kabati', 'icon': 'wardrobe-outline', 'parts': {'Side-L': {'jina': 'Side Panel (L)', 'icon': 'border-left', 'dim': [0.6, 2.0, 0.018], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Panel (R)', 'icon': 'border-right', 'dim': [0.6, 2.0, 0.018], 'kazi': 'kuchora()'}, 'Top': {'jina': 'Top Panel', 'icon': 'border-top', 'dim': [1.2, 0.6, 0.018], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Bottom Panel', 'icon': 'border-bottom', 'dim': [1.2, 0.6, 0.018], 'kazi': 'kuchora()'}, 'Divide': {'jina': 'Vertical Divider', 'icon': 'border-vertical', 'dim': [0.55, 1.9, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Rafu', 'icon': 'reorder-horizontal', 'dim': [0.58, 0.55, 0.018], 'kazi': 'kuchora()'}, 'Door-L': {'jina': 'Mlango (L)', 'icon': 'door-closed', 'dim': [0.58, 1.95, 0.018], 'kazi': 'kuchora()'}, 'Door-R': {'jina': 'Mlango (R)', 'icon': 'door-closed', 'dim': [0.58, 1.95, 0.018], 'kazi': 'kuchora()'}, 'Back': {'jina': 'Back Panel', 'icon': 'texture-box', 'dim': [1.18, 1.98, 0.003], 'kazi': 'kuchora()'}}},
            'Nightstand': {'jina': 'Nightstand', 'icon': 'table-side', 'parts': {'Top': {'jina': 'Top Surface', 'icon': 'table-top', 'dim': [0.45, 0.4, 0.018], 'kazi': 'kuchora()'}, 'Side': {'jina': 'Side Wall', 'icon': 'format-vertical-align-center', 'dim': [0.4, 0.5, 0.018], 'kazi': 'kuchora()'}, 'Drawer': {'jina': 'Droo Unit', 'icon': 'dresser', 'dim': [0.4, 0.15, 0.35], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Bottom Plate', 'icon': 'border-bottom', 'dim': [0.45, 0.4, 0.018], 'kazi': 'kuchora()'}, 'Leg': {'jina': 'Mguu', 'icon': 'arrow-down-thick', 'dim': [0.03, 0.03, 0.15], 'kazi': 'kuchora()'}}},
            'Bunk-Bed': {'jina': 'Bunk Bed', 'icon': 'bed-outline', 'parts': {'Post': {'jina': 'Nguzo Kuu', 'icon': 'format-vertical-align-center', 'dim': [0.07, 0.07, 1.8], 'kazi': 'kuchora()'}, 'Rail-L': {'jina': 'Side Rail', 'icon': 'format-horizontal-align-center', 'dim': [1.9, 0.12, 0.03], 'kazi': 'kuchora()'}, 'Slat': {'jina': 'Rungu', 'icon': 'reorder-horizontal', 'dim': [1.0, 0.05, 0.02], 'kazi': 'kuchora()'}, 'Ladder': {'jina': 'Ngazi Rung', 'icon': 'reorder-horizontal', 'dim': [0.4, 0.05, 0.03], 'kazi': 'kuchora()'}, 'Guard': {'jina': 'Guard Rail', 'icon': 'reorder-vertical', 'dim': [1.2, 0.1, 0.02], 'kazi': 'kuchora()'}}},
            
            # --- UHIFADHI ---
            'Shoe-Rack': {'jina': 'Shoe Rack', 'icon': 'shoe-sneaker', 'parts': {'Side-L': {'jina': 'Side Panel (L)', 'icon': 'border-left', 'dim': [0.35, 1.0, 0.018], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Panel (R)', 'icon': 'border-right', 'dim': [0.35, 1.0, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Rafu ya Viatu', 'icon': 'reorder-horizontal', 'dim': [0.8, 0.3, 0.018], 'kazi': 'kuchora()'}, 'Top': {'jina': 'Top Plate', 'icon': 'border-top', 'dim': [0.8, 0.35, 0.018], 'kazi': 'kuchora()'}, 'Back': {'jina': 'Back Panel', 'icon': 'texture-box', 'dim': [0.8, 1.0, 0.003], 'kazi': 'kuchora()'}}},
            'Droo': {'jina': 'Droo', 'icon': 'dresser', 'parts': {'Front': {'jina': 'Face Plate', 'icon': 'square-outline', 'dim': [0.6, 0.2, 0.018], 'kazi': 'kuchora()'}, 'Side-L': {'jina': 'Side Wall (L)', 'icon': 'border-left', 'dim': [0.45, 0.18, 0.012], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Wall (R)', 'icon': 'border-right', 'dim': [0.45, 0.18, 0.012], 'kazi': 'kuchora()'}, 'Back': {'jina': 'Back Wall', 'icon': 'border-top', 'dim': [0.58, 0.18, 0.012], 'kazi': 'kuchora()'}, 'Bottom': {'jina': 'Sakafu', 'icon': 'floor-plan', 'dim': [0.55, 0.4, 0.003], 'kazi': 'kuchora()'}}},
            'Island': {'jina': 'Island', 'icon': 'countertop', 'parts': {'Top': {'jina': 'Worktop', 'icon': 'table-top', 'dim': [1.8, 0.9, 0.04], 'kazi': 'kuchora()'}, 'Side': {'jina': 'Unit Side', 'icon': 'border-vertical', 'dim': [0.8, 0.86, 0.018], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Base Plate', 'icon': 'border-bottom', 'dim': [1.6, 0.8, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Inner Shelf', 'icon': 'reorder-horizontal', 'dim': [1.56, 0.78, 0.018], 'kazi': 'kuchora()'}, 'Door': {'jina': 'Cabinet Door', 'icon': 'door-closed', 'dim': [0.4, 0.7, 0.018], 'kazi': 'kuchora()'}}},
            'Sideboard': {'jina': 'Sideboard', 'icon': 'cupboard-outline', 'parts': {'Top': {'jina': 'Top Board', 'icon': 'table-top', 'dim': [1.5, 0.45, 0.02], 'kazi': 'kuchora()'}, 'Side': {'jina': 'End Panel', 'icon': 'border-vertical', 'dim': [0.45, 0.8, 0.018], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Base Plate', 'icon': 'border-bottom', 'dim': [1.5, 0.45, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Inner Shelf', 'icon': 'reorder-horizontal', 'dim': [1.46, 0.4, 0.018], 'kazi': 'kuchora()'}, 'Door': {'jina': 'Cabinet Door', 'icon': 'door-closed', 'dim': [0.45, 0.7, 0.018], 'kazi': 'kuchora()'}}},
            'Sinki': {'jina': 'Sinki', 'icon': 'countertop-outline', 'parts': {'Top': {'jina': 'Top Surface', 'icon': 'table-top', 'dim': [1.2, 0.6, 0.02], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Unit Base', 'icon': 'package-variant', 'dim': [1.2, 0.6, 0.85], 'kazi': 'kuchora()'}, 'Fascia': {'jina': 'Front Fascia', 'icon': 'dock-top', 'dim': [1.2, 0.15, 0.018], 'kazi': 'kuchora()'}, 'Side': {'jina': 'Cabinet Side', 'icon': 'border-vertical', 'dim': [0.58, 0.85, 0.018], 'kazi': 'kuchora()'}, 'Door': {'jina': 'Sink Door', 'icon': 'door-closed', 'dim': [0.58, 0.65, 0.018], 'kazi': 'kuchora()'}}},
            
            # --- OFISI & MAKAZI ---
            'Bookshelf': {'jina': 'Bookshelf', 'icon': 'bookshelf', 'parts': {'Side-L': {'jina': 'Side Panel (L)', 'icon': 'border-left', 'dim': [0.3, 2.4, 0.018], 'kazi': 'kuchora()'}, 'Side-R': {'jina': 'Side Panel (R)', 'icon': 'border-right', 'dim': [0.3, 2.4, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Rafu', 'icon': 'border-horizontal', 'dim': [1.96, 0.3, 0.018], 'kazi': 'kuchora()'}, 'Back': {'jina': 'Back Panel', 'icon': 'texture-box', 'dim': [2.0, 2.4, 0.003], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Bottom Plate', 'icon': 'border-bottom', 'dim': [2.0, 0.3, 0.018], 'kazi': 'kuchora()'}}},
            'Workstation': {'jina': 'Workstation', 'icon': 'laptop', 'parts': {'Top': {'jina': 'Desk Top', 'icon': 'table-top', 'dim': [2.4, 1.2, 0.025], 'kazi': 'kuchora()'}, 'Leg-S': {'jina': 'End Support', 'icon': 'border-vertical', 'dim': [0.8, 0.72, 0.025], 'kazi': 'kuchora()'}, 'Modesty': {'jina': 'Modesty Panel', 'icon': 'border-top', 'dim': [2.2, 0.4, 0.018], 'kazi': 'kuchora()'}, 'Privacy': {'jina': 'Privacy Divider', 'icon': 'view-column', 'dim': [2.4, 0.4, 0.012], 'kazi': 'kuchora()'}, 'Cable': {'jina': 'Cable Tray', 'icon': 'dock-bottom', 'dim': [2.0, 0.1, 0.05], 'kazi': 'kuchora()'}}},
            'Podium': {'jina': 'Podium', 'icon': 'microphone-variant', 'parts': {'Desk': {'jina': 'Top Slant Desk', 'icon': 'ray-end', 'dim': [0.6, 0.5, 0.018], 'kazi': 'kuchora()'}, 'Front': {'jina': 'Front Panel', 'icon': 'card-outline', 'dim': [0.6, 1.1, 0.018], 'kazi': 'kuchora()'}, 'Side': {'jina': 'Side Wall', 'icon': 'border-vertical', 'dim': [0.4, 1.1, 0.018], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Base Foot', 'icon': 'table-bottom', 'dim': [0.6, 0.6, 0.04], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Inside Shelf', 'icon': 'reorder-horizontal', 'dim': [0.56, 0.35, 0.018], 'kazi': 'kuchora()'}}},
            
            # --- NJE & ZIADA ---
            'Pergola': {'jina': 'Pergola', 'icon': 'home-outline', 'parts': {'Post': {'jina': 'Support Post', 'icon': 'format-vertical-align-center', 'dim': [0.15, 0.15, 2.5], 'kazi': 'kuchora()'}, 'Beam-M': {'jina': 'Main Beam', 'icon': 'border-horizontal', 'dim': [3.0, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Beam-C': {'jina': 'Cross Beam', 'icon': 'reorder-horizontal', 'dim': [3.0, 0.15, 0.05], 'kazi': 'kuchora()'}, 'Rafter': {'jina': 'Rafter Slat', 'icon': 'reorder-horizontal', 'dim': [3.2, 0.1, 0.05], 'kazi': 'kuchora()'}, 'Brace': {'jina': 'Corner Brace', 'icon': 'trending-up', 'dim': [0.5, 0.1, 0.05], 'kazi': 'kuchora()'}}},
            'Planter': {'jina': 'Planter', 'icon': 'flower-outline', 'parts': {'Side-L': {'jina': 'Long Side', 'icon': 'distribute-horizontal-center', 'dim': [1.0, 0.4, 0.02], 'kazi': 'kuchora()'}, 'Side-S': {'jina': 'Short Side', 'icon': 'distribute-vertical-center', 'dim': [0.36, 0.4, 0.02], 'kazi': 'kuchora()'}, 'Base': {'jina': 'Floor Plate', 'icon': 'floor-plan', 'dim': [0.96, 0.36, 0.02], 'kazi': 'kuchora()'}, 'Cap': {'jina': 'Top Cap Rail', 'icon': 'border-top', 'dim': [1.05, 0.05, 0.02], 'kazi': 'kuchora()'}, 'Leg': {'jina': 'Corner Cleat', 'icon': 'format-vertical-align-bottom', 'dim': [0.04, 0.04, 0.4], 'kazi': 'kuchora()'}}},
            'Dog-House': {'jina': 'Dog House', 'icon': 'dog-side', 'parts': {'Floor': {'jina': 'Base Floor', 'icon': 'floor-plan', 'dim': [1.0, 1.2, 0.018], 'kazi': 'kuchora()'}, 'Side-W': {'jina': 'Side Wall', 'icon': 'wall', 'dim': [1.2, 0.8, 0.018], 'kazi': 'kuchora()'}, 'Front-W': {'jina': 'Front Wall', 'icon': 'door-open', 'dim': [1.0, 1.0, 0.018], 'kazi': 'kuchora()'}, 'Roof-L': {'jina': 'Roof Left', 'icon': 'home-roof', 'dim': [1.3, 0.7, 0.012], 'kazi': 'kuchora()'}, 'Roof-R': {'jina': 'Roof Right', 'icon': 'home-roof', 'dim': [1.3, 0.7, 0.012], 'kazi': 'kuchora()'}, 'Ridge': {'jina': 'Ridge Cap', 'icon': 'border-top', 'dim': [1.3, 0.1, 0.012], 'kazi': 'kuchora()'}}},
            'Sunbed': {'jina': 'Sunbed', 'icon': 'umbrella-outline', 'parts': {'Frame-S': {'jina': 'Side Frame', 'icon': 'distribute-horizontal-center', 'dim': [2.0, 0.1, 0.05], 'kazi': 'kuchora()'}, 'Frame-C': {'jina': 'Cross Member', 'icon': 'reorder-horizontal', 'dim': [0.6, 0.1, 0.05], 'kazi': 'kuchora()'}, 'Slat': {'jina': 'Top Surface Slat', 'icon': 'reorder-horizontal', 'dim': [0.7, 0.05, 0.02], 'kazi': 'kuchora()'}, 'Leg-F': {'jina': 'Front Leg', 'icon': 'format-vertical-align-bottom', 'dim': [0.05, 0.05, 0.3], 'kazi': 'kuchora()'}, 'Leg-B': {'jina': 'Back Leg', 'icon': 'format-vertical-align-bottom', 'dim': [0.05, 0.05, 0.3], 'kazi': 'kuchora()'}, 'Adjust': {'jina': 'Ratchet Back', 'icon': 'trending-up', 'dim': [0.6, 0.7, 0.05], 'kazi': 'kuchora()'}}},
            'Partition': {'jina': 'Partition', 'icon': 'view-column-outline', 'parts': {'Post': {'jina': 'Main Vertical Post', 'icon': 'format-vertical-align-center', 'dim': [0.05, 0.05, 2.4], 'kazi': 'kuchora()'}, 'Slat-H': {'jina': 'Horizontal Slat', 'icon': 'reorder-horizontal', 'dim': [1.4, 0.05, 0.012], 'kazi': 'kuchora()'}, 'Frame-T': {'jina': 'Top Rail', 'icon': 'border-top', 'dim': [1.5, 0.05, 0.05], 'kazi': 'kuchora()'}, 'Frame-B': {'jina': 'Bottom Rail', 'icon': 'border-bottom', 'dim': [1.5, 0.05, 0.05], 'kazi': 'kuchora()'}, 'Panel': {'jina': 'Infill Panel', 'icon': 'texture-box', 'dim': [0.4, 2.3, 0.003], 'kazi': 'kuchora()'}}},
            'Counter': {'jina': 'Counter', 'icon': 'storefront-outline', 'parts': {'Top': {'jina': 'Transaction Top', 'icon': 'table-top', 'dim': [1.5, 0.3, 0.025], 'kazi': 'kuchora()'}, 'Work': {'jina': 'Work Surface', 'icon': 'table-top', 'dim': [1.5, 0.6, 0.025], 'kazi': 'kuchora()'}, 'Front': {'jina': 'Front Fascia', 'icon': 'card-outline', 'dim': [1.5, 1.1, 0.018], 'kazi': 'kuchora()'}, 'Side': {'jina': 'End Gable', 'icon': 'border-vertical', 'dim': [0.6, 1.1, 0.018], 'kazi': 'kuchora()'}, 'Kick': {'jina': 'Recessed Kick', 'icon': 'border-bottom', 'dim': [1.5, 0.1, 0.018], 'kazi': 'kuchora()'}, 'Shelf': {'jina': 'Under Counter Shelf', 'icon': 'reorder-horizontal', 'dim': [1.46, 0.5, 0.018], 'kazi': 'kuchora()'}}},
            'Ngazi': {'jina':'Ngazi','icon':'stairs','parts':{'Stringer':{'jina':'Stringer','icon':'trending-up', 'dim':[3.2,0.25,0.05],'kazi':'kuchora()'},'Tread':{'jina':'Tread','icon':'reorder-horizontal','dim':[0.9,0.25,0.04],'kazi':'kuchora()'},'Riser':{'jina':'Riser','icon':'border-top','dim':[0.9,0.18,0.02],'kazi':'kuchora()'}}},
            'Wine-Rack': {'jina':'Wine Rack','icon':'bottle-wine-outline','parts':{'Frame':{'jina':'Box','icon':'square-outline','dim':[0.6,0.3,1.2],'kazi':'kuchora()'},'Grid':{'jina':'Grid','icon':'grid','dim':[0.56,0.28,0.012],'kazi':'kuchora()'},'Neck':{'jina':'Holder','icon':'circle-outline','dim':[0.1,0.1,0.012],'kazi':'kuchora()'}}},
            'Shoe-Rack': {'jina':'Shoe Rack','icon':'shoe-sneaker','parts':{'Shelf':{'jina':'Shelf','icon':'reorder-horizontal','dim':[0.8,0.3,0.018],'kazi':'kuchora()'},'Side':{'jina':'Side','icon':'border-vertical','dim':[0.35,1.0,0.018],'kazi':'kuchora()'}}},
            'Droo': {'jina':'Droo','icon':'dresser','parts':{'Front':{'jina':'Front','icon':'square-outline','dim':[0.6,0.2,0.018],'kazi':'kuchora()'},'Side':{'jina':'Side','icon':'format-vertical-align-center','dim':[0.45,0.18,0.012],'kazi':'kuchora()'},'Bottom':{'jina':'Bottom','icon':'floor-plan', 'dim':[0.55,0.4,0.003],'kazi':'kuchora()'}}}
        }

        self.malighafi_kazi={
            '1':Vipimo.Vipimo('Taarifa za mbao ',kundi='Mbao',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['bei','umbali','usafiri']},'uelekeo':{'active_color':'white','list':['kuzalisha','kuchana','kuranda']}}),
            '2':Vipimo.Vipimo('High density fiberboard',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            '3':Vipimo.Vipimo('Medium density fiberboard',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            '4':Vipimo.Vipimo('Low density fiberboard',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            '5':Vipimo.Vipimo('Marine board',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            '6':Vipimo.Vipimo('Ceiling board',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            '7':Vipimo.Vipimo('Plywood',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali','idadi','usafiri']},'uelekeo':{'active_color':'white','list':['bei']}}),
            #'8':Vipimo.Vipimo('Panel nyigine',kundi='Board',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene']},'umbali':{'active_color':'khaki','list':['umbali x','umbali y','umbali z']},'uelekeo':{'active_color':'white','list':['nyuzi x','nyuzi y','nyuzi z']}})

        }
        #self.malighafi_kazi['1'].badili_jina=1
        self.Malighafi_dict={
            'Nje':{'jina':'Mbao','icon':'cupboard-outline','kazi':self.malighafi_kazi['1']},
            'Hdf':{'jina':'Hdf','icon':'format-vertical-align-center','kazi':self.malighafi_kazi['2']},
            'Mdf':{'jina':'Mdf','icon':'format-horizontal-align-center','kazi':self.malighafi_kazi['3']},
            'Ldf':{'jina':'Ldf','icon':'door','kazi':self.malighafi_kazi['4']},
            'Marine':{'jina':'Marine','icon':'layer','kazi':self.malighafi_kazi['5']},
            'Ceiling':{'jina':'Ceiling\nboard','icon':'dresser-outline','kazi':self.malighafi_kazi['6']},
            'Plywood':{'jina':'Plywood','icon':'mirror','kazi':self.malighafi_kazi['7']},
            #'Panel':{'jina':'Panel\nnyingine','icon':'layers-triple','kazi':self.malighafi_kazi['8']}

        }

        self.Mteja_kazi={
            '1':Vipimo.Vipimo('Taarifa za mteja',kundi='Mteja',path=self.db_path,dict={'majina':{'active_color':'yellow','list':['jina la kwanza','jina la kati','jina la mwisho']},'mawasiliano':{'active_color':'khaki','list':['jinsia','mahali','jina maarufu']},'mengineyo':{'active_color':'white','list':['anachohitaji','simu','email']}}),
        }
        
        self.Mteja_dict={
            'Utambulisho':{'jina':'Utambulisho','icon':'account','kazi':self.Mteja_kazi['1']},
            
        }
        
        
        
        
        # 2. Setup the Navigation Drawer
        self.nav_drawer = MDNavigationDrawer(radius=(0, dp(0), dp(16), 16))
        #self.content_screen.add_widget(self.nav_drawer)
        # 3. Create Menu Functions
        def mbao_mpya():
            def ondoa(e):
                self.menu.dismiss()
                self.nav_drawer.set_state("close") 
            Clock.schedule_once(ondoa,0)
            self.nav_drawer.set_state("close")  
            kaz=Vipimo.Vipimo('Mbao',kundi='Mbao',path=self.db_path,dict={'vipimo':{'active_color':'yellow','list':['urefu','upana','unene']},'gharama_za_awali':{'active_color':'khaki','list':['kuranda','kuchana','kuzalisha']},'gharama_za_usafiri':{'active_color':'white','list':['umbali','nauli ya mbao','gharama ya mbao']}})
            kaz.badili_jina=1
            self.loading(self.content_screen,Rail_box.Rail_box(1,{'vipimo':{'jina':'vipimo','icon':'ruler','kazi':kaz}},chini=Maelezo.Chaguo(1,{'Asili':['Shambani','Kiwandani'],'Aina':['Ngumu','Laini']})))#
        def misumari():
            self.content_screen.clear_widgets()
            self.menu.dismiss()
            self.content_screen.add_widget(MisumariGui.Muonekano())
            self.nav_drawer.set_state("close")
        
        
        
            

        def Malighafi_menu(button_caller):
            items = [
                {"text": "Malighafi", "on_release": lambda: self.malighafi()},
                {"text": "Misumari","on_release":lambda: misumari()},
                {"text": "Gundi"},
                {"text": "Msasa"},
                {"text": "Highross"},
                {"text": "Sanding sealer"},
                {"text": "Primer"},
                {"text": "Clear"},
                {"text": "Rangi"},
                
                
            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        def Karakana_menu(button_caller):
            items = [
                {"text": "Mahali", "on_release": lambda: mbao_mpya()},
                {"text": "Ukubwa wa eneo","on_release":lambda: misumari()},
                {"text": "Umiliki"},
                {"text": "Jengo/majengo"},
            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        def Vitendeakazi_menu(button_caller):
            items = [
                {"text": "Mashine zote", "on_release": lambda: mbao_mpya()},
                {"text": "Mashine za umeme","on_release":lambda: misumari()},
                {"text": "Mashine bila umeme"},
                {"text": "Mashine za kuchaji"},
                {"text": "Mashine za maandalizi"},
                {"text": "Mashine zinazotarajiwa"}
            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        def Bidhaa_menu(self, caller):
            items = [{
                "text": v['jina'],
                'left_icon':v['icon'], 
                "on_release": lambda *args, item_data=v: self.kabati(item_data['jina'],item_data['parts'])
                
            } for k, v in self.bidhaa_mradi_dct.items()]
            self.bidhaa_list=list(i['text'] for i in items)
            self.menu = MDDropdownMenu(caller=caller, items=items,position="bottom", width_mult=4, max_height=dp(400))
            self.menu.bind(on_release=lambda *x: self.menu.dismiss())
            self.menu.open()


        def Uwekezaji_menu(button_caller):
            items=[
                {'text':'Eneo'},
                {'text':'Jengo/majengo'},
                {'text':'Vifaa'},
                {'text':'Rasilimali watu'},
                {'text':'Usafiri'},
                {'text':'Muda'},
                {'text':'Nishati'},
            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        def Rasilimaliwatu_menu(button_caller):
            items=[
                {'text':'Mafundi'},
                {'text':'Wasafirishaji'},
                {'text':'Store keeper'},
                {'text':'Mtunza taarifa'},
                
            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        #self.db_path = self.get_database_path() # Hifadhi path rasmi hapa
        print(f">>> Database ipo hapa: {self.db_path}")
    
    

        def utambulisho_wa_mteja():
            def ondoa(e):
                self.menu.dismiss()
                self.nav_drawer.set_state("close") 
            Clock.schedule_once(ondoa,0)
            
            self.loading(self.content_screen,Rail_box.Rail_box(1,self.Mteja_dict,chini=Maelezo.Chaguo(1,{'Asili':['Shambani','Kiwandani'],'Aina':['Ngumu','Laini']}))) 
        
        def Wateja_menu(button_caller):
            items=[
                {'text':'Mteja',"on_release": lambda: utambulisho_wa_mteja()},
                {'text':'Fundi'},
                {'text':'Muwekezaji'}

            ]
            self.menu = MDDropdownMenu(caller=button_caller, items=items, position="bottom", width_mult=4)
            self.menu.open()

        # 4. Build the UI
        layout = MDNavigationLayout()
        
        # Main Screen Content
        main_box = MDGridLayout(cols=1, padding=dp(20))
        
        self.content_screen.add_widget(main_box)

        # Navigation Drawer Content
        drawer_menu = MDNavigationDrawerMenu()
        drawer_menu.add_widget(MDNavigationDrawerLabel(text="Karakana"))
        
        # Malighafi Item
        malighafi_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Malighafi"),
            on_release=lambda x: Malighafi_menu(x)
        )
        
        # Malighafi Item
        karakana_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Karakana"),
            on_release=lambda x: Karakana_menu(x)
        )

        # Malighafi Item
        vitendeakazi_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Vifaa vya kazi"),
            on_release=lambda x: Vitendeakazi_menu(x)
        )

        # Malighafi Item
        bidhaa_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Bidhaa"),
            on_release=lambda x: Bidhaa_menu(self,x)
        )
        

        # Malighafi Item
        uwekezaji_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Uwekezaji"),
            on_release=lambda x: Uwekezaji_menu(x)
        )
        

        # Malighafi Item
        rasilimaliwatu_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Rasilimali watu"),
            on_release=lambda x: Rasilimaliwatu_menu(x)
        )
        

        # Malighafi Item
        wateja_item = MDNavigationDrawerItem(
            MDNavigationDrawerItemLeadingIcon(icon="nail"),
            MDNavigationDrawerItemText(text="Mteja"),
            on_release=lambda x: Wateja_menu(x)
        )


        drawer_menu.add_widget(karakana_item)
        drawer_menu.add_widget(vitendeakazi_item)
        drawer_menu.add_widget(malighafi_item)
        drawer_menu.add_widget(bidhaa_item)
        drawer_menu.add_widget(uwekezaji_item)
        drawer_menu.add_widget(rasilimaliwatu_item)
        drawer_menu.add_widget(wateja_item)
        self.nav_drawer.add_widget(drawer_menu)

        layout.add_widget(self.manager)
        layout.add_widget(self.nav_drawer)
        print(">>> Kila kitu kipo tayari!")
        # Kwenye main.py / andaa_mazingira_ya_uchoraji:
        self.status_label = MDLabel(
            text="Tayari...", 
            markup=True,  # <--- HII NI MUHIMU!
            role='small',
            adaptive_height=True,

            # ... zingine ...
        )
        self.error_label = MDLabel(
            text="", 
            markup=True,  # <--- HII NI MUHIMU!
            role='small'
            # ... zingine ...
        )

        return layout
    #Kabati.kabati_taarifa()
    def get_database_path(self):
        import os
        from kivy.utils import platform

        if platform == 'android':
            # Hapa ndipo tunapoficha siri: Tunatumia folder la Documents la simu
            from android.storage import primary_external_storage_path
            sd_path = primary_external_storage_path()
            # Tunatengeneza folder maalum ambalo halifutiki kirahisi
            folder = os.path.join(sd_path, "Documents", "Karakana_Data")
        else:
            # Kwa Windows/PC, iweke kwenye Documents za user---os.path.expanduser("~"),
            folder = os.path.join(os.getcwd(), "Documents", "Karakana_BIM_Data")

        if not os.path.exists(folder):
            os.makedirs(folder)

        return os.path.join(folder)

    def onyesha_error_popup(self, ujumbe_wa_error):
        """Inafungua popup ya Kivy na kuonyesha traceback kamili"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        #from kivymd.uix.scrollview import ScrollView

        # Layout ya ndani ya popup
        kitangulizi=ScrollView(
            size_hint_y=None,
            height=Window.height*0.6,
            scroll_timeout=500,
            effect_cls='ScrollEffect'
        )
        layout = kitangulizi

        # TextInput inaruhusu ku-scroll na ku-copy text hata ikiwa ndefu
        maandishi = MDLabel(
            text=f"\n{ujumbe_wa_error}", 
            markup=True,
            role='small',
            adaptive_height=True,

        )
        #kitangulizi.add_widget()
        try:layout.add_widget(maandishi)
        except:print(f"Ila error ilikuwa ni\n{maandishi.text}")

        # Kitufe cha kufunga popup
        kitufe_funga = Button(text="Funga", size_hint_y=None, height='45dp')
        

        # Tengeneza Popup yenyewe
        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
        
        #from kivy.core.window import Window
        popup = MDDialog(
            MDDialogHeadlineText(text="Changamoto za kiufundi",role='small'),
            MDDialogContentContainer(
                layout,
                orientation='vertical'
            ),
            radius=(7,7,7,7),
            theme_height='Custom',
            adaptive_height=True,
            height=0.5*Window.height,
            opacity=0
        )
        
        
        
        #kitufe_funga.bind(on_release=popup.dismiss)
        
        # Fungua popup ionekane kwenye screen
        try:popup.open()
        except:print('kuna shida kwenye popup error!')


    def malighafi(self):
        def ondoa(e):
            self.menu.dismiss()
            self.nav_drawer.set_state("close") 
        Clock.schedule_once(ondoa,0)
        self.nav_drawer.set_state("close")  
        #kaz=Vipimo.Vipimo('Malighafi',kundi='Mdf',path=self.db_path,self.malighafi_dict={'vipimo':{'active_color':'yellow','list':['urefu','upana','unene']},'gharama_za_awali':{'active_color':'khaki','list':['kuranda','kuchana','kuzalisha']},'gharama_za_usafiri':{'active_color':'white','list':['umbali','nauli ya mbao','gharama ya mbao']}})
        #kaz.badili_jina=1
        self.loading(self.content_screen,Rail_box.Rail_box(1,self.Malighafi_dict,chini=Maelezo.Chaguo(1,{'Asili':['Shambani','Kiwandani'],'Aina':['Ngumu','Laini']}))) 
    def kabati(self,item,dicti):
            self.bidhaa_jina3=[]
            
            self.bidhaa_jina=item.lower()
            db_path = os.path.join(self.db_path, 'Mteja.sqlite')
            karakana_jina = f"Uwanja wa uchoraji wa {item}"

            
            def ondoa(e):
                self.menu.dismiss()
                self.nav_drawer.set_state("close") 
            Clock.schedule_once(ondoa, 0)

            # 1. Safisha screen na weka Injini ya 3D
            self.content_screen.clear_widgets()
            #self.loading(self.content_screen,Rail_box.Rail_box(1,kabati_dct))
            #self.content_screen.add_widget(self.engine_3d)

            # 2. Tengeneza function ndogo (Callback) itakayocheza na RailBox
             # Fungua kurekebisha miondoko
            scroll = ScrollView(
                scroll_timeout=500,
                effect_cls='ScrollEffect'
            )
            
            
            list_ya_wateja = MDList()
            try:
                # Hii inatusaidia kupata data kwa kutumia majina ya column badala ya namba (0, 1, 2)
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        COALESCE([jina maarufu], [jina la kwanza]) AS jina_chaguo,
                        mahali, 
                        anachohitaji,
                        Namba 
                    FROM Mteja
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    item = MDListItem()
                    # 7. Bind tukio la kubonyeza (Event)
                    # Hii inajenga ramani papo hapo: "uwanja wa kuchorea mlango", "uwanja wa kuchorea meza", nk.
                    self.karakana_map = {bidhaa.lower(): f"uwanja wa kuchorea {bidhaa.title()}" for bidhaa in self.bidhaa_list}
                    ll=[]
                    
                    def mchakato_wa_hitaji(inst, r=row):
                        mtu=''
                        self.m_id=r['Namba']
                        mahali=r['mahali']
                        self.bidhaa_jina4=str(r['anachohitaji'])
                        self.bidhaa_jina2=str(r['anachohitaji'])
                        hitaji_raw = self.bidhaa_jina4
                        for child in inst.children:
                            try:
                                print(child.children[0].text)
                                
                            except:
                                print(child.children[0].children[1].text)
                                mtu=child.children[0].children[1].text
                            try:
                                if isinstance(child.children, Boxlayout):# MDListItemHeadlineText):
                                    
                                    print(mtu)
                            except:pass
                        # Check kama kuna koma (inaashiria ni list)
                        if ',' in hitaji_raw:
                            # Tenganisha kwa koma na ondoa nafasi (strip)
                            vitu = [v.strip() for v in hitaji_raw.split(',') if v.strip()]
                            for k in vitu:
                                vitu[vitu.index(k)]=k.lower()
                            self.kazi=vitu
                            self.bidhaa_jina2=vitu
                            #self.engine_3d.painter.kazi=vitu
                            if len(vitu) > 1:
                                # ITENGENEZE MENU HAPA HAPA
                                menu_items = [
                                    {
                                        "text": v.title(),
                                        "on_release": lambda x=v.lower(),m=mtu,no=r['Namba'],vt=vitu: fanya_maamuzi(m,x,no,vt,mahali),
                                    } for v in vitu
                                ]
                                # Fungua Menu kwenye ile item iliyobonyezwa
                                from kivymd.uix.menu import MDDropdownMenu
                                self.drop_menu = MDDropdownMenu(caller=inst, items=menu_items, width_mult=4)
                                self.drop_menu.open()
                                return # Tunatoka hapa ili isiendelee na logic ya chini
                        else:
                            self.bidhaa_jina2=[hitaji_raw.lower()] 
                            #self.engine_3d.painter.kazi= [hitaji_raw.lower()]      
                            # Kama haina koma au ni kitu kimoja tu, fanya maamuzi moja kwa moja
                            fanya_maamuzi(mtu,hitaji_raw.lower(),r['Namba'],[hitaji_raw.lower()],mahali)

                    # ONDOA "self" hapa kama function ipo ndani ya kabati()
                    def fanya_maamuzi(mtu,jina_lililovunwa,id,kazi,mahali):
                        # 1. Geuza kuwa herufi ndogo na safisha nafasi
                        self.engine_3d.painter.camera=[]
                        jina = jina_lililovunwa.lower().strip()
                        try:self.drop_menu.dismiss()
                        except: pass
                        # 2. CHUJIO KIKUU: Kama neno 'kabati' limo popote
                        if self.bidhaa_jina in jina:
                            print(f">>> Mfumo umetambua neno {self.bidhaa_jina} ndani ya: {jina.upper()}")
                            print(f">>> Nafungua uwanja wa kuchorea {self.bidhaa_jina} moja kwa moja...")
                            # Ite function ya kabati (hakikisha unaitumia self.kabati kama ipo nje ya scope)
                            self.mteja=mtu.title()
                            self.andaa_mazingira_ya_uchoraji(jina,self.bidhaa_jina5.ndani,mtu,self.m_id,kazi,mahali)
                            for item in self.bidhaa_jina5.rail_items: # Assuming rail ina list ya items zake
                                item.bind(on_release=lambda x, k=item.key: self.mchoraji_wa_rail(k, dicti[k]))
                            return # Tunatoka hapa kwa ushindi, hatuhitaji kuangalia mengine

                        # 3. CHUJIO LA PILI: Kwa bidhaa nyingine (Automatic redirection)
                        # Hapa inatumia ile 'self.bidhaa_list' uliyoivuna njiani
                        kipo = False
                        
                        for bidhaa in [b.lower() for b in self.bidhaa_list]:
                            if bidhaa in jina:
                                karakana = f"uwanja wa kuchorea {bidhaa.title()}"
                                
                                #try:
                                for e in self.bidhaa_jina2:
                                    print(f'{mtu} {self.bidhaa_jina}>>>{e}')
                                    if self.bidhaa_jina.lower() in e.lower():
                                        self.bidhaa_jina3.append(e)
                                #except:pass
                                self.bidhaa_jina1=bidhaa
                                
                                self.onyesha_ujumbe_wa_redirection(jina.title(),scroll,mtu,id,kazi,mahali)
                                kipo = True
                                break
                                
                        if not kipo:
                            # 4. Kama neno 'kabati' halimo na hakuna fenicha nyingine inayojulikana
                            self.onyesha_ujumbe_wa_onyo(jina.title(),scroll)


                    
                    # 1. Maandalizi ya data kutoka kwenye Database
                    jina = row['jina_chaguo'] if row['jina_chaguo'] else "Mteja Asiye na Jina"
                    mahali = row['mahali'] if row['mahali'] else "Hajataja"
                    hitaji = row['anachohitaji'] if row['anachohitaji'] else "Vipimo"
                    namba = row['Namba'] if row['Namba'] else "0"
                    
                    # 2. Tengeneza Mzazi wa List Item
                    
                    # 3. Weka Icon ya Kamtu (Leading)
                    item.add_widget(MDListItemLeadingIcon(
                        icon="account-circle-outline"
                    ))
                    
                    # 4. Weka Jina la Mteja (Headline)
                    item.add_widget(MDListItemHeadlineText(
                        text=str(jina)
                    ))
                    
                    # 5. Weka Maelezo ya Mahali na Hitaji (Supporting)
                    item.add_widget(MDListItemSupportingText(
                        text=f"Kutoka {mahali.title()} ana hitaji: {hitaji.upper()}"
                    ))
                    
                    # 6. Weka Namba ya ID upande wa kulia (Trailing)
                    item.add_widget(MDListItemTrailingSupportingText(
                        text=f"{namba}"
                    ))
                    def mtej(e):
                        self.mteja=jina.title()
                    self.m_id=namba
                    # 7. Bind tukio la kubonyeza (Event)
                    # Unganisha item na hii logic
                    def kurupua(e):
                        self.m_id=row['Namba']
                        
                    item.bind(on_release=mchakato_wa_hitaji)
                    self.bidhaa_itm=item
                    
                    # 8. Ongeza Item kwenye MDList yako
                    list_ya_wateja.add_widget(item)
                    #self.project_name

                    
                    
                conn.close()
            except Exception as e:
                print(f"Kosa: {e}")
                print("\n" + "="*20 + " ERROR LOCATED " + "="*20)
                traceback.print_exc() 
                print("="*55 + "\n")
            #list_ya_wateja.add_widget(OneLineListItem(text="Mteja 1"))
            scroll.add_widget(list_ya_wateja)
            # 3. Pakia Rail_box na ipe mchoraji wetu kama 'Action'
            # Hapa tunai-cheat RailBox: badala ya kuipa moduli, tunaipa function yetu
            rail = Rail_box.Rail_box(1,dicti,faili1=scroll)
            self.uchoraji_rail=rail
            self.bidhaa_jina5=rail
            # Mfano ndani ya andaa_mazingira au kabati function:
                    # Ndani ya function ya kabati(self, item, dicti):
            try:
                if hasattr(self.bidhaa_jina5, 'rail_items') and self.bidhaa_jina5.rail_items:
                    for r_item in self.bidhaa_jina5.rail_items:
                        # Bind tukio la mbofyo kwa kutumia kodi yetu mpya ya unyama
                        r_item.bind(on_release=lambda x, k=r_item.key: self.mchoraji_wa_rail(k, dicti[k]))
                    
                    # Toa mrejesho kuwa kila kitu kiko sawa
                    self.status_label.text = f"[color=00ADB5]➔ Railbox imepakiwa: {len(self.bidhaa_jina5.rail_items)} parts tayari.[/color]"
                else:
                    # Hapa ndipo exception inapoandikwa kwenye Status Bar badala ya Print
                    self.status_label.text = "[color=FF5252]⚠️ Error: Rail_box haina vifaa (rail_items) vya ku-bind![/color]"
            
            except Exception as e:
                # Catch kosa lolote lingine lililojificha
                self.status_label.text = f"[color=FF5252]⚠️ Kosa la Algorithm: {str(e)}[/color]"

                # Mbinu ya Kitalamu: Overwrite on_item_release ya hii instance ya rail pekee
                # Hii hailengi Rail_box.py yenyewe, inalenga hii 'rail' widget ya hapa tu
                

            self.loading(self.content_screen, rail)
            def mteja(e):
                rail.ndani.clear_widgets()
                if rail.faili != '':
                    
                    rail.ndani.add_widget(rail.faili) 
            rail.nje.clear_widgets()
            self.engine_3d.files.bind(on_release=mteja)
            try:rail.nje.add_widget(rail.ndani)
            except:
                rail.ndani.parent.remove_widget(rail.ndani)
                rail.nje.add_widget(rail.ndani)
            rail.ndani.md_bg_color="#121212"
            rail.ndani.add_widget(MDLabel(
                text=f"\n\n\n\n\n\n[color=E67E22][b]KARIBU KATIKA ULIMWENGU WA {karakana_jina.upper()}[/b][/color]\nKifuatacho sasa ni wewe kuchagua jina la mteja ili uewze kumchorea {karakana_jina.lower()} yeye anapenda!!",
                halign="center", markup=True, font_style="Headline", role="small",
                valign='center',theme_text_color="Custom", text_color='#2ECC71',
                size_hint_y=None, height=dp(50)
            ))
            try:rail.ndani.add_widget(rail.files)
            except:
                rail.files.parent.remove_widget(rail.files)
                rail.ndani.add_widget(rail.files)
                        

        
    def loading(self,widget,instance):
        
        txt1=random.choice(['Subiri kidogo....','Subiri kwanza...',f'Kuna vitu napangilia maana {random.choice(self.fundi)} kaviacha ovyo ovyo',f'Ah heb mwite {random.choice(self.fundi)} kwanza!\nKuna faili silioni huku\n subiri kidogo...'])
        clr=random.choice(['yellow','green','blue','purple','khaki','white'])
        clr1= random.choice(['white','green','khaki','purple','blue','yellow'])   
        txt2=random.choice(['Ahh nshakipata nlichokuwa nakitafuta','Ah tayari bhana..!','Yes kitu hiki hapaaa...!','Yeah mambo yamekaa sawa tayari','Mambo si haya bhana..!\nKila kitu kipo sawa sasa!!!'])
        label = MDLabel(
            pos_hint={'center_x': .5, 'center_y': .5},
            md_bg_color='black',
            text_color=clr,
            text=txt1,
            halign='center'
        )
        
        def fungua_kabati(e):
            widget.remove_widget(label)
            widget.add_widget(instance)
        t1=random.choice([1.75,1.25,1])    
        def badili_text(e):
            label.text=txt2
            label.text_color=clr1
            Clock.schedule_once(fungua_kabati, t1)
        t=random.choice([3,2.5,2,1.5])
        def fungua(e):
            widget.add_widget(label)
            Clock.schedule_once(badili_text, t)
        Clock.schedule_once(fungua,0)

    def mchoraji_wa_rail(self, item_key, item_data):
        """
        Rail Linkage: Inafungua workshop kwanza kisha inajaza data 
        ili kuzuia AttributeError ya f_id.
        """
        try:
            import time
            info = item_data
            p = self.engine_3d.painter
            
            # 1. UPDATE STATUS (Visual Feedback mapema)
            # Hii inabadilisha label ya Cyan kule juu na Status kule chini
            ujumbe = f"Sasa unachora: {info.get('jina', 'Kipande kipya')}"
            p.update_status(ujumbe)

            # 2. KICKSTART WORKSHOP (Lazima iwe mwanzo!)
            # Hii function ndiyo inayounda 'self.f_id', 'self.f_w' nk.
            # Bila hii, kodi itasema 'object has no attribute f_id'
            p.show_workshop()

            # 3. TAYARISHA DATA ZA UJENZI
            # Jina la kipekee (Unique ID)
            id_name = f"{info.get('jina', 'Part')}_{int(time.time())}"
            # Vipimo toka kwenye Dictionary ya fenicha (dim)
            w, h, d = info.get('dim', [0.6, 2.0, 0.02])

            # 4. JAZA MA-FIELD YA WORKSHOP (Automation Unyama)
            # Sasa hivi TextFields zipo tayari kwenye RAM, tunaweza kuziandika
            p.f_id.text = str(id_name)
            p.f_wood.text = str(info.get('jina', 'Mninga (Bloodwood)'))
            p.f_w.text = str(w)
            p.f_h.text = str(h)
            p.f_d.text = str(d)

            # 5. MREJESHO KWENYE TERMINAL (Optional Debug)
            print(f"BIM Success: Data ya {id_name} imepakiwa kitalamu.")

        except Exception as e:
            # Kama kuna lolote limeenda mrama, ripoti kwenye Status Bar ya chini
            if hasattr(self.engine_3d.painter, 'update_status'):
                self.engine_3d.painter.update_status(f"Rail Link Error: {str(e)}", is_error=True)
            else:
                print(f"Kosa la Rail Link: {e}")

    def andaa_mazingira_ya_uchoraji(self, jina, container, mteja, mteja_id,kazi,mahali):
        """Toleo la Unyama: Inapitisha ID kwa Painter na kulipua mchoro papo hapo"""
        
        try:
            from kivy.core.window import Window
            from kivy.clock import Clock
            
            if container is None: return 

            # 1. Safisha Engine kiti cha zamani kuzuia 'Widget already has a parent'
            if hasattr(self, 'engine_3d') and self.engine_3d.parent:
                self.engine_3d.parent.remove_widget(self.engine_3d)
            container.clear_widgets()
            
            # 2. Jenga UI Workbench (Labels na Studio)
            workbench = MDBoxLayout(orientation='vertical')#, md_bg_color="#121212")
            
            # Header
            h_pad, h_v_pad = Window.width * 0.04, Window.height * 0.012
            header = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=[h_pad, h_v_pad], spacing=5)
            try:
                header.add_widget(MDLabel(
                    text=f"\nMradi: [color=E67E22]{mteja.upper()}[/color] | [color=E67E22][b]{jina.upper()}[/b][/color]", 
                    markup=True, font_style="Title", role="small", theme_text_color="Custom", text_color="#EEEEEE"
                ))
            except:pass
            self.part_label = MDLabel(text="\n\nTunasonga mbele...", font_style="Body", role="small", theme_text_color="Custom", text_color="#00ADB5",markup=True)
            try:header.add_widget(self.part_label)
            except:pass
            #try:header.add_widget(self.error_label)
            #except:pass
            workbench.add_widget(header)
            #workbench.add_widget()

            # Studio Canvas
            self.studio_canvas = MDRelativeLayout(size_hint=(1, 1))#, md_bg_color="#1A1A1A")
            self.studio_canvas.add_widget(self.engine_3d)
            workbench.add_widget(self.studio_canvas)

            # Footer
            footer = MDBoxLayout(adaptive_height=True, md_bg_color="#1E1E1E", padding=[h_pad, 5])
            #self.status_label = MDLabel(text="➔ Mfumo unajiandaa...", theme_text_color="Custom", text_color="#BDC3C7")
            try:footer.add_widget(self.status_label)
            except:
                self.status_label.parent.remove_widget(self.status_label)
                footer.add_widget(self.status_label)

            workbench.add_widget(footer)
            
            container.add_widget(workbench)
            
            # 3. SET DATA KWA PAINTER (Hapa ndipo siri ya Mr Lee ilipo)
            # Tunapachika taarifa ndani ya painter kabla ya uchoraji kuanza
            
            # 4. MCHAKATO WA AUTO-LOAD
            def mlipuko_wa_data(dt):
                self.engine_3d.painter.trigger_auto_save()
                self.engine_3d.painter.render_arch_scene()
                self.engine_3d.painter.scene_objects = [] 
                # Jaribu kurejesha kumbukumbu (ndani ya SmamMorphEngine)
                alifanikiwa = self.engine_3d.painter.rejesha_kumbukumbu(mteja_id,kazi,jina)
                    
                print(alifanikiwa,jina)
                self.update_status=self.engine_3d.painter.update_status
                if alifanikiwa:
                    self.update_status(f"BIM: Kazi ya mteja namba {mteja_id} [{mteja}] imerejeshwa.")
                    
                else:
                    # Kama ni mteja mpya kabisa
                    self.engine_3d.painter.scene_objects = [] 
                    self.engine_3d.painter.render_arch_scene()
                    self.update_status(f"Mradi Mpya: {mteja}")
                self.engine_3d.painter.current_mteja_id = str(mteja_id)
                self.engine_3d.painter.current_mteja = str(mteja)
                self.engine_3d.painter.kazi=kazi
                self.engine_3d.painter.project_name = str(jina)
                self.engine_3d.painter.project_location = mahali
                self.current_project=jina

            # Ipe injini 0.4s kujiandaa ndipo data ilipuke kioni
            Clock.schedule_once(mlipuko_wa_data, 0.4)
            


        except Exception as e:
            print(f"CRITICAL BIM ERROR: {e}")

    def onyesha_ujumbe_wa_redirection(self, jina, scroll_widget,mteja,id,kazi,mahali):
        
        kinachowezekana=self.bidhaa_jina3
        print(f'kinachowezekana hapa {kinachowezekana}')
        baba = scroll_widget.parent
        rail_instance = getattr(scroll_widget, 'rail', None)
        if not baba: return
        baba.clear_widgets()

        # Rangi zenye Contrast ya juu
        BG_GIZA = "#121212"   # Kiza nene
        RANGI_TEAL = "#00ADB5" # Teal inayong'aa (Inaonekana vizuri)
        RANGI_WEUPE = "#EEEEEE" # Weupe wa Silver

        karakana_jina = self.karakana_map.get(jina.lower(), f"uwanja wa kuchorea {self.bidhaa_jina1.title()}")

        mazingira = MDBoxLayout(
            orientation='vertical', padding=dp(40), spacing=dp(25),
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint=(0.85, None), height=dp(500), opacity=0
        )
        
        # Icon: Compass (Inaashiria uelekeo/redirection)
        mazingira.add_widget(MDLabel(
            text="compass-outline", font_style="Icon", halign="center",
            font_size=dp(90), theme_text_color="Custom", text_color=RANGI_TEAL,
            size_hint_y=None, height=dp(100)
        ))

        # Headline: Weupe uliokolea
        mazingira.add_widget(MDLabel(
            text=f"[b]ELEKEA {karakana_jina.upper()}[/b]",
            halign="center", markup=True, font_style="Headline", role="small",
            theme_text_color="Custom", text_color=RANGI_WEUPE,
            size_hint_y=None, height=dp(50)
        ))
        
        # Maelezo: Silver (Inasomeka kwa urahisi)
        if kinachowezekana!=[]:
            if len(kinachowezekana)==1:kinachowezekana=kinachowezekana[0]
            elif len(kinachowezekana)==2:kinachowezekana=f'{self.bidhaa_jina3[0]} au {self.bidhaa_jina3[1]}'
            else:
                kinachowezekana=", ".join(kinachowezekana[:-1]) + " au " + kinachowezekana[-1]
                
            labda=f'\nKulingana na mfumo wa ukusanyaji taarifa uliouchagua [color=#2ecc71]{self.bidhaa_jina1.lower()}[/color] na mteja uliyemchagua [color=#2ecc71]{mteja.title()}[/color] tunaweza kumchorea [color=#2ecc71]{kinachowezekana}[/color]\nhivyo basi ni vyema ukachague tena ni kipi haswa ulichohitaji tuanze ku_deal nacho.'
            
        else:labda=''
        mazingira.add_widget(MDLabel(
            text=f"Mradi wa [color=E67E22][b]'{jina.title()}'[/b][/color] unahitaji zana zinazotumika kuchorea [color=E67E22][b]{self.bidhaa_jina1.upper()}[/b][/color].{labda}",
            halign="center", markup=True, theme_text_color="Primary",
            text_color="#A9A9B9", # Dark Gray
            font_size=dp(16)
        ))
        btn_stay = MDButton(
            MDButtonText(text=f"Baki hapa tumchoree {mteja.title()} {kinachowezekana}", theme_text_color="Custom", text_color=BG_GIZA),
            style="filled", theme_bg_color="Custom", md_bg_color=RANGI_TEAL,
            pos_hint={"center_x": .5}, size_hint_x=0.8
        )
        mn=MDDropdownMenu(caller=btn_stay)
        
        def baki(jn):
            try:mn.dismiss()
            except:pass
            for i in self.bidhaa_itm.children:
                print(self.bidhaa_itm.bind)
            self.bidhaa_jina4=kinachowezekana
            self.andaa_mazingira_ya_uchoraji(jn,self.bidhaa_jina5.ndani,mteja,id,kazi,mahali)
        
        if kinachowezekana!=[]:
            #print(f'mhhh {kinachowezekana}')
            def opn(e):
                mn.open()
                
            def twnz(e):
                baki(kinachowezekana)
            mazingira.add_widget(btn_stay)
            if re.search(r',|\bau\b', kinachowezekana):# in kinachowezekana:
                vipande=re.split(r',|\bau\b',kinachowezekana)
                vinavyowezekana=[v.strip() for v in vipande if v.strip()]
                
                itms=[{
                    'text':i,
                    'on_release':lambda j=i:baki(j)
                }for i in vinavyowezekana
                ]
                mn.items=itms
                
                #mazingira.add_widget(mn)
                btn_stay.bind(on_release=opn)
            else:
                # Hii inaondoa functions zote zilizokuwa zimeunganishwa na on_release
                #btn_stay.unbind_uid('on_release', btn_stay.get_property_observers('on_release')[0].uid)
                btn_stay.unbind_uid('on_release',opn)

                btn_stay.bind(on_release=twnz)

        def rudi(x):
            if rail_instance and hasattr(rail_instance, 'ndani'):
                rail_instance.ndani.clear_widgets()
                rail_instance.ndani.add_widget(scroll_widget)
                self.bidhaa_jina3=[]
                self.bidhaa_jina2=[]

        btn_go = MDButton(
            MDButtonText(text=f"Rudi kwenye orodha ya wateja", theme_text_color="Custom", text_color=BG_GIZA),
            style="filled", theme_bg_color="Custom", md_bg_color=RANGI_TEAL,
            pos_hint={"center_x": .5}, size_hint_x=0.8
        )
        btn_go.bind(on_release=rudi)
        mazingira.add_widget(btn_go)

        def nenda_karakana(x):
            if rail_instance and hasattr(rail_instance, 'ndani'):
                #rail_instance.ndani.clear_widgets()
                #rail_instance.ndani.add_widget(scroll_widget)
                itms=self.bidhaa_mradi_dct
                self.bidhaa_jina3=[]
                self.bidhaa_jina2=[]
                self.kabati(itms[self.bidhaa_jina1.title()]['jina'],itms[self.bidhaa_jina1.title()]['parts'])

        btn_go1 = MDButton(
            MDButtonText(text=f"Twenzetu {karakana_jina}", theme_text_color="Custom", text_color=BG_GIZA),
            style="filled", theme_bg_color="Custom", md_bg_color=RANGI_TEAL,
            pos_hint={"center_x": .5}, size_hint_x=0.8
        )
        btn_go1.bind(on_release=nenda_karakana)
        mazingira.add_widget(btn_go1)

        baba.add_widget(mazingira)
        self.bidhaa_jina3=[]
        self.bidhaa_jina2=[]
        Animation(opacity=1, duration=0.8).start(mazingira)

    def onyesha_ujumbe_wa_onyo(self, jina, scroll_widget):
        baba_wa_scroll = scroll_widget.parent
        if not baba_wa_scroll: return
        baba_wa_scroll.clear_widgets()

        RANGI_KIJANI = "#2ECC71" # Emerald Green
        RANGI_WEUPE = "#FFFFFF"

        onyo = MDBoxLayout(
            orientation='vertical', padding=dp(40), spacing=dp(25),
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint=(0.85, None), height=dp(450), opacity=0
        )
        
        # Icon: Information/Note (Taarifa ya upole)
        onyo.add_widget(MDLabel(
            text="information-variant", font_style="Icon", halign="center",
            font_size=dp(90), theme_text_color="Custom", text_color=RANGI_KIJANI,
            size_hint_y=None, height=dp(100)
        ))

        onyo.add_widget(MDLabel(
            text="Kumbukumbu ya Mradi", halign="center",
            font_style="Headline", role="small", theme_text_color="Custom",
            text_color=RANGI_WEUPE, size_hint_y=None, height=dp(40)
        ))
        
        onyo.add_widget(MDLabel(
            text=f"Kipengele hiki cha [b]{jina}[/b] ni kwa ajili ya taarifa.\nUsimamizi kamili unafanyika kwenye list kuu.",
            halign="center", markup=True, theme_text_color="Secondary",
            font_size=dp(16)
        ))

        rail_instance = getattr(scroll_widget, 'rail', None)
        def rudi_kwa_nguvu(inst):
            if rail_instance and hasattr(rail_instance, 'ndani'):
                rail_instance.ndani.clear_widgets()
                rail_instance.ndani.add_widget(scroll_widget)

        btn_rudi = MDButton(
            MDButtonText(text="NIMEFAHAMU", theme_text_color="Custom", text_color=RANGI_KIJANI),
            style="outlined", pos_hint={"center_x": .5}, size_hint_x=0.7
        )
        btn_rudi.line_color = RANGI_KIJANI
        btn_rudi.bind(on_release=rudi_kwa_nguvu)
        onyo.add_widget(btn_rudi)
        
        baba_wa_scroll.add_widget(onyo)
        Animation(opacity=1, duration=1).start(onyo)

    def update_status(self, ujumbe, is_error=False):
        """Inahakikisha ripoti inafika kwenye label hata kama kuna hitilafu"""
        try:
            color = "FF5252" if is_error else "00ADB5"
            prefix = "Error: " if is_error else "➔ "
            
            # 1. Update Status Label ya Footer kama ipo
            if hasattr(self, 'status_label'):
                self.status_label.text = f"[color={color}]{prefix}{ujumbe}[/color]"
            
            # 2. Backup: Print kwenye console kwa ajili ya ufundi
            print(f"BIM Exception Status: {ujumbe}")
            
        except Exception as e:
            print(f"Mnyororo wa status umekatika: {e}")



        
# 1. Define the fix
def safe_anim_complete(self, *args):
    # This prevents the "'NoneType' object has no attribute 'set_active_item'" error
    if hasattr(self, "_navigation_rail") and self._navigation_rail:
        self._navigation_rail.set_active_item(self)

# 2. Apply the fix to the library class directly
MDNavigationRailItem.anim_complete = safe_anim_complete
if __name__ == "__main__":
    print(">>> APP INAANZA KURUUN...")
    try:
        KarakanaApp().run()
    except Exception as e:
        print(f">>> ERROR YA AJABU: {e}")
        print("\n" + "="*20 + " ERROR LOCATED " + "="*20)
        traceback.print_exc() 
        print("="*55 + "\n")

# Ndani ya main.py
def on_rail_click(data):
    app = App.get_running_app()
    app.part_label.text = f"➔ Sasa unachora: {data['jina']}" # Hii itabadilika PAPO HAPO!


import sys
from kivy.logger import Logger

class LogStream:
    def __init__(self, painter):
        self.painter = painter
    def write(self, s):
        if s.strip():
            # Tuma kosa moja kwa moja kwenye ule ubao wako wa Status
            self.painter.update_status(f"Err: {s}", is_error=True)
        Logger.error(f"Console: {s}")
    def flush(self): pass

# Ndani ya KarakanaApp kwenye on_start au build:
# sys.stderr = LogStream(self.engine_3d.painter)
