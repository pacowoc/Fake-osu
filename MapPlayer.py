
import pygame,sys
from pygame.locals import *
import json
import math
import Utilities
import bezier
import numpy
import ResultScreen


BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (120,120,120)
TRANSPARENT = (0,0,0,0)
FONT = "fonts\\Aller_Lt.ttf"

DEBUG_MODE= False
def Play(target,map_,diff,skin,mods):

  ##LOAD TEXTURES AND MAP

  Hit_circle_original=pygame.image.load("skins\\"+skin+"\\circle.png").convert_alpha()
  Approach_circle_original=pygame.image.load("skins\\"+skin+"\\approach_circle.png").convert_alpha()
  Cursor=pygame.image.load("skins\\"+skin+"\\cursor.png").convert_alpha()
  P300=pygame.image.load("skins\\"+skin+"\\300.png").convert_alpha()
  P100=pygame.image.load("skins\\"+skin+"\\100.png").convert_alpha()
  P50=pygame.image.load("skins\\"+skin+"\\50.png").convert_alpha()
  Pmiss=pygame.image.load("skins\\"+skin+"\\0.png").convert_alpha()
  Slider_body_original=pygame.image.load("skins\\"+skin+"\\slider_body.png").convert_alpha()
  Spinner=pygame.image.load("skins\\"+skin+"\\spinner.png").convert_alpha()

  Hitsound=pygame.mixer.Sound("skins\\"+skin+"\\hitsound.ogg")
  Bonus=pygame.mixer.Sound("skins\\"+skin+"\\spinnerbonus.wav")
  content = json.load(open('maps\\'+map_+"\\"+diff+'\\map.json'))
  try:
    if mods[1] == 1:  
      pygame.mixer.music.load("maps\\"+map_+"\\music_dt.wav")
    elif mods[1] == -1:
      pygame.mixer.music.load("maps\\"+map_+"\\music_ht.wav")
    else:
      pygame.mixer.music.load("maps\\"+map_+"\\music.wav")
  except:
    pygame.mixer.music.load("skins\\"+skin+"\\failsave.mp3")
  #Extract content

  AR = content["Info"]["AR"]
  CS = content["Info"]["CS"]
  OD = content["Info"]["OD"]
  Start_delay = content['Info']["Delay"]
  Object_list =content["Objects"]

  #Dirty slider stuff

  i = 0
  while i < len(Object_list):
    if Object_list[i]["Type"] == "S":
      Object_list[i]["Type"] = "S_body"
      Object_list.insert(i,{
        "Type":"S_head",
        "Time":Object_list[i]["Time"],
        "Posx":Object_list[i]["Posx"][0],
        "Posy":Object_list[i]["Posy"][0]
      })
    i+=1
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
  if mods[2] == -1:
    Mods_Multi *= 0.3
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
  if mods[1] == -1:
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
    Fade_end = 800+80*(5-AR)
    Hit = 1200+120*(5-AR)

  elif(AR==5):#ar=5
    Fade_end = 800
    Hit = 1200

  elif(AR>5):#high ar
    Fade_end = 800+100*(5-AR)
    Hit = 1200+150*(5-AR)

  #OD self.Hit window calculations
  W300 = 80-6*OD
  W100 = 140-8*OD
  W50 = 200-10*OD
  if(OD<5):#low od
    spinner_req = 5-2*(5-OD)/5
  elif(OD==5):#od=5
    spinner_req = 5
  elif(OD>5):#high od
    spinner_req = 5-2.5*(5-OD)/5
  #CS display calculations

  R = 54.4-4.48*CS

  #Transform Resizable surface

  Hit_circle = pygame.Surface((2*R,2*R)).convert_alpha()
  pygame.transform.scale(Hit_circle_original,(2*R,2*R),dest_surface=Hit_circle)

  Slider_body = pygame.Surface((2*R,2*R)).convert_alpha()
  pygame.transform.scale(Slider_body_original,(2*R,2*R),dest_surface=Slider_body)

  Slider_ball = pygame.Surface((5*R,5*R)).convert_alpha()
  pygame.transform.scale(Hit_circle_original,(5*R,5*R),dest_surface=Slider_ball)
    
    #Assign Timechart
  timechart=[]
  timechart_F=[]
  timechart_C=[]
  for obj in Object_list:
    timechart.append(int(obj["Time"])-Hit)
    timmechart = tuple(timechart)
  for i in range(len(timechart)):
    timechart_F.append(i)
    
    #initialize
  map_start = pygame.time.get_ticks()
  pygame.key.set_repeat(0)
  pygame.mouse.set_visible(0)
  Score = 0
  Acc_Score = 0
  pygame.key.set_repeat()
  Acc = 0
  Combo = 0
  Score_cache = []
  span=0
  spins = 0
  spin_time = 0
  spin_number = 0
  rating_count = [0,0,0,0]
  max_combo = 0
  FPS_clock=pygame.time.Clock()
  music = False
  pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
  ##MAIN LOOP

  while True:
    #Get time
    Curr_time = pygame.time.get_ticks()
    if music == False and Curr_time>=map_start+Start_delay:
      pygame.mixer.music.play()
      music=True
    FPS_clock.tick()
    FPS = FPS_clock.get_fps()
    curr_Objects = []
    for event in pygame.event.get():
      if (event.type == QUIT):
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_z or event.key == K_x:
          clicktime = Curr_time
          for curr_notecount in timechart_C:
            if Object_list[curr_notecount]["Type"]=="C":
              Posx = Object_list[curr_notecount]["Posx"]
              Posy = Object_list[curr_notecount]["Posy"]
              distance = math.sqrt((Mouse_pos[0]-Posx)**2+(Mouse_pos[1]-Posy)**2)
              if distance<R:
                error = clicktime-timechart[timechart_C[0]]-map_start-Hit
                error = abs(error)
                if error<=W300:
                  Score_cache.append((300,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Hit_Value=300
                  rating_count[0]+=1
                  Combo+=1
                  Hitsound.play()
                elif error<=W100:
                  Score_cache.append((100,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Hit_Value=100
                  rating_count[1]+=1
                  Combo+=1
                  Hitsound.play()
                elif error<=W50:
                  Score_cache.append((50,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Hit_Value=50
                  rating_count[2]+=1
                  Combo+=1
                  Hitsound.play()
                else:
                  Score_cache.append((0,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Combo=0
                  rating_count[3]+=1
                  Hit_Value=0
                Acc_Score += Hit_Value
                Score += Hit_Value+(Hit_Value*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
                timechart_C.remove(curr_notecount)
                break
            #Slider head
            if Object_list[curr_notecount]["Type"]=="S_head":
              Posx = Object_list[curr_notecount]["Posx"]
              Posy = Object_list[curr_notecount]["Posy"]
              distance = math.sqrt((Mouse_pos[0]-Posx)**2+(Mouse_pos[1]-Posy)**2)
              if distance<R:
                error = clicktime-timechart[curr_notecount]-map_start-Hit
                error = abs(error)
                if error<=W50:
                  Score_cache.append((300,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Acc_Score += 300
                  rating_count[0]+=1
                  Hitsound.play()
                  Combo+=1
                  timechart_C.remove(curr_notecount)
                  Hit_Value = 300
                else:
                  Score_cache.append((0,clicktime,Utilities.center(Posx,Posy,50,30)))
                  Combo=0
                  rating_count[3]+=1
                  timechart_C.remove(curr_notecount)
                  timechart_C.remove(curr_notecount+1)
                  Hit_Value = 0
                Score += Hit_Value+(Hit_Value*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)   
                break
    #Hold cycle
    if pygame.key.get_pressed()[K_x] or pygame.key.get_pressed()[K_z]:
      for curr_notecount in timechart_C:
        if Object_list[curr_notecount]["Type"] == "S_body":
          Posx = Object_list[curr_notecount]["Posx"]
          Posy = Object_list[curr_notecount]["Posy"]
          Span = Object_list[curr_notecount]["Span"]
          nodes = numpy.asfortranarray([Posx,Posy])
          main_curve = bezier.Curve(nodes, degree=len(Posx)-1)
          if W50<Curr_time-timechart[curr_notecount]-Hit-map_start<Span-W50:
            SliderballX = main_curve.evaluate((Curr_time-Hit-timechart[curr_notecount]-map_start)/Span).tolist()[0][0]
            SliderballY = main_curve.evaluate((Curr_time-Hit-timechart[curr_notecount]-map_start)/Span).tolist()[1][0]
            distance = math.sqrt((Mouse_pos[0]-SliderballX)**2+(Mouse_pos[1]-SliderballY)**2)
            if distance>2.5*R:
              #Slider break
              Acc_Score+=100
              rating_count[1]+=1
              Score_cache.append((100,Curr_time,Utilities.center(SliderballX,SliderballY,50,30)))
              Combo=0
              timechart_C.remove(curr_notecount)
        if Object_list[curr_notecount]["Type"] == "G":
          if Mouse_pos[0] >= 540 and Mouse_pos[1] <= 360:
            quadrants[0]=1
          elif Mouse_pos[0] <= 540 and Mouse_pos[1] <= 360:
            quadrants[1]=1
          elif Mouse_pos[0] <= 540 and Mouse_pos[1] >= 360:
            quadrants[2]=1
          elif Mouse_pos[0] >= 540 and Mouse_pos[1] >= 360:
            quadrants[3]=1
          if quadrants == [1,1,1,1]:
            quadrants=[0,0,0,0]
            spins+=1
            if spins>span*spinner_req/1000:
              Score+=1000
              Bonus.play()
            else:
              Score+=100

          if math.ceil(spins-span*spinner_req/1000)*1000>0:
            spin_number = math.ceil(spins-span*spinner_req/1000)*1000
            spin_time = Curr_time
    if pygame.key.get_pressed()[K_z]==False and pygame.key.get_pressed()[K_x]==False:

      for curr_notecount in timechart_C:

        if Object_list[curr_notecount]["Type"] == "S_body":
          Posx = Object_list[curr_notecount]["Posx"]
          Posy = Object_list[curr_notecount]["Posy"]
          Span = Object_list[curr_notecount]["Span"]
          nodes = numpy.asfortranarray([Posx,Posy])
          main_curve = bezier.Curve(nodes, degree=len(Posx)-1)
          SliderballX = main_curve.evaluate((Curr_time-(Hit+timechart[curr_notecount])-map_start)/Span).tolist()[0][0]
          SliderballY = main_curve.evaluate((Curr_time-(Hit+timechart[curr_notecount])-map_start)/Span).tolist()[1][0]
          #in slider body
          if W50+20<=Curr_time-(timechart[curr_notecount]+Hit)-map_start<=Span-W50:
            Acc_Score+=100
            Hit_Value=100
            rating_count[1]+=1
            Score_cache.append((100,Curr_time,Utilities.center(SliderballX,SliderballY,50,30)))
            Combo=0
            timechart_C.remove(curr_notecount)
            Score += Hit_Value+(Hit_Value*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)

          #in/over leaving window
          elif Span-W50<Curr_time-(timechart[curr_notecount]+Hit)-map_start<Span+W50:
            rating_count[0]+=1
            Acc_Score+=300
            Hit_Value=100
            Hitsound.play()
            Score_cache.append((300,Curr_time,Utilities.center(SliderballX,SliderballY,50,30)))
            Combo+=1
            timechart_C.remove(curr_notecount)
            Score += Hit_Value+(Hit_Value*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
            Score += Span

          elif Span+W50<=Curr_time-(timechart[curr_notecount]+Hit)-map_start:
            rating_count[1]+=1
            Acc_Score+=100
            Hit_Value=100
            Score_cache.append((100,Curr_time,Utilities.center(SliderballX,SliderballY,50,30)))
            Combo=0
            timechart_C.remove(curr_notecount)
            Score += Hit_Value+(Hit_Value*(Combo-1)*(AR+OD+CS)*Mods_Multi/25)
          break
    #Score icon

    if Curr_time-spin_time <= 500:
      Spin_text = Utilities.render_text(str(spin_number),FONT,80,GRAY)
      curr_Objects.append((Spin_text[0],(540-1/2*Spin_text[1],400)))


    for scoreicon in Score_cache:
      if Curr_time-scoreicon[1] > 500:
        Score_cache.remove(scoreicon)
      P300.set_alpha(255*(1-(Curr_time-scoreicon[1])/500))
      P100.set_alpha(255*(1-(Curr_time-scoreicon[1])/500))
      P50.set_alpha(255*(1-(Curr_time-scoreicon[1])/500))
      Pmiss.set_alpha(255*(1-(Curr_time-scoreicon[1])/500))
      if scoreicon[0]==300:
        curr_Objects.append((P300,scoreicon[2]))
      elif scoreicon[0]==100:
        curr_Objects.append((P100,scoreicon[2]))
      elif scoreicon[0]==50:
        curr_Objects.append((P50,scoreicon[2]))
      elif scoreicon[0]==0:
        curr_Objects.append((Pmiss,scoreicon[2]))
    for curr_notecount in timechart_C:
      if(Object_list[curr_notecount]["Type"]=="C")and Curr_time >= timechart[curr_notecount]+map_start+Hit+W50:
        Score_cache.append((0,timechart[curr_notecount]+map_start+Hit+W50,(Object_list[curr_notecount]["Posx"]-25,Object_list[curr_notecount]["Posy"]-15)))
        timechart_C.remove(curr_notecount)
        rating_count[3]+=1
        Combo=0
      if Object_list[curr_notecount]["Type"]=="S_head" and Curr_time >= timechart[curr_notecount]+map_start+Hit+W50:
        Score_cache.append((0,timechart[curr_notecount]+map_start+Hit+W50,(Object_list[curr_notecount]["Posx"]-25,Object_list[curr_notecount]["Posy"]-15)))
        timechart_C.remove(curr_notecount)
        try:
          timechart_C.remove(curr_notecount+1)
        except:
          pass
        rating_count[3]+=1
        Combo=0
      if Object_list[curr_notecount]["Type"]=="E":
        Acc = Acc_Score/(len(timechart)-1)/300
        pygame.mixer.music.unload()
        ResultScreen.Render(target,map_,diff,skin,mods,Score,Acc,rating_count,max_combo)
      if(Curr_time >= timechart[curr_notecount]+map_start+span+Hit and Object_list[curr_notecount]["Type"]=="G"):
        if spins>span*spinner_req/1000:
          Score_cache.append((300,timechart[curr_notecount]+Hit+map_start+span,(515,335)))
          Acc_Score+=300
          Hitsound.play()
          timechart_C.remove(curr_notecount)
          rating_count[0]+=1
          Combo+=1
          Acc = Acc_Score/(len(timechart)-1)/300
        elif spins>span*spinner_req/2000:
          Score_cache.append((100,timechart[curr_notecount]+Hit+map_start+span,(515,335)))
          Acc_Score+=100
          Hitsound.play()
          timechart_C.remove(curr_notecount)
          rating_count[1]+=1
          Combo+=1
          Acc = Acc_Score/(len(timechart)-1)/300
        elif spins>1:
          Score_cache.append((50,timechart[curr_notecount]+Hit+map_start+span,(515,335)))
          Acc_Score+=50
          Hitsound.play()
          timechart_C.remove(curr_notecount)
          rating_count[2]+=1
          Combo+=1
          Acc = Acc_Score/(len(timechart)-1)/300
        else:
          Score_cache.append((0,timechart[curr_notecount]+Hit+map_start+span,(515,335)))
          Acc_Score+=0
          Hitsound.play()
          timechart_C.remove(curr_notecount)
          rating_count[3]+=1
          Combo=0
          Acc = Acc_Score/(len(timechart)-1)/300

    if(Curr_time >= timechart[timechart_F[0]]+map_start):
      if Object_list[timechart_F[0]]["Type"]=="C":
          timechart_C.append(timechart_F[0])
          timechart_F.pop(0)

      elif Object_list[timechart_F[0]]["Type"]=="S_head":
          for i in range(2):
            timechart_C.append(timechart_F[0])
            timechart_F.pop(0)

      elif Object_list[timechart_F[0]]["Type"]=="G":
          span = Object_list[timechart_F[0]]["Span"]
          spins=0
          quadrants=[0,0,0,0]
          timechart_C.append(timechart_F[0])
          timechart_F.pop(0)
      elif Object_list[timechart_F[0]]["Type"]=="E":
          timechart_C.append(timechart_F[0])
          timechart_F.pop(0)

    if timechart_C != [] and timechart_C[0] >= 1:
      Acc = Acc_Score/(timechart_C[0])/300
    elif timechart_F != [] and timechart_F[0] != 0:
      Acc = Acc_Score/(timechart_F[0])/300

    for curr_notecount in timechart_C:
        #Circle
      if Object_list[curr_notecount]["Type"]=="C":
          Posx = Object_list[curr_notecount]["Posx"]
          Posy = Object_list[curr_notecount]["Posy"]
          #1.Fade in
          if(Curr_time-timechart[curr_notecount]-map_start<=Fade_end):
            approach_circle_size = 2*R*(4-3*(Curr_time-timechart[curr_notecount]-map_start)/Hit)
            Hit_circle.set_alpha(255*(Curr_time-timechart[curr_notecount]-map_start)/Fade_end)
            if(approach_circle_size>0):
              Approach_circle = pygame.Surface((approach_circle_size,approach_circle_size)).convert_alpha()
              pygame.transform.scale(Approach_circle_original,(approach_circle_size,approach_circle_size),dest_surface=Approach_circle)
              curr_Objects.append((Approach_circle,Utilities.center(Posx,Posy,approach_circle_size,approach_circle_size)))
            curr_Objects.append((Hit_circle,Utilities.center(Posx,Posy,2*R,2*R)))
            #2.Full opacity

          if(Curr_time-timechart[curr_notecount]-map_start>Fade_end and Curr_time-timechart[curr_notecount]-map_start)<(Hit+W50):
            approach_circle_size = 2*R*(4-3*(Curr_time-timechart[curr_notecount]-map_start)/Hit)
            Hit_circle.set_alpha(255)
            if(approach_circle_size>0):
              Approach_circle = pygame.Surface((approach_circle_size,approach_circle_size)).convert_alpha()
              pygame.transform.scale(Approach_circle_original,(approach_circle_size,approach_circle_size),dest_surface=Approach_circle)
              curr_Objects.append((Approach_circle,Utilities.center(Posx,Posy,approach_circle_size,approach_circle_size)))
            curr_Objects.append((Hit_circle,Utilities.center(Posx,Posy,2*R,2*R)))
      #Slider head
      if Object_list[curr_notecount]["Type"]=="S_head":
        Posx = Object_list[curr_notecount]["Posx"]
        Posy = Object_list[curr_notecount]["Posy"]
        approach_circle_size = 2*R*(4-3*(Curr_time-timechart[curr_notecount]-map_start)/Hit)
        if Curr_time-timechart[curr_notecount]-map_start<Hit+W50:
          if(approach_circle_size>0):
            Approach_circle = pygame.Surface((approach_circle_size,approach_circle_size)).convert_alpha()
            pygame.transform.scale(Approach_circle_original,(approach_circle_size,approach_circle_size),dest_surface=Approach_circle)
          curr_Objects.append((Hit_circle,Utilities.center(Posx,Posy,2*R,2*R)))
          curr_Objects.append((Approach_circle,Utilities.center(Posx,Posy,approach_circle_size,approach_circle_size)))

      #Slider body
      if Object_list[curr_notecount]["Type"]=="S_body":
        Posx = Object_list[curr_notecount]["Posx"]
        Posy = Object_list[curr_notecount]["Posy"]
        Span = Object_list[curr_notecount]["Span"]
        nodes = numpy.asfortranarray([Posx,Posy])
        main_curve = bezier.Curve(nodes, degree=len(Posx)-1)
        curr_Objects.append((Hit_circle,Utilities.center(Posx[-1],Posy[-1],2*R,2*R)))
        if 0<(Curr_time-timechart[curr_notecount]-Hit-map_start)/Span<1:
          SliderballX = main_curve.evaluate((Curr_time-(Hit+timechart[curr_notecount])-map_start)/Span).tolist()[0][0]
          SliderballY = main_curve.evaluate((Curr_time-(Hit+timechart[curr_notecount])-map_start)/Span).tolist()[1][0]
          curr_Objects.append((Slider_ball,Utilities.center(SliderballX,SliderballY,5*R,5*R)))
          curr_Objects.append((Hit_circle,Utilities.center(SliderballX,SliderballY,2*R,2*R)))
        for i in range(50):
          curr_Objects.append((Slider_body,Utilities.center(main_curve.evaluate(i/50).tolist()[0][0],main_curve.evaluate(i/50).tolist()[1][0],2*R,2*R)))

      #Spinner
      if Object_list[curr_notecount]["Type"]=="G":
        curr_Objects.append((Spinner,(290,110)))

    #Mouse cursor
    Mouse_pos = pygame.mouse.get_pos()
    curr_Objects.append((Cursor,Utilities.center(Mouse_pos[0],Mouse_pos[1],50,50)))

    #Score counter
    Score_text = Utilities.render_text(str(math.ceil(Score)),FONT,40,WHITE)
    curr_Objects.append((Score_text[0],(target.get_width()-Score_text[1]-30,30)))

    #Combo counter
    Combo_text = Utilities.render_text(str(Combo)+"x",FONT,80,WHITE)
    curr_Objects.append((Combo_text[0],(50,target.get_height()-Combo_text[2]-50)))

    #Acc counter
    Acc_text = Utilities.render_text(str(math.ceil(Acc*10000)/100)+"%",FONT,30,WHITE)
    curr_Objects.append((Acc_text[0],(target.get_width()-Acc_text[1]-50,30+Score_text[2])))

    if DEBUG_MODE:
      Timer_text = Utilities.render_text(str(Curr_time-map_start),FONT,30,WHITE)
      curr_Objects.append((Timer_text[0],(0,0)))
      FPS_text = Utilities.render_text(str(FPS),FONT,30,WHITE)
      curr_Objects.append((FPS_text[0],(0,30)))

    if Combo>max_combo:
      max_combo = Combo
    Utilities.render(target,curr_Objects)