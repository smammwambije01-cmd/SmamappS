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
#import pickle,shelve
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

class Chaguo(MDGridLayout):
    def __init__(self,title,title_labels_dict,**kwargs):
        super().__init__(**kwargs)
        self.cols=1
        self.size_hint_y=0.1225
        self.nje=MDGridLayout(
                #padding=5,
                cols=1#+len(title_labels_dict[i]),
                #md_bg_color='black',
                
            )

        

        self.ndani_ndani=MDGridLayout(
            padding=2,
            md_bg_color='black',
            cols=3
        )
            
        self.ndani=MDGridLayout(
            padding=5,
            cols=1,
            spacing=1,
            md_bg_color='khaki'
        )

        lst={}


        def kwa_kila(title,labels,lay):
            kitu={}
            lll=[]
            
            for i in labels:
                
                kitu[i]={
                    'layout':MDGridLayout(
                        spacing=20,
                        md_bg_color='grey',
                        cols=3
                    ),
                    'checkbox':MDCheckbox(
                        active=False,
                        color_active='blue',
                        color_inactive='black',
                        
                    ),
                    'label':MDLabel(text=i,role='small',text_color='yellow'),
                    
                }
                lll.append(kitu[i]['checkbox'])
                def zima_wengine(x):
                    #lll.remove()
                    for ii in lll:
                        if ii != x:#kitu[i]['checkbox']:
                            ii.active=False
                        #kitu[i]['checkbox']
                        x.active=True   
                kitu[i]['checkbox'].bind(on_release=lambda x:zima_wengine(x))
                #.add_widget(kitu[i]['grid'])
                kitu[i]['layout'].add_widget(kitu[i]['checkbox'])
                kitu[i]['layout'].add_widget(kitu[i]['label'])
                lay.add_widget(kitu[i]['layout']) 

        
        for i in  title_labels_dict:
            lst[i]=MDGridLayout(
                padding=2,
                cols=1+len(title_labels_dict[i]),
                md_bg_color='black',
                
            )
            lst[i].add_widget(MDLabel(text=i,text_color='blue'))
            #.add_widget(kitu[i]['layout']) 
            
            kwa_kila(i,title_labels_dict[i],lst[i])   
        for i in lst:
            self.ndani.add_widget(lst[i])
        self.nje.add_widget(self.ndani)  
        self.add_widget(self.nje)

class Machaguo(MDGridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=1