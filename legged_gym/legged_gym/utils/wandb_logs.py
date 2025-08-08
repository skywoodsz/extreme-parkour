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
        # self.table = wandb.Table(columns=["time", "episode"] + self.conditions,
        #                         allow_mixed_types=True,
        #                         log_mode="MUTABLE")
        self.table_episode_count = 0
        self.joint_episode_count = 0

        wandb.define_metric("reset_conditions", step_metric="reset_step")
        wandb.define_metric("Joint Velocity/*", step_metric="joint_step")
        wandb.define_metric("Joint Torque/*", step_metric="joint_step")

    def log_reset(self, triggered_conditions):
        self.table_episode_count += 1
        wandb_dict = {
            f"reset/{cond}": int(cond in triggered_conditions)  # True -> 1, False -> 0
            for cond in self.conditions
        }
        wandb.log(wandb_dict, commit=False)

    
    def log_joint_states(self, dof_vel=None, dof_torque=None):
        self.joint_episode_count += 1
        wandb_dict = {"joint_step": self.joint_episode_count}
        for i, name in enumerate(self.dof_names):
            wandb_dict[f"Joint Velocity/{self.dof_names[i]}"] = dof_vel[i]
            wandb_dict[f"Joint Torque/{self.dof_names[i]}"] = dof_torque[i]
        
        wandb.log(wandb_dict, commit=False)

    def log_dis_to_origin(self, dis_to_origin, threshold, threshold_upper, threshold_lower):
        wandb_dict = {"dis_to_origin": dis_to_origin,
                      "threshold": threshold,
                      "threshold_upper": threshold_upper,
                      "threshold_lower": threshold_lower}
        wandb.log(wandb_dict, commit=False)
    
    def log_terrain_level(self, level):
        wandb_dict = {"level": level}
        wandb.log(wandb_dict, commit=False)