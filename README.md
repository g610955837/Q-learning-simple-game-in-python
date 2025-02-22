# Q-learning-simple-game-in-python
#Assignment 1 - Reinforcement Learning Game Design
Wang Zihao
3160722
________________________________________
1. Project Overview
This project involves the design and implementation of a game using Q-learning, a reinforcement learning algorithm. The objective is to create a game where an AI-controlled agent learns to make optimal decisions based on rewards and penalties. The chosen game is a simple plane-dodging simulation, where the AI controls a plane that must avoid falling obstacles. Through this project, I demonstrate the application of Q-learning in designing a functional game environment, implementing the algorithm, and evaluating its performance.
________________________________________
2. Game Design
2.1 Clear Objective and Rules
The game's objective is straightforward: the AI-controlled plane must avoid colliding with randomly generated obstacles falling from the top of the screen. The plane can only move left or right, and the game ends when the plane collides with an obstacle. The primary goal is to maximize the survival time of the plane.
Rules :
The plane starts at the bottom center of the screen.
Obstacles are generated at random positions above the screen and fall downward.
If the plane collides with an obstacle, the game resets.
The AI earns positive rewards for surviving longer and negative rewards for collisions.
2.2 State Space and Action Space
•	State Space :
The state space includes the position of the plane and the relative positions of the three closest obstacles. Each state is represented as a tuple containing the plane's position and the relative positions of the obstacles. This simplification reduces the complexity of the state space while retaining sufficient information for decision-making.
 
•	Action Space :
The action space consists of two possible actions: moving left (LEFT) or moving right (RIGHT). These actions correspond to horizontal movements of the plane.
 
2.3 Reward Function
The reward function is designed to encourage the AI to avoid collisions and maximize survival time:
•	Positive Rewards : The AI receives a small positive reward (+1) for each step it survives without colliding with an obstacle.
•	Negative Rewards : A large penalty (-100) is applied when the plane collides with an obstacle, signaling undesirable behavior.
 
2.4 Documentation of Game Design
The game was implemented using Python and the Pygame library. The user interface (UI) displays the following elements:
•	The plane, represented as a white triangle.
•	Falling obstacles, represented as red rectangles.
 
•	A leaderboard in the bottom-left corner showing the survival times of the last eight crashes.
•	A timer in the top-right corner indicating the current survival time.
________________________________________
3. Q-Learning Implementation
 

3.1 Q-Learning Algorithm
The Q-learning algorithm was implemented to enable the AI to learn an optimal policy for avoiding obstacles. The algorithm operates by iteratively updating a Q-table, which stores the expected cumulative rewards for each state-action pair.
3.2 Role of the Q-Table
The Q-table serves as the core component of the Q-learning algorithm. It acts as a lookup table that maps states to actions, storing the expected rewards for each possible action in a given state. Initially, the Q-table is empty, and the AI explores the environment by taking random actions. Over time, the table is updated based on the rewards received, allowing the AI to learn which actions lead to better outcomes.
Key aspects of the Q-table implementation include:
•	State Representation : Each state is represented as a tuple containing the plane's position and the relative positions of the three closest obstacles.
•	Action Selection : The AI uses an epsilon-greedy strategy to balance exploration and exploitation. Initially, the AI explores more frequently by choosing random actions. As training progresses, the exploration rate decreases, and the AI relies more on the learned Q-values.
3.3 Techniques Used
To ensure effective learning, the following techniques were implemented:
•	Epsilon-Greedy Exploration : The exploration rate (epsilon) starts at a high value (e.g., 0.8) and gradually decays over time, reducing the frequency of random actions.
•	Learning Rate : Controls the weight of new information when updating the Q-table. A moderate learning rate (e.g., 0.3) was chosen to balance stability and adaptability.
•	Discount Factor : Determines the importance of future rewards. A discount factor of 0.95 was used to emphasize long-term rewards.
 

3.4 Evaluation of Policy Learning
After training the AI for 10 episodes, significant improvements were observed. Initially, the plane crashed almost immediately, but by the end of training, it could survive for extended periods, demonstrating the effectiveness of the Q-learning algorithm.
 
________________________________________
4. Game Interaction
4.1 User Interface (UI)
The game's UI was developed using the Pygame library. It provides a visual representation of the game environment and allows the AI to interact with the obstacles.
 
4.2 Display Elements
The UI includes the following features:
•	The plane's position and movement are displayed in real-time.
•	Obstacles are rendered as red rectangles that fall from the top of the screen.
•	A leaderboard in the bottom-left corner tracks the survival times of the last eight crashes.
•	A timer in the top-right corner shows the current survival time.
 
4.3 Use of Libraries/Frameworks
Pygame was chosen for its simplicity and flexibility in creating 2D games. The library provides tools for rendering graphics, handling user input, and managing game loops, making it well-suited for this project.
4.4 User Experience
The game runs smoothly, with intuitive visuals that clearly convey the AI's actions and the game's progression. The leaderboard and timer provide additional feedback, enhancing the overall user experience.
________________________________________
5. Documentation and Presentation
5.1 Written Report
This report documents the game design, Q-learning implementation, and evaluation results. It provides a comprehensive overview of the project, including the challenges faced and the solutions implemented.
5.3 Challenges and Solutions
One of the main challenges was defining an appropriate state space. Initially, the state space included all obstacles, leading to excessive complexity. To address this, the state space was simplified to include only the three closest obstacles. Additionally, fine-tuning the learning rate and discount factor was crucial for achieving optimal performance.
5.4 Overall Quality
The project demonstrates a clear understanding of reinforcement learning principles and their practical application. The documentation and presentation are concise, well-organized, and effectively communicate the key aspects of the project.
________________________________________
6. Deliverables
1.	GitHub Repository : https://github.com/g610955837/Q-learning-simple-game-in-python
2.	YouTube Demo Video : 1、https://www.youtube.com/watch?v=uaDgzQ5zai4
                      2、https://www.youtube.com/watch?v=zbRNusKsLYY
________________________________________
7. Conclusion
This project successfully applies Q-learning to design a functional game environment where an AI-controlled plane learns to avoid obstacles. The implementation demonstrates the effectiveness of reinforcement learning in solving decision-making problems. Future work could involve extending the game's complexity or exploring advanced reinforcement learning techniques, such as deep Q-networks (DQN).

