'''
Time: 23rd July 2025 
Author: skywoodsz 
'''

import wandb
import datetime

class wandbLogs:
    def __init__(self, conditions=None, dof_names=None):
        '''
        conditions: reset conditions
        '''
        if conditions is None or dof_names is None:
            return
    
        self.conditions = conditions
        self.dof_names = dof_names
        self.table = wandb.Table(columns=["time", "episode"] + self.conditions)
        self.table_episode_count = 0
        self.joint_episode_count = 0

    def log_reset(self, triggered_conditions):
        self.table_episode_count += 1
        row = [
            datetime.datetime.now().strftime("%H:%M:%S"),
            self.table_episode_count
        ]
        for cond in self.conditions:
            row.append("✅" if cond in triggered_conditions else "❌")

        self.table.add_data(*row)
        wandb.log({"reset_conditions": self.table}, commit=False)
    
    def log_joint_states(dof_vel=None, dof_torque=None):
        self.joint_episode_count += 1
        wandb_dict = {}
        for i, name in enumerate(self.dof_names):
            wandb_dict[f"Joint Velocity/{self.dof_names[i]}"] = dof_vel[i]
            wandb_dict[f"Joint Torque/{self.dof_names[i]}"] = dof_torque[i]
        
        wandb.log(wandb_dict, step=self.joint_episode_count)