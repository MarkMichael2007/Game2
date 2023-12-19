# Import Kivy modules
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import NumericProperty
from random import randint

# Constants
BULLET_SPEED = 10
ENEMY_SPEED = 5
ENEMY_SPAWN_INTERVAL = 2

class ShooterGame(Widget):
    player = None
    bullets = []
    enemies = []
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ShooterGame, self).__init__(**kwargs)
        self.player = Button(size=(50, 50), pos=(100, 100))  # Example player widget
        self.add_widget(self.player)

    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            self.player.center_x = touch.x
            self.player.center_y = touch.y
        else:
            self.fire_bullet()

    def update(self, dt):
        self.move_bullets()
        self.move_enemies()
        self.check_collision()
        self.spawn_enemies()

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.pos = Vector(*bullet.pos) + Vector(0, BULLET_SPEED)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.pos = Vector(*enemy.pos) + Vector(0, -ENEMY_SPEED)

    def fire_bullet(self):
        bullet = Button(
            size=(10, 30),
            pos=(self.player.x + self.player.width / 2 - 5, self.player.y + self.player.height),
        )
        self.bullets.append(bullet)
        self.add_widget(bullet)

    def spawn_enemies(self):
        if randint(1, int(60 / ENEMY_SPAWN_INTERVAL)) == 1:
            enemy = Button(
                size=(30, 30),
                pos=(randint(0, self.width - 30), self.height),
            )
            self.enemies.append(enemy)
            self.add_widget(enemy)

    def check_collision(self):
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.collide_widget(enemy):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
            self.remove_widget(bullet)

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
            self.remove_widget(enemy)

class ShooterApp(App):
    def build(self):
        game = ShooterGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    ShooterApp().run()
