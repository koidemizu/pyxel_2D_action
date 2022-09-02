# -*- coding: utf-8 -*-
import pyxel

def check_move(player, x, c, t):
    
    """
    Player coordinates
         
           2        pm1
  (x, y).--.----------.----
        |                 |
      7.|                 |.8
        |       P         |        
      5.|                 |.6
        |                 |
        ---.----------.----
           4          3
        
    """
      
    #Position Set
    px = int((player.p_x + c[0] + 2) // 8)
    py = int((player.p_y + c[1]) // 8)
      
    px2 = int((player.p_x + c[0] + 8) // 8)
    py2 = int((player.p_y + c[1] + 8) // 8)
      
    px3 = int((player.p_x + c[0] + 6) // 8)
    py3 = int((player.p_y + c[1] + 6) // 8)
      
    px4 = int((player.p_x + c[0]) // 8)
    py4 = int((player.p_y + c[1] + 2) // 8)
      
    pm1 = pyxel.tilemap(t).pget(px3, py)
    pm2 = pyxel.tilemap(t).pget(px, py)
    pm3 = pyxel.tilemap(t).pget(px3, py2)
    pm4 = pyxel.tilemap(t).pget(px, py2)
      
    pm5 = pyxel.tilemap(t).pget(px4, py3)
    pm6 = pyxel.tilemap(t).pget(px2, py3)
    pm7 = pyxel.tilemap(t).pget(px4, py4)
    pm8 = pyxel.tilemap(t).pget(px2, py4)
     
    #collision detection
    #Move UP
    if x == 1:
        if pm1[1] > 5 and pm2[1] > 5:
            return True

    #Move DOWN
    elif x == 3:
        if pm3[1] > 5 and pm4[1] > 5:
            return True
        else:
            return False
            
    #Move RIGHT
    elif x == 2:
        if pm6[1] > 5 and pm8[1] > 5:
            return True
    #Move LEFT
    elif x == 4:
        if pm5[1] > 5 and pm7[1] > 5:
            return True
    else:
        return False

