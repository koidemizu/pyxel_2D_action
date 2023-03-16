# -*- coding: utf-8 -*-
#2D-action_game

import pyxel
from module import collisionDetection as cD, playerDraw as pD, mapScan as mS

class APP:
  def __init__(self):
      pyxel.init(128, 128, fps = 30,)      
      self.StatusSet()                    
      pyxel.run(self.update, self.draw)
      
  def StatusSet(self):
      pyxel.load('assets/assets.pyxres')      
      pyxel.mouse(False)
      self.bullet_mode = 0
      self.manu_mode = 2
      self.course = 0
      self.easy_flag = 0
      self.camera_set_x = 32 * self.course
      self.time = 0
      self.final_map = 7
      self.max_f = 100
      self.max_a = 100
      self.atk = 1
      self.PlayerReset()
      self.enemy_list = [
                         (0, 1), (1, 1), (2, 1), (3, 1) ,
                         (4, 1), (5, 1), (6, 1), (7, 1) , (8, 1) ,
                         (0, 2), (1, 2), (2, 2), (3, 2) ,
                         (4, 2), (5, 2), (6, 2), (7, 2) , (8, 2) ,
                         (0, 3), (1, 3), (2, 3), (3, 3) ,
                         (4, 3), (5, 3), (6, 3), (7, 3) , (8, 3) ,
                         (0, 4), (1, 4), (2, 4), (3, 4) ,
                         (4, 4), (5, 4) ,(6, 4), (7, 4) ,
                        ]      
      self.enemy_break = {
                         (0, 1):(0, 7),
                         (1, 1):(1, 7),
                         (2, 1):(2, 7),
                         (3, 1):(3, 7),
                         (4, 1):(4, 7),
                         (5, 1):(4, 7),
                         (6, 1):(4, 7),
                         (7, 1):(4, 7),
                         (8, 1):(4, 7),
                         (0, 2):(0, 8),
                         (1, 2):(1, 8),
                         (2, 2):(2, 8),
                         (3, 2):(3, 8),
                         (4, 2):(4, 7),
                         (5, 2):(4, 7),
                         (6, 2):(4, 7),
                         (7, 2):(4, 7),                         
                         (8, 2):(4, 7),                         
                         (0, 3):(0, 9),
                         (1, 3):(1, 9),
                         (2, 3):(2, 9),
                         (3, 3):(3, 9),
                         (4, 3):(4, 7),
                         (5, 3):(4, 7),
                         (6, 3):(4, 7),
                         (7, 3):(4, 7),                         
                         (8, 3):(4, 7),
                         (0, 4):(4, 7),
                         (1, 4):(4, 7),
                         (2, 4):(4, 7),
                         (3, 4):(4, 7),
                         (4, 4):(4, 7),
                         (5, 4):(4, 7),
                         (6, 4):(4, 7),
                         (7, 4):(4, 7),
                         }
      self.EnemyReset()
      self.OtherReset()
      self.game_flag = -1      
      self.tile = 0 
      self.EnemyListCreste()
      self.title_col = 3
      self.sel_upg = 1      
      self.map_visible = False
      
  def PlayerReset(self):
      type = 0
      self.player = Player(type, self.max_a, self.max_f, self.atk)    
      
  def EnemyReset(self):
      self.enemy_pos = {}
      self.enemy_num = 0
      self.enemy_num_m = 0
      self.active_enemy = 0

  def OtherReset(self):
      self.effect = []
      self.camera = [self.camera_set_x * 8, 0]
      self.bullets = []
      self.e_bullets = []
      self.msg_y = -10            
      self.up_a = 0
      self.up_f = 0
      self.up_atk = 0
      self.game_end = 0
      self.sel_upg = 1
      self.map_visible = False
      
  def EnemyListCreste(self):
      self.enemy_pos = {}
      self.map_data = []
      self.map_data = mS.map_scan(self.tile, self.camera_set_x)   
      #Enemy list create
      for m0 in range(160):
          for m1 in range(160):              
              tile = pyxel.tilemap(self.tile).pget(m1 + self.camera_set_x, m0)              
              if tile in self.enemy_list:
                  if tile[1] == 4:
                      if tile[0] < 8:
                          hp = 5
                  else:
                      t0 = 1
                      #if tile[0] == 0:
                      #    t0 = 1
                      #else:
                      #    t0 = 1
                      hp_add = 0.1 * self.easy_flag
                      if tile[0] > 4:
                          hp = 10 * tile[1] * t0 * (1 + (self.tile * (0.5 + hp_add)))
                      else:
                          hp = 5 * tile[1] * t0 * (1 + (self.tile * (0.5 + hp_add)))
                  self.enemy_pos[(m1 + self.camera_set_x, m0)] = [hp, tile]    
      self.enemy_num = 0      
      for md in self.map_data:
          self.enemy_num += md.count(2)    
      print(self.enemy_num)  
      
  def PlayerA_UP(self, num):
      self.max_a += num
    
  def PlayerF_UP(self, num):
      self.max_f += num    

  def PlayerAtk_UP(self, num):
      self.atk += num
      
  def update(self):     
          
      #Title Screen
      if self.game_flag == -1:
          if (pyxel.btnp(pyxel.KEY_S) or 
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
             ):
              self.camera_set_x = 32 * self.course              
              self.OtherReset()
              self.tile = 0
              self.map_data = []
              self.map_data = mS.map_scan(self.tile, self.camera_set_x)              
              self.game_flag = 0
              self.EnemyListCreste()
              if self.bullet_mode == 0:
                  self.PlayerA_UP(10)
                  self.PlayerF_UP(10)
                  self.PlayerAtk_UP(1)

          if (pyxel.btnp(pyxel.KEY_UP) or 
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
              if self.manu_mode < 2:
                  self.manu_mode += 1
          elif (pyxel.btnp(pyxel.KEY_DOWN) or 
             pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
              if self.manu_mode > 0:
                  self.manu_mode -= 1                  

          if self.manu_mode == 0:
              if (pyxel.btnp(pyxel.KEY_RIGHT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):       
                 if self.easy_flag < 2:
                      self.easy_flag += 1
              elif (pyxel.btnp(pyxel.KEY_LEFT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                 if self.easy_flag > 0:
                      self.easy_flag -= 1
          elif self.manu_mode == 1:                        
              if (pyxel.btnp(pyxel.KEY_RIGHT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):          
                  if self.bullet_mode < 2:
                      self.bullet_mode += 1
              elif (pyxel.btnp(pyxel.KEY_LEFT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                  if self.bullet_mode > 0:
                      self.bullet_mode -= 1
          elif self.manu_mode == 2:                        
              if (pyxel.btnp(pyxel.KEY_RIGHT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):          
                  if self.course < 1:
                      self.course += 1
              elif (pyxel.btnp(pyxel.KEY_LEFT) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                  if self.course > 0:
                      self.course -= 1

              
      #Game Continue
      elif self.game_flag == 0:
          if self.msg_y < 150:
              if self.game_end == 10:
                  if self.msg_y < 50:
                      self.msg_y += 1
              else:
                  self.msg_y += 1          
          if self.game_end == 10:
              if self.tile == self.final_map:
                self.game_flag = 100
                self.msg_y = -10
              else:
                self.player.p_m2 = 0
                if self.msg_y > 49:
                    if (pyxel.btnp(pyxel.KEY_S) or 
                       pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                       pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or
                       pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                       pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
                       ):
                        if self.sel_upg == 1:
                            self.tile += 1
                            self.PlayerA_UP(self.up_a)
                            if self.easy_flag == 0:
                                self.PlayerA_UP(10)
                                self.PlayerF_UP(10)
                                self.PlayerAtk_UP(1)
                            self.PlayerReset()
                            self.EnemyReset()
                            self.OtherReset()
                            self.EnemyListCreste()
                        elif self.sel_upg == 2:
                            self.tile += 1
                            self.PlayerF_UP(self.up_f)
                            if self.easy_flag == 0:
                                self.PlayerA_UP(10)
                                self.PlayerF_UP(10)
                                self.PlayerAtk_UP(1)                            
                            self.PlayerReset()
                            self.EnemyReset()
                            self.OtherReset()
                            self.EnemyListCreste()
                        elif self.sel_upg == 3:
                            self.tile += 1
                            self.PlayerAtk_UP(self.up_atk)
                            if self.easy_flag == 0:
                                self.PlayerA_UP(10)
                                self.PlayerF_UP(10)
                                self.PlayerAtk_UP(1)
                            self.PlayerReset()
                            self.EnemyReset()
                            self.OtherReset()
                            self.EnemyListCreste()
              
                if (pyxel.btnp(pyxel.KEY_UP) or 
                   pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                    if self.sel_upg > 1:
                        self.sel_upg -= 1              
                elif (pyxel.btnp(pyxel.KEY_DOWN) or 
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                    if self.sel_upg < 3:
                        self.sel_upg += 1
          else:              
              self.time += 1
              self.PlayerUpdate()
              self.EnemyUpdate()
          if pyxel.btnp(pyxel.KEY_4):                            
              self.game_end = 10
              self.msg_y = 0
              self.up_a = pyxel.rndi(10, 20)
              self.up_f = pyxel.rndi(10, 20)
              self.up_atk = pyxel.rndi(1, 5) 
     #     if pyxel.btnp(pyxel.KEY_5):
     #         self.game_flag = 99
      
      #Game Over
      elif self.game_flag == 99 or self.game_flag == 100:
          if (pyxel.btnp(pyxel.KEY_S) or 
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                 pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
                 ):
              self.StatusSet()          
        
          if self.game_flag == 99:
            if len(self.effect) > 0:
                pass
            else:
                self.effect.append(Effect(self.player.p_x + self.camera[0] - 2, 
                                      self.player.p_y + self.camera[1] - 3, 2))                 

      #Jump Update
      if self.player.p_j == True:          
          self.player.p_f -= 2                
          
          if self.player.p_f < 1:
              self.player.p_j = False
          else:    
              if cD.check_move(self.player, 1, self.camera, self.tile):
                  self.camera[1] -= 1
                  self.player.Jump()          
      #Fall Update
      else:          
          if cD.check_move(self.player, 3, self.camera, self.tile):
              self.camera[1] += 1
              self.player.Dawn()              
              
      #Enemy Bullets
      for eb in self.e_bullets:
          eb.update()
          etx = eb.eb_x // 8
          ety = eb.eb_y // 8
          ptx = self.player.p_x + self.camera[0]
          pty = self.player.p_y + self.camera[1]
          e_tgt_tile = pyxel.tilemap(self.tile).pget(etx, ety)
          if e_tgt_tile in self.enemy_list:
              pass
          elif e_tgt_tile[1] > 5:
              pass
          else:              
              self.effect.append(Effect(eb.eb_x, eb.eb_y, 1))
              if eb in self.e_bullets:
                  self.e_bullets.remove(eb)
              
          if (eb.eb_x > ptx and eb.eb_x < ptx + 7 and
                eb.eb_y > pty and eb.eb_y < pty + 7):              
              self.effect.append(Effect(eb.eb_x - 4, eb.eb_y - 2, 0))
              dmg_add = self.tile * (0.5 + (self.easy_flag * 0.1))
              if self.player.Damage(int(2 + (1 + dmg_add))) == False:
                  self.game_flag = 99
                  self.player.p_j = False
              if eb in self.e_bullets:
                  self.e_bullets.remove(eb)
            
      #Player Bullets
      for b in self.bullets:
          b.update()          
          tx = b.b_x // 8
          ty = b.b_y // 8
          tgt_tile = pyxel.tilemap(self.tile).pget(tx, ty)
          if tgt_tile[1] > 5:
              pass
          elif tgt_tile in self.enemy_list:
              self.enemy_pos[(tx, ty)][0] -= self.player.p_atk
              self.effect.append(Effect(b.b_x - 4, b.b_y, 0))
              if self.enemy_pos[(tx, ty)][0] < 1:

                  #Enemy Delete action
                  if self.enemy_pos[(tx, ty)][1] == (1, 4):
                    print("OOO")
                    for des1 in range(10):
                        angx = pyxel.rndi(0, 3)
                        angy = pyxel.rndi(0, 3)
                        new_e_bullet = EnemyBullet(b.b_x + angx,
                                                     b.b_y + angy,
                                                     2, -2 + des1, 1)
                        self.e_bullets.append(new_e_bullet)
                    for des2 in range(10):
                        angx = pyxel.rndi(0, 3)
                        angy = pyxel.rndi(0, 3)
                        new_e_bullet = EnemyBullet(b.b_x + angx,
                                                     b.b_y + angy,
                                                     4, -2 + des2, 1)
                        self.e_bullets.append(new_e_bullet)       


                  pyxel.tilemap(self.tile).pset(tx, ty, 
                                                self.enemy_break[tgt_tile])
                  self.effect.append(Effect(b.b_x - 4, b.b_y, 4))
                  self.enemy_num -= 1
                  #if (self.enemy_num == 10 or self.enemy_num == 5 
                  #   or self.enemy_num == 1):
                  #    self.msg_y = -10
                  #    self.enemy_num_m = self.enemy_num
                  if self.enemy_num <= 0:
                      self.game_end = 10
                      self.msg_y = -10     
                      self.sel_upg = 1
                      self.up_a = pyxel.rndi(10, 30)
                      self.up_f = pyxel.rndi(10, 30)
                      self.up_atk = pyxel.rndi(1, 5)                      
              if b in self.bullets:
                  if (tx, ty) == b.last_pos:
                      pass
                  else:
                      b.last_pos_set((tx, ty))       
                      self.effect.append(Effect(b.b_x, b.b_y, 1))
                      b.hp -= 1
                      if b.hp < 1:
                          self.bullets.remove(b)
                  
          else:                                                               
              if b in self.bullets:
                  if (tx, ty) == b.last_pos:
                      pass
                  else:
                      b.last_pos_set((tx, ty))       
                      self.effect.append(Effect(b.b_x, b.b_y, 1))
                      b.hp -= 1
                      if b.hp < 1:
                          self.bullets.remove(b)
              
      #Effect
      for ef in self.effect:
          ef.update()
          if ef.ef_t < 0:
              self.effect.remove(ef)
              
  def draw(self):      
      if self.game_flag == -1:
          self.draw_title()
      else:          
          self.draw_game_main()
          if self.game_flag == 99:
              self.draw_game_over()  
          elif self.game_flag == 100:
              self.draw_game_clear()  
      pyxel.text(79, 2, "TIME:" + str(self.time//30), 0)
      pyxel.text(80, 3, "TIME:" + str(self.time//30), 10)

  def draw_title(self):
      pyxel.cls(0)
      pyxel.rectb(0, 0, 128, 128, 1)  
      pyxel.text(2, 3, "Target_Shooting", 9)      
      if pyxel.frame_count % 60 == 0:
          if self.title_col == 3:
              self.title_col = 11
          else:
              self.title_col = 3     
      pyxel.text(2, 10, "Press S or Any GamePad Button", self.title_col)      
      #pyxel.text(2, 20, "MAP: " + str(self.tile + 1), 9)

      pyxel.text(2, 25, "Change game options", 9)
      pyxel.text(2, 35, "Up/Down key: Select item", 3)
      pyxel.text(2, 45, "Left/Right key: Change option", 3)


      if self.manu_mode == 0:
          pyxel.blt(15, 108, 0, 0, 40, 8, 9, 15)
      elif self.manu_mode == 1:
          pyxel.blt(15, 85, 0, 0, 40, 8, 9, 15)
      elif self.manu_mode == 2:
          pyxel.blt(15, 62, 0, 0, 40, 8, 9, 15)

      pyxel.text(25, 55, "--Course--", 10)
      if self.course == 0:
          pyxel.text(28, 65, "Course:A", 10)
      elif self.course == 1:
          pyxel.text(28, 65, "Course:B", 10)
      elif self.course == 2:
          pyxel.text(28, 65, "Course:C", 10)

      pyxel.text(25, 78, "--Bullet type--", 10)
      if self.bullet_mode == 0:
          pyxel.text(28, 88, "Normal bullet", 10)
      elif self.bullet_mode == 1:
          pyxel.text(28, 88, "Piercing bullet", 10)
      elif self.bullet_mode == 2:
          pyxel.text(28, 88, "3Way bullet", 10)

      pyxel.text(25, 101, "--Difficulty--", 10)
      if self.easy_flag == 0:
          pyxel.text(28, 111, "Easy mode", 10)
      elif self.easy_flag == 1:
          pyxel.text(28, 111, "Normal mode", 10)
      elif self.easy_flag == 2:
          pyxel.text(28, 111, "Hard mode", 10)                     

  def draw_map(self):
      map_draw_x = 5
      map_draw_y = 30
      pyxel.rect(map_draw_x-1, map_draw_y-1, 91, 91, 0)
      pyxel.rectb(map_draw_x-1, map_draw_y-1, 91, 91, 9)      
      for md in range(len(self.map_data)):
          for md2 in range(len(self.map_data[md])):
              if self.map_data[md][md2] == 1:
                  pyxel.rect(map_draw_x+md2 * 3, map_draw_y+md * 3, 2, 2, 5)
              elif self.map_data[md][md2] == 2:
                  pyxel.rect(map_draw_x+md2 * 3, map_draw_y+md * 3, 2, 2, 8)
              if md2 == self.player.p_x // 4 and md == self.player.p_y // 4:                  
                  pyxel.text(map_draw_x + md2 * 3 - 3, map_draw_y + md * 3 - 5, "P", 9) 

  def draw_game_over(self):
      gsx = 45
      gsy = 50
      pyxel.rect(0, gsy - 3, 128, 30, 0)
      pyxel.rectb(0, gsy - 3, 128, 30, 7)

      pyxel.text(gsx - 1, gsy + 1, "GAME OVER!!", 1)      
      pyxel.text(gsx, gsy, "GAME OVER!!", 8)      
      
      pyxel.text(4, gsy + 10, "Press S or Any GamePad Button", 9)                          

  def draw_game_clear(self):
      gsx = 35
      gsy = 50
      pyxel.rect(0, gsy - 3, 128, 35, 0)
      pyxel.rectb(0, gsy - 3, 128, 35, 7)
      
      if self.easy_flag == 0:
          mstr = "EASY MODE"
          mcol = 10
      elif self.easy_flag == 1:
          mstr = "NOMAL MODE"
          mcol = 9
      elif self.easy_flag == 2:
          mstr = "HARD MODE"
          mcol = 8

      pyxel.text(gsx - 22, gsy, mstr + " ALL MAP CLEAR!!", mcol)      
      pyxel.text(4, gsy + 10, "Thank you for playing", 6)                  
      pyxel.text(4, gsy + 20, "Press S or Any GamePad Button", 6)         

  def draw_game_main(self):
      pyxel.cls(0)            
      
      #Draw tilemap
      pyxel.bltm(0, 0, self.tile, self.camera[0], self.camera[1], 128, 128, 15)
      
      #Bullets draw////////////////////////////////////////////////////////
      for b in self.bullets:
          pyxel.rect(b.b_x - self.camera[0],
                     b.b_y - self.camera[1],
                     1, 1, 10)
          
      #Enemy Bullets draw//////////////////////////////////////////////////
      for eb in self.e_bullets:
          pyxel.rect(eb.eb_x - self.camera[0],
                     eb.eb_y - self.camera[1],
                     2, 1, 8)
          
      #Effect draw////////////////////////////////////////////////////////
      for ef in self.effect:
          pyxel.blt(ef.ef_x - self.camera[0],
                    ef.ef_y - self.camera[1],
                    1, 0 + ef.ef_v * 8, 0 + ef.ef_v2 * 8, 8, 8, 15)
      
      #Player draw////////////////////////////////////////////////////
      #Game Continue
      if self.game_flag == 0 or self.game_flag == 100:          
          pD.player_draw(self.player, self.max_a, self.max_f)
      #Game Over
      elif self.game_flag == 99:
          x = self.player.p_x
          y = self.player.p_y  
          pyxel.blt(x, y, 0, 0, 32, 8, 8, 15)     
          
      pyxel.rectb(0, 0, 128, 128, 1)      
      
      #Messages///////////////////////////////////////////////////////////      
      if self.game_end == 10 and self.game_flag < 100:
        pyxel.rect(1, self.msg_y - 3, 126, 80, 0)
        pyxel.rectb(1, self.msg_y - 3, 126, 80, 7)
        pyxel.text(45, self.msg_y,"Map clear!",1)
        pyxel.text(46, self.msg_y,"Map clear!",10)      
        if self.msg_y > 49:
            pyxel.text(4, 60,"Select upgrade",7)
            pyxel.text(4, 70,"and go to the next map.",7)
            pyxel.text(4, 80, "Up and Down keys: Select", 6)
            pyxel.text(24, 90,"1: Armor + " + str(self.up_a),7)
            pyxel.text(24, 100,"2: Fuel + " + str(self.up_f),7)
            pyxel.text(24, 110,"3: Attack Power + " + str(self.up_atk),7)
            pyxel.text(4, 119, "Press S or Any GamePad Button", 6)     
            pyxel.blt(15, 90+((self.sel_upg-1) * 10) - 1, 1, 16, 0, 8, 8, 15)
    #  elif (self.enemy_num_m == 10 or self.enemy_num_m == 5 
    #     or self.enemy_num_m == 1):        
    #      pyxel.text(29, self.msg_y,"Remaining targets: " + 
    #                 str(self.active_enemy),1)
    #      pyxel.text(30, self.msg_y,"Remaining targets: " + 
    #                 str(self.active_enemy),10)
      else:
        if self.game_flag == 100:
            pass
        else:
            pyxel.text(29, self.msg_y, "MAP:" + str(self.tile + 1), 1)
            pyxel.text(30, self.msg_y, "MAP:" + str(self.tile + 1), 10)          
            pyxel.text(29, self.msg_y + 9, "Destroy all targets.", 1)
            pyxel.text(30, self.msg_y + 9, "Destroy all targets.", 10)          
      
      
      if self.map_visible == True:
        self.draw_map()
      if self.tile == self.final_map:
          pyxel.text(2, 2, "MAP:FINAL", 0)
          pyxel.text(3, 3, "MAP:FINAL", 10)
      else:
          pyxel.text(2, 2, "MAP:" + str(self.tile + 1), 0)
          pyxel.text(3, 3, "MAP:" + str(self.tile + 1), 10)
      #Debug//////////////////////////////////////////////////////////
      #pyxel.rect(4, 4, 20, 30, 0)
      #pyxel.text(5, 5, "hp" + str(self.player.p_hp), 7)      
      #pyxel.text(5, 15, "fl" + str(self.player.p_f), 7)      
      #pyxel.text(5, 25, "atk" + str(self.player.p_atk), 7)           

     
  def PlayerUpdate(self):
      self.player.p_af = False
      
      #Energy Recover
      if self.player.p_f < self.max_f + 1:
          self.player.p_f += self.max_f // 100
          
      #Player Attack
      if pyxel.btn(pyxel.KEY_V) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
          if self.player.p_m == 1:
              m = self.player.p_m_b
          else:
              m = self.player.p_m
          if self.player.p_f > 2 and pyxel.frame_count % 3 == 0:
              if self.bullet_mode == 0:
                  b_hp = 1
                  b_uf = 2
              elif self.bullet_mode == 1:
                  b_hp = 2
                  b_uf = 6
              elif self.bullet_mode == 2:
                  b_hp = 1
                  b_uf = 8

              self.player.p_f -= b_uf              
              if self.bullet_mode == 2:
                  for nb in range(3):
                      new_b = Bullet(self.player.p_x + 3 + self.camera[0],
                             (self.player.p_y + (2 * nb)) + self.camera[1],
                             m,
                             self.player.p_angle, b_hp)
                      self.bullets.append(new_b)

              else:
                  new_b = Bullet(self.player.p_x + 3 + self.camera[0],
                             self.player.p_y + 3 + self.camera[1],
                             m,
                             self.player.p_angle, b_hp)
                  self.bullets.append(new_b)
                
      #Mini Map
      if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        x = pyxel.mouse_x 
        y = pyxel.mouse_y
        if x < 128 and x > 0 and y < 128 and y > 0:
            if self.map_visible == True:
                self.map_visible = False
            else:
                self.map_visible = True
                
      if (pyxel.btnp(pyxel.KEY_UP) or 
          pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)):
          self.player.CngAngle(-1)
          self.player.p_af = True

      elif (pyxel.btnp(pyxel.KEY_DOWN) or 
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)):
          self.player.CngAngle(1)   
          self.player.p_af = True           
          
      #Jump
      if (pyxel.btn(pyxel.KEY_SPACE) or 
         pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
         if self.player.p_j == False and self.player.p_f > 10:
              if self.player.p_m == 1:
                  pass
              else:
                  self.player.p_m_b = self.player.p_m
              self.player.p_m = 1              
              self.player.p_c += 1
              self.player.p_j = True
      else:
          self.player.p_j = False
          
      #Move RIGHT
      if (pyxel.btn(pyxel.KEY_RIGHT) or 
         pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
          self.player.p_m = 2
          self.player.p_c += 1          
          if cD.check_move(self.player, 2, self.camera, self.tile):
              if self.player.p_j == True:
                  self.player.p_x += 1
                  self.camera[0] += 1
              else:
                  self.player.p_x += 1
                  self.camera[0] += 1
      #Move LEFT       
      elif (pyxel.btn(pyxel.KEY_LEFT) or 
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
          self.player.p_m = 4
          self.player.p_c += 1          
          if cD.check_move(self.player, 4, self.camera, self.tile):
              if self.player.p_j == True:
                  self.player.p_x -= 1
                  self.camera[0] -= 1
              else:
                  self.player.p_x -= 1
                  self.camera[0] -= 1

      else:
          if self.player.p_j == False:
              if self.player.p_m == 1:
                  self.player.p_m = self.player.p_m_b
              self.player.p_c = 0
              self.player.p_m2 = 0          

  def EnemyUpdate(self):
      #Enemy
      self.active_enemy = 0
      for enemy in self.enemy_pos:                
          ecn = pyxel.rndi(1, 6)
          
          if self.enemy_pos[enemy][1][1] < 4:              
              if self.enemy_pos[enemy][0] >= 1:
                  self.active_enemy += 1
              
          if  self.enemy_pos[enemy][0] < 1:
              pass
          #Attack action          
          elif pyxel.frame_count % (50 - self.enemy_pos[enemy][1][1] * ecn) == 0:              
              enm_x = enemy[0] * 8
              enm_y = enemy[1] * 8
              pre_x = self.player.p_x + self.camera[0]
              pre_y = self.player.p_y + self.camera[1]
              dist_x = abs(enm_x - pre_x)
              dist_y = abs(enm_y - pre_y)
              ang = 0
              spd = 3
              #spd = pyxel.rndi(2, 3)
              if dist_y > 16:
                  ang = pre_y - enm_y
                  if ang > 0:
                      ang = 2
                  elif ang < 0:
                      ang = -2                  
              elif dist_y > 24:
                  ang = pre_y - enm_y
                  if ang > 0:
                      ang = 3
                  elif ang < 0:
                      ang = -3 
                            
              if  self.enemy_pos[enemy][1][0] < 5:
                  vx = 50 + self.tile * self.enemy_pos[enemy][1][0]
                  vy = 50 + self.tile * self.enemy_pos[enemy][1][0]
              elif self.enemy_pos[enemy][1][0] in [5, 6, 7, 8]:                  
                  vx = 150
                  vy = 150
              
              if dist_x < vx and dist_y < vy:
                  if self.enemy_pos[enemy][1][1] == 4:
                        pass
                  else:
                      if  self.enemy_pos[enemy][1][0] < 5:
                          if enm_x > pre_x:
                              v = 4
                              new_e_bullet = EnemyBullet(enm_x + 3,
                                                     enm_y + 3,
                                                     v, ang, spd)
                          else:
                              v = 2
                              new_e_bullet = EnemyBullet(enm_x + 3,
                                                     enm_y + 3,
                                                     v, ang, spd)
                          self.e_bullets.append(new_e_bullet)
                          atk_chk = pyxel.rndi(0, 5)
                          if self.tile > 3 and atk_chk < 1:
                             new_e_bullet = EnemyBullet(enm_x + 3,
                                                     enm_y + 3,
                                                     v, ang, 1)
                             self.e_bullets.append(new_e_bullet)

                      elif self.enemy_pos[enemy][1][0] in [5, 6, 7, 8]:
                          ang_x = pyxel.rndi(1, 3)                          
                          ang_y = pyxel.rndi(1, 3)                          
                          if enm_x > pre_x:
                              new_e_bullet = EnemyBullet(enm_x + ang_x,
                                                     enm_y + ang_y,
                                                     4, ang, spd)
                          else:
                              new_e_bullet = EnemyBullet(enm_x + ang_x,
                                                     enm_y + ang_y,
                                                     2, ang, spd)
                          self.e_bullets.append(new_e_bullet)
                      
                          se = pyxel.rndi(1, 5)
                          senum = pyxel.rndi(4, 8)
                          if se < 2:
                              for sei in range(senum):
                                  if sei % 2 == 0:
                                      i_v = 2
                                  else:
                                      i_v = 4
                                  
                                  a_i = pyxel.rndi(-4, 4)
                                  new_e_bullet = EnemyBullet(enm_x + ang_x,
                                                         enm_y + ang_y,
                                                         i_v, a_i, spd)
                                  self.e_bullets.append(new_e_bullet) 
      
      if  self.active_enemy < 1:
          for ene_del in self.enemy_pos:
              self.enemy_pos[ene_del][0] = 0
          self.enemy_num = 0
          self.game_end = 10
          self.msg_y = -10     
          self.sel_upg = 1
          self.up_a = pyxel.rndi(10, 20)
          self.up_f = pyxel.rndi(10, 20)
          self.up_atk = pyxel.rndi(1, 5)                    
              
class Player:
    def __init__(self, type, ma, mf, atk):
        self.p_hp = ma
        self.p_x = 8
        self.p_y = 8
        self.p_m = 2
        self.p_m_b = 0
        self.p_m2 = 0
        self.p_c = 0        
        self.p_j = False
        self.p_f = mf
        self.p_t = type
        self.p_angle = 0
        self.p_af = False
        self.p_atk = atk
        
    def Jump(self):
        self.p_y -= 1
            
    def Dawn(self):     
        self.p_y += 1
                
    def CngAngle(self, a):
        if self.p_angle > 4 and a > 0:
            pass
        elif self.p_angle < -4 and a < 0:
            pass
        else:
            self.p_angle += a
            
    def Damage(self, n):
        self.p_hp -= n
        if self.p_hp > 0:
            return True
        else:
            return False
        
class Bullet:
    def __init__(self, x, y, v, a, hp):
        self.b_x = x
        self.b_y = y         
        self.b_v = v   
        self.b_angle = a
        self.hp = hp
        self.last_pos = (0, 0)
        
    def update(self):
        if self.b_v == 2:
            self.b_x += 3
        elif self.b_v == 4:
            self.b_x -= 3
        self.b_y += self.b_angle

    def last_pos_set(self, pos):
        self.last_pos = pos
       
            
class EnemyBullet:
    def __init__(self, x, y, v, a, s):
        self.eb_x = x
        self.eb_y = y         
        self.eb_v = v         
        self.eb_angle = a
        self.eb_speed = s
        
    def update(self):
        if self.eb_v == 2:
            self.eb_x += self.eb_speed
        elif self.eb_v == 4:
            self.eb_x -= self.eb_speed 
        self.eb_y += self.eb_angle            
     
class Effect:
    def __init__(self, x, y, v2):
        self.ef_x = x
        self.ef_y = y
        self.ef_t = 10
        self.ef_v = 0
        self.ef_v2 = v2
        
    def update(self):
        self.ef_t -= 1
        if self.ef_t < 5:
            self.ef_v = 1
APP()

