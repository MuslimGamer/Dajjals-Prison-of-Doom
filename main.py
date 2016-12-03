import pyglet

COLOR_RED = (255, 0, 0, 255)

class Main:
    def run(self):
        window = pyglet.window.Window()
        
        sprite = self.create_color(32, 32, COLOR_RED)
        sprite.x = (window.width - sprite.width) // 2
        sprite.y = (window.height - sprite.height) // 2

        @window.event
        def on_draw():
            window.clear()
            sprite.draw()

        pyglet.app.run()

    # color_tuple is a four-colour tuple (R, G, B, A).
    def create_color(self, width, height, color_tuple):
        img = pyglet.image.SolidColorImagePattern(color_tuple).create_image(32, 32)
        sprite = pyglet.sprite.Sprite(img)
        return sprite

Main().run()

#img = pyglet.image.load('images/splash-mg.png')
#sprite = pyglet.sprite.Sprite(img, x = (window.width - img.width) // 2,
#    y = (window.height - img.height) // 2)
