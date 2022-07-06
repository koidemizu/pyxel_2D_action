# -*- coding: utf-8 -*-
import pyxel

def player_draw(player):
    x = player.p_x
    y = player.p_y      
    t = player.p_t * 32
    #Jump
    if player.p_j == True:          
        player.p_m2 += 1          
        if player.p_m_b == 2 or player.p_m_b == 0:
            pyxel.blt(x, y, 0, 8, 0 + t, 8, 8, 15)
            if player.p_m2 % 3 == 0:
                pyxel.blt(x - 6, y + 6, 0, 16, 0, 8, 8, 15)
            else:
                pyxel.blt(x - 6, y + 6, 0, 24, 0, 8, 8, 15)
        elif player.p_m_b == 4:
            pyxel.blt(x, y, 0, 8, 8 + t, 8, 8, 15)
            if player.p_m2 % 3 == 0:
                pyxel.blt(x + 6, y + 6, 0, 16, 8, 8, 8, 15)
            else:
                pyxel.blt(x + 6, y + 6, 0, 24, 8, 8, 8, 15)           
    else:
        #Move right    
        if player.p_m == 2:
            if player.p_c % 15 == 0:
                player.p_m2 += 1
            if player.p_m2 % 2 == 0:
                pyxel.blt(x, y, 0, 0, 16 + t, 8, 8, 15)
                if player.p_c > 0:
                    pyxel.blt(x - 6, y, 0, 16, 16, 8, 8, 15)
            else:
                pyxel.blt(x, y, 0, 8, 16 + t, 8, 8, 15)
                if player.p_c > 0:
                    pyxel.blt(x - 6, y, 0, 24, 16, 8, 8, 15)
        #Move left
        elif player.p_m == 4:
            if player.p_c % 15 == 0:
                player.p_m2 += 1
            if player.p_m2 % 2 == 0:
                pyxel.blt(x, y, 0, 0, 24 + t, 8, 8, 15)
                if player.p_c > 0:
                    pyxel.blt(x + 6, y, 0, 16, 24, 8, 8, 15)
            else:
                pyxel.blt(x, y, 0, 8, 24 + t, 8, 8, 15)
                if player.p_c > 0:
                    pyxel.blt(x + 6, y, 0, 24, 24, 8, 8, 15)              
        elif player.p_m == 0:
            pyxel.blt(x, y, 0, 0, 0 + t, 8, 8, 15)      