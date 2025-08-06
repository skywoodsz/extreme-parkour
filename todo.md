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

 5. refine 2
 - 整定_reward_jump_height的参数 (done)
 - check update terrain threshold (done)

6. refine 3
 - 挖坑 + 不挖坑 (done)
 - 修复阈值bug (done)
 - log 加入log_dis_to_origin来check阈值 (done)

7. refine 5
 - wall len从2->1

8. refine 6 (parkour_wall2 和 parkour_wall_gap2)
 - 固定wall到robot y方向的距离，能在起跳时登墙. 0.2-0.5m (done)
 - goals不在墙上，在一条直线上 (done)
 - 调整起始goal的位置，方便跳跃 (done)
 - 合适的下放height和初始速度 (done)
 - 裁减scandot(done)

9. refine 7 
- 预定义base轨迹
 
1.1 aaa-qq:
1.1.1
- 修改height jumping trakcing为regulation，用linear函数
- 加入orientation regulation，保证没有奇怪的姿态变化行为
- reset时将关节朝墙，希望提升samping 效率学会蹬墙

1.2 aaa-pp:
1.2.1
- 修改height jumping trakcing为regulation，用linear函数
- 加入orientation regulation，保证没有奇怪的姿态变化行为
- reset时将关节朝墙，希望提升samping 效率学会蹬墙
1.2.2
- 在墙之外惩罚hip，墙上不惩罚hip
- 在墙上的样本不update terrain课程
- 减小从原点开始的update terrain课程阈值
- 取消差分计算torque