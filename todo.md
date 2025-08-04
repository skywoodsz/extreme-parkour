1. 建立wall地形:
   - 课程设计 (done)
   - goal设计 (done)

2. 建立机器人
   - rewards
   - terminate (done)
   - order (done)
   - defalut (done)

3. debug
 - wandb debug logger (done)
 - check reach goal distance (done) 12m
 - check update terrain threshold (done)
 - reset时一半在墙上 一半在地上 (done)
 - 取消45度以下terrain (done)

4. refine
 - 填坑 + terminate + 墙长宽高不变 (done)
 - check reach goal distance (done)
 - check update terrain threshold 改称goal distance作阈值 (done)
 - 加goal height rewards (done)
 - 改在墙上初始化的robot goal (done)
 - 墙上初始化的robot有初始速度