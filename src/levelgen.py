back = [
    "99999999999999999999\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n",
    "90000000000000000009\n"
]

class BlockType:
    NULL = 0
    SPEED_UP = 1
    NORMAL = 2
    COPY = 3
    SPEED_DOWN = 6
    WALL = 9

BLOCK_TYPE_VALUE = [
    1500,    
    10,
    100,
    10,
    100,
    100,
    10,
    100,
    0,
    0,
]

maxValue = 0
for x in BLOCK_TYPE_VALUE:
    maxValue += x

def randomGen():
    import random
    val = random.randint(0, maxValue)
    for i, x in enumerate(BLOCK_TYPE_VALUE):
        val -= x
        if val <= 0:
            return i

for x in range(11, 100):
    with open('data/level/' + str(x) + ".x", "w") as fp:
        fp.write("99999999999999999999\n")
        for i in range(7):
            row = "9"
            for j in range(18):
                row += str(randomGen())
            row += "9\n"
            fp.write(row)
        for i in range(8):
            fp.write("90000000000000000009\n")
