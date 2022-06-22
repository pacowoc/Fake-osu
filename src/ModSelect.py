
import math
from msilib.schema import Font
import pygame
import sys
import os
import json
from pygame.locals import *
import Button
import Menu
import MapPlayer
import Utilities
import Text

FONT = "fonts/Aller_Lt.ttf"
WHITE = (255,255,255)

def Render(target,map_,skin):
    Cursor=pygame.image.load("skins/"+skin+"/cursor.png").convert_alpha()
    Mods = [0,0,0,0]
    Diff_list = list(os.listdir("C:\Fake osu!\Fake osu!\maps\\"+ map_ +"\\maps"))
    Diff_list = sorted(Diff_list, key=lambda diff:json.load(open("maps/"+map_+"/maps/"+diff+"/map.json"))["Info"]["Order"]) 
    SelectedIndex = 0
    Diff = Diff_list[SelectedIndex%len(Diff_list)]  
    LeaderBoard_dict = {} 
    for x in Diff_list:
        LeaderBoard_dict[x] = sorted(list(json.load(open('maps/'+map_+"/maps/"+x+'/local_leaderboard.json'))["Contents"]), key= lambda a:a['Score'],reverse=True)
    try:
        Background=pygame.image.load("maps/"+map_+"/background.png").convert_alpha()
    except:
        Background=pygame.Surface((1080,720))
        Background.fill(WHITE) 
    Background.set_alpha(100)
    HR = pygame.image.load("skins/"+skin+"/hr.png").convert_alpha()
    EZ = pygame.image.load("skins/"+skin+"/ez.png").convert_alpha()
    DT = pygame.image.load("skins/"+skin+"/dt.png").convert_alpha()
    HT = pygame.image.load("skins/"+skin+"/ht.png").convert_alpha()
    HD = pygame.image.load("skins/"+skin+"/hd.png").convert_alpha()
    FL = pygame.image.load("skins/"+skin+"/fl.png").convert_alpha()
    NM = pygame.image.load("skins/"+skin+"/nm.png").convert_alpha()
    BackButton=pygame.image.load("skins/"+skin+"/back.png").convert_alpha()
    BackButtonH=pygame.image.load("skins/"+skin+"/back_selected.png").convert_alpha()
    PlayButton=pygame.image.load("skins/"+skin+"/play.png").convert_alpha()
    PlayButtonH=pygame.image.load("skins/"+skin+"/play_selected.png").convert_alpha()

    Back_button = Button.ClickButton(BackButton,BackButtonH,140,640)
    Play_button = Button.ClickButton(PlayButton,PlayButtonH,940,640)
    HD_button = Button.ToggleButton([NM,HD],628,508)
    DT_button = Button.ToggleButton([NM,DT,HT],753,508)
    HR_button = Button.ToggleButton([NM,HR,EZ],878,508)
    FL_button = Button.ToggleButton([NM,FL],1003,508)
    SS = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/SS.png").convert_alpha(),(90,90),SS)
    SS_HD = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/SS_hd.png").convert_alpha(),(90,90),SS_HD)
    S = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/S.png").convert_alpha(),(90,90),S)
    S_HD = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/S_hd.png").convert_alpha(),(90,90),S_HD)
    A = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/A.png").convert_alpha(),(90,90),A)
    B = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/B.png").convert_alpha(),(90,90),B)
    C = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/C.png").convert_alpha(),(90,90),C)
    D = pygame.Surface((90,90)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/D.png").convert_alpha(),(90,90),D)
    DiffSelect = pygame.Surface((500,80)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/mapselect.png").convert_alpha(),(500,80),DiffSelect)
    DiffselectH = pygame.Surface((500,80)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/mapselect_selected.png").convert_alpha(),(500,80),DiffselectH)
    LeaderBoard = pygame.Surface((400,85)).convert_alpha()
    pygame.transform.scale(pygame.image.load("skins/"+skin+"/mapselect.png").convert_alpha(),(400,85),LeaderBoard)
    Overlay = pygame.image.load("skins/"+skin+"/modselect_overlay.png").convert_alpha()
    Diff_text = (Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE),
                Text.Text(FONT,40,WHITE))
    Score_text = (Text.Text(FONT,60,WHITE),
                Text.Text(FONT,60,WHITE),
                Text.Text(FONT,60,WHITE),
                Text.Text(FONT,60,WHITE),
                Text.Text(FONT,60,WHITE))
    Acc_text = (Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE))
    MCombo_text = (Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE))
    Mod_text = (Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE),
                Text.Text(FONT,15,WHITE))
    Disc_text = Text.Text(FONT,40,WHITE)
    AR_OD_text = Text.Text(FONT,30,WHITE)
    CS_L_text = Text.Text(FONT,30,WHITE)

    content = json.load(open('maps/'+map_+"/maps/"+Diff+'/map.json'))
    while True:
        Mouse_pos = pygame.mouse.get_pos()
        Curr_Objects = [(Background,(0,0))]
        Curr_Objects.append((Overlay,(0,0)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Menu.Render(target,skin)
                if event.key == K_RETURN:
                    MapPlayer.Play(target,map_,Diff,skin,Mods)
                if event.key == K_DOWN:
                    SelectedIndex+=1
                    Diff = Diff_list[SelectedIndex%len(Diff_list)]   
                if event.key == K_UP:
                    SelectedIndex-=1
                    Diff = Diff_list[SelectedIndex%len(Diff_list)]   
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: #LMB
                    pos = event.pos
                    if Back_button.get_overlay(pos[0],pos[1]):
                        Menu.Render(target,skin)
                    if Play_button.get_overlay(pos[0],pos[1]):
                        MapPlayer.Play(target,map_,Diff,skin,Mods)
                    if HD_button.get_overlay(pos[0],pos[1]):
                        HD_button.next_state()
                    if DT_button.get_overlay(pos[0],pos[1]):
                        DT_button.next_state()
                    if HR_button.get_overlay(pos[0],pos[1]):
                        HR_button.next_state()
                    if FL_button.get_overlay(pos[0],pos[1]):
                        FL_button.next_state()
                
                if event.button == 2: #RMB
                    pos = event.pos
                    if HD_button.get_overlay(pos[0],pos[1]):
                        HD_button.previous_state()
                    if DT_button.get_overlay(pos[0],pos[1]):
                        DT_button.previous_state()
                    if HR_button.get_overlay(pos[0],pos[1]):
                        HR_button.previous_state()
                    if FL_button.get_overlay(pos[0],pos[1]):
                        FL_button.previous_state()
        AR = content["Info"]["AR"]
        CS = content["Info"]["CS"]
        OD = content["Info"]["OD"]
        Time = content["Objects"][-1]["Time"]
        if Mods[2] == 1:
            AR*=1.4
            CS*=1.4
            OD*=1.4
            if AR>10:
                AR=10
            if CS>10:
                CS=10
            if OD>10:
                OD=10

        if Mods[2] == 2:
            AR*=0.5
            CS*=0.5
            OD*=0.5

        if Mods[1] == 1:
            if AR<=5:
                AR = 8/15*AR+5
            else:
                AR = 2/3*AR+13/3
        
            OD = 2/3*OD+40/9
            Time /= 1.5
        if Mods[1] == 2:
            if AR<=5:
                AR = 4/3*AR-5
            elif AR<=7:
                AR = 5/3*AR-20/3
            else:
                AR = 4/3*AR-13/3
            OD = 4/3*OD-40/9
            Time /= 0.75
        for i in range(5):
            Curr_Objects.append((LeaderBoard,(40,140+90*i)))
        for i in range(-2,3):
            if i != 0:
                Curr_Objects.append((DiffSelect,(540,200+85*i)))
                Diff_text[i+2].render_tlcorner(Curr_Objects,Diff_list[(SelectedIndex+i)%len(Diff_list)],545,85*i+205)
            else:
                Curr_Objects.append((DiffselectH,(520,200)))
                Diff_text[2].render_tlcorner(Curr_Objects,Diff_list[(SelectedIndex)%len(Diff_list)],545,205)
        for i in range(min(5,len(LeaderBoard_dict[Diff]))):
            Acc_text[i].render_trcorner(Curr_Objects,str(math.ceil(10000*LeaderBoard_dict[Diff][i]["Acc"])/100)+"%",435,140+90*i)
            MCombo_text[i].render_trcorner(Curr_Objects,str(LeaderBoard_dict[Diff][i]["MCombo"])+"x",435,170+90*i)
            text = ""
            if LeaderBoard_dict[Diff][i]["Mods"][2] == -1:        #EZ
                text = text+"EZ"
            if LeaderBoard_dict[Diff][i]["Mods"][1] == -1:        #HT
                text = text+"HT"
            if LeaderBoard_dict[Diff][i]["Mods"][0] == 1:         #HD
                text = text+"HD"
            if LeaderBoard_dict[Diff][i]["Mods"][1] == 1:         #DT
                text = text+"DT"
            if LeaderBoard_dict[Diff][i]["Mods"][2] == 1:         #HR
                text = text+"HR"
            if LeaderBoard_dict[Diff][i]["Mods"][3] == 1:         #FL
                text = text+"FL"
            Mod_text[i].render_trcorner(Curr_Objects,text,435,200+90*i)
            Score_text[i].render_tlcorner(Curr_Objects,str(math.ceil(LeaderBoard_dict[Diff][i]["Score"])),160,155+90*i)

            if LeaderBoard_dict[Diff][i]["Rank"] == "SS":
                if LeaderBoard_dict[Diff][i]["Mods"][0] == 1 or LeaderBoard_dict[Diff][i]["Mods"][3] == 1:
                    Curr_Objects.append((SS_HD,(55,140+90*i)))
                else:
                    Curr_Objects.append((SS,(55,140+90*i)))
            if LeaderBoard_dict[Diff][i]["Rank"] == "S":
                if LeaderBoard_dict[Diff][i]["Mods"][0] == 1 or LeaderBoard_dict[Diff][i]["Mods"][3] == 1:
                    Curr_Objects.append((S_HD,(55,140+90*i)))
                else:
                    Curr_Objects.append((S,(55,140+90*i)))
            if LeaderBoard_dict[Diff][i]["Rank"] == "A":
                Curr_Objects.append((A,(55,140+90*i)))
            if LeaderBoard_dict[Diff][i]["Rank"] == "B":
                Curr_Objects.append((B,(55,140+90*i)))
            if LeaderBoard_dict[Diff][i]["Rank"] == "C":
                Curr_Objects.append((C,(55,140+90*i)))
            if LeaderBoard_dict[Diff][i]["Rank"] == "D":
                Curr_Objects.append((D,(55,140+90*i)))


        Mods = [HD_button.get_state(),DT_button.get_state(),HR_button.get_state(),FL_button.get_state()]
        Disc_text.render_tlcorner(Curr_Objects,map_+"["+Diff+"]",40,0)
        AR_OD_text.render_tlcorner(Curr_Objects,"AR:"+str(round(AR*10)/10)+"  "+"OD:"+str(round(OD*10)/10),40,40)
        CS_L_text.render_tlcorner(Curr_Objects,"CS:"+str(round(CS*10)/10)+"  "+"Length:"+str(round(Time)),40,70)
    
        Back_button.render_center(Curr_Objects,Back_button.get_overlay(Mouse_pos[0],Mouse_pos[1]))
        Play_button.render_center(Curr_Objects,Play_button.get_overlay(Mouse_pos[0],Mouse_pos[1]))
        HD_button.render_center(Curr_Objects)
        DT_button.render_center(Curr_Objects)
        HR_button.render_center(Curr_Objects)
        FL_button.render_center(Curr_Objects)
        Curr_Objects.append((Cursor,Utilities.center(Mouse_pos[0],Mouse_pos[1],50,50)))
        Utilities.render(target,Curr_Objects)

                





