# -*- coding: utf-8 -*-
#2D-action_game

import pyxel
from module import collisionDetection as cD, playerDraw as pD

class APP:
  def __init__(self):
      pyxel.init(180, 128)
      
      pyxel.load('assets/assets.pyxres')
      #pyxel.load('assets/assets_dom.pyxres')
      #pyxel.load('assets/assets_mt.pyxres')
      
      pyxel.mouse(False)
      
      type = 0
      self.player = Player(type)
      self.bullets = []
      self.e_bullets = []
      self.enemy_list = [
                         (0, 1), (1, 1), (2, 1), (3, 1) ,
                         (0, 2), (1, 2), (2, 2), (3, 2) ,
                        ]      
      self.enemy_break = {
                         (0, 1):(0, 7),
                         (1, 1):(1, 7),
                         (2, 1):(2, 7),
                         (3, 1):(3, 7),
                         (0, 2):(0, 8),
                         (1, 2):(1, 8),
                         (2, 2):(2, 8),
                         (3, 2):(3, 8),
                         }
      self.enemy_pos = {}
      self.effect = []
      self.camera = [0, 0]
      self.game_flag = 0
      
      for m0 in range(160):
          for m1 in range(160):
              tile = pyxel.tilemap(0).pget(m1, m0)
              if tile in self.enemy_list:
                  self.enemy_pos[(m1, m0)] = [5, tile]
                    
      pyxel.run(self.update, self.draw)
     
  def update(self):                      
      #Game Continue
      if self.game_flag == 0:
          self.PlayerUpdate()
          self.EnemyUpdate()
      #Game Over
      elif self.game_flag == 99:
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
              if cD.check_move(self.player, 1, self.camera):
                  self.camera[1] -= 1
                  self.player.Jump()          
      #Fall Update
      else:          
          if cD.check_move(self.player, 3, self.camera):
              self.camera[1] += 1
              self.player.Dawn()              
              
      #Enemy Bullets
      for eb in self.e_bullets:
          eb.update()
          etx = eb.eb_x // 8
          ety = eb.eb_y // 8
          ptx = self.player.p_x + self.camera[0]
          pty = self.player.p_y + self.camera[1]
          e_tgt_tile = pyxel.tilemap(0).pget(etx, ety)
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
              if self.player.Damage(2) == False:
                  self.game_flag = 99
                  self.player.p_j = False
              if eb in self.e_bullets:
                  self.e_bullets.remove(eb)
            
      #Player Bullets
      for b in self.bullets:
          b.update()          
          tx = b.b_x // 8
          ty = b.b_y // 8
          tgt_tile = pyxel.tilemap(0).pget(tx, ty)
          if tgt_tile[1] > 5:
              pass
          elif tgt_tile in self.enemy_list:              
              self.enemy_pos[(tx, ty)][0] -= 1
              self.effect.append(Effect(b.b_x - 4, b.b_y, 0))
              if self.enemy_pos[(tx, ty)][0] < 1:
                  pyxel.tilemap(0).pset(tx, ty, self.enemy_break[tgt_tile])
                  self.effect.append(Effect(b.b_x - 4, b.b_y, 4))
              if b in self.bullets:
                  self.bullets.remove(b)
          else:              
              self.effect.append(Effect(b.b_x, b.b_y, 1))
              if b in self.bullets:
                  self.bullets.remove(b)
              
      #Effect
      for ef in self.effect:
          ef.update()
          if ef.ef_t < 0:
              self.effect.remove(ef)
              

  def draw(self):
      pyxel.cls(0)
      
      #Draw tilemap
      pyxel.bltm(0, 0, 0, self.camera[0], self.camera[1], 128, 128, 15)
      
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
      if self.game_flag == 0:          
          pD.player_draw(self.player)
      #Game Over
      elif self.game_flag == 99:
          x = self.player.p_x
          y = self.player.p_y  
          pyxel.blt(x, y, 0, 0, 32, 8, 8, 15)     
          
      #Info//////////////////////////////////////////////////////////
      pyxel.rectb(0, 0, 128, 128, 1)      
      pyxel.rect(128, 0, 53, 128, 0)
      pyxel.rectb(127, 0, 53, 128, 1)
      bp = 2

      pyxel.text(128, 0 + bp, "Armor", 9)
      pyxel.rectb(128, 7 + bp, 51, 10, 9)
      for hp in range(self.player.p_hp // 4):
          pyxel.rect(128 + hp * 2, 10 + bp, 1, 4, 9)
          
      pyxel.text(128, 22 + bp, "Energy", 9)
      pyxel.rectb(128, 29 + bp, 51, 10, 9)
      for fuel in range(self.player.p_f // 4):
          pyxel.rect(128 + fuel * 2, 32 + bp, 1, 4, 9)                   
          
      pyxel.text(128, 40 + bp, "coordinate", 9)
      pyxel.text(128, 48 + bp, "(" + str(int(self.player.p_x)) + "," + 
                 str(int(self.player.p_y)) + ")", 9)
      pyxel.text(128, 55 + bp, "Angle: " + str(self.player.p_angle * -1), 9)

     
  def PlayerUpdate(self):
      #Energy Recover
      if self.player.p_f < 101:
          self.player.p_f += 1
          
      #Player Attack
      if pyxel.btn(pyxel.KEY_V):
          if self.player.p_m == 1:
              m = self.player.p_m_b
          else:
              m = self.player.p_m
          if self.player.p_f > 2 and pyxel.frame_count % 3 == 0:
              self.player.p_f -= 2
              new_b = Bullet(self.player.p_x + 3 + self.camera[0],
                             self.player.p_y + 3 + self.camera[1],
                             m,
                             self.player.p_angle)
              self.bullets.append(new_b)
                  
              
      if pyxel.btnp(pyxel.KEY_UP):
          self.player.CngAngle(-1)
      elif pyxel.btnp(pyxel.KEY_DOWN):
          self.player.CngAngle(1)              
          
      #Jump
      if pyxel.btn(pyxel.KEY_SPACE):
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
      if pyxel.btn(pyxel.KEY_RIGHT):
          self.player.p_m = 2
          self.player.p_c += 1          
          if cD.check_move(self.player, 2, self.camera):
              if self.player.p_j == True:
                  self.player.p_x += 1
                  self.camera[0] += 1
              else:
                  self.player.p_x += 1
                  self.camera[0] += 1
      #Move LEFT       
      elif pyxel.btn(pyxel.KEY_LEFT):
          self.player.p_m = 4
          self.player.p_c += 1          
          if cD.check_move(self.player, 4, self.camera):
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
      for enemy in self.enemy_pos:
          if  self.enemy_pos[enemy][0] < 1:
              pass
          #Attack action
          elif pyxel.frame_count % (30 - self.enemy_pos[enemy][1][1] * 3) == 0:              
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
              if dist_x < 50 and dist_y < 50:
                  if enm_x > pre_x:
                      new_e_bullet = EnemyBullet(enm_x + 3,
                                                 enm_y + 3,
                                                 4, ang, spd)
                  else:
                      new_e_bullet = EnemyBullet(enm_x + 3,
                                                 enm_y + 3,
                                                 2, ang, spd)
                  self.e_bullets.append(new_e_bullet)
              
              
class Player:
    def __init__(self, type):
        self.p_hp = 100
        self.p_x = 8
        self.p_y = 8
        self.p_m = 2
        self.p_m_b = 0
        self.p_m2 = 0
        self.p_c = 0        
        self.p_j = False
        self.p_f = 100
        self.p_t = type
        self.p_angle = 0
        
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
    def __init__(self, x, y, v, a):
        self.b_x = x
        self.b_y = y         
        self.b_v = v   
        self.b_angle = a
        
    def update(self):
        if self.b_v == 2:
            self.b_x += 3
        elif self.b_v == 4:
            self.b_x -= 3
        self.b_y += self.b_angle
       
            
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

