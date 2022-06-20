import pygame,sys
from pygame.locals import *
import json
import math
import Utilities 
import ResultScreen
import Gameplay.Circle as Circle
import Gameplay.Slider as Slider
import Gameplay.Spinner as Spinner
import Gameplay.End as End
import Text


BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (120,120,120)
TRANSPARENT = (0,0,0,0)
FONT = "fonts/Aller_Lt.ttf"

DEBUG_MODE= True
def Play(target,map_,diff,skin,mods):
  #Load text objects
  Spin_text = Text.Text(FONT,80,GRAY)
  Score_text = Text.Text(FONT,40,WHITE)
  Combo_text = Text.Text(FONT,80,WHITE)
  Acc_text = Text.Text(FONT,30,WHITE)
  if DEBUG_MODE:
    FPS_text = Text.Text(FONT,30,WHITE)

  ##LOAD TEXTURES AND MAP

  Hit_circle_original=pygame.image.load("skins/"+skin+"/circle.png").convert_alpha()
  Approach_circle_original=pygame.image.load("skins/"+skin+"/approach_circle.png").convert_alpha()
  Cursor=pygame.image.load("skins/"+skin+"/cursor.png").convert_alpha()
  P300=pygame.image.load("skins/"+skin+"/300.png").convert_alpha()
  P100=pygame.image.load("skins/"+skin+"/100.png").convert_alpha()
  P50=pygame.image.load("skins/"+skin+"/50.png").convert_alpha()
  Pmiss=pygame.image.load("skins/"+skin+"/0.png").convert_alpha()
  Slider_body_original=pygame.image.load("skins/"+skin+"/slider_body.png").convert_alpha()
  Spinner_original=pygame.image.load("skins/"+skin+"/spinner.png").convert_alpha()
  Flashlight_filter = pygame.image.load("skins/"+skin+"/flashlight_filter.png").convert_alpha()

  Hitsound=pygame.mixer.Sound("skins/"+skin+"/hitsound.ogg")
  Bonus=pygame.mixer.Sound("skins/"+skin+"/spinnerbonus.wav")
  content = json.load(open('maps/'+map_+"/maps/"+diff+'/map.json'))
  try:
    if mods[1] == 1:  
      pygame.mixer.music.load("maps/"+map_+"/music_dt.wav")
    elif mods[1] == 2:
      pygame.mixer.music.load("maps/"+map_+"/music_ht.wav")
    else:
      pygame.mixer.music.load("maps/"+map_+"/music.wav")
  except:
    pygame.mixer.music.load("skins/"+skin+"/failsave.mp3")
  #Extract content

  AR = content["Info"]["AR"]
  CS = content["Info"]["CS"]
  OD = content["Info"]["OD"]
  Start_delay = content['Info']["Delay"]
  Object_list =content["Objects"]

  Object_list = tuple(Object_list)
  ##CALCULATIONS
  Mods_Multi = 1
  
  #HR
  if mods[2] == 1:
    Mods_Multi *= 1.06
    AR*=1.4
    CS*=1.4
    OD*=1.4
    if AR>10:
      AR=10
    if CS>10:
      CS=10
    if OD>10:
      OD=10

  #EZ
  if mods[2] == 2:
    Mods_Multi *= 0.5
    AR*=0.5
    CS*=0.5
    OD*=0.5

  #DT
  if mods[1] == 1:
    Mods_Multi*=1.12
    #LOW AR --> HIGH AR
    if AR<=5:
      AR = 8/15*AR+5
    #HIGH AR --> HIGH AR
    else:
      AR = 2/3*AR+13/3
        
    OD = 2/3*OD+40/9
    for obj in Object_list:
      try:
        obj["Span"] /= 1.5
      except:
        pass
      obj["Time"] /= 1.5
    Start_delay /= 1.5

  #HT
  if mods[1] == 2:
    Mods_Multi*=0.3
    #LOW AR --> LOW AR
    if AR<=5:
      AR = 4/3*AR-5
    #HIGH AR --> LOW AR
    elif AR<=7:
      AR = 5/3*AR-20/3
    #HIGH AR --> HIGH AR
    else:
      AR = 4/3*AR-13/3
    OD = 4/3*OD-40/9
    for obj in Object_list:
      try:
        obj["Span"] /= 0.75
      except:
        pass
      obj["Time"] /= 0.75
    Start_delay /= 0.75
  #AR display calculations
  if(AR<5):#low ar
    Delta = 1200+120*(5-AR)

  elif(AR==5):#ar=5
    Delta = 1200

  elif(AR>5):#high ar
    Delta = 1200+150*(5-AR)

  #OD Hit window calculations

  W300 = 80-6*OD
  W100 = 140-8*OD
  W50 = 200-10*OD
  if(OD<5):#low od
    spinner_req = (5-2*(5-OD)/5)/1000
  elif(OD==5):#od=5
    spinner_req = 1/1000
  elif(OD>5):#high od
    spinner_req = (5-2.5*(5-OD))/1000
  
  #CS display calculations
  Radius = 54.4-4.48*CS

  #Transform Resizable surface=
  Hit_circle = pygame.Surface((2*Radius,2*Radius)).convert_alpha()
  pygame.transform.scale(Hit_circle_original,(2*Radius,2*Radius),dest_surface=Hit_circle)

  Slider_body = pygame.Surface((2*Radius,2*Radius)).convert_alpha()
  pygame.transform.scale(Slider_body_original,(2*Radius,2*Radius),dest_surface=Slider_body)

  Slider_ball = pygame.Surface((5*Radius,5*Radius)).convert_alpha()
  pygame.transform.scale(Hit_circle_original,(5*Radius,5*Radius),dest_surface=Slider_ball)
    
  #Assign Timechart
  notechart_F=[]
  notechart_C=[]
  for obj in Object_list:
    if obj["Type"]=="C":
      notechart_F.append(Circle.Circle(obj["Posx"],obj["Posy"],Radius,obj["Time"],Delta,Hit_circle))
    if obj["Type"]=="S":
      notechart_F.append(Slider.Slider(obj["Posx"],obj["Posy"],Radius,obj["Time"],obj["Span"],Delta))
    if obj["Type"]=="G":
      notechart_F.append(Spinner.Spinner(obj["Time"],obj["Span"],spinner_req*obj["Span"]))
    if obj["Type"]=="E":
      notechart_F.append(End.End(obj["Time"]))
  
  # initialize
  Map_start = pygame.time.get_ticks()
  pygame.key.set_repeat()
  Score = 0
  Acc_Score = 0
  Acc = 0
  Combo = 0
  Acc_Divider = 0
  Score_cache = []
  Rating_Count = {"300":0,"100":0,"50":0,"0":0}
  Max_Combo = 0
  FPS_Clock=pygame.time.Clock()
  Music = False
  pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
  
  #           #
  # MAIN LOOP #
  #           #
  while True:
    #Get time
    Curr_Time = pygame.time.get_ticks() - Map_start
    MousePosX = pygame.mouse.get_pos()[0]
    MousePosY = pygame.mouse.get_pos()[1]
    if Music == False and Curr_Time>=Start_delay:
      pygame.mixer.music.play()
      Music=True
    FPS_Clock.tick()
    FPS = FPS_Clock.get_fps()
    Curr_Objects = []
    for event in pygame.event.get():

      #Quit
      if (event.type == QUIT):
        pygame.quit()
        sys.exit()
      
      #Z or X pressed
      if event.type == KEYDOWN:
        if event.key == K_z or event.key == K_x:
          for note in notechart_C:
            if type(note) is Circle.Circle:
              #Check if the cursor is in the hitcircle 
              distance = math.sqrt((MousePosX-note.Posx)**2+(MousePosY-note.Posy)**2)
              if distance<Radius:
                Hit = note.hit_eval(Curr_Time,W300,W100,W50)
                if Hit:
                  Combo+=1
                  Hitsound.play()
                else:
                  Combo=0
                Rating_Count[str(Hit)] += 1
                Score_cache.append((Hit,Curr_Time,(note.Posx-25,note.Posy-15)))
                Acc_Score += Hit
                Score += Hit+(Hit*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
                notechart_C.remove(note)
                Acc_Divider+=1
                Acc=Utilities.division(Acc_Score,Acc_Divider)/300
                break

            #Slider head
            if type(note) is Slider.Slider and note.HeadHit==False:
              #Check if the cursor is in the hitcircle 
              distance = math.sqrt((MousePosX-note.HPosx)**2+(MousePosY-note.HPosy)**2)
              if distance<Radius:
                note.HeadHit = True
                Hit= note.head_hit_eval(Curr_Time,W50)
                if Hit:
                  Combo+=1
                  Hitsound.play()
                  Acc_Divider+=1
                else:
                  Combo=0
                  notechart_C.remove(note)
                  Acc_Divider+=2
                Rating_Count[str(Hit)] += 1
                Score_cache.append((Hit,Curr_Time,(note.HPosx-25,note.HPosy-15)))
                Acc_Score += Hit
                Score += Hit+(Hit*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
                Acc=Utilities.division(Acc_Score,Acc_Divider)/300
                break
    
    #Z or x held
    if pygame.key.get_pressed()[K_x] or pygame.key.get_pressed()[K_z]:
      for note in notechart_C:
        #Slider
        if type(note) is Slider.Slider:
          if W50<Curr_Time-note.Time<note.Span-W50:
            #Check if Slider break
            distance = math.sqrt((MousePosX-note.get_ball_x(Curr_Time))**2+(MousePosY-note.get_ball_y(Curr_Time))**2)
            if distance>2.5*Radius:
              Acc_Score+=100
              Acc_Divider+=1
              Acc=Utilities.division(Acc_Score,Acc_Divider)/300
              Rating_Count["100"]+=1
              Score_cache.append((100,Curr_Time,(note.get_ball_x(Curr_Time)-25,note.get_ball_y(Curr_Time)-15)))
              Combo=0
              notechart_C.remove(note)
            
        #Check spinner quadrant
        if type(note) is Spinner.Spinner:
          # I
          if MousePosX >= 540 and MousePosY <= 360:
            note.Quadrants[0]=1
          # II
          elif MousePosX <= 540 and MousePosY <= 360:
            note.Quadrants[1]=1
          # III
          elif MousePosX <= 540 and MousePosY >= 360:
            note.Quadrants[2]=1
          # IV
          elif MousePosX >= 540 and MousePosY >= 360:
            note.Quadrants[3]=1
          #Spin completion(all 4 quadrants cleared)
          if note.Quadrants == [1,1,1,1]:
            note.Quadrants=[0,0,0,0]
            note.Spins+=1
            if note.Spins>note.Req:
              Score+=1000
              Bonus.play()
            else:
              Score+=100
          if note.Spins>note.Req:
            Spin_text.render_center(Curr_Objects,str(1000*math.ceil(note.Spins-note.Req)),540,450)

    #Neither Z nor X is pressed
    if pygame.key.get_pressed()[K_z]==False and pygame.key.get_pressed()[K_x]==False:
      for note in notechart_C:
        if type(note) is Slider.Slider:
          #in slider body
          if (W50<=Curr_Time-note.Time<=note.Span-W50 or note.Span+W50<=Curr_Time-note.Time) and note.HeadHit:
            Acc_Score+=100
            Rating_Count["100"]+=1
            Acc_Divider+=1
            Acc=Utilities.division(Acc_Score,Acc_Divider)/300
            Score_cache.append((100,Curr_Time,(note.get_ball_x(Curr_Time)-25,note.get_ball_y(Curr_Time)-15)))
            Score += 100+(100*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
            Combo=0
            notechart_C.remove(note)
            
          #in/over leaving window
          elif note.Span-W50<Curr_Time-note.Time<note.Span+W50:
            Rating_Count["300"]+=1
            Acc_Score+=300
            Hitsound.play()
            Acc_Divider+=1
            Acc=Utilities.division(Acc_Score,Acc_Divider)/300
            Score_cache.append((300,Curr_Time,(note.get_ball_x(Curr_Time)-25,note.get_ball_y(Curr_Time)-15)))
            Combo+=1
            notechart_C.remove(note)
            Score += 300+(300*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
            Score += note.Span
          break
    
    #Score icon
    for scoreicon in Score_cache:
      if Curr_Time-scoreicon[1] > 500:
        Score_cache.remove(scoreicon)
      P300.set_alpha(255*(1-(Curr_Time-scoreicon[1])/500))
      P100.set_alpha(255*(1-(Curr_Time-scoreicon[1])/500))
      P50.set_alpha(255*(1-(Curr_Time-scoreicon[1])/500))
      Pmiss.set_alpha(255*(1-(Curr_Time-scoreicon[1])/500))
      if scoreicon[0]==300:
        Curr_Objects.append((P300,scoreicon[2]))
      elif scoreicon[0]==100:
        Curr_Objects.append((P100,scoreicon[2]))
      elif scoreicon[0]==50:
        Curr_Objects.append((P50,scoreicon[2]))
      elif scoreicon[0]==0:
        Curr_Objects.append((Pmiss,scoreicon[2]))
    
    for note in notechart_C:
      #Misses by running out of time
      if type(note) is Circle.Circle and Curr_Time >= note.Time+W50:
        Score_cache.append((0,Curr_Time,(note.Posx-25,note.Posy-15)))
        notechart_C.remove(note)
        Rating_Count["0"]+=1
        Acc_Divider+=1
        Acc=Utilities.division(Acc_Score,Acc_Divider)/300
        Combo=0
        Score_cache.append((0,Curr_Time,(note.Posx-25,note.Posy-15)))
      if type(note) is Slider.Slider and Curr_Time >= note.Time+W50 and note.HeadHit == False:
        notechart_C.remove(note)
        Rating_Count["0"]+=1
        Acc_Divider+=2
        Acc=Utilities.division(Acc_Score,Acc_Divider)/300

      #Ending the map
      if type(note) is End.End:
        Acc=Utilities.division(Acc_Score,Acc_Divider)/300
        pygame.mixer.music.unload()
        ResultScreen.Render(target,map_,diff,skin,mods,Score,Acc,Rating_Count,Max_Combo)
      
      #Detect the end of spinner(s)
      if type(note) is Spinner.Spinner and Curr_Time >= note.Time + note.Span:
        Hit=note.End()
        if Hit:
          Combo+=1
          Hitsound.play()
        else:
          Combo=0
        Rating_Count[str(Hit)] += 1
        Score_cache.append((Hit,Curr_Time,(515,345)))
        Acc_Score += Hit
        Score += Hit+(Hit*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
        notechart_C.remove(note)
        Acc_Divider+=1
        Acc=Utilities.division(Acc_Score,Acc_Divider)/300
        
    #Check for a new note to load
    if(Curr_Time >= notechart_F[0].Time-Delta):
      notechart_C.append(notechart_F[0])
      notechart_F.pop(0)

    #Render#

    for note in notechart_C:
      #Circle
      if type(note) is Circle.Circle:
        if mods[0] == 1: #HD
          note.render_hc_hd(Curr_Objects,Curr_Time)
        else:
          note.render_ac(Curr_Objects,Approach_circle_original,Curr_Time)
          note.render_hc(Curr_Objects,Curr_Time)
      if type(note) is Slider.Slider:
        #Slider body
        note.render_body(Curr_Objects,Slider_body)
        #Slider head
        note.render_head_ac(Curr_Objects,Approach_circle_original,Curr_Time)
        note.render_head_hc(Curr_Objects,Hit_circle)
        #Slider ball
        if 0<(Curr_Time-note.Time)/note.Span<1:
          note.render_follow_circle(Curr_Objects,Hit_circle,Slider_ball,Curr_Time)
        #Slider end
        note.render_end(Curr_Objects,Hit_circle)
  

      #Spinner
      if type(note) is Spinner.Spinner:
        Curr_Objects.append((Spinner_original,(290,110)))
    #FL
    if mods[3] == 1:
      Curr_Objects.append((Flashlight_filter,(MousePosX-1080,MousePosY-1080)))
    #Score counter
    Score_text.render_trcorner(Curr_Objects,str(math.ceil(Score)),1050,30)
    #Combo counter
    Combo_text.render_blcorner(Curr_Objects,str(Combo)+"x",50,690)
    #Acc counter
    Acc_text.render_trcorner(Curr_Objects,str(math.ceil(Acc*10000)/100)+"%",1050,30+Score_text.get_size_y(Score))
    #FPS counter
    if DEBUG_MODE:
      FPS_text.render_tlcorner(Curr_Objects,str(int(FPS)),0,30)
    #Mouse cursor
    Curr_Objects.append((Cursor,Utilities.center(MousePosX,MousePosY,50,50)))
    if Combo>Max_Combo:
      Max_Combo = Combo
    Utilities.render(target,Curr_Objects)
