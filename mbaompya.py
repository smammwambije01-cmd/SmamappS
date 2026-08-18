from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.divider import MDDivider

from kivymd.app import MDApp

class Mbao():
    def __init__(self,container):
        self.cntn= container  
    def gui(self):
        r3='yellow'
        r4='grey'
        mbaompya_grid=MDGridLayout(
            cols=1,
            md_bg_color='blue', 
            padding=5  
              
        )
        
        mbao=MDGridLayout(
            cols=1,
            md_bg_color='blue'
            
        )
        mbaompya_label=MDLabel(
            text='MBAO MPYA',
            halign='center',
            text_color='white'

        )
        mbao.add_widget(mbaompya_label)

        utambulisho=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=5
        )
        utambulisho_label=MDGridLayout(
            cols=1,
            md_bg_color='white'
            
        )
        utambulisho_jina=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        utambulisho_jina1=MDGridLayout(
            cols=2,
            md_bg_color=r4,
            spacing=2,
            padding=3
        )
        utambulisho_jina.add_widget(utambulisho_jina1)
        utambulisho_text=MDLabel(
            text='Utambulisho',
            halign='center',
            text_color='blue'
        )
        utambulisho_label.add_widget(utambulisho_text)
        jina_la_mbao=MDLabel(
            text='Jina la mbao:',
            text_color=r3
        )
        utambulisho_jina1.add_widget(jina_la_mbao)
        jina_la_mbao_tf=MDTextField(
            halign='center',
            multiline=False,
            #leading_text='Jina la mbao'
        )
        utambulisho_jina1.add_widget(jina_la_mbao_tf)

        utambulisho_asili=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        utambulisho_asili1=MDGridLayout(
            cols=3,
            md_bg_color=r4,
            spacing=2,
            padding=5
        )
        utambulisho_asili.add_widget(utambulisho_asili1)
        
        asili_ya_mbao=MDLabel(
            text='Asili ya mbao:',
            text_color=r3
            #halign='center'
        )
        utambulisho_asili1.add_widget(asili_ya_mbao)
        asili_ya_mbao1=MDLabel(
            text='shambani',
            #halign='center'
        )
        utambulisho_asili1.add_widget(asili_ya_mbao1)
        asili_ya_mbao2=MDLabel(
            text='kiwandani',
            #halign='center'
        )
        utambulisho_asili1.add_widget(asili_ya_mbao2)

        utambulisho_aina=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        utambulisho_aina1=MDGridLayout(
            cols=3,
            md_bg_color=r4,
            spacing=2,
            padding=5
        )
        utambulisho_aina.add_widget(utambulisho_aina1)
        
        aina_ya_mbao=MDLabel(
            text='Aina ya mbao:',
            text_color=r3
            #halign='center'
        )
        utambulisho_aina1.add_widget(aina_ya_mbao)
        aina_ya_mbao1=MDLabel(
            text='ngumu',
            #halign='center'
        )
        utambulisho_aina1.add_widget(aina_ya_mbao1)
        aina_ya_mbao2=MDLabel(
            text='laini',
            #halign='center'
        )
        utambulisho_aina1.add_widget(aina_ya_mbao2)


        vipimo=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=5
        )
        vipimo_label=MDGridLayout(
            cols=1,
            md_bg_color='white'
            
        )
        vipimo_urefu=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        vipimo_jina1=MDGridLayout(
            cols=3,
            md_bg_color=r4,
            spacing=2,
            padding=3
        )
        vipimo_urefu.add_widget(vipimo_jina1)
        vipimo_text=MDLabel(
            text='Vipimo',
            halign='center',
            text_color='blue'
        )
        vipimo_label.add_widget(vipimo_text)
        urefu=MDLabel(
            text='Urefu:',
            text_color=r3
        )
        vipimo_jina1.add_widget(urefu)
        vipimo.add_widget(vipimo_label)
        urefu_tf=MDTextField(
            halign='center',
            multiline=False,
            #leading_text='Jina la mbao'
        )
        vipimo_jina1.add_widget(urefu_tf)

        upana=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        upana1=MDGridLayout(
            cols=3,
            md_bg_color=r4,
            spacing=2,
            padding=5
        )
        upana.add_widget(upana1)
        
        upanalebel=MDLabel(
            text='Upana:',
            text_color=r3
            #halign='center'
        )
        upana1.add_widget(upanalebel)
        upana_tf=MDTextField(
            #text='shambani',
            #halign='center'
        )
        upana1.add_widget(upana_tf)
        upana2=MDLabel(
            text='inchi',
            #halign='center'
        )
        upana1.add_widget(upana2)

        unene=MDGridLayout(
            cols=1,
            md_bg_color='white',
            padding=3
            
        )
        unene1=MDGridLayout(
            cols=3,
            md_bg_color=r4,
            spacing=2,
            padding=5
        )
        unene.add_widget(unene1)
        
        unenelebel=MDLabel(
            text='Unene:',
            text_color=r3
            #halign='center'
        )
        unene1.add_widget(unenelebel)
        unene_tf=MDTextField(
            #text='ngumu',
            #halign='center'
        )
        unene1.add_widget(unene_tf)
        unene2=MDLabel(
            text='inchi',
            #halign='center'
        )
        unene1.add_widget(unene2)



        lb4=MDLabel(
            text='Aina ya mbao',
            halign='center'
        )
        txt2=MDTextField(
            halign='center',
            multiline=False
        )
        lb5=MDLabel(
            text='Shambani',
            halign='center'
        )
        asilia1=MDGridLayout(
            cols=2,
            md_bg_color='white'
            
        )
        lb6=MDLabel(
            text='Mbao ngumu',
            halign='center'
        )
        txt2=MDTextField(
            halign='center',
            multiline=False
        )
        asilia2=MDGridLayout(
            cols=2,
            md_bg_color='white'
        )
        kiwandani=MDLabel(
            text='Kiwandani',
            halign='center'    
        )
        mbao_laini=MDLabel(
            text='Mbao laini',
            halign='center'
        )
        hh=MDTextField(
            halign='center',
            multiline=False
        )
        utambulisho.add_widget(utambulisho_label)
        
        #asilia.add_widget(lb3)
        #asilia.add_widget(lb4)
        asilia1.add_widget(lb5)
        asilia1.add_widget(lb6)
        asilia2.add_widget(kiwandani)
        asilia2.add_widget(mbao_laini)
        dvd=MDDivider(
            color='blue',
            size_hint_y=0.1
        )

        mbaompya_grid.add_widget(mbao)
        mbaompya_grid.add_widget(utambulisho)
        mbaompya_grid.add_widget(utambulisho_jina)
        mbaompya_grid.add_widget(utambulisho_asili)
        mbaompya_grid.add_widget(utambulisho_aina)
        mbaompya_grid.add_widget(dvd)

        mbaompya_grid.add_widget(vipimo)
        mbaompya_grid.add_widget(vipimo_urefu)
        mbaompya_grid.add_widget(unene)
        mbaompya_grid.add_widget(upana)
        
        #cont.add_widget(asilia)
        #cont.add_widget(asilia1)
        #cont.add_widget(asilia2)

        self.cntn.add_widget(mbaompya_grid)
        return mbaompya_grid
