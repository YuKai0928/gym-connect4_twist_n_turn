from gym.envs.registration import register

register(
    id='Connect4_Twist_n_Turn-v0',
    entry_point='gym_connect4_twist_n_turn.envs:Connect4_TnT_Env',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )