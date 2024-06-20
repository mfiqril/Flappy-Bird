from ursina import *       
import random

app = Ursina()

# Load textures for score display
num0 = load_texture("0.png")
num1 = load_texture("1.png")
num2 = load_texture("2.png")
num3 = load_texture("3.png")
num4 = load_texture("4.png")
num5 = load_texture("5.png")
num6 = load_texture("6.png")
num7 = load_texture("7.png")
num8 = load_texture("8.png")
num9 = load_texture("9.png")
nums = [num0, num1, num2, num3, num4, num5, num6, num7, num8, num9]

# Set fullscreen
window.fullscreen = True

# Flappy Bird object
class Flappy(Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            scale=(0.5, 0.4, 0.001),
            texture=load_texture("bird1.png"),
            collider="box",
            z=-1
        )

    def update(self):
        self.y -= 2 * time.dt
        if held_keys["space"]:
            self.texture = load_texture("bird2.png")
        else:
            self.texture = load_texture("bird3.png")
        if self.y <= -2.6:  # Translasi ke atas
            self.y = 1

    def input(self, key):
        if key == "space":
            self.y += 0.7
            Audio('wing.ogg', volume=2)

# Objek tanah
class Tanah(Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            scale=(25, 8.5, -1),
            texture=load_texture("ground")
        )

    # Translasi
    def update(self):
        self.x -= 0.5 * time.dt
        if self.x <= -2.5:
            self.x = 5.18

# Latar kota
class Kota(Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            y=-3.5,
            scale=(26, 1.6, 0.001),
            texture=load_texture("base"),
            z=-2
        )

    # Translasi
    def update(self):
        self.x -= 2.5 * time.dt
        if self.x <= -5:
            self.x = 5.8

# Objek atap
class Atap(Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            y=4.3,
            scale=(26, 1.6, 0.001),
            texture=load_texture("base"),
            z=-2,
            rotation=(180, 0, 0)
        )

    # Translasi
    def update(self):
        self.x -= 2.5 * time.dt
        if self.x <= 5:
            self.x = -5.8

# Objek pilar
class Tup(Entity):
    def __init__(self, rotation=(0, 0, 0), x=7, y=-2):
        super().__init__(
            model="cube",
            y=y,
            x=x,
            scale=(0.8, 5.1, 0.001),
            texture=load_texture("pillar"),
            collider="box",
            rotation=rotation,
            z=-1
        )
        self.scored = False

    def update(self):
        self.x -= 2 * time.dt
        if self.x <= -10:
            self.x += 36
            self.y = random.uniform(-4.5, -1.5)
            self.scored = False
            if self.rotation == (0, 0, 180):
                self.y += 6.7
        if self.x < kus.x and not self.scored and self.rotation == (0, 0, 0):  # Pastikan hanya pilar bawah yang menghitung skor
            self.scored = True
            update_score()

# Objek Score
class Puan(Entity):
    def __init__(self, texture=num0, x=0.2, z=-0.1):
        super().__init__(
            model="cube",
            texture=texture,
            scale=(0.4, 0.5, 0.01),
            z=z,
            x=x,
            y=3
        )

score = 0
score_display = []

# Update skor
def update_score():
    global score, score_display
    score += 1

    for digit in score_display:
        destroy(digit)

    score_display = []
    score_str = str(score)
    for i, char in enumerate(score_str):
        digit = int(char)
        score_display.append(Puan(texture=nums[digit], x=-0.2 + i * 0.3))

# Reset game
def reset_game():
    global score, score_display
    score = 0
    for digit in score_display:
        destroy(digit)
    score_display = []
    kus.position = (0, 0)
    kus.rotation = (0, 0, 0)
    kus.texture = load_texture("bird1.png")
    for tup in tups:
        destroy(tup)
    tups.clear()
    setup_tups()
    game_over_entity.disable()
    restart_button.disable()
    application.resume()

# Looping objek pilar
tups = []
def setup_tups():
    for i in range(18):
        x = 7 + i * 3.5
        y_bottom = random.uniform(-4.5, -1.5)
        y_top = y_bottom + 6.7
        tups.append(Tup(x=x, y=y_bottom))
        tups.append(Tup(rotation=(0, 0, 180), x=x, y=y_top))

kus = Flappy()
tanah = Tanah()
kota = Kota()
atap = Atap()

# Audio menabrak
def update():
    kushit = kus.intersects()
    if kushit.hit:
        Audio('hit.wav', volume=2)
        kus.rotation = (0, 0, 180)
        application.pause()
        global game_over_entity, restart_button
        game_over_entity = Entity(model="cube", texture=load_texture("gameover.png"), z=-3, scale=(6.5, 1.8), x=0.01, y=0)
        restart_button = Button(text="Restart", color=color.blue, scale=(0.1, 0.05), origin=(0, 0), x=0, y=-0.2, on_click=reset_game)

setup_tups()

def input(key):
    if held_keys["q"]:
        application.quit()

app.run()
