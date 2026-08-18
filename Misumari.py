import pickle,shelve

class Msumari():
    def __init__(ms,saiz,idad,gharama=4000):
        ms.dbms='Misssumari'
        ms.saiz=saiz
        ms.idad=idad
        ms.saizi='saizi_ya_msumari_wa_inchi_%s'%ms.saiz
        ms.idadi='idadi_ya_misumari_ya_inchi_%s'%ms.saiz
        ms.kipenyo='kipenyo_cha_msumari_wa_inchi_%s'%ms.saiz
        ms.uzito='uzito_wa_misumari_ya_inchi_%s'%ms.saiz
        ms.urefu='urefu_wa_msumari_wa_inchi_%s'%ms.saiz
        ms.gharama=gharama/4
        
        #ms.uref=30.4*int(saiz)
        ms.uwiano={'0.6':8380,'0.75':5630,'1':3300,'1.5':970,'2':420,'2.5':280,'3':180,'4':90,'5':48,'6':30}
        ms.data={}
        ms.hakuna=0

    def uongo(ms):
        if '%s'%ms.saiz not in ms.uwiano:
            ms.hakuna=0
            jb=1
        else:
            jb=0
        return jb
            
    def ingiza_taarifa(ms):        
        uz=input('UzitO = ')        
        kp=input('KipenyO = ')
        id=input('Idadi = ')
        ms.taarifa(uz,kp,id)       
        return [uz,kp,id]
    
    def Uzito_wa_misumari(ms,idadi):
        f=ms.data#ms.dbms)
        try:
            idd=int(f[ms.idadi])
        except KeyError:
            try:f[ms.idadi]=ms.uwiano[str(ms.saiz)]
            except KeyError:ms.hakuna=1
            idd=int(f[ms.idadi])

        try:
            uzt=int(f[ms.uzito])
        except KeyError:
            uzt=1    
        #f.close()
        uzito=uzt*int(idadi)/idd
        def gharam():
            uz=uzito//0.25
            uztt=uzito%4
            if uztt>0:
                uz=uz+1
            else:
                pass
            gharama=int(uz)* int(ms.gharama)
            uzto=uz/4
            rbb=uz%4
            rb=uz//4
            if uzto==0.25:
                uzto='robo'
            elif uzto==0.5:
                uzto='nusu'
            elif uzto==0.75:
                uzto='robo tatu'
            #elif uzto==0.5:
                #uzto='nusu'
            return uzto,gharama
        grm=gharam()
        return [uzito, grm[0],grm[1]]
    
    def nambie_uzito(ms):
        #ms.saiz=saiz
        my=ms.Uzito_wa_misumari(ms.idad)
        db=ms.data
        #for i in db:
        idd=ms.idad
        sz=ms.saiz
        if my[1]==0.25:
            kizio='robo kilo'
        elif my[1]==0.5:
            kizio='nusu kilo'
        elif my[1]==0.75:
            kizio='nusu na robo kilo'
        else:
            kizio='kilo %s'%my[1]
        uzito='Misumari %s ya inch %s ni sawa na %s\n na gharama yake ni %s\nuzito halisi ni %skg'%(idd,sz,kizio,my[2],my[0])
        #db.close()
        #print(uzito)
        return str(uzito)
        
''' 
sz=input('SaizI = ')
msu=Msumari() 
idd=input('Idadi = ')
msu.nambie_uzito_wa(sz,idd)
      
my=msu.Uzito_wa_misumari(idd)
db=shelve.open(msu.dbms)
#for i in db:
print('misumari %s ya inch %s ni sawa na %s kilo na gharama yake ni %s\nuzito halisi ni %skg'%(idd,sz,my[1],my[2],my[0]))
db.close()'''