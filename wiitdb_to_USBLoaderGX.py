from lxml import builder as xmlb
from lxml import etree as xmlt
from lxml.etree import SubElement as xmlse
from untangle import parse as up

#Map Category To Category ID
gameTypeMap={
  'Wii':                  '01',
  'WiiWare':              '02',
  'GameCube':             '03',
  'Programs':             '04',
  'Third-Party':          '05',
  '.':                    '06', #Spacer Can't Have An Empty Name Or USBLoaderGX Will Crash But Also Can't Have The Same Name Or It Won't Work \:D/
  'VC-Arcade':            '07',
  'VC-Commodore 64':      '08',
  'VC-MSX':               '09',
  'VC-N64':               '10',
  'VC-NeoGeo':            '11',
  'VC-NES':               '12',
  'VC-Sega Genesis':      '13',
  'VC-SEGA Master System':'14',
  'VC-SNES':              '15',
  'VC-Turbo Grafx 1.6':   '16',
  '. ':                   '17', #Spacer Can't Have An Empty Name Or USBLoaderGX Will Crash But Also Can't Have The Same Name Or It Won't Work \:D/
  'Region-None':          '18',
  'Region-NTSC':          '19',
  'Region-PAL':           '20',
  '.  ':                  '21', #Spacer Can't Have An Empty Name Or USBLoaderGX Will Crash But Also Can't Have The Same Name Or It Won't Work \:D/
  'Players-(1)':          '22',
  'Players-(2)':          '23',
  'Players-(3)':          '24',
  'Players-(4)':          '25',
  'Players-(5-8)':        '26',
  'Players-(9-32)':       '27',
  '.   ':                 '28', #Spacer Can't Have An Empty Name Or USBLoaderGX Will Crash But Also Can't Have The Same Name Or It Won't Work \:D/
  'ReqInput-Normal':      '29',
  'ReqInput-Nunchuk':     '30',
  'ReqInput-Gamecube':    '31',
  'ReqInput-Classic':     '32',
  'ReqInput-Exotic':      '33',
}
gameTypeMapKeysList=list(gameTypeMap.keys())
gameTypeMapValuesList=list(gameTypeMap.values())

#Controller Type Map
inputNormal=set([
  'wiimote',
  'motionplus'
])
inputNunchuk=set(['nunchuk'])
inputGamecube=set(['gamecube'])
inputClassic=set(['classiccontroller'])
inputExotic=set([
  '3dglasses',
  'balanceboard',
  'dancepad',
  'drums',
  'gameboy advance',
  'guitar',
  'keyboard',
  'microphone',
  'mii',
  'nintendods',
  'udraw',
  'wheel',
  'wiispeak',
  'zapper'
])

#General XML Struct Stuff
xmldocBase=xmlb.ElementMaker()
USBLoaderGX=xmldocBase.USBLoaderGX
Revision=xmldocBase.Revision
Categories=xmldocBase.Categories
GameCategories=xmldocBase.GameCategories

#The Structs I Use
xmldocLayout=USBLoaderGX(
  Revision('1283'),
  Categories(),
  GameCategories()
)

#Making The "All" Category
defaultCategory=xmlse(xmldocLayout[1], 'Category') # type: ignore
defaultCategory.set('ID','00')
defaultCategory.set('Name','All')

#Making Categories For All Types In The "gameTypeMap" JSON
for gameType,gameID in gameTypeMap.items():
  autogenCategory=xmlse(xmldocLayout[1], 'Category') # type: ignore
  autogenCategory.set('ID',gameID)
  autogenCategory.set('Name',gameType)

#Time To Actually Parse WiiTDB
wiitdb_xml=up('wiitdb.xml')
for game in wiitdb_xml.datafile.game:
  #Match WiiTDB Game Type With My Own ID
  gameType=''
  if game.type.cdata=='': gameType='Wii'
  elif game.type.cdata=='Channel': gameType='Programs'
  elif game.type.cdata=='Homebrew': gameType='Third-Party'
  elif game.type.cdata=='VC-NEOGEO': gameType='VC-NeoGeo'
  elif game.type.cdata=='CUSTOM': gameType='Third-Party'
  elif game.type.cdata=='VC-C64': gameType='VC-Commodore 64'
  elif game.type.cdata=='VC-MD': gameType='VC-Sega Genesis'
  elif game.type.cdata=='VC-PCE': gameType='VC-Turbo Grafx 1.6'
  elif game.type.cdata=='VC-SMS': gameType='VC-SEGA Master System'
  else: gameType=game.type.cdata

  #Generate Game Parent In XML
  curGameParent=xmlse(xmldocLayout[2], 'Game') # type: ignore

  #Set Game ID On Parent
  curGameParent.set('ID',game.id.cdata)

  #Get And Set Title From WiiTDB On Parent
  try: #Only One Locale
    gameLang=game.locale['lang']
    if gameLang=='EN': curGameParent.set('Title',game.locale.title.cdata)
  except TypeError: #Multiple Locales
    titleFound=False
    for lang in game.locale:
      gameLang=lang['lang']
      if gameLang=='EN':
        curGameParent.set('Title',lang.title.cdata)
        titleFound=True
        break
  
  #Add Game To "All" Category
  allDefaultCategory=xmlse(curGameParent, 'Category') # type: ignore
  allDefaultCategory.set('ID','00')
  allDefaultCategory.set('Name','All')

  #Add Game To Found Game Type With My Categories From "gameTypeMap" JSON
  gameTypeChildCategory=xmlse(curGameParent, 'Category') # type: ignore
  curGameType=gameTypeMap.get(gameType)
  gameTypeChildCategory.set('ID',curGameType)
  gameTypeChildCategory.set('Name',gameTypeMapKeysList[gameTypeMapValuesList.index(curGameType)]) # type: ignore

  #Add Game To Region From "gameTypeMap" JSON
  regionTypeChildCategory=xmlse(curGameParent, 'Category') # type: ignore
  gameRegion=game.region.cdata
  if gameRegion=='': gameRegionMap=gameTypeMap.get('Region-None')
  else: gameRegionMap=gameTypeMap.get(''.join(['Region-',gameRegion.rsplit('-',1)[0]]))

  regionTypeChildCategory.set('ID',gameRegionMap)
  regionTypeChildCategory.set('Name',gameTypeMapKeysList[gameTypeMapValuesList.index(gameRegionMap)]) # type: ignore

  #Add Game To Amount Of Players Categories From "gameTypeMap" JSON
  playerCountChildCategory=xmlse(curGameParent, 'Category') # type: ignore
  curPlayers=int(str(game.input['players']))
  #curOnlinePlayers=int(str(game.wi_fi['players'])) <-- Considering That Official Online Play Is Gone I'm Ignoring This... Also Because Unofficial Online Services Most Likely Don't Match Up With This Anymore Anyways /shrug

  if curPlayers==2: curPlayersMap=gameTypeMap.get('Players-(2)')
  elif curPlayers==3: curPlayersMap=gameTypeMap.get('Players-(3)')
  elif curPlayers==4: curPlayersMap=gameTypeMap.get('Players-(4)')
  elif curPlayers>=5 and curPlayers<=8: curPlayersMap=gameTypeMap.get('Players-(5-8)')
  elif curPlayers>=9: curPlayersMap=gameTypeMap.get('Players-(9-32)')
  else: curPlayersMap=gameTypeMap.get('Players-(1)')

  playerCountChildCategory.set('ID',curPlayersMap)
  playerCountChildCategory.set('Name',gameTypeMapKeysList[gameTypeMapValuesList.index(curPlayersMap)]) # type: ignore

  #Add Game To Controller Type Required From "gameTypeMap" JSON
  controllerTypeChildCategory=xmlse(curGameParent, 'Category') # type: ignore
  try: #Has Input Types
    curControllerTypes=set()
    for controller in game.input.control:
      if controller['required']=='true': curControllerTypes.add(controller['type'])

    #Honestly Don't Wanna Check For If Multiple Controllers Are "Required" So Lazy Hierarchical Approach :ok_hand:
    if any(a in inputExotic for a in curControllerTypes): curControllerType=gameTypeMap.get('ReqInput-Exotic') #Controller Type Is Exotic
    elif any(a in curControllerTypes for a in inputClassic): curControllerType=gameTypeMap.get('ReqInput-Classic') #Controller Type Is Classic
    elif any(a in curControllerTypes for a in inputGamecube): curControllerType=gameTypeMap.get('ReqInput-Gamecube') #Controller Type Is Gamecube
    elif any(a in curControllerTypes for a in inputNunchuk): curControllerType=gameTypeMap.get('ReqInput-Nunchuk') #Controller Type Is Nunchuk
    elif any(a in curControllerTypes for a in inputNormal): curControllerType=gameTypeMap.get('ReqInput-Normal') #Controller Type Is Normal
    else: curControllerType=gameTypeMap.get('ReqInput-Normal') #Shouldn't Be Possible!!!

  except AttributeError: curControllerType=gameTypeMap.get('ReqInput-Normal') #Somehow Has Literally No Input Types

  controllerTypeChildCategory.set('ID',curControllerType)
  controllerTypeChildCategory.set('Name',gameTypeMapKeysList[gameTypeMapValuesList.index(curControllerType)]) # type: ignore

#Crap The File Out
xmlData=b''.join([b'<?xml version="1.0" encoding="UTF-8"?>\n',xmlt.tostring(xmldocLayout,encoding="UTF-8",xml_declaration=False,pretty_print=True)]) # type: ignore
with open('GXGameCategories.xml','wb') as f: f.write(xmlData)
