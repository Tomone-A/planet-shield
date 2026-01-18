import pyxel
import math

#降ってくる隕石のクラス
class Enemy:
  speed = 4
  def __init__(self):
    self.restart()
  
  def move(self):
    self.x += self.vx * Enemy.speed
    self.y += self.vy * Enemy.speed

    #壁に当たると跳ね返る処理
    if self.x < 0 or self.x >= 200:
      self.vx = -self.vx
    if self.y < 0 or self.y >= 200:
      self.vy = -self.vy

  def restart(self):
    #座標と角度は完全ランダム
    self.x = pyxel.rndi(0, 199)
    self.y = pyxel.rndi(0, 199)
    self.angle = pyxel.rndi(30, 150)
    self.vx = pyxel.cos(self.angle)
    self.vy = pyxel.sin(self.angle)

#回転するバリアのクラス
class Shield:
  radius = 20 #バリアの半径
  x = 100
  y = 100

  def __init__(self):
    self.move()

  def move(self):
    mx, my = pyxel.mouse_x, pyxel.mouse_y
    self.angle = math.atan2(my - Shield.y, mx - Shield.x)
    #上は中心からマウス位置に引いた直線の角度
    self.sx = Shield.x + 15 * math.cos(self.angle)
    self.sy = Shield.y + 15 * math.sin(self.angle)
    #バリアとなる円の中心の座標は(100, 100)を中心とする半径15の円の円周上を動く

  def catch(self, enemy):
    #バリア円に触れる判定
    if self.sx - 15 <= enemy.x <= self.sx + 15 and self.sy - 15 <= enemy.y <= self.sy + 15:
      return True

  def player_damage(self, enemy):
    #中心の円に当たる判定
    if 80 <= enemy.x < 120 and 80 <= enemy.y <= 120:
      return True


class App:
  def __init__(self):
    pyxel.init(200, 200)
    pyxel.mouse(True)
    pyxel.load("my_resource.pyxres")
    pyxel.playm(1, loop = True)
 
    pyxel.sound(0).set(notes='C4D4C4', tones='SSS', volumes='22', effects='NN', speed=8) #得点
    pyxel.sound(3).set(notes='A3A1', tones='SN', volumes='22', effects='SN', speed=10) #ダメージと爆発

    self.enemies = [Enemy()] #隕石
    self.shield = Shield() #バリア
    self.hp_color = 11 #残りHPによって惑星の色を変える。最初は緑

    self.score = 0 #守った回数
    self.missed = 0 #ダメージを受けた回数

    pyxel.run(self.update, self.draw)
  
  def update(self):
    if self.missed < 10:
      self.shield.move()
      for enemy in self.enemies:
        enemy.move()
        #バリアで守った時の処理
        if self.shield.catch(enemy):
          pyxel.play(0, 0, loop = False)
          self.score += 1
          enemy.restart()

          #10点ごとに敵が増える
          if self.score > 0 and self.score % 10 == 0:
            self.enemies.append(Enemy())
        
        if pyxel.btnp(pyxel.KEY_SPACE):
          #緊急回避：scoreを減らし敵を消滅させる
          pyxel.play(3, 3, loop = False)
          self.score -= 1
          enemy.restart()
        
        #被ダメージ処理
        if self.shield.player_damage(enemy):
          pyxel.play(3, 3, loop = False)
          self.missed += 1
          enemy.restart()
        
        #惑星の色を黄色、赤と変える処理
        if self.missed >= 4:
          self.hp_color = 10
          if self.missed >= 7:
            self.hp_color = 8
    else:
      pyxel.stop()
  
  def draw(self):
    if self.missed < 10:
      pyxel.cls(0)
      pyxel.blt(0, 0, 0, 0, 0, 200, 200, 0) #背景画像

      #？ボタンの表示
      pyxel.rect(175, 15, 15, 15, 7)
      pyxel.text(180, 20, '?', 0) 

      #バリアとなる円
      pyxel.circ(self.shield.sx, self.shield.sy, 15, 12)

      #惑星（HP減少とともに色が変わり、黒い穴が開いていく）
      pyxel.circ(Shield.x, Shield.y, Shield.radius, self.hp_color)
      pyxel.circ(Shield.x, Shield.y, 2 * self.missed, 0)

      #隕石と緊急回避による爆発の描画
      for enemy in self.enemies:
        pyxel.circ(enemy.x, enemy.y, 2, pyxel.rndi(8,10))
        if pyxel.btnp(pyxel.KEY_SPACE):
          pyxel.circ(enemy.x, enemy.y, 10, 7)  
      
      #スコアの表示
      pyxel.text(10, 10, 'score: ' + str(self.score), 7) 
      
      #操作説明の表示処理
      if 175 <= pyxel.mouse_x <= 190 and 15 <= pyxel.mouse_y <= 30:
        pyxel.text(90, 15, 'operate with mouse', 13) 
        pyxel.text(10, 20, 'your score', 13)
        pyxel.text(90, 175, '[SPACE] = enemy explode', 13) 
        pyxel.text(90, 185, 'but your point is decrease', 13) 
      
    #10回ミスでゲームオーバー
    else:
      pyxel.cls(0)
      pyxel.text(80, 80, 'game over', 7)
      pyxel.text(75, 90, 'score:', 7)
      pyxel.text(110, 90, str(self.score), 7)
      return

App()