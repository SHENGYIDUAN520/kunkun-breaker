GAME_SIZE = (800, 600)
PLAYER_SIZE_W = 96
PLAYER_SIZE_H = 128
SPRITE_SIZE_W = 40
SPRITE_SIZE_H = 40

PLAYER_RES = (
    'res/player/0.png',
    'res/player/1.png',
    'res/player/2.png',
    'res/player/3.png',
    'res/player/4.png',
    'res/player/5.png',
    'res/player/6.png',
)

BALL_RES = "res/ball.png"
BLOCK_RES_FMT = "res/block/%d.png"

GAME_OVER_RES = "res/lose.png"

class BlockType:
    NULL = 0
    SPEED_UP = 1
    NORMAL = 2
    COPY = 3
    SPEED_DOWN = 6
    WALL = 9

class SoundRes:
    JNTM = 'snd/jntm.WAV'
    NGM = 'snd/niganma.WAV'
