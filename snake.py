import pyglet #zpřístupní grafickou knihovnu
from random import randrange

TILE_SIZE = 32

green_image = pyglet.image.load('green.png')
apple_image = pyglet.image.load('apple.png')


snake_images = {} # prázdný slovník
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start  + '-' + end # podle čeho to budu vybírat
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_images[key] = image

#print(snake_images)

def get_direction(a, b):
    if b == 'end':
        return 'end'
    a_x, a_y = a
    b_x, b_y = b # 0 -1 = -1
    dx = a_x - b_x
    dy = a_y - b_y
    if dx == 1:
        return 'left'
    elif dx == -1:
        return 'right' # jeď doprava
    elif dy == -1:
        return 'top'
    elif dy == 1:
        return 'bottom'
    else:
        return 'end'

# hrajeme
# když narazíme, už nehrajeme
# když už nehrajeme, nedělat game


class GameState:
    def initialize(self):
        self.snake = [(1,2),(2,2),(3,2),(3,3),(3,4),(3,5),(4,5)]
        self.food = []#[(2,0),(5,1),(1,4)]#rozmístíme jablíčka na souřadnice
        self.direction = (0,-1)
        self.dead = False

        self.add_food()
        self.add_food()
        self.add_food()

    def add_food(self):
        for i in range(100):
            x = randrange(window.width // TILE_SIZE)
            y = randrange(window.height // TILE_SIZE)
            food_position = x,y
            if not (food_position in self.snake or food_position in self.food):
                self.food.append(food_position)
                return

    def draw(self): #funkčnost herního stavu
         for prev, current, nxt in zip(
            ['end'] + self.snake[:-1],
            self.snake,self.snake[1:] + ['end']):
            dir_to_prev = get_direction(current, prev) # směr k následujícímu
            dir_to_next = get_direction(current, nxt) # směr k novému
            if dir_to_next == 'end' and self.dead:
                dir_to_next = 'dead'
            key = dir_to_prev + '-' + dir_to_next # spojí se
            x, y = current
            snake_images[key].blit(
                x * TILE_SIZE, y * TILE_SIZE,
                width=TILE_SIZE, height=TILE_SIZE,
            )
         for x,y in self.food:
            apple_image.blit(
            x * TILE_SIZE, y * TILE_SIZE,
            width = TILE_SIZE,height=TILE_SIZE,
            )

    def move(self, dt):
        if self.dead:
            return
        direction_x, direction_y = self.direction
        old_head = self.snake[-1]
        old_x, old_y = old_head
        new_x = old_x + direction_x
        new_y = old_y + direction_y
        new_head = new_x, new_y
        if new_head in self.food: # prodluž se, když něco sníš
            print('HAM!')
            self.add_food()
            self.food.remove(new_head) # chci smazat konkrétní prvek
        else:
            del self.snake[0] #smaž, jen když něco sníš
        if new_head in self.snake:
            self.dead = True
        self.snake.append(new_head)
        if new_x < 0:
            self.dead = True
        elif new_y < 0:
            self.dead = True
        elif new_x > window.width // TILE_SIZE:
            self.dead = True
        elif new_y > window.height // TILE_SIZE:
            self.dead = True


window = pyglet.window.Window()

state = GameState()
state.initialize()


#label = pyglet.text.Label("Ahoj Káťo!", x=10, y=20)


@window.event
def on_draw():
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    window.clear()
    state.draw()


@window.event
def on_key_press(key_code, modifier):
    print(key_code, modifier)
    if key_code == pyglet.window.key.LEFT:
        state.direction = -1,0
    elif key_code == pyglet.window.key.RIGHT:
        state.direction = +1,0
    elif key_code == pyglet.window.key.DOWN:
        state.direction = 0,-1
    elif key_code == pyglet.window.key.UP:
        state.direction = 0,+1

print(pyglet.window.key.LEFT)
print(pyglet.window.key.RIGHT)
print(pyglet.window.key.DOWN)
print(pyglet.window.key.UP)

pyglet.clock.schedule_interval(state.move, 1/6)

pyglet.app.run() # spustí applikaci vše nastavené
print('Hotovo')
