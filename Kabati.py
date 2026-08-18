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

class Rail_box(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vp=Vipimo.Vipimo(1)       
        self.input_field=self.vp.urefu
        self.cols = 2
        class box(MDRelativeLayout):
            def __init__(slf,**kwargs):
                super().__init__(**kwargs)
                slf.pos_hint={"top": 0}
                self.spacing=5
                self.md_bg_color='grey'
            def show_popup(slf):
                self.show_popup()
        self.box=box()
        #self.box.show_popup=ObjectProperty()
        self.popup_box=self.vp#ObjectProperty()
        self.nav_r = MDNavigationRail(anchor='bottom',md_bg_color='grey', type='labeled',size_hint=(0.175,0.75))
        self.files=MDNavigationRailMenuButton(
            icon= "folder-outline" 
        )
        label_0 = MDNavigationRailItemLabel(font_size=4,text='Mafaili', text_color='yellow')
        self.files.add_widget(label_0)    
        self.nav_r.add_widget(self.files)
        # 1. Create the item
        self.vipimo_vya_nje = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_1 = MDNavigationRailItemIcon(size_hint=(0.075,1),icon='cupboard-outline')
        self.label_1 = MDNavigationRailItemLabel(font_size=4,text='Kwa nje', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_nje._navigation_rail = self.nav_r
        self.icon_1._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_nje.add_widget(self.icon_1)
        self.vipimo_vya_nje.add_widget(self.label_1)
        self.nav_r.add_widget(self.vipimo_vya_nje)
        def vipimo(e):
            self.box.clear_widgets()
            #self.box.add_widget(Vipimo.Vipimo('box la nje'))
        self.vipimo_vya_nje.bind(on_release=vipimo)
        #self.add_widget(self.nav_r)

        # 1. Create the item
        self.vipimo_vya_wima = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_2 = MDNavigationRailItemIcon(icon='format-vertical-align-center',radius=(0,0,0,0))
        self.label_2 = MDNavigationRailItemLabel(text='Wima', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_wima._navigation_rail = self.nav_r
        self.icon_2._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_wima.add_widget(self.icon_2)
        self.vipimo_vya_wima.add_widget(self.label_2)
        self.nav_r.add_widget(self.vipimo_vya_wima)
        
        def wima(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('panel za wima')) 
            
                     
        self.vipimo_vya_wima.bind(on_release=wima)

        # 1. Create the item
        self.vipimo_vya_ulalo = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_3 = MDNavigationRailItemIcon(icon='format-horizontal-align-center')
        self.label_3 = MDNavigationRailItemLabel(text='Ulalo', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_ulalo._navigation_rail = self.nav_r
        self.icon_3._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_ulalo.add_widget(self.icon_3)
        self.vipimo_vya_ulalo.add_widget(self.label_3)
        self.nav_r.add_widget(self.vipimo_vya_ulalo)
        def ulalo(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('panel za ulalo')) 

        self.vipimo_vya_ulalo.bind(on_release=ulalo)
        # 1. Create the item
        self.vipimo_vya_milango = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_4 = MDNavigationRailItemIcon(icon='door')
        self.label_4 = MDNavigationRailItemLabel(text='Milango', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_milango._navigation_rail = self.nav_r
        self.icon_4._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_milango.add_widget(self.icon_4)
        self.vipimo_vya_milango.add_widget(self.label_4)
        self.nav_r.add_widget(self.vipimo_vya_milango)
        def milango(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('mlango wa kabati')) 

        self.vipimo_vya_milango.bind(on_release=milango)
        # 1. Create the item
        self.vipimo_vya_droo = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_5 = MDNavigationRailItemIcon(icon='dresser-outline')
        self.label_5 = MDNavigationRailItemLabel(text='Droo', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_droo._navigation_rail = self.nav_r
        self.icon_5._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_droo.add_widget(self.icon_5)
        self.vipimo_vya_droo.add_widget(self.label_5)
        self.nav_r.add_widget(self.vipimo_vya_droo)

        def droo(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('droo')) 

        self.vipimo_vya_droo.bind(on_release=droo)

        # 1. Create the item
        self.vipimo_vya_kioo = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_6 = MDNavigationRailItemIcon(icon='mirror')
        self.label_6 = MDNavigationRailItemLabel(text='Kioo', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_kioo._navigation_rail = self.nav_r
        self.icon_6._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_kioo.add_widget(self.icon_6)
        self.vipimo_vya_kioo.add_widget(self.label_6)
        self.nav_r.add_widget(self.vipimo_vya_kioo)
        def kioo(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('kioo')) 

        self.vipimo_vya_kioo.bind(on_release=kioo)
        # 1. Create the item
        self.vipimo_vya_mbao = MDNavigationRailItem()
        
        # 2. Create children
        self.icon_7 = MDNavigationRailItemIcon(icon='layers-triple')
        self.label_7 = MDNavigationRailItemLabel(text='Ubao', text_color='yellow')
        
        # 3. CRITICAL: Manually link the children to the rail
        # This is what's usually missing in manual Python assembly
        self.vipimo_vya_mbao._navigation_rail = self.nav_r
        self.icon_7._navigation_rail = self.nav_r
        
        # 4. Assemble
        self.vipimo_vya_mbao.add_widget(self.icon_7)
        self.vipimo_vya_mbao.add_widget(self.label_7)
        self.nav_r.add_widget(self.vipimo_vya_mbao)

        def mbao(e):
            def prnt(e):
                pass#print('nmefika hapa')
            self.box.clear_widgets()            
            self.box.add_widget(Vipimo.Vipimo('mbao')) 

        self.vipimo_vya_mbao.bind(on_release=mbao)
        
        
        self.add_widget(self.nav_r)
        self.add_widget(self.box)
   
    def show_popup(self, *args):
        # Slide up to 40% of the screen height
        anim = Animation(pos_hint={"center_x": 0.5, "top": 1.2}, duration=3)
        anim.start(self.popup_box)
        # Focus input so keyboard pops up automatically
        Clock.schedule_once(lambda dt: setattr(self.input_field, 'focus', True), 0.4)
        #print('mbona tayari!!')
    def hide_popup(self, *args):
        self.input_field.focus = False
        anim = Animation(pos_hint={"center_x": 0.5, "top": 0}, duration=0.2)
        anim.start(self.popup_box)







