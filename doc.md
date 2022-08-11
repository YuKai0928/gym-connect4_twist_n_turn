# Documentation



## Basic Framework

```python
import gym
import gym_connect4_twist_n_turn
env = gym.make('Connect4_Twist_n_Turn-v0', height=5, width=6, connect=4)
```

## Some Utilities



Methods & Parameters:

- env.step(action)
  - Return `observations`, `reward vector`, `done ` and `info`
    - 
- env.get_moves()
  - return a list with 2 list, each containing valid operation for index of laying disc and rotation
  - return empty list if the game is terminated
- env.reset()
  - return observation for two players of initial state.
- env.check_termination()
  - Check current board and return `winner player id` and `reward_vector` 
    - Winner player id can be 
      - `None` : Game in progress.
      - `-1` : draw
      - `1` : player 1 wins
      - `2` : player 2 wins
    - Reward_vector is reward value for two players.

