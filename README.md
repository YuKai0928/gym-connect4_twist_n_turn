# gym-connect4_twist_n_turn
This repo contains a gym environment of game "connect4 twist &amp; turns", which is a variety of origin game "connect 4"

![](/Users/yukai/Documents/Sinica_intern/connect4_twist/gym-connect4_twist_n_turn/prototype.jpg)

Pic source: [baordgamegeek](https://boardgamegeek.com/boardgame/199351/connect-4-twist-turn)

## Game Introduction

This is a a variety version of game "connect 4", which has a circular board and rotation operation on each row(layer) c.w or c.c.w.

Player 1 goes first.

Two players take turns to lay a disc and do a rotation operation. (no rotation is also a valid rotation operation)

The game terminates when there is a 4-in-a-row (there is a winner) or no space for any new disc (draw)

The 4-in-a-row line can be vertical / horizontal / diagonally

### Rotation 

When it's your turn, after you lay a disc, you can do a rotation operation on one of the row/layer.

Each rotation operation can move at most one block (counter) clockwisely.

After the rotation, all the "floating discs" will drop down.

**We only check winning state after one player finishes his all operation**

**If both players got a 4-in-a-row of their discs,  a draw occurs.**



## Simple Demo

1. Clone this repo
2. cd into `./gym-connect4_twist_n_turn`
3. Run `demo.py` and you will see the process and result of game with two random agent.



## Step Format

use `env.step(action)` to feed next operation of next player.

- action is a list with two integer. 
- action[0] is the x-axis of next move.
- action[1] is the encoded rotation operation:
  - 0 for no rotation
  - [1,height] => rotate counter-clockwisely on the layer action[1]
  - [height+1,2*height] => rotate clockwisely on the layer action[1] - height

