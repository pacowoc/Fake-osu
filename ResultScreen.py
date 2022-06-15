import pygame,sys
import Utilities
import math
from pygame.locals import *

FONT = "fonts\\Aller_Lt.ttf"
WHITE = (255,255,255)

def Render(target,map_,diff,skin,mods,score,acc,rating_count,max_combo):
    Rank_texture={}
    Rank_texture["SS"]=pygame.image.load("skins\\"+skin+"\\SS.png").convert_alpha()
    Rank_texture["S"]=pygame.image.load("skins\\"+skin+"\\S.png").convert_alpha()
    Rank_texture["A"]=pygame.image.load("skins\\"+skin+"\\A.png").convert_alpha()
    Rank_texture["B"]=pygame.image.load("skins\\"+skin+"\\B.png").convert_alpha()
    Rank_texture["C"]=pygame.image.load("skins\\"+skin+"\\C.png").convert_alpha()
    Rank_texture["D"]=pygame.image.load("skins\\"+skin+"\\D.png").convert_alpha()
    Cursor=pygame.image.load("skins\\"+skin+"\\cursor.png").convert_alpha()
    GUI=pygame.image.load("skins\\"+skin+"\\result_screen.png").convert_alpha()
    FC=pygame.image.load("skins\\"+skin+"\\FC.png").convert_alpha()
    HR = pygame.image.load("skins\\"+skin+"\\hr.png").convert_alpha()
    EZ = pygame.image.load("skins\\"+skin+"\\ez.png").convert_alpha()
    DT = pygame.image.load("skins\\"+skin+"\\dt.png").convert_alpha()
    HT = pygame.image.load("skins\\"+skin+"\\ht.png").convert_alpha()
    try:
        Background=pygame.image.load("maps\\"+map_+"\\background.png").convert_alpha()
    except:
        Background=pygame.Surface((1080,720))
        Background.fill(WHITE)
    do_FC=False
    map_combo=rating_count[0]+rating_count[1]+rating_count[2]+rating_count[3]
    if max_combo == map_combo:
        do_FC=True
    if rating_count[0] == map_combo:
        rank = "SS"
    elif rating_count[0]>=0.9*map_combo and rating_count[3]==0 and rating_count[2]<=0.01*map_combo:
        rank = "S"
    elif (rating_count[0]>=0.8*map_combo and rating_count[3]==0 )or rating_count[0]>=0.9*map_combo:
        rank = "A"
    elif (rating_count[0]>=0.7*map_combo and rating_count[3]==0 )or rating_count[0]>=0.8*map_combo:
        rank = "B"
    elif rating_count[0]>=0.6*map_combo:
        rank = "C"
    else:
        rank = "D"
    while True:
        for event in pygame.event.get():
            if (event.type == QUIT):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN):
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        curr_Objects = []
        curr_Objects.append((Background,(0,0)))
        curr_Objects.append((GUI,(0,0)))
        if do_FC:
            curr_Objects.append((FC,(400,507)))
        curr_Objects.append((Rank_texture[rank],(576,47)))

        MComboText = Utilities.render_text("Max combo:"+str(max_combo)+"x",FONT,30,WHITE)
        curr_Objects.append((MComboText[0],(100,527)))
        Acc_text = Utilities.render_text("Accuracy: "+str(math.ceil(acc*10000)/100)+"%",FONT,30,WHITE)
        curr_Objects.append((Acc_text[0],(100,433)))

        Score_text = Utilities.render_text("Score:"+str(math.ceil(score)),FONT,50,WHITE)
        curr_Objects.append((Score_text[0],(100,329)))

        Rating_text_300 = Utilities.render_text(str(rating_count[0]),FONT,50,WHITE)
        curr_Objects.append((Rating_text_300[0],Utilities.center(230,145,Rating_text_300[1],90)))

        Rating_text_100 = Utilities.render_text(str(rating_count[1]),FONT,50,WHITE)
        curr_Objects.append((Rating_text_100[0],Utilities.center(456,145,Rating_text_100[1],90)))

        Rating_text_50 = Utilities.render_text(str(rating_count[2]),FONT,50,WHITE)
        curr_Objects.append((Rating_text_50[0],Utilities.center(230,252,Rating_text_50[1],90)))

        Rating_text_0 = Utilities.render_text(str(rating_count[3]),FONT,50,WHITE)
        curr_Objects.append((Rating_text_0[0],Utilities.center(456,252,Rating_text_0[1],90)))

        Topic_text = Utilities.render_text(map_+"["+diff+"]",FONT,35,WHITE)
        curr_Objects.append((Topic_text[0],(10,10)))
        mod_count = 0
        if mods[2] == -1:
            curr_Objects.append((EZ,(576+80*mod_count,397)))
            mod_count+=1
        if mods[1] == -1:
            curr_Objects.append((HT,(576+80*mod_count,397)))
            mod_count+=1
        if mods[1] == 1:
            curr_Objects.append((DT,(576+80*mod_count,397)))
            mod_count+=1
        if mods[2]== 1:
            curr_Objects.append((HR,(576+80*mod_count,397)))
            mod_count+=1


        Mouse_pos = pygame.mouse.get_pos()
        curr_Objects.append((Cursor,Utilities.center(Mouse_pos[0],Mouse_pos[1],50,50)))
        Utilities.render(target,curr_Objects)