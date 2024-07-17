import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

class MLP(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DQNAgent:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = MLP(input_dim, output_dim)
        self.target_model = MLP(input_dim, output_dim)
        self.update_target_model()
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.output_dim)
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return torch.argmax(act_values[0]).item()

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state).unsqueeze(0)
            next_state = torch.FloatTensor(next_state).unsqueeze(0)
            target = reward
            if not done:
                target = reward + self.gamma * torch.max(self.target_model(next_state)[0]).item()
            target_f = self.model(state)
            target_f[0][action] = target
            self.optimizer.zero_grad()
            loss = self.criterion(self.model(state), target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_state_dict(torch.load(name))

    def save(self, name):
        torch.save(self.model.state_dict(), name)
def train_dino_agent(env, agent, episodes, batch_size):
    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, agent.input_dim])
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, agent.input_dim])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                agent.update_target_model()
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2f}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

# Assuming `env` is your game environment
input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n
agent = DQNAgent(input_dim, output_dim)
train_dino_agent(env, agent, episodes=1000, batch_size=32)

def evaluate_dino_agent(env, agent, episodes):
    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, agent.input_dim])
        total_reward = 0
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, agent.input_dim])
            state = next_state
            total_reward += reward
            if done:
                print(f"episode: {e}/{episodes}, score: {time}, total reward: {total_reward}")
                break

# Evaluate the trained agent
evaluate_dino_agent(env, agent, episodes=10)
