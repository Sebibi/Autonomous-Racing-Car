import os.path

import gymnasium as gym

from stable_baselines3 import A2C

# env = gym.make("CartPole-v1", render_mode="rgb_array")
#
# model = A2C("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=50_000)
#
# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)
#     vec_env.render("human")
#     # VecEnv resets automatically
#     # if done:
#     #   obs = vec_env.reset()
#
#

if not os.path.exists("a2c_lunar.zip"):
    env = gym.make("LunarLander-v2", render_mode="rgb_array")
    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100_000, progress_bar=True)
    model.save("a2c_lunar")
else:
    env = gym.make("LunarLander-v2", render_mode="human")
    model = A2C.load("a2c_lunar.zip")
    assert model, "Model not found {}".format(model)

print("Testing model")
observation, info = env.reset()
sum_reward = 0
terminated = False
while not terminated:
    action, _state = model.predict(observation, deterministic=True)
    observation, reward, terminated, truncated, info = env.step(action)
    sum_reward += reward
    print("Reward", sum_reward)

env.close()