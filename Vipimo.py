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
from kivy.utils import platform

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
import sqlite3
#Window.softinput_mode = "pan"
#from kivy.core.window import Window

# 'p
# Optional: Add a smooth animation for the movement
#Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}

main_dict={}

main_dict['dhamira']=''
main_dict['updated_menu_items']=[]
main_dict['mzunguko_wa_mwisho']={}
main_dict['Taarifa']={}
main_dict['vinavyohitajika']={}
main_dict['vilivyohifadhiwa']={}
main_dict['previous']=0
check_dict={'vipimo':{'active_color':'yellow','list':['upana','urefu','unene'],'lazima':[2,0]},'umbali':{'active_color':'green','list':['ubali x','umbali y','umbali z']},'nyuzi':{'active_color':'brown','list':['nyuzi x','nyuzi y','nyuzi z']}}

class Vipimo(MDGridLayout):
    def __init__(self,jina_la_kitu,path='',kundi='',dict=check_dict,faili='',**kwargs):
        super().__init__(**kwargs)
        self.kundi=kundi
        
        
        self.indx=0
        self.kundi=kundi
        self.size_hint_y=0.75
        self.size_hint=(0.985,0.75)
        self.pos_hint={'top':0.985}
        self.padding=5
        self.md_bg_color='khaki'
        self.tf_list=[]
        self.tf_all={}
        self.all_labels={}
        self.active_label={}
        self.vizio={}
        self.vionjo=random.choice(['Twende kaz!','Haya','Haya sasa','Mmmh','Ummh','Yeah','Naam','Yes','Ndiyo','Ok'])
        self.mshangao=random.choice(['...!','..!!','!!!','...','..!..!!'])
        self.vimsha='%s%s'%(self.vionjo,self.mshangao)
        self.urefu=ObjectProperty()
        self.ingiza_upana=jina_la_kitu
        self.pos_y={'top':0}
        main_dict['menu_items']=[]
        main_dict['items_menu']={}
        self.pannel_no=''
        self.pannel_no_label_text=''
        self.pannel_count=''
        self.radius=(10,10,10,10)
        self.mahali_color='yellow'
        self.umbali_color='brown'
        self.kizio='mm'
        self.cols=1
        self.dict=dict
        self.dhamira=jina_la_kitu
        self.mizunguko=0
        self.jina=jina_la_kitu
        self.taarifa='Taarifa'
        self.vinavyohitajika=main_dict['vinavyohitajika']
        main_dict['mzunguko_%s'%self.dhamira]=0
        self.path=os.path.join(path,'%s.sqlite'%self.kundi)
        
        self.faili=faili
        self.parent_check_list=dict
        self.badili_jina=0
        self.parent_check_dict={}
        self.mwisho=ObjectProperty()
        try:self.mwenendo=main_dict['mwenendo_wa_taarifa_za_%s'%self.dhamira]
        except:self.mwenendo=main_dict['mwenendo_wa_taarifa_za_%s'%self.dhamira]={}
        self.kichwa_cha_habari_1=MDLabel(halign='center',role='small',text_color='khaki',size_hint_y=0.1)
        self.ndani=ObjectProperty()
        self.chini=ObjectProperty()
        try:qpq=main_dict['vilivyohifadhiwa'][self.kundi]
        except:main_dict['vilivyohifadhiwa'][self.kundi]={}
        main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]={}
        global mwisho_kabisa
        mwisho_kabisa=main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]
        # 4. Leta Injini ya Mchoro
        from Mchoro import KichoraSamaniInjini
        
        # Anzisha uwanja mpya wa Mchoro ndani ya wigo
        self.uwanja = KichoraSamaniInjini(
            size_hint=(1, 1),
            hali="picha" # Ionyeshe uhalisia wa mbao
        )
        #self.data=main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]
        self.fagia=ObjectProperty()
        self.ngapi=MDTextField(
            
            mode='filled',
            on_text_validate=lambda x:(self.remove_ngapi(x)),
            input_filter='int'
        )
        self.indicator=MDLinearProgressIndicator(
            size_hint=(0.75,0.05),
            indicator_color='blue'
        )
        
        self.wigo1=MDGridLayout(
            cols=1,
            size_hint=(0.9975,0.65),
            spacing=15,
            md_bg_color='black',
            radius=(7.5,7.5,7.5,7.5)
            #padding=
        )
        self.pannel_no_label=MDLabel(
            text=self.pannel_no_label_text,
            halign='center',
            text_color='khaki'
        )
        self.wigo=MDGridLayout(
            cols=1,
            size_hint=(0.995,0.6),
            #spacing=15,
            md_bg_color='black',
            radius=(5,5,5,5)
            #padding=
        )
        try:self.wigo1.add_widget(self.wigo)
        except:pass
        try:self.add_widget(self.wigo1)
        except:pass
        #self.aina=aina
        self.list1=['hapa kwanza','jaza hapa','anza na hapa','umeruka hapa']

        self.drop=ObjectProperty()
        self.vipimo=MDGridLayout(
            cols=1,
            padding=5
            #padding=40()
        )
        self.yes_mahali=1
        
        #umbali
        self.chaguo_umbali=MDGridLayout(
            cols=2,
            padding=40,
            spacing=80
        )
        
        
        

        

        
        self.ngapi_hint=MDTextFieldHintText(
            text=random.choice(['Andika idadi hapa mwaisa!','Hiyo idadi andika hapa','Andika hapa','Hapa hapa hapa!!!','Weka idadi hapaaa...!!'])
        )
        try:self.ngapi.add_widget(self.ngapi_hint)
        except:pass
        def idadi_cheki(instance):
            if self.cheki_idadi.active:
                #self.ngapi.text=''
                self.upana_label.text_color='khaki'
                self.pannel_no_label.text_color='green'
                self.pannel_no_label.text='Panel gapi?'
                self.ngapi.focus=True
                self.pannel.cols=2
                try:self.pannel.add_widget(self.ngapi)
                except BaseException:self.ngapi.focus=True
            else:
                self.upana_label.text_color='grey'
        


        #vipimo
        
        #mwisho
        self.Mwisho=MDGridLayout(
            cols=2,
            padding=20,
            pos_hint={'center_x':0.5,'bottom':0.1},
            #md_bg_color='red'
        )
        for i in range(2):
            try:self.Mwisho.add_widget(MDLabel())
            except:pass

        def mrejesho_menu(b_caller):
            self.drop=MDDropdownMenu(
                id='menu',
                caller=b_caller,
                items=main_dict['menu_items'],
                position='bottom',
                width_mult=3
                
            )
            self.drop.open()
        
        self.mrejesho=MDButton(
            id='mrejesho',
            theme_bg_color='Custom',
            theme_width='Custom',
            md_bg_color='yellow',
            size_hint_min_x=0.4,
            radius=(0,0,0,5),
            on_release=lambda x:mrejesho_menu(x),
            size_hint=(0.425,1)
        )

        self.mrejesho_text=MDButtonText(
            
            text='     Mrejesho       ',
            
        )

        self.upana_label=MDLabel(
            text='Tambulisha idadi',
            text_color='khaki'
            
        )
        
        self.hifadhi=MDButton(
            theme_bg_color='Custom',
            theme_width='Custom',
            md_bg_color='yellow',
            size_hint_min_x=0.4,
            radius=(0,0,5,0),
            size_hint=(0.425,1),
            on_release = self.kamilisha_kila_kitu

            
        )
        self.hifadhi_text=MDButtonText(
            text=random.choice(['           Hifadhi         ',' Tunza hizo taarifa']),
            
        )
        
        self.chaguo_idadi=MDGridLayout(
            cols=2,
            padding=40,
            spacing=80
        )
        self.cheki_idadi=MDCheckbox(color_inactive='khaki', active=False, size_hint=(None, None), size=(dp(40), dp(40)))
    
        pcl=self.parent_check_list
        pcd=self.parent_check_dict
        
        
        
        for i in pcl:
            pcd[i]={
                'child':MDGridLayout(cols=2,padding=40,spacing=80),
                'chaguo_instance':Chaguo(i,self.dhamira,kundi=self.kundi,idadi_label=self.pannel_no_label,indicator=self.indicator,mzunguko=main_dict['mzunguko_%s'%self.dhamira],idadi_mizunguko=self.upana_label.text,vizio=self.vizio,active_labels=self.active_label,all_labels=self.all_labels,tf_all=self.tf_all,parent=self.vipimo,children=pcl[i]['list'],active_color2=pcl[i]['active_color'],active_list=self.tf_list),
                'check_box':MDCheckbox(color_inactive='khaki', active=False, size_hint=(None, None), size=(dp(40), dp(40)))
            }
            

        self.cheki_idadi.bind(on_release=idadi_cheki)  
        try:self.chaguo_idadi.add_widget(self.cheki_idadi)
        except:pass
        try:self.chaguo_idadi.add_widget(self.upana_label)
        except:pass
        try:self.mrejesho.add_widget(self.mrejesho_text)
        except:pass
        try:self.Mwisho.add_widget(self.mrejesho)
        except:pass
        try:self.hifadhi.add_widget(self.hifadhi_text)
        except:pass
        try:self.Mwisho.add_widget(self.hifadhi)
        except:pass
        
        self.kichwa_cha_habari=MDLabel(
            text='%s'%self.dhamira,
            halign='center',
            pos_hint={'center_y':0.35},
            text_color='blue'
        )
        kichwa='%s'%self.kichwa_cha_habari.text
        def Nyongeza(e):
            swali=[
                'Kama unataka kukazia kichwa cha habari bonyeza 1\nKutazama Mchoro bonyeza 2\nKuongezea wazo jipya boyeaz 3\nkuendelea na kujaza taarifa boneza 0'
            ]
            def r_emove(a):
                
                if nyongeza.text!='':
                    self.vipimo.clear_widgets()
                    main_dict['dhamira']=nyongeza.text
                    
                    self.parent_check_list=main_dict['text_field_za_%s'%nyongeza.text]=main_dict['text_field_za_%s'%self.dhamira]
                    main_dict.pop('text_field_za_%s'%self.dhamira)    
                    self.dhamira=self.kichwa_cha_habari.text=nyongeza.text
                else:
                    def sepa(e):
                        if nyongeza.text=='':
                            self.kichwa_cha_habari.text=kichwa
                            self.vipimo.clear_widgets()
                            
                    nyongeza.bind(on_leave=sepa)
                    
                    
            self.kichwa_cha_habari.text=random.choice(['Vipi hapo?','Mbona kama hivyo?','Namna gani tena?','Kuna jipya?'])
            nyongeza=MDTextField(
                theme_bg_color='Custom',
                theme_width='Custom',
                md_bg_color='blue',
                size_hint_min_x=0.4,
                radius=(0,0,5,0),
                size_hint=(0.425,1),
                multiline=False
            )
            nyongeza.bind(on_text_validate=r_emove)
            self.vipimo.clear_widgets()
            try:self.vipimo.add_widget(nyongeza)
            except:pass
            nyongeza.focus=True

        if self.kundi == 'Mbao':self.kichwa_cha_habari.bind(on_leave=Nyongeza)


        self.pannel=MDGridLayout(
            cols=1,
            padding=5
        )

        
        try:self.pannel.add_widget(self.pannel_no_label)
        except:pass
        #urefu       
        global lengo_indicator,lengo_parent,lengo1,ngapi_tf
        lengo_indicator=self.indicator
        lengo_parent=self.pannel
        lengo1=self.dhamira
        ngapi_tf=self.ngapi
        idadi_txt1=self.upana_label.text
        self.kichwa=MDGridLayout(cols=1)
        try:self.kichwa.add_widget(self.kichwa_cha_habari)
        except:pass
        try:self.wigo.add_widget(self.kichwa)
        except:pass

        
        for i in self.parent_check_dict:
            self.wigo.add_widget(self.parent_check_dict[i]['chaguo_instance'])      
        try:self.wigo.add_widget(self.chaguo_idadi)
        except:pass
        try:self.wigo.add_widget(self.pannel)
        except:pass
        try:self.wigo.add_widget(self.vipimo)
        except:pass
        try:self.wigo.add_widget(self.Mwisho)
        except:pass

    def Hifadhi(self):
        if self.fagia!=None:
            try:Clock.schedule_once(self.fagia,(5+len(main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira])*len(main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]['1'])))
            except:pass
            
        def dct(table,dict):
            jina_la_table=table
            ll=dict
            if not ll:
                return
            db_path=self.path
            db=sqlite3.connect(db_path)
            csr=db.cursor()
            keys=list(ll.keys())

            columns=', '.join([f'[{k}] TEXT' for k in keys])
            qr=f'CREATE TABLE IF NOT EXISTS {jina_la_table} (Namba INTEGER PRIMARY KEY AUTOINCREMENT, {columns})'
            csr.execute(qr)
            
            csr.execute(f'PRAGMA table_info({jina_la_table})')
            cols_zilizopo=[info[1] for info in csr.fetchall()]
            for k in keys:
                if k not in cols_zilizopo:
                    try:
                        csr.execute(f'ALTER TABLE {jina_la_table} ADD COLUMN [{k}]')
                        def nambie(e):
                            self.vipimo.clear_widgets()
                            txt=f'{k} meongezwa kwenye {jina_la_table}'
                            try:self.vipimo.add_widget(MDLabel(text=txt, text_color='white'))
                            except:pass
                        nambie(1)
                        Clock.schedule_once(nambie,2)
                    except Exception as e:
                        self.vipimo.clear_widgets()
                        txt=f'imeshindikana kwa sababu {e} {jina_la_table}'
                        try:self.vipimo.add_widget(MDLabel(text=txt, text_color='white'))
                        except:pass


            ingiza_data=', '.join([f'?'for _ in keys])

            columns_=', '.join([f'[{k}]'for k in keys])
            iqr=f'INSERT INTO {jina_la_table} ({columns_}) VALUES ({ingiza_data})'
            try:
                csr.execute(iqr,tuple(ll.values()))
                
                
                db.commit()
                mtu=random.choice(['Stany ','Stany_BABE ','Mr_SMAM ','Mr_ROBORT '])
                weka=random.choice(['weka ','tia ','hifadhi ','ingiza '])
                ndani=random.choice(['ndani ya ','kwenye '])
                
                
                
                dd=[]
                for i in dict:
                    dd.append(i)
                db.row_factory=sqlite3.Row                  
                csr.execute(f'SELECT * FROM {jina_la_table}')
                data=csr.fetchall()
                
                self.vipimo.clear_widgets()
                try:self.vipimo.add_widget(MDLabel(text=f'Subiri kidogo Data zinahifadhiwa ndani ya {db_path}', text_color='white'))
                except:pass
                self.kianzishe(0)

            except sqlite3.OperationalError as sor:
                print(sor)
            finally:
                db.close()
        dict={}
        self.data=d ={}
        for i in main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]:
            d[i]={}
            self.data[i]={}
            for ii in main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][i]:
                d[i]['Jina']=self.dhamira
                self.data[i]['Jina']=self.dhamira
                if self.faili!='':
                    d[i][f'{self.faili[0]}']=f'{self.faili[1]}'
                    self.data[i][f'{self.faili[0]}']=f'{self.faili[1]}'
                d[i][ii]=main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][i][ii]
                self.data[i][ii]=main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][i][ii]
                print(f'aaah{self.data}')
        
        for i in d:
            print(f'{i}>>>{d[i]}')
            dct('%s'%self.kundi,d[i])



    def kamilisha_kila_kitu(self, *args):
        # 1. HATUA YA KWANZA: Hifadhi kwenye Database
        self.Hifadhi() 
        
        # 2. HATUA YA PILI: Chora Mchoro (Tumia Clock ili isikwame)
        # Hii itafuta UI ya zamani na kutanua wigo kama tulivyokubaliana
        #self.hifadhi_na_chora_kitalamu() 
        
        # 3. HATUA YA TATU: Piga Picha (Screenshot)
        # Tunampa sekunde 0.5 ili Mchoro uwe umeshajichora kwanza kioni
        #Clock.schedule_once(lambda dt: self.piga_picha_ya_mchoro(self.faili[1]), 0.5)



    def onyesha_mchoro_kwenye_wigo(self, *args):
        # 1. Ondoa self.chini ili kutoa nafasi ya chini
        if self.chini and self.chini.parent:
            self.chini.parent.remove_widget(self.chini)
        
        # 2. Tanua wigo uchukue kioo chote (Full Height)
        # Tunaiambia wigo itumie 100% ya urefu uliobaki
        self.wigo1.size_hint_y = 1.0  # Mzazi wa wigo
        self.wigo.size_hint_y = 1.0   # Wigo yenyewe
        
        # 3. Safisha wigo (Futa fomu/vitu vya zamani)
        self.wigo.clear_widgets()
        
        # 4. Ongeza kichwa cha habari juu kabisa ya Mchoro
        try:
            self.wigo.add_widget(self.kichwa_cha_habari_1)
        except:
            pass

        # 5. Leta injini kutoka Mchoro.py
        from Mchoro import KichoraSamaniInjini
        
        # Mchoro sasa utakuwa mkubwa na wenye nafasi ya kutosha
        ujazo_wa_mchoro = KichoraSamaniInjini(
            size_hint=(1, 1), # Sasa unajaza eneo lote la wigo lililotanuka
            hali="picha"
        )
        
        # 6. Weka Mchoro ndani ya wigo uliotanuka
        self.wigo.add_widget(ujazo_wa_mchoro)
        
        # 7. Chora data za mteja (Drop Shadow itakuwemo ndani ya Mchoro.py)
        ujazo_wa_mchoro.chora_kutoka_database(self.faili[1])
        
        print("Mchoro umetanuka kitalamu mwaisa! Kila kitu kiko wazi sasa.")
        

    def kamilisha_kazi_na_onyesha_mchoro(self, *args):
        # 1. Jisajili (Hifadhi data ya mwisho kwenye SQLite)
        # Hapa unaita function yako ya hifadhi uliyoitengeneza
        try:
            self.Hifadhi() 
        except:
            print("Taarifa imeshasajiliwa tayari!")

        # 2. Safisha UI (Futa kero ya 'self.chini' na TextFields)
        if self.chini and self.chini.parent:
            self.chini.parent.remove_widget(self.chini)
        
        # 3. Tanua uwanja (Wigo expand)
        # Iambie wigo ichukue kioo chote sasa
        self.wigo1.size_hint_y = 1.0
        self.wigo.size_hint_y = 1.0
        self.wigo.clear_widgets()

        uwanja=self.uwanja
        
        # 5. Ongeza Kichwa cha Habari na Mchoro
        self.wigo.add_widget(self.kichwa_cha_habari_1)
        self.wigo.add_widget(uwanja)

        # 6. Amuru injini isome vipimo na ichore
        # 'self.faili' ndiyo inashikilia ID ya mteja/kazi yako
        uwanja.chora_kutoka_database(self.faili[1])
        
        # 7. Bonus: Weka kitufe kidogo cha 'Rudia' (Back)
        # Ili fundi akitaka kurekebisha vipimo aweze kurudi
        self.ongeza_kitufe_cha_kurudi()

    def ongeza_kitufe_cha_kurudi(self):
        # Hii itaweka kitufe kidogo cha kurudi pembeni ya Mchoro
        back_btn = MDButton(
            style="tonal",
            pos_hint={'right': 0.95, 'top': 0.1},
            on_release=lambda x: self.rudisha_fomu_ya_vipimo()
        )
        back_btn.add_widget(MDButtonText(text="Sahihisha"))
        self.wigo.add_widget(back_btn)

    def hifadhi_na_chora_kitalamu(self, *args):
        # Hatua ya 1: Hifadhi taarifa mara moja (Main Thread)
        try:
            self.Hifadhi()
            print("Taarifa imehifadhiwa...")
        except Exception as e:
            print(f"Kosa la database: {e}")
            return

        # Hatua ya 2: Panga uchoraji ufanyike baada ya muda mfupi sana
        # Hii 0.1 inaruhusu app kupumua na kufanya 'Cleanup' ya UI kwanza
        #Clock.schedule_once(self.anzisha_mchoro_mubashara, 0.1)

    def anzisha_mchoro_mubashara(self, dt):
        """ Hii inaitwa na Clock baada ya database kuwa tayari """
        
        # 1. Safisha UI na Tanua Wigo (Expand)
        try:
            if self.chini and self.chini.parent:
                self.chini.parent.remove_widget(self.chini)
        except :pass
            
        self.wigo1.size_hint_y = 1.0
        self.wigo.size_hint_y = 1.0
        self.wigo.clear_widgets()

        # 2. Leta Injini ya Mchoro
        from Mchoro import KichoraSamaniInjini
        uwanja = KichoraSamaniInjini(size_hint=(1, 1), hali="picha")
        
        # 3. Weka Lebo na Uwanja wa Mchoro
        self.wigo.add_widget(self.kichwa_cha_habari_1)
        self.wigo.add_widget(uwanja)

        # 4. Amuru injini isome vipimo vipya
        uwanja.chora_kutoka_database(self.faili[1])
        
        print("Mchoro umekamilika kitalamu!")

    def on_touch_move(self, touch):
        if 'multitouch_sim' in touch.profile or len(self.uwanja._touches) > 1:
            # Logic ya Zoom kwa vidole viwili hapa
            pass

    def piga_picha_ya_mchoro(self, jina_la_mteja):
        if platform == 'android':
            # 1. Kwa Android: Tunatumia folder la 'Pictures' la mfumo ili ionekane kwenye Gallery
            from android.storage import primary_external_storage_path
            base_path = primary_external_storage_path()
            folder = os.path.join(base_path, 'Pictures', 'Karakana_Quotes')
        """ Inachukua Mchoro uliopo kioo na kuusave kama PNG """
        folder = '/home/smam_mwambije/Pictures/Karakana_Quotes'
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        faili_jina = os.path.join(folder, f"Mchoro_{jina_la_mteja}.png")
        
        # Hapa ndipo ujanja ulipo: Tunachukua eneo la Mchoro pekee
        self.export_to_png(faili_jina)
        print(f"Safi! Picha imehifadhiwa hapa: {faili_jina}")
        return faili_jina




    def kianzishe(self,mzunguko):
        db=sqlite3.connect(self.path)
        cs=db.cursor()
        cs.execute(f'SELECT * FROM {self.kundi}')
        data=cs.fetchall()
        db.commit()
        l=[]
        
        for i in main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]:
            l.append(main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][i])
        sekunde=len(l[mzunguko-1])
        
        #self.vipimo.clear_widgets()
        if mzunguko < len(l):
            self.event=Clock.schedule_once(lambda mz=mzunguko:self.badilisha(mzunguko),1*sekunde)
        else:
            if self.mwisho!=None:
                self.wigo.clear_widgets()
                try:self.ndani.remove_widget(self.chini)
                except:pass
                try:self.wigo.add_widget(self.kichwa_cha_habari_1)
                except:pass
                try:self.wigo.add_widget(self.mwisho)
                except:pass
                

            

    def badilisha(self,dt):
            l=[]
            for i in main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]:
                l.append(i)
            
            mtu=random.choice(['Stany ','Stany_BABE ','Mr_SMAM ','Mr_ROBORT '])
            weka=random.choice(['weka ','tia ','hifadhi ','ingiza '])
            ndani=random.choice(['ndani ya ','kwenye '])
            db=sqlite3.connect(self.path)
            cs=db.cursor()
            cs.execute(f'SELECT * FROM {self.kundi}')
            data=cs.fetchall()
            db.commit()
            
            
            taarifa=data[len(data)-len(l)+dt-1]                 
            txt=f'{mtu} ame{weka}{taarifa}ndani ya safu ya {self.kundi}'
            self.vipimo.clear_widgets()
            try:self.vipimo.add_widget(MDLabel(text=txt, text_color='white'))
            except:pass
            self.indx=self.indx+1
        
            self.kianzishe(dt+1)
            
            
            
    def remove_ngapi(self,e):
        if main_dict['dhamira']!='':self.dhamira=main_dict['dhamira']
        def tulia(e):
            self.ngapi.error=False
        self.ngapi.bind(on_text=tulia)
        try: self.ngapi.text=int(self,ngapi.text)
        except:
            self.ngapi.error=True
        
        tupo=random.choice(['tupo','ndo tunaingia','unaanza kuandika data za','ndani ya','unachojaza sasa ni data za'])
        ll=[]
        for i in self.tf_list:
            ll.append(i)
        next=self.tf_all[ll[0]]

        self.pannel.remove_widget(self.ngapi)
        self.pannel_count=self.ngapi.text
        global mizunguko,lengo,idadi_txt,label_ya_idadi
        '''try:
            if self.mizunguko==100000000:
                mizunguko=mzunguko_
        except NameError:
            mizunguko=self.ngapi'''
        lengo=self.dhamira
        idadi_txt=self.upana_label.text
        #mizunguko=int(self.ngapi.text)+mizunguko
        label_ya_idadi=self.pannel_no_label
        
        maelekezo=[
            'Inaonyesha unataka kuongeza vipimo vya vitu %s'%self.ngapi.text
        ]
        try:
            try: idadi=main_dict['mzunguko_wa_%s'%self.dhamira]
            except KeyError:idadi=main_dict['mzunguko_wa_%s'%self.dhamira]=0
            try:
                multplier=len(main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])])
                
            except KeyError:multplier=1
            #self.mwenendo['%s'%len(self.mwenendo)]={'mizunguko':self.ngapi.text,'vipimo':{'idadi':int(multplier),'vilivyoratibiwa':idadi,'majina':main_dict['text_field_za_%s'%self.dhamira]}}
            
            try:
                
                previous=main_dict['previous']
                
            except:    
                previous=0
            try:
                multiplier=self.mwenendo['%s'%(len(self.mwenendo)-2)]['vipimo']['idadi']
                
            except:
                multiplier=int(multplier)
            self.mizunguko=int(self.ngapi.text)*multplier
            try: mm=main_dict['mizunguko_ya_%s'%self.dhamira]
            except KeyError:main_dict['mizunguko_ya_%s'%self.dhamira]=int(self.ngapi.text)*multplier
            
            if main_dict['mizunguko_ya_%s'%self.dhamira]==main_dict['mzunguko_wa_%s'%self.dhamira]:main_dict['mizunguko_ya_%s'%self.dhamira]=int(main_dict['mzunguko_wa_%s'%self.dhamira])
            try:valu=int(main_dict['mizunguko_ya_%s'%self.dhamira])
            except:
                main_dict['mizunguko_ya_%s'%self.dhamira]=int(main_dict['mzunguko_wa_%s'%self.dhamira])
            if 0<int(self.ngapi.text)<int(previous):
                self.ngapi.error=True
                #try:self.ngapi.add_widget(MDTextFieldHelperText(text=random.choice(maelekezo)))
                #except:pass
                lengo_parent.remove_widget(lengo_indicator)
                lengo_parent.cols=3
                try:lengo_parent.add_widget(self.ngapi)                    
                except:pass
                self.ngapi.focus=True
                
            
            elif int(self.ngapi.text)>int(previous):

                main_dict['mizunguko_ya_%s'%self.dhamira]=int(main_dict['mzunguko_wa_%s'%self.dhamira])+(int(self.ngapi.text)-int(previous))*multplier
                self.vipimo.clear_widgets()
                try:self.vipimo.add_widget(next)
                except:pass
                next.focus=True
                if main_dict['namba_ya_mzunguko_kamili']>1:
                    tft=main_dict['mizunguko_ya_%s'%self.dhamira]-int(main_dict['mzunguko_wa_%s'%self.dhamira])
                    main_dict['mzunguko_wa_%s'%self.dhamira]=previous*multiplier
                    main_dict['mizunguko_ya_%s'%self.dhamira]=main_dict['mzunguko_wa_%s'%self.dhamira]+tft
            else:
                main_dict['mizunguko_ya_%s'%self.dhamira]=int(self.ngapi.text)*multplier
                self.ngapi.error=False
            main_dict['idadi_error0_%s'%self.dhamira]=0
            self.indicator.value=100*int(main_dict['mzunguko_wa_%s'%self.dhamira])/int(main_dict['mizunguko_ya_%s'%self.dhamira])
            

        except ValueError:
            self.ngapi.error=True
        if self.ngapi.error ==False:
            self.vipimo.clear_widgets()
            try:self.vipimo.add_widget(next)
            except:pass
            next.focus=True
        else:pass
        
        try:l_no=label_no+1
        except NameError:
            l_no=1
        self.pannel_no_label.text='%s %s %s_no_%s'%(self.vimsha,tupo,self.dhamira,l_no)
        
        #
        
        #lengo_parent.clear_widgets()
        try:
            lengo_parent.cols=1
            lengo_parent.add_widget(lengo_indicator)
        except BaseException:pass
    
class Chaguo(MDGridLayout):
    def __init__(self,text,lengo_,kundi='',idadi_label=ObjectProperty(),indicator=ObjectProperty(),mzunguko=1,idadi_mizunguko=100000000,vizio={},active_labels={},all_labels={},tf_all={},parent=ObjectProperty(),children=['........','......','.....'],active_color1='yellow',active_color2='brown',deactive_color1='khaki',deactive_color2='khaki',state=False,active_list=[],**kwargs):
        super().__init__(**kwargs)
        if main_dict['dhamira'] == '':
            self.dhamira=lengo_
        else:self.dhamira=main_dict['dhamira']
        self.size_hint_y=0.5
        if text==StringProperty():
            self.text=[text,text]
        else:self.text=[text,text]
        main_dict['unit_%s'%self.dhamira]=1/len(children)
        self.child=children
        main_dict['mzunguko_%s'%self.dhamira]=mzunguko
        self.active_color1=active_color1
        self.active_color2=active_color2
        self.deactive_color1=deactive_color1
        self.deactive_color2=deactive_color2
        self.cols=1
        self.master=BooleanProperty(0)
        self.utambulisho_idadi=self.master
        self.padding=40,
        self.spacing=80
        self.mrejesho=0
        self.cb_list={}
        self.lb_list={}
        self.tf_list=tf_all
        self.actv_tf=[]
        self.tf_all=tf_all
        self.txf_list=active_list
        self.actv_sorted_tf=[]
        self.kizio=vizio
        self.active_label=active_labels
        self.constant_text=all_labels
        self.idadi_label=idadi_label
        self.bado=0
        self.kundi=kundi
        self.idadi_mizunguko=idadi_mizunguko
        self.indicator=indicator
        
        
        

        try:self.chek_list=main_dict['text_field_za_%s'%self.dhamira]
        except KeyError:self.chek_list=main_dict['text_field_za_%s'%self.dhamira]=[]
        self.box=MDGridLayout(
            cols=2*len(children)
        )
        try:self.mwenendo=main_dict['mwenendo_wa_taarifa_za_%s'%self.dhamira]
        except:self.mwenendo=main_dict['mwenendo_wa_taarifa_za_%s'%self.dhamira]={}
        try:mwendo=self.mwenendo['mzunguko_kamili']  
        except:
            self.mwenendo['mzunguko_kamili'] ={}  
        lengo=''
        
       
        def child(i,iii,ii,iv,v):
            try:aa=main_dict['text_field_za_%s'%self.dhamira]
            except:
                self.dhamira=main_dict['dhamira']

            def hifadhi_hamisha(instance1):
                value=instance1.text
                main_dict['text_field_ya_%s-%s'%(iv.text.lower(),self.dhamira)]=instance1
                main_dict['kizio_cha_%s-%s'%(iv.text.lower(),self.dhamira)]=value
                parent.clear_widgets()
                #nani anafuata
                if self.chek_list.index(instance1)<len(self.chek_list)-1:
                    instance2=self.chek_list[(self.chek_list.index(instance1))+1]

                else:
                    ll=[]
                    lll=[]
                    for iiii in self.txf_list:
                        ll.append(iiii)
                    try:
                        instance2=self.tf_list[ll[0]]
                    except BaseException:
                        instance2=self.tf_list[iii]
                try:parent.add_widget(instance2)
                except:pass
                instance2.focus=True
                ii.text_color=self.active_color2
            def txt_kizio(x):
                self.kizio[v]=x.text
                parent.clear_widgets()
                
                if len(self.txf_list)<=1:
                    try:parent.add_widget(self.tf_list[iii])
                    except:pass
                    self.tf_list[iii].focus=True
                else:
                    parent.clear_widgets()
                    
                    ll=[]
                    lll=[]
                    for iiii in self.txf_list:
                        ll.append(iiii)
                    try:
                        parent.clear_widgets()
                        try:parent.add_widget(self.tf_list[ll[0]])
                        except:pass
                        self.tf_list[ll[0]].focus=True
                    except BaseException:
                        parent.clear_widgets()
                        try:parent.add_widget(self.tf_list[iii])
                        except:pass
                        self.tf_list[iii].focus=True
                ii.text_color=self.active_color2
            try:
                ee=main_dict['namba_ya_mzunguko_kamili']
            except:main_dict['namba_ya_mzunguko_kamili']=1
                            
            if i.active:
                ii.text_color='white'#self.active_color2
                self.actv_tf.append(iii)
                self.txf_list.append(iii)
                self.active_label[v]=iv
                but_kiz=MDTextField(
                    theme_text_color='Custom',
                    text_color_focus= "white",
                    theme_line_color="Custom",
                    line_color_normal="green",
                    text_color_normal='yellow',
                    theme_bg_color='Custom',
                    theme_width='Custom',
                    radius=(0,0,0,0),
                    multiline=False,
                    on_text_validate=lambda x:hifadhi_hamisha(x)
                )#x:txt_kizio(x))#,input_filter='string')
                try:but_kiz.add_widget(MDTextFieldHintText(theme_text_color='Custom',text_color_normal="white",text='Kizio cha %s'%iv.text.lower(),text_color=self.active_color2))
                except:pass
                parent.clear_widgets()
                try:uu=main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]
                except:main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]={}
                main_dict['text_field_za_%s'%self.dhamira].append(but_kiz)
                try:q=main_dict['index_za_text_field__%s'%(self.dhamira)]
                except:main_dict['index_za_text_field__%s'%(self.dhamira)]={}
                main_dict['index_za_text_field__%s'%(self.dhamira)][iv.text]=len(main_dict['text_field_za_%s'%self.dhamira])-1
                self.actv_tf.append(iii)
                self.txf_list.append(iii)
                try:act_tf=main_dict['txtf_list_za_active_%s'%self.dhamira]
                except KeyError:act_tf=main_dict['txtf_list_za_active_%s'%self.dhamira]=[]
                main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][iv.text]=len(main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])])+1
                ping=len(main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])])+1
                main_dict['txtf_list_za_active_%s'%self.dhamira].append(self.tf_list[iii])
                main_dict['len_list_active_checkbutton_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]=len(main_dict['text_field_za_%s'%self.dhamira])
                main_dict['nafasi_ya_chekibox_%s_%s'%(self.dhamira,iv.text.lower())]=len(main_dict['text_field_za_%s'%self.dhamira])
                try:parent.add_widget(self.chek_list[0])
                except:pass
                self.chek_list[0].focus=True
                
            else:
                try:
                    main_dict['text_field_za_%s'%self.dhamira].remove(main_dict['text_field_za_%s'%self.dhamira][main_dict['index_za_text_field__%s'%(self.dhamira)][iv.text]])
                    
                
                except :pass
                tl=[]
                for i in main_dict['text_field_za_%s'%self.dhamira]:
                    tl.append(i)
                main_dict['index_za_text_field__%s'%(self.dhamira)].pop(iv.text)
                main_dict['txtf_list_za_active_%s'%self.dhamira].remove(self.tf_list[iii])
                ii.text_color=self.deactive_color2
                try:main_dict['len_list_active_checkbutton_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]=main_dict['len_list_active_checkbutton_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]-1
                except:pass
                self.actv_tf.remove(iii)
                self.txf_list.remove(iii)
                try:
                    main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])].pop(iv.text)
                    tl=[]
                    for i in main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]:
                        tl.append(i)
                        main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][i]=int(tl.index(i)+1)
                except:pass
                try:self.active_label.pop(iii)
                except KeyError:pass
            try:main_dict['updated_menu_items']=main_dict['updated_menu_items']+1
            except:pass
            

            self.actv_sorted_tf.clear()          
        h1=random.choice(['Lazima ujaze','Anza na','ni vyema kuanza na'])
        h2=random.choice(['kwanza','kwanza halafu ndo uendelee na kinachofuata','','maana ni taarifa ya muhimu']) 
        main_dict['textfield_list_za_%s'%self.dhamira]=[]
        for i in range(len(children)):
            
            hint=self.lb_list['lb_%s'%children[i]]=MDLabel(role='small',text=children[i].title(),id='lb_%s'%children[i])
            this1='tf_cb_%s'%children[i]
            self.tf_list['tfh_%s'%children[i]]=MDTextFieldHintText(theme_text_color='Custom',text_color_normal="white",text=children[i])
            self.tf_list['tf_cb_%s'%children[i]]=MDTextField(
                theme_text_color='Custom',
                text_color_focus= "white",
                theme_line_color="Custom",
                line_color_normal="yellow",
                multiline=False,radius=(0,0,0,0),size_hint=(0.9,None),theme_bg_color='Custom',md_bg_color='white',mode='outlined',on_text_validate=lambda x,y=this1,h=hint,prt=parent:self.text_on_validate(prt,x,y,h))
            main_dict['textfield_list_za_%s'%self.dhamira].append(self.tf_list['tf_cb_%s'%children[i]])
            main_dict['textfield_%s_%s'%(self.dhamira,children[i])]=self.tf_list['tf_cb_%s'%children[i]]
            #self.tf_list['tfp_%s'%children[i]]=MDTextFieldHelperText(mode='on_error',text='%s %s %s'%(h1,children[i],h2))
            for a in [self.tf_list['tfh_%s'%children[i]]]:
                try:self.tf_list['tf_cb_%s'%children[i]].add_widget(a)
                except:pass
            
            self.cb_list['cb_%s'%children[i]]=MDCheckbox(color_inactive='khaki',color_active=self.active_color2,active=state,id='cb_%s'%children[i])
     
        for i,ii in zip(self.cb_list,self.lb_list):
            lb=self.lb_list[ii]
            lbtxt=ii
            self.cb_list[i].md_bg_color='khaki'
            self.lb_list[ii].text_color='khaki'
            self.constant_text[ii]=lb.text
            tf=('tf_%s'%i)
            self.cb_list[i].bind(on_active=lambda x,y,tf='tf_%s'%i,iii=self.lb_list[ii],iv=lb,v=lbtxt:child(x,tf,iii,iv,v))
            try:self.box.add_widget(self.cb_list[i])
            except:pass
            try:self.box.add_widget(self.lb_list[ii])
            except:pass
        try:self.add_widget(self.box)
        except:pass
    
    
    def angalia(self,parent,e):
        try:
            dict_=main_dict['cheki_box_zinazotazamwa'][int(main_dict['ruhusa_ya_%s'%self.dhamira])-1][4]
            if main_dict['ruhusa_ya_%s'%self.dhamira]<=len(dict_):
                
                  
                self.onyesha(parent,e)
                main_dict['ruhusa_ya_%s'%self.dhamira]=main_dict['ruhusa_ya_%s'%self.dhamira]+1

        except:
            parent.clear_widgets()
            try:parent.add_widget(MDLabel(text='Nnadhani umeona ulichokijaza.',text_color='white'))
            except:pass
            main_dict['ruhusa_ya_%s'%self.dhamira]=1
        
    def onyesha(self,parent,e):
        try:aa=main_dict['ruhusa_ya_%s'%self.dhamira]   
        except:yeah=main_dict['ruhusa_ya_%s'%self.dhamira]=1                   
        parent.clear_widgets()
        fmt=main_dict['cheki_box_zinazotazamwa'][int(main_dict['ruhusa_ya_%s'%self.dhamira])-1]
        try:parent.add_widget(MDLabel(text='%s ni %s %s'%(fmt[0],fmt[1],fmt[2]),text_color='khaki'))
        except:pass       
        Clock.schedule_once(lambda aaa=parent,bb=e:self.angalia(main_dict['mlengwa'],bb),4)
                
    def text_on_validate(self,parent,this,this1,hint,this_idadi=0):
        if main_dict['dhamira']!='':
            lengo1=self.dhamira=main_dict['dhamira']
        parent.clear_widgets()
        try:aa=main_dict['Taarifa'][self.kundi]
        except:main_dict['Taarifa'][self.kundi]={}
        try:aa=main_dict['Taarifa'][self.kundi][self.dhamira]
        except:main_dict['Taarifa'][self.kundi][self.dhamira]={}
        def text_field_set(x):
            
            mk=main_dict['mzunguko_wa_mwisho']#['%s'%x
            
            llll=[]
            for i in mk[x]:
                txtf1=mk[x][i]['vtf']
                txtf2=mk[x][i]['ktf']
                cb=mk[x][i]['checkbox']
                cbz=dir(mk[x][i]['idadi'])
                lcbz=[]
                for ai in cbz:
                    lcbz.append(ai)
                
                                
                txtf1.text=mk[x][i]['value']
                txtf2.text=mk[x][i]['kizio']
                llll.append([i,txtf2.text,txtf1.text,x,lcbz])
            main_dict['cheki_box_zinazotazamwa']=llll
            ii={}
            ii['n']=0
            main_dict['mlengwa']=parent
            self.onyesha(parent,llll)
        tfl=main_dict['txtf_list_za_active_%s'%self.dhamira]
        if tfl. index(this)<len(tfl)-1:anayefuata=tfl[tfl.index(this)+1]
        else:anayefuata=tfl[0]
        try:
            mz=main_dict['mizunguko_ya_%s'%self.dhamira]
            try:mz1=main_dict['mzunguko_wa_%s'%self.dhamira]
            except KeyError:main_dict['mzunguko_wa_%s'%self.dhamira]=0
            
            try:
                if main_dict['mzunguko_wa_%s'%self.dhamira]<=main_dict['mizunguko_ya_%s'%self.dhamira]:
                    main_dict['mzunguko_wa_%s'%self.dhamira]=main_dict['mzunguko_wa_%s'%self.dhamira]+1
                    if main_dict['mzunguko_wa_%s'%self.dhamira]==main_dict['mizunguko_ya_%s'%self.dhamira]:
                        try:nmk=main_dict['namba_ya_mzunguko_kamili']
                        except:nmk=main_dict['namba_ya_mzunguko_kamili']=1
                        
                        self.indicator.value=100*(main_dict['mzunguko_wa_%s'%self.dhamira]/main_dict['mizunguko_ya_%s'%self.dhamira])
                        
                        main_dict['mizunguko_ya_%s'%self.dhamira]='mwisho'
                        
                        try:parent.add_widget(MDLabel(text='M W I S H O . . . !'))
                        except:pass
                        kielezi=random.choice(['tayari','kwenye mfumo','kikamilifu','tayari kwa ajili ya kuchakatwa',''])
                        def mwisho(e):
                            parent.clear_widgets()
                            try:parent.add_widget(lb)
                            except:pass
                        
                        no=main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]
                        
                        tf_kizio=main_dict['text_field_ya_%s-%s'%(hint.text.lower(),self.dhamira)]
                
                        kizio=main_dict['kizio_cha_%s-%s'%(hint.text.lower(),self.dhamira)]
                        actv_cb=main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]
                        self.mwenendo['mzunguko_kamili']['%s'%no][hint.text]={'value':this.text,'vtf':this,'kizio':tf_kizio.text,'ktf':tf_kizio,'checkbox':self.cb_list['cb_%s'%hint.text.lower()],'idadi':'%s'%actv_cb,'nafasi':main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][hint.text]}
                        main_dict['Taarifa'][self.kundi][self.dhamira]['%s'%no][hint.text]={'value':this.text,'vtf':this,'kizio':tf_kizio.text,'ktf':tf_kizio,'checkbox':self.cb_list['cb_%s'%hint.text.lower()],'idadi':'%s'%actv_cb,'nafasi':main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][hint.text]}                       
                        try:
                            aaa=main_dict['items_menu']
                    
                        except:
                            main_dict['items_menu']={}
                        
                        
                        main_dict['items_menu'][no]=(
                            {
                                'text':'%s namba_%s'%(self.dhamira,no),
                                'on_release':lambda x='%s'%no:text_field_set(x)
                            }
                        )
                        main_dict['menu_items'].clear()
                        for i in main_dict['items_menu']:
                            main_dict['menu_items'].append(main_dict['items_menu'][i])
                        
                        lst=[]
                        print(main_dict['mizunguko_ya_%s'%self.dhamira])
                        main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira]=mwisho_kabisa
                        
                        for ie in self.mwenendo['mzunguko_kamili']:
                            
                            if int(ie)>len(main_dict['mzunguko_wa_mwisho']):
                                try:mm=main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][ie]
                                except:main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][ie]={}#
                                print(main_dict['mizunguko_ya_%s'%self.dhamira])
                                for ky in self.mwenendo['mzunguko_kamili'][ie]:
                                    #rint(ky['value'])
                                    main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][ie]['kizio_cha_%s'%ky]=self.mwenendo['mzunguko_kamili'][ie][ky]['kizio']  
                                    main_dict['vilivyohifadhiwa'][self.kundi][self.dhamira][ie]['%s'%ky]=self.mwenendo['mzunguko_kamili'][ie][ky]['value'] 
                                                    
                                main_dict['mzunguko_wa_mwisho'][ie]=self.mwenendo['mzunguko_kamili'][ie]
                        self.mwenendo['mzunguko_kamili'].clear()
                        main_dict['namba_ya_mzunguko_kamili']=main_dict['namba_ya_mzunguko_kamili']+1
                        
                        main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]=main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili']-1)]
                        #global previous
                        previous=main_dict['previous']=no
                        
                    else:
                        
                        try:nmk=main_dict['namba_ya_mzunguko_kamili']
                        except:nmk=main_dict['namba_ya_mzunguko_kamili']=1
                        try:
                            no=main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]
                            
                        except:
                            try:
                                
                                no=len(main_dict['mzunguko_wa_mwisho'])
                                if no==0:
                                    no=1 
                                    main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]=0
                                else:main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]=no
                                
                            except:    
                                main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]=0
                                no=0
                                
                
                        if (main_dict['mzunguko_wa_%s'%self.dhamira]-1)%len(main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])])==0:
                            no=main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]=main_dict['mzunguko_kamili_wa_%s_no_%s'%(self.dhamira,nmk)]+1
                               
                        try:
                            aa=self.mwenendo['mzunguko_kamili']['%s'%no]
                            bb=main_dict['Taarifa'][self.kundi][self.dhamira]['%s'%no]

                        except:
                            self.mwenendo['mzunguko_kamili']['%s'%no]={}
                            main_dict['Taarifa'][self.kundi][self.dhamira]['%s'%no]={}

                        
                        tf_kizio=main_dict['text_field_ya_%s-%s'%(hint.text.lower(),self.dhamira)]
            
                        kizio=main_dict['kizio_cha_%s-%s'%(hint.text.lower(),self.dhamira)]
                        actv_cb=main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])]
                        self.mwenendo['mzunguko_kamili']['%s'%no][hint.text]={'value':this.text,'vtf':this,'kizio':tf_kizio.text,'ktf':tf_kizio,'checkbox':self.cb_list['cb_%s'%hint.text.lower()],'idadi':'%s'%actv_cb,'nafasi':main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][hint.text]}                       
                        main_dict['Taarifa'][self.kundi][self.dhamira]['%s'%no][hint.text]={'value':this.text,'vtf':this,'kizio':tf_kizio.text,'ktf':tf_kizio,'checkbox':self.cb_list['cb_%s'%hint.text.lower()],'idadi':'%s'%actv_cb,'nafasi':main_dict['active_check_box_za_%s_no_%s'%(self.dhamira,main_dict['namba_ya_mzunguko_kamili'])][hint.text]}                       
                        
                        try:parent.add_widget(anayefuata)
                        except:pass
                        anayefuata.focus=True
                        self.indicator.value=100*(main_dict['mzunguko_wa_%s'%self.dhamira]/main_dict['mizunguko_ya_%s'%self.dhamira])
                        try:
                            aaa=main_dict['items_menu']
                    
                        except:
                            main_dict['items_menu']={}
                        
                        
                        main_dict['items_menu'][no]=(
                            {
                                'text':'%s namba_%s'%(self.dhamira,no),
                                'on_release':lambda x='%s'%no:text_field_set(x)
                            }
                        )
                        main_dict['menu_items'].clear()
                        for i in main_dict['items_menu']:
                            main_dict['menu_items'].append(main_dict['items_menu'][i])
                        
                else:
                    pass
            except TypeError:
                parent.clear_widgets()    
                try:parent.add_widget(MDLabel(text='Fuata utaratibu kijana'))
                except:pass
            
        except KeyError as ke:
            print (ke)
            ni_=random.choice(['Ningependa','Ni vyema','Itapendeza kama utaniwezesha','Me nataka'])
            ku_=random.choice(['kujua','kufahamu','kutabua','unijulishe','ukanijulisha'])
            data=random.choice(['data za %s'%self.dhamira,'%s_data'%self.dhamira,self.dhamira])
            kwz=random.choice(['kwanza','','kwanza\nYaani boya kitufe pembeni ya neno "%s" alafu kitakuonyesha mahali pa kuandika hiyo idadi'%self.idadi_mizunguko])
            txt='%s %s idadi ya %s %s'%(ni_,ku_,data,kwz)
            parent.clear_widgets()
            try:parent.add_widget(MDLabel(role='small',text=txt,text_color='red'))
            except:pass

        
    