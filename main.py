import pyglet

window = pyglet.window.Window()

img = pyglet.image.load('images/splash-mg.png')
sprite = pyglet.sprite.Sprite(img, x = (window.width - img.width) // 2,
    y = (window.height - img.height) // 2)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()