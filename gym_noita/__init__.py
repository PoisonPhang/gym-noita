from gym.envs.registration import register

register(
    id='noita-v0',
    entry_point='gym_noita.envs:NoitaEnv',
)
