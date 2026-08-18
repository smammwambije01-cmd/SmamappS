# shelve,dbm.dumb
import sqlite3
import os
import random
import math
import json
from kivy.graphics import Color, Rectangle, Line
from rectpack import newPacker
import traceback
# Kivy Base Imports
from kivy.clock import Clock 
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

# Kivy Properties
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

# KivyMD Layouts
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout

# KivyMD Components (Buttons & Labels)
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton, MDFabButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import (
    MDDialog, 
    MDDialogHeadlineText, 
    MDDialogContentContainer, 
    MDDialogButtonContainer
)
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldHelperText
from kivymd.uix.menu import MDDropdownMenu

# KivyMD List Components
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTertiaryText,
    MDListItemTrailingCheckbox,
)
#from kivy.uix.scrollview import ScrollView

path_='/home/smam_mwambije/.config/karakana'

class Mteja(MDGridLayout):
    def __init__(self,data,p_key,kichwa,nav_rail=ObjectProperty(),path='',**kwargs):
        super().__init__(**kwargs)
        self.data=data
        self.namba=0
        self.cols=1
        self.nav_rail=nav_rail
        self.items={}
        self.ktu=[]
        self.prnt=ObjectProperty()
        self.rail=ObjectProperty()
        self.item=ObjectProperty()
        self.ndani=ObjectProperty()
        self.chini=ObjectProperty()
        self.g_prnt=ObjectProperty()
        self.ndani_kabisa=ObjectProperty()
        self.faili={}
        self.kichwa={}
        self.path_=path
        self.kichwa_cha_habari=''
        path=os.path.join(self.path_,f'{self.data}.sqlite')   
        try:
            print('Ndo naingia hapa')
            print(path)
            taarifa=sqlite3.connect(path)
            
            taarifa.row_factory=sqlite3.Row
            cs=taarifa.cursor()
            dat=cs.fetchall()
            zote=cs.execute(f'SELECT * FROM {data} ')
            items={}
            sclll=ScrollView()
            lst=MDList()
            print(f'Taarifa zote hizi hapa {dat}')
            for i in zote:
                try:
                    if i['jina maarufu']!='None' or i['jina maarufu']!='':jina=i['jina maarufu']
                        
                           
                except:
                    if i['jina la kwanza']!='None' or i['jina maarufu']!='':jina=i['jina la kwanza']
                
                try:
                    hitaji=i['anachohitaji']
                    items[f'{i["Namba"]}']=MDListItem(on_release=lambda itm: self.unda_kazi(itm))
                    print(1)
                    self.faili[items[f'{i["Namba"]}']]=[f'{p_key} ya {data}',f'{i[p_key]}']
                    print(2)
                    items[f'{i["Namba"]}icon']=MDListItemLeadingIcon(icon='account')
                    if f'{jina}'=='None' or f'{jina}'=='':
                        print('kimeumana!')
                        try:                          
                            jina=f'Mteja fulani {i["Namba"]}'
                            hitaji=f'Kabati namba {i["Namba"]}'
                            print('imetiki')
                        except:pass
                            
                    mahal=i["mahali"]     
                    if f'{mahal}'=='None' or f'{mahal}'=='':
                        print('kimeumana!')
                        try:
                            mahal=f'Mahali fulani {i["Namba"]}'
                            hitaji=f'Kabati namba {i["Namba"]}'
                            print('imetiki')
                        except:pass
                            
                    print(jina)
                    items[f'{i["Namba"]}head']=MDListItemHeadlineText(text=jina)
                    print(4)
                    items[f'{i["Namba"]}supp']=MDListItemSupportingText(text=mahal,role='small')
                    print(5)
                    items[f'{i["Namba"]}tert']=MDListItemTertiaryText(text=hitaji,role='small')
                    print(6)
                    txt=self.kichwa[items[f'{i["Namba"]}']]=f'{jina.title()} {kichwa.lower()} {hitaji.upper()}'
                    print(7)
                except    Exception as er:print(er)
                
                for ii in [items[f'{i["Namba"]}icon'],items[f'{i["Namba"]}head'],items[f'{i["Namba"]}supp'],items[f'{i["Namba"]}tert']]:
                    items[f'{i["Namba"]}'].add_widget(ii)
                lst.add_widget(items[f'{i["Namba"]}'])
            #taarifa.commit()
            taarifa.close()
            scrlll.add_widget(lst)
            self.add_widget(scrlll)
            print(f'Hizi hapa \n{dat}')
        except Exception as error:
            print(error.with_traceback(error.__traceback__))
        
    def unda_kazi(self,item):    
        self.namba=1
        def kazia():
            
            for i in self.items:
                try:
                    self.items[i]['kazi'].kichwa.clear_widgets()
                    txt=MDLabel(halign='center',role='small',text_color='white',text=f'{self.kichwa[item]}\n{self.items[i]["kazi"].kichwa_cha_habari.text}')
                    self.items[i]['kazi'].kichwa.add_widget(txt)
                    next=self.items[i]['kazi'].mwisho=Chagua_malighafi(kichwa='Material specification',path=self.path_)
                    self.items[i]['kazi'].ndani=self.ndani
                    self.items[i]['kazi'].chini=self.chini
                    next.prnt=self.items[i]['kazi'].ndani
                    self.items[i]['kazi'].kichwa_cha_habari_1.text=f'{txt.text}\n{next.kichwa_cha_habari.upper()}'
                    next.prnt_label=self.items[i]['kazi'].kichwa_cha_habari_1
                    next.g_prnt=self.g_prnt
                    next.kitu=self.items[i]['kazi'].kichwa_cha_habari.text
                    next.kazi=self.items[i]['kazi']
                    self.items[i]['kazi'].fagia=next.anza_kuchagua
                    
                except Exception as ee:print(ee)
                self.items[i]['kazi'].faili=[f'{self.faili[item][0]}',f'{self.faili[item][1]}']
                
                self.rail.vipimo(self.ktu[i],self.items[i]['kazi']) 
        kazia()
        self.prnt.remove_widget(self)
       
        self.item=item 
        self.kichwa_cha_habari=item.on_release 
        print(self.kichwa_cha_habari)






class Chagua_malighafi(MDGridLayout):
    def __init__(self, data=[], kichwa='', path='',mhitaji='', **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.path = path
        self.kichwa_cha_habari = kichwa
        self.kazi = mhitaji
        self.mahitaji={}
        #self.kazi.update_status=self.kazi.update_status
        self.Gharama=MDListItemHeadlineText()
        self.makundi_ya_mbao={}    
        self.rangi_zote={}
        
        import math, random
        self.double_touch=False
        
        
        # Bind kitendo cha ku-click checkbox na mbao husika
        
        # 1. CONTAINER KUU YA MAELEZO (Unyama wa No Overlap)
        
        
        # ScrollView ya kuruhusu list ndefu kuserereka (do_scroll_y=True)
        self.scrll = ScrollView(size_hint=(1, None), height="400dp")#(do_scroll_x=False, do_scroll_y=True)
        self.boards = ScrollView()
        # Hapa ndipo maelezo yote ya quotation yanapopangwa mstari kwa mstari
        self.list_container = MDBoxLayout(
            orientation='vertical', 
            adaptive_height=True, 
            spacing=15
        )
        
        try:self.scrll.add_widget(self.list_container)
        except:pass
        #self.kionesura.add_widget(self.scrll)
        #self.add_widget(self.scrll)

        # 2. FOOTER YA SALAMU NA CHAT
        self.machaguo = MDBoxLayout(
            orientation='vertical', 
            size_hint_y=0.25, 
            padding=10
        )
        self.salamu = MDLabel(
            text="Inachakata mchoro...", 
            halign='center', 
            theme_text_color="Custom", 
            text_color="blue",
            font_style="Body",
            role="small"
        )
        #self.machaguo.add_widget(self.salamu)
        self.add_widget(self.machaguo)

    def anza_kuchakata_mita(self, panels_kutoka_3d):
        """Injini ya QS: Inageuza Panels (Mita) kuwa Mbao za soko (mm)"""
        self.thamani_ya_mbao=6000
        self.thamani__ya_mbao=6000
        self.ufundi = 0
        ufundi=0
        self.jumla=0
        self.Lazima={}

        try:

            self.list_container.clear_widgets()
        
            # Pata jina la mbao toka studio ya 
            mat_jina=[]
            for obj in self.kazi.scene_objects:
                if obj.get('asili') not in mat_jina:
                    mat_jina.append(obj.get('asili'))    
            
            # A: CHUJA MATERIAL (Is it wood or something else?)
            vitu_visivyo_mbao = ['kioo', 'glass', 'mesh', 'net', 'kalu', 'aluminium','sakafu','ukuta','plywood','kitu']
            ni_mbao = not any(nono in mat_jina for nono in vitu_visivyo_mbao)

            # B: DATA ZA DATABASE (Smart Query)
            #kama asili ni mbao onyesha mbao zilizopo database ili user achague
            mbao_data = self.Mbao_Database_Smart_Query()
            urefu_mm_std = 3600#float(mbao_data['urefu']) * 300 # Futi 12 -> 3600mm
            bei_ya_mbao_nzima = 6000#float(mbao_data['bei'])

            # C: HESABU ZA KUKATA (Paneling Logic)
            idadi_ya_mbao_nzima = 0
            total_gundi = 0
            maungiox=self.sehemu_mbao_zimekutana(panels_kutoka_3d,'x')
            maungioy=self.sehemu_mbao_zimekutana(panels_kutoka_3d,'y')
            maungioz=self.sehemu_mbao_zimekutana(panels_kutoka_3d,'z')
            screws=0
            eneo_la_maungio=0
            for i in maungiox:
                screws += maungiox[i]['Screws']
                eneo_la_maungio += maungiox[i]['Eneo']
            for i in maungioy:
                screws += maungioy[i]['Screws']
                eneo_la_maungio += maungioy[i]['Eneo']
            for i in maungioz:
                screws += maungioz[i]['Screws']
                eneo_la_maungio += maungioz[i]['Eneo']
            '''for p in panels_kutoka_3d:
                for pp in panels_kutoka_3d:
                    if self.uwezekano(p['mipaka']['x'][1],pp['mipaka']['x'][0],0.005):# and p['id']!=pp['id']:
                        maungio[f'x_{len(maungio)+1}']={'majirani':{p['id']:p['mipaka']['x'][1],pp['id']:pp['mipaka']['x'][0]}}
                        #print(f"Mipaka ya {p['id']} ni:\n   x {p['mipaka']['x']}\nMipaka ya {pp['id']} ni:\n   x ({pp['mipaka']['x']})")'''
            #for k in maungio:
            #screws=self.sawazisha(screws,450)
            #print(screws)
            
            #if ni_mbao:
                
            mbaozote=self.mbao_zinazohitajika(1,6)
            print(f"mimbao={mbaozote}")
            idadi_ya_mbao_nzima=mbaozote['mbao']
            self.gharama_mbao_total=mbaozote['gharama']
            total_gundi=self.sawazisha(mbaozote['gundi'],75) 
                

            # D: HESABU ZA ENEO (Surface Area kwa Mita za Mraba)
            eneo_m2 = 0
            for p in panels_kutoka_3d:
                w, h, d = [float(n) for n in p['dim']]
                # Kanuni ya Prism: 2(wh + wd + hd)
                eneo_m2 += 2 * (w*h + w*d + h*d)
            self.eneo=eneo_m2
                        
            self.msasa=self.Muhimu('Msasa',self.kazi.sawazisha(3*round(self.eneo/6000000,1),0.25),2000,2000)
            self.msasa=self.Muhimu('Patex',self.kazi.sawazisha(3*round(self.eneo/6000000,1)*15/250,0.005),2000,2000)
            #print(self. msasa,self.eneo)
            # E: MATERIAL & COSTING (Dawa ya TypeError: Zote ni float sasa)
            
            ujazo_lita=0
            self.kazi.makundi_ya_mwonekano()
            rangizote=self.kazi.makundi_ya_mwonekano()[1]
            #rangizote.pop('[0.26, 0.16, 0.11, 1]')
            print(rangizote)
            print(self.kazi.makundi_ya_mwonekano())
            rl=[]
            if len(rangizote)>1:
                
                for i in rangizote:
                    marangi=self.kazi.sawazisha(rangizote[i]['eneo']*1.3 /9000000 ,0.25)
                    ujazo_lita += marangi
                    try:aa=rangizote[i]['jina']
                    except:rangizote[i]['jina']="Hiyo rangi nyingine"
                    self.rangi_zote[i]={'jina':rangizote[i]['jina'],'kiasi':marangi*self.kazi.eneo_,'thamani':13000,'gharama':marangi*self.kazi.eneo_*13000}
                    if rangizote[i]['jina'] not in rl:rl.append(rangizote[i]['jina'])
                self.kazi.update_status(f'Kumbuka saivi kuna rangi za aina {len(rangizote)} ambazo ni {rl,rangizote} na ujazo wake utakuwa ni lita {ujazo_lita}')
            else:
                for i in rangizote:
                    rl.append(rangizote[i]['jina'])
                    marangi=self.kazi.sawazisha((rangizote[i]['eneo'])*1.3 /9000000,0.25)
                    ujazo_lita += marangi
                    self.rangi_zote['rangi']={'jina':rangizote[i]['jina'],'kiasi':marangi*self.kazi.eneo_,'thamani':13000,'gharama':marangi*self.kazi.eneo_*13000}
                    self.kazi.update_status(f'Kwa saivi kuna rangi yaaina moja tu na ambayo ni {rl[0]} ujazo wake utakuwa ni lita {ujazo_lita}')
            


            # Bei ya ufundi kulingana na ugumu (Scale ya 13k)
            sila=ujazo_lita/2
            mwonekano=ujazo_lita*self.kazi.eneo_
            thiner=sila+mwonekano
            primer=ujazo_lita/2
            gundi_ya_maji=self.kazi.sawazisha(eneo_la_maungio/500000,1)
            
            
            #self.gharama_mbao_total = float(idadi_ya_mbao_nzima) * bei_ya_mbao_nzima
            # Hesabu ya mwisho (Jumla ya mradi)
            jumla_kuu = self.gharama_mbao_total + (ufundi * 5.0)
            #{'kauli':f"Vipande (Pannels): Jumla ya vipande {len(panels_kutoka_3d)} vimepatikana.",'thamani':0},
            #{'kauli':f"Eneo la rangi: Mita za mraba {eneo_m2:.2f} (Inahitaji lita {ujazo_lita:.2f}).",'thamani':0},
                
            # F: RIPOTI (Maneno ya kijanja kwa bosi)
            ripoti = [
                {'kauli':f"Sealer lita {sila} = {sila*13000}/=",'thamani':sila*13000,'jina':'Sealer','idadi':sila,'value':13000},
                {'kauli':f"Primer lita {primer} = {primer*13000}/=",'thamani':primer*13000,'jina':'Primer','idadi':primer,'value':13000},
                {'kauli':f"Thiner lita {thiner} = {thiner*7000}/=",'thamani':thiner*7000,'jina':'Highross','idadi':thiner,'value':7000},
                {'kauli':f"Clear/Rangi lita {mwonekano} = {mwonekano*13000}/=",'thamani':mwonekano*13000,'jina':'rangi','idadi':mwonekano,'value':13000},
            ]
            #ripoti.append({'kauli':f" Mbao [b]{idadi_ya_mbao_nzima}[/b] za Futi {mbao_data['urefu']}.",'thamani':0})
            #if ni_mbao:
                
            ripoti.append({'kauli':f"Gundi ya moto: Gram {total_gundi:.1f} zinahitajika.",'thamani':5000*total_gundi/75,'jina':'Gundi ya moto','idadi':total_gundi,'value':round(5000/75,0)})
            ripoti.append({'kauli':f"Gundi ya maji: mls {gundi_ya_maji:.1f} zinahitajika.",'thamani':25*gundi_ya_maji,'jina':'Gundi ya maji','idadi':gundi_ya_maji,'value':25})
                
            
            if screws>=250:
                ripoti.append({'kauli':f"Screws: {screws:.0f} zinahitajika.",'thamani':25*screws,'jina':'Screws','idadi':screws,'value':20})
            else:
                ripoti.append({'kauli':f"Screws: {screws:.0f} zinahitajika.",'thamani':30*screws,'jina':'Screws','idadi':screws,'value':25})
            #ripoti.append({'kauli':f"[b][size=20sp]JUMLA KUU: Tsh[/size][/b]",'thamani':self.jumla})
            aina={'kauli':f"Mbao: [b][color=00ADB5]{mat_jina}[/color][/b]",'thamani':0},
            self.asilia=MDListItemHeadlineText(text=f"Aina ya material: [b][color=00ADB5]{mat_jina}[/color][/b]") 
            self.f_asili=MDListItem(
                self.asilia              
            )
            #print('mmmmmmmm!')
            self.f_asili.bind(on_touch_up=lambda i, t: self.open_asili_menu(i) if i.collide_point(*t.pos) else None)
            
            self.list_container.add_widget(self.f_asili)
            mbao_idadi={'kauli':f"Mbao [b]{idadi_ya_mbao_nzima}[/b] = Tsh {self.gharama_mbao_total:,.0f}/=",'thamani':self.gharama_mbao_total}
                
            self.idai_ya_mbao=MDListItemHeadlineText(text=mbao_idadi['kauli']) 
            self.f_idadi=MDListItem(
                self.idai_ya_mbao              
            )
            self.mbao_check = MDListItemTrailingCheckbox(active=False)
            # Bind kitendo cha ku-click checkbox na mbao husika
            self.mbao_check.bind(on_release=lambda cb,thamani=int(mbao_idadi['thamani']): self.gharama(cb,self.gharama_mbao_total,mbao_idadi['kauli'],'mbao'))
            
            if mbao_idadi['thamani']!=0:self.f_idadi.add_widget(self.mbao_check)
            #print('mmmmmmmm!')
            #self.f_asili.bind(on_touch_up=lambda i, t: self.open_asili_menu(i) if i.collide_point(*t.pos) else None)
            
            self.list_container.add_widget(self.f_idadi)

            # G: CHORA RIPOTI (Wrapping & Spacing)
            for line in ripoti:
                
                is_visible = False
                
                # Tengeneza Item ya List
                item = MDListItem(
                    MDListItemHeadlineText(text=line['kauli'])                   
                )
                
                # Weka Checkbox upande wa kulia
                check = MDListItemTrailingCheckbox(active=is_visible)
                # Bind kitendo cha ku-click checkbox na mbao husika
                check.bind(on_release=lambda cb,thamani=int(line['thamani']),kitu=line['kauli'],jina=line['jina'],idadi=line['idadi'],value=line['value']: self.gharama(cb,thamani,kitu,jina,idadi,value ))
                
                if line['thamani']!=0:item.add_widget(check)
                self.list_container.add_widget(item)
                
            self.muhimu_check = MDListItemTrailingCheckbox(active=False)
            items=[
                {
                    'text':self.Lazima[i]['text'],
                } for i in self.Lazima
            ]
            
            
            
            self.itm0 = double(items=items)
            self.muhimu=MDListItemHeadlineText() 
            self.muhimu.text=f"{random.choice(['Visivyokwepeka','Vyenye ulazima','Vitu vya lazima','Muhimu','Vitu vya muhimu'])} = {self.lazima()}"
            self.vya_muhimu={'kauli':f"{random.choice(['Visivyokwepeka','Vyenye ulazima','Vitu vya lazima','Muhimu','Vitu vya muhimu'])} = {self.lazima()}",'thamani':self.lazima()}
            self.muhimu_check.bind(on_release=lambda cb,thamani=int(self.vya_muhimu['thamani']): self.gharama(cb,self.lazima(),self.vya_muhimu['kauli'],'muhimu'))
            self.itm0. add_widget(self.muhimu)
            self.itm0.bind(on_release=self.list_ya_lazima)            
        
            self.list_container.add_widget(self.itm0)




            ufundi={'kauli':f"Ufundi = {self.ufundi}",'thamani':self.ufundi}
            self.Ufundi=MDListItemHeadlineText(text=ufundi['kauli']) 
            
            self.itm = MDListItem()
            self.itm. add_widget(self.Ufundi)
            self.ufundi_check = MDListItemTrailingCheckbox(active=False)
            # Bind kitendo cha ku-click checkbox na mbao husika
            def ufundii(kt):
                if kt.active:self.salamu.text=f"Jumla ya gharama za materials ni: Tsh {self.jumla}\nUfundi ni {self.ufundi}\nKazi nzima inagharimu {self.jumla+self.ufundi}"
                else:self.salamu.text=f"Jumla ya gharama za materials ni: Tsh {self.jumla}\nUfundi ni {self.ufundi}"

            self.ufundi_check.bind(on_release=lambda cb,thamani=int(ufundi['thamani']): ufundii(cb))#gharama(cb,ufundi['thamani'],ufundi['kauli']))
            
            
            self.list_container.add_widget(self.itm)
            #self.salamu.text = str(self.kazi.makundi_ya_mwonekano())

        except Exception as e:
            self.kazi.update_status(f"QS Error: {traceback.format_exc()}",True)
            self.salamu.text = f"Kosa la QS: {str(e)[:30]}"

    def Mbao_Database_Smart_Query(self,Board=False):
        """Inasoma soko la mbao kitalamu"""
        if not Board:path = os.path.join(self.path, 'Mbao.sqlite')
        else:path = os.path.join(self.path, 'Board.sqlite')
        board=0
        #zote=0

        default_data = {
            "Seplasi(1,6)":{'jina':'Seplasi','urefu': 12, 'unene':1, 'upana':6, 'kuranda':1000, 'kuchana':1000, 'kuzalisha':1000, 'usafiri':1000, 'bei': 6500,'asili':'Mbao'}
        }
        default_data1 = {
            "Board":{'jina':'Board','urefu': 8, 'unene':1, 'upana':4, 'usafiri':5000, 'bei': 45000,'asili':'Board'},
        }
        if Board: default_data=default_data1
        try:
            
            if not os.path.exists(path):
                self.salamu.text=f"Kimeumana kwenye database ya Mbao: hakuna hiyo database inaitwa {path}."
                self.kazi.update_status(f"Kimeumana kwenye database ya Mbao: hakuna hiyo database inaitwa {path}.")
                return default_data
            conn = sqlite3.connect(path)
            conn.row_factory = sqlite3.Row
            cs = conn.cursor()
            #print('duh')
            # Jaribu kutafuta jina linalofanana (LIKE)
            #if zote==0:res = cs.execute("SELECT  jina, [bei], [unene], [urefu], [upana], [kuranda], [kuchana], [usafiri] FROM Mbao WHERE upana LIKE ?", (f'{upana}',)).fetchall()
            res = cs.execute("SELECT  jina, [bei], [unene], [urefu], [upana], [kuranda], [kuchana], [kuzalisha], [usafiri] FROM Mbao ").fetchall()
            #except:pass
            d={}           
            #if res:
            for i in res:
                d[f"{i['jina']}({i['unene']},{i['upana']})"]={'jina':i['jina'],'unene':i['unene'],'upana':i['upana'],'urefu':i['urefu'],'bei':i['bei'],'kuranda':i['kuranda'],'kuchana':i['kuchana'],'kuzalisha':i['kuzalisha'],'usafiri':i['usafiri'],'asili':'Mbao'}
                
            try:
                path1=os.path.join(self.path, 'Board.sqlite')
                conn1= sqlite3.connect(path1)
                conn1.row_factory = sqlite3.Row
                cs1 = conn1.cursor()
                res1 = cs1.execute("SELECT  jina, [bei], [unene], [urefu], [upana], [umbali], [idadi], [usafiri] FROM Board ").fetchall()
                for i in res1:
                    d[f"{i['jina']}({i['unene']},{i['upana']})"]={'jina':i['jina'],'unene':i['unene'],'upana':i['upana'],'urefu':i['urefu'],'bei':i['bei'], 'usafiri':i['usafiri'],'asili':'Board'}
                
                board=1
            except:
                board=0
                self.kazi.update_status('data za board hazipo')
                    
                    
            print(f'\n\n    kwenye database kuna {d}')
            if len(d)>0:
                return d
        except Exception as e:
            self.kazi.update_status(e,is_error=True)
            return default_data


    def gharama(self,kituu,thamani,kitu,jina='',idadi=0,value=0):
        thamani=int(thamani)
        print(kitu)
        if not f"Ufundi" in kitu:ufundi=True
        else:ufundi=False
        if kituu.active:
            if jina=='muhimu':
                for jna in self.Lazima:
                    self.jumla=self.jumla+self.Lazima[jna]['thamani']
                    self.mahitaji[jna]={'thamani':self.Lazima[jna]['kiasi'],'idadi':self.Lazima[jna]['idadi'],'gharama':self.Lazima[jna]['thamani']}
            elif jina=='mbao':
                self.mbao_zinazohitajika()
                makundi_ya_mbao=self.makundi_ya_mbao
                for jna in makundi_ya_mbao:
                    self.jumla=self.jumla+makundi_ya_mbao[jna]['thamani']
                    self.mahitaji[jna]={'thamani':makundi_ya_mbao[jna]['thamani'],'idadi':makundi_ya_mbao[jna]['idadi'],'gharama':makundi_ya_mbao[jna]['gharama']}
            elif 'rangi' in kitu.lower():
                rangi=self.rangi_zote
                for jna in rangi:
                    self.jumla=self.jumla+rangi[jna]['gharama']
                    self.mahitaji[f"Rangi ({rangi[jna]['jina']})"]={'thamani':rangi[jna]['thamani'],'idadi':rangi[jna]['kiasi'],'gharama':rangi[jna]['gharama']}
            

            else:
                if jina!='':pass
                else:jina=kitu
                self.jumla=self.jumla+thamani
                self.mahitaji[jina]={'thamani':value,'idadi':idadi,'gharama':thamani}
        else:
            if jina=='muhimu':
                for jna in self.Lazima:
                    self.jumla=self.jumla-self.Lazima[jna]['thamani']
                    self.mahitaji.pop(jna)
            elif jina=='mbao':
                self.mbao_zinazohitajika()
                makundi_ya_mbao=self.makundi_ya_mbao
                for jna in makundi_ya_mbao:
                    self.jumla=self.jumla-makundi_ya_mbao[jna]['thamani']
                    self.mahitaji.pop(jna)#={'thamani':makundi_ya_mbao[jna]['thamani'],'idadi':makundi_ya_mbao[jna]['idadi'],'gharama':makundi_ya_mbao[jna]['gharama']}
            elif 'rangi' in kitu.lower():
                rangi=self.rangi_zote
                for jna in rangi:
                    self.jumla=self.jumla-rangi[jna]['gharama']
                    
                    self.mahitaji.pop(f"Rangi ({rangi[jna]['jina']})")#={'thamani':rangi[jna]['thamani'],'idadi':rangi[jna]['kiasi'],'gharama':rangi[jna]['gharama']}
            

            else:
                if jina!='':pass
                else:jina=kitu
                self.jumla=self.jumla-thamani
                self.mahitaji.pop(jina)#={'thamani':value,'idadi':idadi,'gharama':thamani}
            
        if ufundi:
            if self.jumla!=0:
                self.ufundi=self.jumla/3
                self.Ufundi.text=f"Ufundi = {self.ufundi}"
                try:self.itm.add_widget(self.ufundi_check)
                except:pass
            else:
                self.itm.remove_widget(self.ufundi_check)
                self.ufundi=self.jumla/3
        self.ufundi_check.active=False
        #self.mahitaji['UFUNDI']={'thamani':'','idadi':len(self.mahitaji)-1,'gharama':self.ufundi}
        self.salamu.text=f"Jumla ya gharama za materials ni: Tsh {self.jumla}\nUfundi ni {self.ufundi}"

    def uwezekano(self,v11, v22, torerance):
        r=''
        v1,v2=v11,v22
        if -torerance <=v1-v2<=torerance:
            #print(f'{v1} >>> {v2-torerance}')
            r = True

        else:
            #print(f'{v1} >>> {v2}\n{v1} >>> {v2-torerance}\n{v1} >>> {v2+torerance}\n{v1+torerance} >>> {v2-torerance}\n{v1-torerance} >>> {v2+torerance}\n{v1-torerance} >>> {v2}\n{v1+torerance} >>> {v2}\n\n')
            r = False
        return r
    def open_asili_menu(self, caller):
        from kivy.core.window import Window
        if self.mbao_check.active:
            self.mbao_check.active=False
            self.jumla=self.jumla-self.thamani__ya_mbao
            self.salamu.text=f"Jumla ya gharama zilizochahuliwa ni: Tsh {self.jumla}"
        mbao=self.makundi_ya_mbao
        menu_items = [
            {
                "text": f"{mbao[xx]['mbao']['jina'] } {'{'}{mbao[xx]['idadi']}{'}'} = {mbao[xx]['gharama']}",
                "role":'small',
                "on_release": lambda mn=self, xxx=mbao[xx]['mbao']['jina'], x=mbao[xx]['asili']: self.set_asili(mn,xxx,x),
            } for xx in mbao
        ]
        
        self.m__asili = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            position="bottom",
            #role='small',
            width=Window.width * 0.8,
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        self.m__asili.open()

    def set_asili(self,caller, jina,values):
        objects=self.kazi.scene_objects
        print(f"asili ya {jina} ni {values}")
        mabadiliko={}
        for i in objects:
            #print(f"i.get= {i['asili']}>>jina={jina}")
            #print(f"na asili ya {i['halisi']['mbao']} ni {i['asili']}")
            if i['halisi']['mbao']['jina']==jina:
                
                mabadiliko[i['id']]={'halisi':i['halisi'],'asili':values}
        text=values
        
        self.open_aasili_menu(jina,caller,mabadiliko=mabadiliko)
    def open_aasili_menu(self,jina,caller,mabadiliko=''):
        from kivy.core.window import Window
        #mk=self.mahesabu
        #.chagua_mbao=
        menu_items = [
            {
                "text": asili_ya_kitu,
                "on_release": lambda x=asili_ya_kitu, c=caller,mb=mabadiliko: self.set_mmbao(x,c,mabadiliko=mb),
            } for asili_ya_kitu in ['Mbao','Board','Plywood','Pvc','Kioo','Chuma']
        ]
        
        self.m___asili = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        self.m___asili.open()


    def set_mmbao(self,jina,caller,mabadiliko=''):
        unene=1
        upana=6
        zzote=1
        objects=caller.kazi.scene_objects
        #id=caller.final_id
        text=jina
        object=caller
        if text=='Mbao':mbao=self.Mbao_Database_Smart_Query()
        else: mbao=self.Mbao_Database_Smart_Query(True)
        #for i in mbao:print(f"\n\n{i}\n\n\n")
            
        menu_items = [
            {
                "text": asili_ya_kitu,
                "on_release": lambda x=asili_ya_kitu, v=mbao[asili_ya_kitu],c=caller,mb=mabadiliko: self.set_mbao(x,v,c,mabadiliko=mb),
            } for asili_ya_kitu in mbao
        ]
        
        self.m__mbao = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            position="bottom",
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        if text != 'Mbao' and text != 'Board':
            #Mbao=mbao
            object.m___asili.dismiss()
            #object.halisi={'mbao':Mbao,'asili':text,'thamani':Mbao['bei'],'vipimo':[Mbao['unene'],Mbao['upana'],Mbao['urefu']]}
            return
        self.m__mbao.open()


    

    def Set__mbao(self,caller, text):
        unene=1
        upana=6
        zzote=1
        objects=caller.scene_objects
        #id=caller.final_id
        
        object=caller
        if text=='Mbao':mbao=self.Mbao_Database_Smart_Query()
        else: mbao=self.Mbao_Database_Smart_Query(True)
        #for i in mbao:print(f"\n\n{i}\n\n\n")
        def set_mbao(jina,mbao):
            print(mbao)
            Mbao=mbao
            
            object.f_asili.text=f'{text}'
            object.halisi={'mbao':mbao,'asili':text,'thamani':Mbao['bei'],'vipimo':[Mbao['unene'],Mbao['upana'],Mbao['urefu']]}
            
            def close(tm):
                object.m_asili.dismiss()
            self.kazi.m_asili.dismiss()
            self.kazi.trigger_auto_save()
            self.m__mbao.dismiss()
            from kivy.clock import Clock
            Clock.schedule_once(close,0.1)
            
        menu_items = [
            {
                "text": asili_ya_kitu,
                "on_release": lambda x=asili_ya_kitu, v=mbao[asili_ya_kitu]: set_mbao(x,v),
            } for asili_ya_kitu in mbao
        ]
        
        self.m__mbao = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            position="bottom",
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        if text != 'Mbao' and text != 'Board':
            #Mbao=mbao
            object.f_asili.text=f'{text}'
            self.kazi.m_asili.dismiss()
            object.m_asili.dismiss()
            #object.halisi={'mbao':Mbao,'asili':text,'thamani':Mbao['bei'],'vipimo':[Mbao['unene'],Mbao['upana'],Mbao['urefu']]}
            return
        self.m__mbao.open()

    def chagua_mbao(self,unene,upana,caller,mabadiliko='',text='Mbao'):
        
        if text=='Mbao':mbao=self.Mbao_Database_Smart_Query()
        else: mbao=self.Mbao_Database_Smart_Query(True)
        
                
        menu_items = [
            {
                "text": asili_ya_kitu,
                "on_release": lambda x=asili_ya_kitu, v=mbao[asili_ya_kitu],c=caller,mb=mabadiliko: self.set_mbao(x,v,c,mabadiliko=mb),
            } for asili_ya_kitu in mbao
        ]
        print(f"......\n    {mbao}")
        self.m_mbao = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
            position="bottom",
            # DAWA: Inachukua 50% ya kimo cha kioo chochote kile
            max_height=Window.height * 0.5 
        )
        self.m_mbao.open()
        
    
    def set_mbao(self,jina,mbao,caller,mabadiliko=''):
        objects=self.kazi.scene_objects
        paneli=0
        if mabadiliko!='':
            #print(f"mababiliiiiiiiiiiiiiiiiiiiko\n\n\n{mabadiliko}\n\n\n..........")
            try:
                for i in objects:
                    if i['id'] in mabadiliko:
                        mwanzo=mabadiliko
                        print(mbao)
                        print(mabadiliko[i['id']]['asili'])
                        i['asili']=f"{mbao['asili']}"
                        i['halisi']['mbao']=mbao
                        i['halisi']['vipimo']=[mbao['unene'],mbao['upana'],mbao['urefu']]
                        i['halisi']['thamani']=mbao['bei']
                        i['halisi']['asili']=mbao['asili']
                        print(f"mababiliiiiiiiiiiiiiiiiiiiko\nkutoka    {mwanzo} kwenda      {i['halisi']}")
                        paneli += 1
            except:self.kazi.update_status(f"{mbao}\n\n{traceback.format_exc()}",True)
            caller.text='Mabadiliko yamefanyika tayari!'
        idadi_ya_mbao=self.mbao_zinazohitajika(int(mbao['unene']),int(mbao['upana']),urefu=mbao['urefu'])
        self.thamani_ya_mbao=mbao['bei']
        self.thamani__ya_mbao=idadi_ya_mbao['gharama']
        self.idai_ya_mbao.text= f'Mbao {idadi_ya_mbao["mbao"]} = {self.thamani__ya_mbao}/='  
        caller.text=jina
        if paneli>0:
            if paneli==1:zi='i'
            else:zi='zi'
            self.salamu.text=f"Panel {paneli} {zi}mebadilishiwa aina ya mbao!"
        else:self.salamu.text=f"Hakuna paneli hata moja iliyofanyiwa mbadiliko!"    
        if len(self.makundi_ya_mbao)==1:za='ya'
        else:za='za'
        self.asilia.text=f"Kuna aina {'[b][color=00ADB5]'}{len(self.makundi_ya_mbao)}[/color][/b] {za} mbao"
        #self.asilia.text = f'Jiandae na {idadi_ya_mbao} za {jina}'
        
        # hasattr(self, 'm_asili'):
        #self.m__asili.dismiss()
        try:self.m_mbao.dismiss()
        except:self.m__mbao.dismiss()

        try:self.m__asili.dismiss()
        except:self.m___asili.dismiss()
        #self.kazi.update_status(f"Vifaa: {jina} vimepakiwa tayari kwa ujenzi.")

        

    def sehemu_mbao_zimekutana(self,mbao,mhimili):
        maungio={}
        mihimili=['x','y','z']
        mhimili_complement=[]
        for i in mihimili:
            if i !=mhimili:
                mhimili_complement.append(i)
        #mhimili_complement=list(mhimili_complement)
        #print(mhimili_complement)
        d1=mihimili.index(mhimili_complement[0])
        d2=mihimili.index(mhimili_complement[1])
        #print (d1,d2 )
        for p in mbao:
            if 'mbao' in p['asili'].lower()  or 'board' in p['asili'].lower():
                for pp in mbao:
                    if 'mbao' in pp['asili'].lower()  or 'board' in pp['asili'].lower():
                        if self.uwezekano(p['mipaka'][mhimili][1],pp['mipaka'][mhimili][0],5):
                            print(p['id'],pp['id'])
                            eneo=0
                            ubao=''
                            urefu=0
                            upana=0
                            screws=0
                            eneo1=p['dim'][d1]*p['dim'][d2]
                            eneo2=pp['dim'][d1]*pp['dim'][d2]
                            def umbali(axis):
                                mwanzop=p['mipaka'][mhimili_complement[axis]][0]
                                mwanzopp=pp['mipaka'][mhimili_complement[axis]][0]
                                mwishop=p['mipaka'][mhimili_complement[axis]][1]
                                mwishopp=pp['mipaka'][mhimili_complement[axis]][1]
                                mipaka=[mwanzop,mwishop,mwanzopp,mwishopp]
                                mipaka.sort()
                                return mipaka[2]-mipaka[1]
                            urf=umbali(0)
                            upn=umbali(1)
                            eneo=urf*upn
                            screwsp=(upn//250)
                            screwsr=(urf//250)
                            screws=screwsp*screwsr
                            
                            maungio[f'Maungio_ya_mhimili_{mhimili}_{len(maungio)+1}']={'majirani':{p['id']:p['mipaka'][mhimili][0],pp['id']:pp['mipaka'][mhimili][1]},'Eneo':eneo,'Screws':screws,'Marefu':urf,'Mapana':upn}
                                
        print(mhimili,maungio)
        return maungio            

    def sawazisha(self,kipimo,kigao):
        #kigao=1/kigao
        kipimo1=kipimo//kigao
        if kipimo%kigao>0:
            kipimo1+1
        kipimo1=kipimo1*kigao
        return float(kipimo1)

    def mbao_zinazohitajika(self,unene=1,upana=6,urefu=12):
        vituu=self.kazi.scene_objects
        bawaba={}
        kitasa={}
        handle={}
        drawrail={}
        board={}
        
        ceiling={}
        marine={}
        
        Marine={}
        plywood={}
        Board={}
        kipande=0
        mbao={}
        for ktu in vituu:
            lkpm=[]
            for kpm in ktu['dim']:
                lkpm.append(kpm)
            lkpm.sort()
            print(lkpm)
            p_urefu_mm = float(lkpm[2])
            p_upana_mm = float(lkpm[1])
            p_unene_mm = float(lkpm[0])
            
                
            if 'lango' in ktu['id'].lower():
                bawaba[ktu['id']]=self.Muhimu(f"Bawaba za {ktu['id'].lower()}",2,3000,3000)
                kitasa[ktu['id']]=self.Muhimu(f"Kitasa cha {ktu['id'].lower()}",1,3500,3500)
                handle[ktu['id']]=self.Muhimu(f"Handle ya {ktu['id'].lower()}",1,2000,3500)
            if 'droo' in ktu['id'].lower():
                drawrail[ktu['id']]=self.Muhimu(f"Drawrail za {ktu['id'].lower()}",1,6000,6000)
                if 'nje' in ktu['id'].lower():handle[ktu['id']]=self.Muhimu(f"Handle ya {ktu['id'].lower()}",1,3000,3000)
            if 'kioo' in ktu['asili'].lower():
                Eneo=p_urefu_mm*p_upana_mm//90000
                drawrail[ktu['id']]=self.Muhimu(f" {ktu['id'].title()}",Eneo,4000,4000)
            if 'plywood' in ktu['asili'].lower():
                plywood['panel_%s'%ktu['id']]={'urefu':p_urefu_mm,'upana':p_upana_mm}
            if 'mdf' in ktu['asili'].lower():
                mdf['mdf_%s'%ktu['id']]={'urefu':p_urefu_mm,'upana':p_upana_mm}

            if 'hdf' in ktu['asili'].lower():
                hdf['hdf_%s'%ktu['id']]={'urefu':p_urefu_mm,'upana':p_upana_mm}

            if 'ldf' in ktu['asili'].lower():
                ldf['ldf_%s'%ktu['id']]={'urefu':p_urefu_mm,'upana':p_upana_mm}
            #print(f"H.......{ktu}")
            def Halisi(jina):
                dict={}
                Booard={}
                if ktu['asili']!='Board':return
                try:
                    print(f"hicho kitu chenyewe sasa{ktu['halisi']}")
                    if jina.lower() in ktu['halisi']['mbao']['jina'].lower():
                        print(f"hicho kitu chenyewe sasa{ktu['halisi']}")
                        
                        #ktu['halisi']['mbao']={'jina':ktu['halisi']['mbao'],'thamani':ktu['halisi']['mbao']['bei']}
                        if '(' not in ktu['halisi']['mbao']['jina']:
                            print(f"ilikuwa hivi {ktu['halisi']['mbao']['jina']}")
                            #ktu['halisi']['mbao']['jina']=f"{ktu['halisi']['mbao']['jina']}({ktu['halisi']['mbao']['jina']['unene']},{ktu['halisi']['mbao']['jina']['upana']})"
                            print(f"imekuwa hivi {ktu['halisi']['mbao']['jina']}")
                        dict[f"{jina.title()}_kwa_ajili_ya_{ktu['id']}"]={'urefu':p_urefu_mm,'upana':p_upana_mm}
                        board[f"{jina.title()}_kwa_ajili_ya_{ktu['id']}"]={'urefu':p_urefu_mm,'upana':p_upana_mm}
                                
                        ktu['halisi']['thamani']=ktu['halisi']['mbao']['jina']['bei']
                        Booard[f"{jina.title()}_kwa_ajili_ya_{ktu['id']}"]=ktu['halisi']
                        Board[f"{jina.title()}_kwa_ajili_ya_{ktu['id']}"]=ktu['halisi']
                        print(Booard)
                    
                    txt=f"Siyo {jina}"

                    if len (dict)>0:txt=f"{txt}\nila kwenye list ya paneli za {jina} kuna {dict}"
                    print(txt)

                except:
                    print(f"kitu chenyewe sasa{ktu['halisi']}")
                    if jina in ktu['halisi']['mbao']['jina'].lower():
                        dict[f"{jina.title()}_kwa_ajili_ya_{ktu['id']}"]={'urefu':p_urefu_mm,'upana':p_upana_mm}
                        #ktu['halisi']['mbao']={'jina':ktu['halisi']['mbao']}
                        
                        #if '(' not in ktu['halisi']['mbao']['jina']:ktu['halisi']['mbao']['jina']=f"{ktu['halisi']['mbao']['jina']}({ktu['halisi']['mbao']['jina']['unene']},{ktu['halisi']['mbao']['jina']['upana']})"
                        #ktu['halisi']['thamani']=ktu['halisi']['mbao']['jina']['bei']
                        Booard=ktu['halisi']
                        print(Booard)
                        
                return board,Board
            Board_=Halisi(ktu['halisi']['mbao']['jina'])
            '''if Board_:
                board,Board=Board_
            '''

            if 'ceiling' in ktu['asili'].lower():
                ceiling['ceiling_%s'%ktu['id']]={'urefu':p_urefu_mm,'upana':p_upana_mm}
        print(board,Board)
        for i,ii,iii in zip([plywood,'ceiling',Board],[plywood,ceiling,board],[15000,10000,45000]):
            if len(ii)>0:
                print(f"\n{ii}\n>>{i}")
                i['idadi']=len(self.panga_paneli(ii)[1])
                 
                try:
                    i['asili']=i['asili']
                    i['gharama']=len(self.panga_paneli(ii)[1])*int(i['thamani'])
                except:
                    i['asili']='Board'
                    i['thamani']=iii
                    i['mbao']={'jina':'Marine board'}
                    i['gharama']=len(self.panga_paneli(ii)[1])*iii
                i['vipimo']=[1,4,8]#[i['mbao']['unene'],i['mbao']['upana'],i['mbao']['urefu']]
                
                
                
                mbao[i['asili']]=i#{'asili':i,,,'mbao':i['asili'],}
                
        mdf_zilizopangwa = self.panga_paneli(board)[1]
        print(mdf_zilizopangwa)
            
        for mdf in mdf_zilizopangwa:
            print(f"\nMDF na. {mdf['board_id']} itakatwa paneli hizi:")
            for p in mdf['paneli_zilizopo']:
                print(f"  - {p}")
        
        list_ya_mbao = MDBoxLayout(orientation="vertical", spacing=50, size_hint_y=None)
        list_ya_mbao.bind(minimum_height=list_ya_mbao.setter('height'))

        # Unaitanya kila board iliyopatikana kwenye hesabu na kuichora
        for mdf in mdf_zilizopangwa:
            mdf_box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=380)
            
            lebo_vipimo = MDLabel(text="Gusa paneli kuona vipimo...", markup=True, size_hint_y=None, height=25)
            
            # Hapa sasa ndio unaita ile Widget ya kuchora pale unapohitaji ionekane
            visualizer = MDFLayout(mdf_data=mdf, status_label=lebo_vipimo, id = mdf['board_id'], size_hint_y=None, height=300)
            
            mdf_box.add_widget(visualizer)
            mdf_box.add_widget(lebo_vipimo)
            list_ya_mbao.add_widget(mdf_box)

        try:self.boards.add_widget(list_ya_mbao)
        except:pass
        

        
        vitu=[]
        makosa=[]
        ni_mbao=False
        Board={}
        for kitu in vituu:
            #print (kitu)
            if 'Mbao' in kitu['asili'] and 'board' not in kitu['asili']:
                
                
                try:
                    kitu['halisi']['idadi']=1
                    #kitu['asili']['thamni']
                    #try:kitu['halisi']['baki']=int(kitu['halisi']['baki'])
                    kitu['halisi']['baki']=int(kitu['halisi']['vipimo'][2])*300
                    #except:print(f".........{kitu}\n")
                    
                    if '(' not in kitu['halisi']['mbao']['jina']:kitu['halisi']['mbao']['jina']=f"{kitu['halisi']['mbao']['jina']}({kitu['halisi']['vipimo'][0]},{kitu['halisi']['vipimo'][1]})"
                    mbao[f"{kitu['asili']}_({kitu['halisi']['mbao']['jina']})"]=kitu['halisi']
                    mbao[f"{kitu['asili']}_({kitu['halisi']['mbao']['jina']})"]['gharama']=0
                    if 'Mbao' in kitu['asili']:
                        mbao[f"{kitu['asili']}_({kitu['halisi']['mbao']['jina']})"]['gundi']=0
                    ni_mbao=True
                    vitu.append(kitu)#try:kitu['halisi']['idadi']=int(kitu['halisi']['idadi'])
                    
                except Exception as e:
                    makosa.append(kitu['id'])
                    print(f'          ......{kitu},,,,,,,\n{e}\n')
        if len(makosa)>0:
            zi='i' if len(makosa)==1 else 'zi'
            namba=len(makosa)
            kosa=f"Kuna paneli {namba} ha{zi}jatolewa maelezo kamili\nYaani {zi}tatengenezwa kwa kutumia mbao gani\n{makosa}"
            self.kazi.update_status(kosa)
            self.salamu.text=kosa    
            
                
        #if len(vitu)>0:
        idadi_ya_mbao_nzima=0
        total_gundi=0
        kuzalisha=0
        urefu_mm_std=int(urefu)*300
        if ni_mbao:
            idadi_ya_mbao_nzima = 0#kitu['halisi']['idadi']
            baki_mm = urefu_mm_std#kitu['halisi']['baki']
            
            for p in vitu:
                lkpm=[]
                for kpm in p['dim']:
                    lkpm.append(kpm)
                lkpm.sort()
                print(lkpm)
                p_urefu_mm = float(lkpm[2]) 
                p_upana_mm = float(lkpm[1]) 
                p_unene_mm = float(lkpm[0]) 
                if 'Mbao' in p['asili']:# 'dim' ni [w, h, d] katika mita. h ni urefu wa panel.
                    
                    # Gundi: urefu * 750 / 25000 (Basic rule)
                    upn=int(p['halisi']['vipimo'][1])
                    vipisi=p_upana_mm//(upn*25)
                    if p_upana_mm%upn*25>0:
                        vipisi=vipisi+1
                    total_gundi += (vipisi-1)*(p_urefu_mm * 750) / 25000
                    #print(f"vipisi awali{vipisi}{p['halisi']['baki']}")
                    unn=int(p['halisi']['vipimo'][0])
                    if unn*25//p_unene_mm>=2:
                        p_urefu_mm=p_urefu_mm//(unn*25//p_unene_mm)
                        if p_urefu_mm%(unn*25//p_unene_mm)>0:
                            vipisi=int(vipisi)+1
                        kuzalisha +=unn*25//p_unene_mm
                        if unn*25%p_unene_mm>=0.01:
                            kuzalisha += 1
                        print (f"{p['halisi']['mbao']['jina']} inabidi izalishwe! njia {kuzalisha} {p_urefu_mm}")
                        print(f'vipisi baada{vipisi}')

                    for i in range(int(vipisi)):
                        #print(f"{p['halisi']} === {p['halisi']['baki']} > {p_urefu_mm}")
                        kabla=mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki']
                        if mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki'] >= p_urefu_mm:
                            mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki'] = mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki']-p_urefu_mm
                            baki_mm -= p_urefu_mm
                        else:
                            mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['idadi'] += 1
                        
                            if mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['gharama']>0:mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['gharama'] += int(mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['thamani'])#+int(p['halisi']['thamani'])
                            else:mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['gharama']=2*int(mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['thamani'])
                            idadi_ya_mbao_nzima += 1
                            mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki']=int(mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['vipimo'][2])*300-p_urefu_mm
                            baki_mm = urefu_mm_std - p_urefu_mm
                        #print(f"{mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]} === mwanzo = {kabla} : {mbao[f"{p['asili']}_({p['halisi']['mbao']['jina']})"]['baki']} > {p_urefu_mm}")
                        #print(f'mpaka sasa {p["id"]} ina kipisi cha mm{p_urefu_mm} : {idadi_ya_mbao_nzima}')
                
                #elif 'board' in p['asili']:
            self.Muhimu(f"Kuranda",idadi_ya_mbao_nzima,1000,1000)        
            self.Muhimu(f"Usafiri wa mbao",idadi_ya_mbao_nzima,1000,1000)        
            self.Muhimu(f"Usafiri wa board",1,15000,15000)        
                    
                
                    
                    
            total_gundi=self.sawazisha(total_gundi,75)
        mbao_zote=0
        gharama=0 
        for i in mbao:
            if int(mbao[i]['idadi'])==1:
                mbao[i]['gharama']=int(mbao[i]['thamani'])
            mbao_zote += int(mbao[i]['idadi'])
            gharama += int(mbao[i]['gharama'])
            print(f"{i}:\n   {mbao[i]}")
        print(f'\nmbao zote!\n{mbao}')
        self.gharama_mbao_total=gharama
        self.makundi_ya_mbao=mbao
        
        #self.kazi.trigger_auto_save()
        #if ni_board:

        return {'mbao':mbao_zote,'gharama':gharama,'gundi':total_gundi,'boards':mdf_zilizopangwa, 'list':list_ya_mbao}

    def Muhimu(self,jina,kiasi,thamani,kimoja=''):       
        kiasi=float(kiasi)
        thamanni=int(kiasi*thamani)
        text=f"{jina.title()} {'{'}{round(kiasi,0)}{'}'} = {thamani}/="
        try:self.Lazima[jina]={'text':text,'kiasi':thamani,'idadi':kiasi,'thamani':thamanni}
        except:
            self.Lazima={}
            self.Lazima[jina]={'text':text,'kiasi':thamani,'idadi':kiasi,'thamani':thamanni}


        return {'text':text,'kiasi':thamani,'idadi':kiasi,'thamani':thamanni}

    def lazima(self):
        lazima=0
        for i in self.Lazima:
            lazima += self.Lazima[i]['thamani']
        if lazima>0:self.itm0.add_widget(self.muhimu_check)
        
        return float(lazima)

    def list_ya_lazima(self,ktu):
        #"on_release": lambda x=jina_la_mbao: self.set_wood(x),
        

        
        print(self.Lazima)



    # =====================================================================
    # SEHEMU YA 1: INJINI YA HESABU (HAKUNA UI YA KIVY HAPA - UNAIITA POPOTE)
    # =====================================================================
    
    def panga_paneli(self,data_za_paneli,board='Board', mdf_w=2440, mdf_h=1220, max_boards=50):
        """
        Inapokea dict ya paneli kutoka kwenye mfumo wako wa 3D na kupiga hesabu ya optimization.
        Inarudisha list ya mbao zilizopangwa tayari kwa ajili ya kuchorwa.
        """
        packer = newPacker(rotation=True)
        
        # Ongeza mbao za MDF zilizopo
        for _ in range(max_boards):
            packer.add_bin(mdf_w, mdf_h)

        # Ongeza paneli kutoka kwenye data yako ya 3D
        for jina, v in data_za_paneli.items():
            for _ in range(1):
                try:packer.add_rect(v["urefu"], v["upana"], rid=jina)
                except:pass# self.kazi.update_status(f"{v}\n{traceback.format_exc()}",True)

        # Run optimization algorithms
        packer.pack()

        # Alika matokeo kwenye muundo safi wa data (Clean Structure)
        mbao_zilizotumika = []
        for b, mdf_ubao in enumerate(packer):
            if len(mdf_ubao) == 0: 
                continue
                
            rectangles = []
            for rect in mdf_ubao:
                rectangles.append({
                    "x": rect.x, "y": rect.y,
                    "w": rect.width, "h": rect.height,
                    "name": rect.rid
                })
            
            mbao_zilizotumika.append({
                "board_id": f"{board}_{b + 1}",
                "mdf_size": (mdf_w, mdf_h),
                "paneli_zilizopo": rectangles
            })
            
        return board,mbao_zilizotumika

    

class MDFLayout(MDBoxLayout):
    def __init__(self, mdf_data, status_label,id, **kwargs):
        super().__init__(**kwargs)
        self.mdf_data = mdf_data
        self.status_label = status_label
        self.paneli_rects = []
        self.bind(size=self.draw_layout, pos=self.draw_layout)
        self.idt=id
        

    def draw_layout(self, *args):
        self.canvas.clear()
        self.paneli_rects.clear()
        if not self.mdf_data:
            return
        
        print(self.mdf_data)
        mdf_w, mdf_h = self.mdf_data["mdf_size"]
        scale_x = self.width / mdf_w
        scale_y = self.height / mdf_h
        self.scale = min(scale_x, scale_y) * 0.9

        self.offset_x = self.x + (self.width - (mdf_w * self.scale)) / 2
        self.offset_y = self.y + (self.height - (mdf_h * self.scale)) / 2
        #print (self.offset_x,self.off)

        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=(self.offset_x, self.offset_y), size=(mdf_w * self.scale, mdf_h * self.scale))
            
            Color(1, 1, 1, 1)
            Line(rectangle=(self.offset_x, self.offset_y, mdf_w * self.scale, mdf_h * self.scale), width=1.5)

            for paneli in self.mdf_data["paneli_zilizopo"]:
                px, py = paneli["x"], paneli["y"]
                pw, ph = paneli["w"], paneli["h"]
                jina = paneli["name"]

                random.seed(hash(jina))
                Color(random.random(), random.random(), random.random(), 0.7)
                
                pos_x = self.offset_x + (px * self.scale)
                pos_y = self.offset_y + (py * self.scale)
                size_x = pw * self.scale
                size_y = ph * self.scale
                
                Rectangle(pos=(pos_x, pos_y), size=(size_x, size_y))

                Color(0, 0, 0, 1)
                Line(rectangle=(pos_x, pos_y, size_x, size_y), width=1)

                self.paneli_rects.append({
                    "x_min": pos_x, "x_max": pos_x + size_x,
                    "y_min": pos_y, "y_max": pos_y + size_y,
                    "data": paneli
                })

    

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            for p in self.paneli_rects:
                if p["x_min"] <= touch.x <= p["x_max"] and p["y_min"] <= touch.y <= p["y_max"]:
                    p_data = p["data"]
                    self.status_label.text = f"[b]Iliyochaguliwa:[/b] {p_data['name']} | [b]Vipimo:[/b] {p_data['w']}mm x {p_data['h']}mm"
                    return True
            self.status_label.text =f"Hiyo ni sehemu ya {self.idt} iliyobaki"
            return True
        return super().on_touch_up(touch)



'''class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        # Hizi data zinaweza kuwa zimetoka kwenye kurender picha yako ya 3D
        data_kutoka_3d = {
            "Mlango Kabati": {"urefu": 700, "upana": 450, "idadi": 4},
            "Upande Kabati": {"urefu": 2000, "upana": 600, "idadi": 2},
            "Shelfu Ndani": {"urefu": 800, "upana": 550, "idadi": 6}
        }

        # HATUABU YA 1: Unapiga hesabu tu (Hapa unaweza kusave hata ripoti ya text)
        mbao_zilizopangwa = SmaMBoarD.panga_paneli(data_kutoka_3d)

        # HATUABU YA 2: Unatengeneza UI na kuamua wapi pa kuonyesha mchoro
        root_layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
        scroll = ScrollView()
        list_ya_mbao = MDBoxLayout(orientation="vertical", spacing=50, size_hint_y=None)
        list_ya_mbao.bind(minimum_height=list_ya_mbao.setter('height'))

        # Unaitanya kila board iliyopatikana kwenye hesabu na kuichora
        for mdf in mbao_zilizopangwa:
            mdf_box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=380)
            
            lebo_vipimo = MDLabel(text="Gusa paneli kuona vipimo...", markup=True, size_hint_y=None, height=25)
            
            # Hapa sasa ndio unaita ile Widget ya kuchora pale unapohitaji ionekane
            visualizer = MDFLayout(mdf_data=mdf, status_label=lebo_vipimo, size_hint_y=None, height=300)
            
            mdf_box.add_widget(visualizer)
            mdf_box.add_widget(lebo_vipimo)
            list_ya_mbao.add_widget(mdf_box)

        scroll.add_widget(list_ya_mbao)
        root_layout.add_widget(root_layout)
        return root_layout'''



    
class double(MDListItem):
    def __init__(self,items=[], **kwargs):
        super().__init__(**kwargs)
        #self.dabo=False
        #self.items=items
        self.mn=self.m_wood = MDDropdownMenu(
            caller=self,
            items=items,
            width=Window.width * 0.8,
            position="bottom",
            max_height=Window.height * 1
        )
    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.dabo=True
                try:self.mn.open()
                except:pass
                #print(self.items)
                
                return True
        self.double_touch=False
        return super().on_touch_up   

