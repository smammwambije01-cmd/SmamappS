from kivy.app import App
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
import random
from kivymd.uix.textfield import (
    MDTextField, 
    MDTextFieldHintText, 
    MDTextFieldHelperText,
    MDTextFieldLeadingIcon,
)
from kivymd.uix.label import MDLabel
#from kivymd.properties import MDObjectProperty
import Misumari
class Muonekano(MDGridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=1

        self.mdtf=MDGridLayout(cols=2)
        self.mdlbl=MDLabel(
            text='Ok anza kuandika saizi ya msumari',
            size_hint_x=.8,
            size_hint_y=0.1,
            halign='center'
        )

        
        #textfield2
        self.mdtf2=MDTextField(
            id='mdtf2',
            mode="filled",           
            input_filter="float",  # Restricts keyboard to numbers/decimals
            #pos_hint={"center_x": .5, "center_y": .8},
            size_hint_x=.8,
            on_focus=self.on_fc,
            #max_text_length=10
            on_text_validate=self.chukua_id
        )
        self.mdht2=MDTextFieldHintText(text="Idadi ya misumari")
        self.mdhp2=MDTextFieldHelperText(text="Ni tarakimu tu ndo zinzhitajika hapo kaka",mode="on_error")
        self.mdtf2.add_widget(self.mdht2)
        self.mdtf2.add_widget(self.mdhp2)
        
        #textfield1
        self.mdtf1=MDTextField(
            id='mdtf1',
            mode='filled',
            input_filter="float", 
            size_hint_x=.8,
            multiline=False,            
            #
            on_text_validate=self.chukua_s
        )
        self.mdli1=MDTextFieldLeadingIcon(icon='ruler')
        self.mdht1=MDTextFieldHintText(text="Urefu wa msumari (inchi)",font_size=4)
        self.mdhp1=MDTextFieldHelperText(text="Ni tarakimu tu ndo zinzhitajika hapo kaka",mode="on_error")
        self.mdtf1.add_widget(self.mdht1)
        self.mdtf1.add_widget(self.mdhp1)
        #self.mdtf1.add_widget(self.mdli1)
        
        self.add_widget(self.mdtf)
        #self.container.add_widget(self)
        self.mdtf.add_widget(self.mdtf1)
        self.mdtf.add_widget(self.mdtf2)
        #self.add_widget(self.mdlbl)

    def chuja(self,mdtf):
        jibu1=['Lazima ujaze hapa kwanza','Mbona hapa ujajaza','Unataka nani akujazie hapa?','Oya! anza na hapa kwanza']
        jibu2=['Haya andika kinachohitajika hapa','jaza hapa basi','umesahau co mzima wewe','una matatizo gani']
        text=mdtf.text
        if not text or text.strip()=='':
            mdtf.error=True
            self.mdhp1.text=random.choice(jibu1)

        mdtf.error=False
        self.mdhp1.text=random.choice(jibu2)

    def on_txt1(self,mdtf,value):
        self.mdtf1.error=False

    def chukua_s(self,e):
        onyo=['Msumari gani tena huo','Huo ni uongo!','Hakunna !!!','Mtumzima bwiii...!']
        jibu1=['Lazima ujaze hapa kwanza','Mbona hapa ujajaza','Unataka nani akujazie hapa?','Oya! anza na hapa kwanza']
        self.chuja(self.mdtf1)
        t2=self.mdtf2#chkua= self.taarifa
        if Misumari.Msumari(self.mdtf1.text,100).uongo()==1 or self.mdtf1.text=='':
            if self.mdtf1.text=='':
                self.mdhp1.text=random.choice(jibu1)
            self.mdtf1.error=True
            self.mdhp1.text=random.choice(onyo)
            #self.mdtf2.focus=True
            self.mdtf1.focus=True
            self.mdtf1.text=''
            
        else:
            self.mdtf1.error=False
            t2.focus=True
            
        
    def on_fc(self,e):
        if self.mdtf1.text=='':
            self.mdtf2.text=''
            self.mdtf1.focus=True

    def chukua_id(self,e):       
        #chkua= self.taarifa
        def chkua_saizi():
            self.mdlbl.text=''
        chkua_saizi()
        self.lete_majibu()
        

    def lete_majibu(self):
        jibu=Misumari.Msumari( self.mdtf1.text,self.mdtf2.text).nambie_uzito()
        rangi=['blue','yellow','purple','green','orange','red','white','brown']
        self.mdlbl.text=jibu
        self.mdlbl.text_color=random.choice(rangi)
        self.mdtf1.focus=True
        
        try:
            self.add_widget(self.mdlbl)

        except BaseException:
            pass

#https://github.com/kivymd/kivymd/archive/master.zip