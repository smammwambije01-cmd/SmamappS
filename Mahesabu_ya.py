import shelve,dbm.dumb
import sqlite3,sqlitedict,os
#from sqlitedict import SqliteDict

#db['jina']='Stanley'
def Mbao(jina,unene,upana):
    path_='/home/smam_mwambije/.config/karakana'
    data='Mbao'#input('database:   ')

    path=os.path.join(path_,f'{data}.sqlite')#taarifa=sqlite3.connect(f'/home/smam_mwambije/.config/karakana/{data}.sqlite')
    taarifa=sqlite3.connect(path)
    taarifa.row_factory=sqlite3.Row
    cs=taarifa.cursor()
    dat=cs.fetchall()
    zote=cs.execute(f'SELECT * FROM {data} ')#WHERE jina ={jina} AND unene={unene} AND upana={upana}' )
    print(unene)
    for i in zote:
        if  i["jina"]==jina and i["unene"]==unene and i["upana"]==upana:
            urefu=i['urefu']
            print(f'urefu ni futi {urefu}')
        else:urefu=10
        
    #urefu=0
    for i in zote:
        print(i['urefu'])
        print(f'Mbao ya {i["jina"]}({i["unene"]},{i["upana"]}) inauzwa {i["gharama ya mbao"]}')
    mbao=zote
    taarifa.close()
    rtn={}
    
    return {'urefu':int(urefu)}
        

vps={'cha kwanza':580,'cha pili':750}


def Mbao_za_wima_na_ulalo(jina,unene,upana,dict,unene_wa_kabati):
    idadi_ya_mbao=1
    mbao=Mbao(jina,unene,upana)
    urefu_wa_mbao=int(mbao['urefu'])*300
    
    idadi=len(dict)
    print(mbao['urefu'])
    l=[]
    ll={}
    lll=[]
    for i in dict:
        lll.append(i)
        l.append(dict[i])   
    baki=urefu_wa_mbao
    anayefuata=0
    while anayefuata<len(l):
        #print(l[anayefuata])
        try:q=ll['mbao namba_%s'%idadi_ya_mbao]
        except:ll['mbao namba_%s'%idadi_ya_mbao]={}
        if baki>=l[anayefuata]:
            baki=baki-l[anayefuata]            
            ll['mbao namba_%s'%idadi_ya_mbao]['kipisi namba_%s'%(anayefuata+1)]={lll[anayefuata]:l[anayefuata]}
            #print(f'baki = {baki}')
            anayefuata=anayefuata+1
        else:
            ll['mbao namba_%s'%idadi_ya_mbao]['kipisi cha %s kilichobaki'%idadi_ya_mbao]=baki
            try:qq=llll
            except:llll={} 
            llll['kipisi cha %s kilichobaki'%idadi_ya_mbao]=baki   
            idadi_ya_mbao=idadi_ya_mbao+1
            baki=urefu_wa_mbao
    

    ll['mbao namba_%s'%idadi_ya_mbao]['kipisi cha %s kilichobaki'%idadi_ya_mbao]=baki
    llll['kipisi cha %s kilichobaki'%idadi_ya_mbao]=baki  
    ll['vipisi vilivyobaki']=llll  
    upana=(int(upana)*25)      
    idadi=unene_wa_kabati//upana
    mzunguko=idadi_ya_mbao
    idadi_ya_mbao=idadi*idadi_ya_mbao
    njia_za_muunganiko=idadi-1
    if unene_wa_kabati%upana>0:
        remainder=unene_wa_kabati%upana
        mbao_mwishoni=((idadi_ya_mbao/idadi)//(upana//remainder)) 
        if ((idadi_ya_mbao/idadi)%(upana//remainder))>0:mbao_mwishoni=mbao_mwishoni+1
        mbao_mwishoni=int(mbao_mwishoni)
        idadi_ya_mbao=idadi_ya_mbao+mbao_mwishoni
        njia_za_muunganiko=idadi
        print(f'upana wa mbao ni mm {upana} layer ilobaki ni mm {remainder} ambayo inaingia mara {upana//remainder} .Hiyo layer inahitaji mbao {mbao_mwishoni} tu!')
    gundi_ya_moto=urefu_wa_mbao*mzunguko*njia_za_muunganiko*750/25000          
    ll['Mbao za panel (wima na ulalo)']=idadi_ya_mbao
    ll['Gundi yamoto ni gram']=gundi_ya_moto
    #ll['gundi ya maji']
    for i in ll:print(f'{i}\n   {ll[i]}')
    return ll
    
jina=input('jina la mbao\n')
unene=input('unene wa mbao(inchi)\n')
upana=input('upana wa mbao(inchi)\n')
unene_wa_kabati=int(input('unene_wa_kabati(mm)\n'))
vps={'wima_1':1000,'wima_2':1500,'ulalo_1':1200,'skatting1':2000,'wima_3':1000,'wima_4':1500,'ulalo_2':1200,'skatting2':2000}
Mbao_za_wima_na_ulalo(jina,unene,upana,vps,unene_wa_kabati)
