import numpy as np
import pygame
import random

pygame.init()

# 配置参数
CONFIG = {"WIDTH": 600, "HEIGHT": 400, "CAR_SIZE": 20, "OBSTACLE_SIZE": 30, "FPS": 30, "BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0)} # 游戏窗口和颜色配置

# 动作空间
ACTIONS = ['LEFT', 'RIGHT'] 
ACTION_SPACE = len(ACTIONS) 

# Q-learning 参数
LEARNING_RATE = 0.3 # 学习率，新知识的权重
DISCOUNT_FACTOR = 0.95 # 折扣因子
EPSILON = 0.8 # 初始探索率
EPSILON_DECAY = 0.7 # 探索率衰减系数，逐渐减少探索比例
MIN_EPSILON = 0.01 

# 初始化 Q 表
Q_TABLE = {} 
survival_times = [] # 记录每次游戏结束时的存活时间

#### 状态离散化函数
def get_state(car_x, car_y, obstacles): # 将连续状态离散化为元组，便于存储在 Q 表中
    state = [] # 初始化状态列表
    for obs in obstacles[:3]: #仅考虑最近的 3 个障碍物以简化状态空间
        relative_x = (obs['x'] - car_x) // CONFIG["OBSTACLE_SIZE"] # 位置
        relative_y = (obs['y'] - car_y) // CONFIG["OBSTACLE_SIZE"] 
        state.append((relative_x, relative_y)) 
    return (int(car_x // CONFIG["CAR_SIZE"]), int(car_y // CONFIG["CAR_SIZE"]), tuple(state)) 

# 更新 Q 表
def update_q_table(state, action, reward, next_state): #更新 Q 表
    if state not in Q_TABLE: Q_TABLE[state] = np.zeros(ACTION_SPACE) # 如果状态未在 Q 表中，初始化为零向量
    if next_state not in Q_TABLE: Q_TABLE[next_state] = np.zeros(ACTION_SPACE) # 如果下一状态未在 Q 表中，初始化为零向量
    current_q = Q_TABLE[state][ACTIONS.index(action)] # 获取当前状态-动作对的 Q 值
    max_future_q = np.max(Q_TABLE[next_state]) # 获取下一状态的最大 Q 值
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_future_q) # Q-learning 更新公式
    Q_TABLE[state][ACTIONS.index(action)] = new_q # 更新当前状态-动作对的 Q 值

# 主游戏类
class SelfDrivingCarGame:
    def __init__(self): # 初始化游戏环境
        self.screen = pygame.display.set_mode((CONFIG["WIDTH"], CONFIG["HEIGHT"])) # 创建游戏窗口
        self.clock = pygame.time.Clock() # 控制帧率
        self.car_x, self.car_y = CONFIG["WIDTH"] // 2, CONFIG["HEIGHT"] - CONFIG["CAR_SIZE"] * 2 # 飞机初始位置
        self.obstacles = [{'x': random.randint(0, CONFIG["WIDTH"] - CONFIG["OBSTACLE_SIZE"]), 'y': random.randint(-CONFIG["HEIGHT"], 0)} for _ in range(5)] # 随机生成障碍物
        self.running = True # 游戏运行标志
        self.epsilon = EPSILON # 当前探索率
        self.font = pygame.font.Font(None, 24) 
        self.start_time = pygame.time.get_ticks() # 时间

    def reset(self): # 重置
        global survival_times
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000 # 计算存活时间）
        survival_times.append(elapsed_time) # 加入记录
        if len(survival_times) > 8: survival_times.pop(0) # 如果记录超过 8 条，删除最早的一条
        self.car_x, self.car_y = CONFIG["WIDTH"] // 2, CONFIG["HEIGHT"] - CONFIG["CAR_SIZE"] * 2 # 重置飞机位置
        self.obstacles = [{'x': random.randint(0, CONFIG["WIDTH"] - CONFIG["OBSTACLE_SIZE"]), 'y': random.randint(-CONFIG["HEIGHT"], 0)} for _ in range(5)] # 重置障碍物
        self.start_time = pygame.time.get_ticks() # 重置计时器

    def step(self, action): # 执行动作并返回奖励和是否结束
        if action == 'LEFT' and self.car_x > 0: self.car_x -= 5 # 左移飞机
        elif action == 'RIGHT' and self.car_x < CONFIG["WIDTH"] - CONFIG["CAR_SIZE"]: self.car_x += 5 # 右移飞机
        for obs in self.obstacles: # 更新障碍物位置
            obs['y'] += 2 # 障碍物下落速度
            if obs['y'] > CONFIG["HEIGHT"]: # 如果障碍物超出屏幕，重新生成
                obs['y'] = random.randint(-CONFIG["HEIGHT"], 0)
                obs['x'] = random.randint(0, CONFIG["WIDTH"] - CONFIG["OBSTACLE_SIZE"])
        collision = any(self.car_x < obs['x'] + CONFIG["OBSTACLE_SIZE"] and self.car_x + CONFIG["CAR_SIZE"] > obs['x'] and self.car_y < obs['y'] + CONFIG["OBSTACLE_SIZE"] and self.car_y + CONFIG["CAR_SIZE"] > obs['y'] for obs in self.obstacles) # 检查碰撞
        reward = -1 if not collision else -100 # 每走一步惩罚 -1，碰撞惩罚 -100
        if collision: self.reset() # 如果碰撞，重置游戏
        return reward, collision # 返回奖励和是否结束

    def draw_plane(self): #绘制飞机（三角形）
        pygame.draw.polygon(self.screen, CONFIG["WHITE"], [(self.car_x, self.car_y), (self.car_x + CONFIG["CAR_SIZE"] // 2, self.car_y - CONFIG["CAR_SIZE"]), (self.car_x + CONFIG["CAR_SIZE"], self.car_y)])

    def draw_obstacles(self): # 绘制障碍物
        for obs in self.obstacles: pygame.draw.rect(self.screen, CONFIG["RED"], (obs['x'], obs['y'], CONFIG["OBSTACLE_SIZE"], CONFIG["OBSTACLE_SIZE"]))

    def render(self): # 游戏画面
        self.screen.fill(CONFIG["BLACK"]) # 背景色
        self.draw_plane() #飞机
        self.draw_obstacles() #障碍物
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000 # 计算存活时间
        time_text = self.font.render(f"Time: {elapsed_time:.1f}s", True, CONFIG["WHITE"]) # 显示当前时间
        self.screen.blit(time_text, (CONFIG["WIDTH"] - 150, 10)) # 在右上角显示时间
        y_offset = 10 
        for i, time in enumerate(survival_times): # 显示存活时间记录
            time_text = self.font.render(f"{i + 1}. {time:.1f}s", True, CONFIG["WHITE"])
            self.screen.blit(time_text, (10, CONFIG["HEIGHT"] - 40 - y_offset))
            y_offset += 20
        pygame.display.flip() 

    def train(self, episodes=500): #训练AI
        for episode in range(episodes): # 进行指定回合数的训练
            self.reset() # 重置游戏状态
            state = get_state(self.car_x, self.car_y, self.obstacles) # 获取初始状态
            total_reward = 0 # 初始化总奖励
            while True: # 开始回合循环
                if random.uniform(0, 1) < self.epsilon: action = random.choice(ACTIONS) # 探索：随机选择动作
                else: action = ACTIONS[np.argmax(Q_TABLE[state])] if state in Q_TABLE else random.choice(ACTIONS) # 利用：选择 Q 值最大的动作
                reward, done = self.step(action) # 执行动作并获取奖励和结束标志
                next_state = get_state(self.car_x, self.car_y, self.obstacles) # 获取下一状态
                update_q_table(state, action, reward, next_state) # 更新 Q 表
                state = next_state # 更新当前状态
                total_reward += reward # 累积奖励
                if done: break # 如果游戏结束，跳出循环
            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY) # 衰减探索率
            print(f"Episode: {episode + 1}, Total Reward: {total_reward}, Epsilon: {self.epsilon:.2f}") # 打印训练信息

    def play(self): # 测试 AI
        self.reset() # 重置游戏状态
        while self.running: # 游戏主循环
            for event in pygame.event.get(): # 处理事件
                if event.type == pygame.QUIT: self.running = False # 如果用户关闭窗口，退出游戏
            state = get_state(self.car_x, self.car_y, self.obstacles) # 获取当前状态
            action = ACTIONS[np.argmax(Q_TABLE[state])] if state in Q_TABLE else random.choice(ACTIONS) # 根据 Q 表选择动作
            self.step(action) # 执行动作
            self.render() # 渲染画面
            self.clock.tick(CONFIG["FPS"]) # 控制帧率
        pygame.quit() # 退出 Pygame

# 主程序
if __name__ == "__main__":
    game = SelfDrivingCarGame() # 创建游戏实例
    print("开始搞事") # 提示训练开始
    game.train(episodes=10) # 训练10个回合
    print("OK了") # 提示训练完成
    game.play() # 开始测试
