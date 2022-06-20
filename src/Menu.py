import pygame,sys
from pygame.locals import *
import Text
import os
import Utilities
import json
import ModSelect
import Button

FONT = "fonts/Aller_Lt.ttf"
WHITE = (255,255,255)

def Render(target,skin):
    pygame.key.set_repeat(400,100)
    MapsNameList = sorted(os.listdir("C:\Fake osu!\Fake osu!\maps"))
    MapSelect = pygame.image.load("skins/"+skin+"/mapselect.png").convert_alpha()
    MapSelectH = pygame.image.load("skins/"+skin+"/mapselect_selected.png").convert_alpha()
    Icon = pygame.image.load("skins/"+skin+"/icon.png").convert_alpha()
    Overlay = pygame.image.load("skins/"+skin+"/menu_overlay.png").convert_alpha()
    Cursor=pygame.image.load("skins/"+skin+"/cursor.png").convert_alpha()
    BackButton=pygame.image.load("skins/"+skin+"/back.png").convert_alpha()
    BackButtonH=pygame.image.load("skins/"+skin+"/back_selected.png").convert_alpha()
    PlayButton=pygame.image.load("skins/"+skin+"/play.png").convert_alpha()
    PlayButtonH=pygame.image.load("skins/"+skin+"/play_selected.png").convert_alpha()
    BPM = Text.Text(FONT,30,WHITE)
    Musician = Text.Text(FONT,30,WHITE)
    Beatmapper = Text.Text(FONT,30,WHITE)
    Map_text = (Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE))
    Back_button = Button.ClickButton(BackButton,BackButtonH,140,640)
    Play_button = Button.ClickButton(PlayButton,PlayButtonH,940,640)
    SelectedIndex = 0
    pygame.event.set_allowed([KEYDOWN,QUIT,MOUSEBUTTONDOWN])
    Background = LoadBackground(MapsNameList,SelectedIndex,skin)
    Info = json.load(open("maps/"+MapsNameList[SelectedIndex%len(MapsNameList)]+"/Info.json"))["Info"]
    while True:
        Curr_time = pygame.time.get_ticks()
        Curr_Objects = []
        Mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if (event.type == QUIT):
                pygame.quit()
                sys.exit()
      
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_DOWN:
                    SelectedIndex+=1
                    Background = LoadBackground(MapsNameList,SelectedIndex,skin)
                    Info = json.load(open("maps/"+MapsNameList[SelectedIndex%len(MapsNameList)]+"/Info.json"))["Info"]
                if event.key == K_UP:
                    SelectedIndex-=1
                    Background = LoadBackground(MapsNameList,SelectedIndex,skin)
                    Info = json.load(open("maps/"+MapsNameList[SelectedIndex%len(MapsNameList)]+"/Info.json"))["Info"]
                if event.key == K_RETURN:
                    ModSelect.Render(target,MapsNameList[SelectedIndex%len(MapsNameList)],skin)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if Back_button.get_overlay(pos[0],pos[1]):
                        pygame.quit()
                        sys.exit()  
                    if Play_button.get_overlay(pos[0],pos[1]):
                        ModSelect.Render(target,MapsNameList[SelectedIndex%len(MapsNameList)],skin)
                                  
        Curr_Objects.append((Background,(0,0)))
        Iconc = pygame.Surface((350+0.02*(Curr_time%300),350+0.02*(Curr_time%300))).convert_alpha()
        pygame.transform.scale(Icon,(350+0.02*(Curr_time%300),350+0.02*(Curr_time%300)),dest_surface= Iconc)
        Curr_Objects.append((Iconc,Utilities.center(225,360,350+0.02*(Curr_time%300),350+0.02*(Curr_time%300))))
        for i in range(-3,4):
            if i != 0:
                Curr_Objects.append((MapSelect,(480,130*i+300)))
                Map_text[i+3].render_tlcorner(Curr_Objects,MapsNameList[(SelectedIndex+i)%len(MapsNameList)],485,130*i+305)
            else:
                Curr_Objects.append((MapSelectH,(450,300)))
                Map_text[3].render_tlcorner(Curr_Objects,MapsNameList[SelectedIndex%len(MapsNameList)],455,130*i+305)
        Curr_Objects.append((Overlay,(0,0)))
        BPM.render_tlcorner(Curr_Objects,"BPM: "+str(Info["BPM"]),30,30)
        Musician.render_tlcorner(Curr_Objects,"Musician: "+str(Info["Musician"]),30,60)
        Beatmapper.render_tlcorner(Curr_Objects,str("Beatmapper: "+Info["Beatmapper"]),30,90)
        Back_button.render_center(Curr_Objects,Back_button.get_overlay(Mouse_pos[0],Mouse_pos[1]))
        Play_button.render_center(Curr_Objects,Play_button.get_overlay(Mouse_pos[0],Mouse_pos[1]))
        Curr_Objects.append((Cursor,Utilities.center(Mouse_pos[0],Mouse_pos[1],50,50)))
        Utilities.render(target,Curr_Objects)

def LoadBackground(list,index,skin):
    try:
        Background=pygame.image.load("maps/"+list[index%len(list)]+"/background.png").convert_alpha()
    except:
        Background=pygame.Surface((1080,720))
        Background.fill(WHITE)
    try: 
        pygame.mixer.music.load("maps/"+list[index%len(list)]+"/music.wav")
    except:
        pygame.mixer.music.load("skins/"+skin+"/failsave.mp3")
    pygame.mixer.music.play()
    Background.set_alpha(100)
    return Background

