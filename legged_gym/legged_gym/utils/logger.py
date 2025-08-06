# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from multiprocessing import Process, Value

DOF_NAMES = ['LF_HAA', 'LF_HFE', 'LF_KFE', 'LF_WHEEL',
             'LH_HAA', 'LH_HFE', 'LH_KFE', 'LH_WHEEL',
             'RF_HAA', 'RF_HFE', 'RF_KFE', 'RF_WHEEL', 
             'RH_HAA', 'RH_HFE', 'RH_KFE', 'RH_WHEEL']

class Logger:
    def __init__(self, dt):
        self.state_log = defaultdict(list)
        self.rew_log = defaultdict(list)
        self.dt = dt
        self.num_episodes = 0
        self.plot_process = None

    def log_state(self, key, value):
        self.state_log[key].append(value)

    def log_states(self, dict):
        for key, value in dict.items():
            self.log_state(key, value)

    def log_rewards(self, dict, num_episodes):
        for key, value in dict.items():
            if 'rew' in key:
                self.rew_log[key].append(value.item() * num_episodes)
        self.num_episodes += num_episodes

    def reset(self):
        self.state_log.clear()
        self.rew_log.clear()

    def plot_states(self):
        self.plot_process = Process(target=self._plot)
        self.plot_process.start()

    def _plot(self):
        nb_rows = 3
        nb_cols = 3
        fig, axs = plt.subplots(nb_rows, nb_cols)
        for key, value in self.state_log.items():
            time = np.linspace(0, len(value)*self.dt, len(value))
            break
        log= self.state_log
        # plot joint targets and measured positions
        a = axs[1, 0]
        if log["dof_pos"]: a.plot(time, log["dof_pos"], label='measured')
        if log["dof_pos_target"]: a.plot(time, log["dof_pos_target"], label='target')
        a.set(xlabel='time [s]', ylabel='Position [rad]', title='DOF Position')
        a.legend()
        # plot joint velocity
        a = axs[1, 1]
        if log["dof_vel"]: a.plot(time, log["dof_vel"], label='measured')
        if log["dof_vel_target"]: a.plot(time, log["dof_vel_target"], label='target')
        a.set(xlabel='time [s]', ylabel='Velocity [rad/s]', title='Joint Velocity')
        a.legend()
        # plot base vel x
        a = axs[0, 0]
        if log["base_vel_x"]: a.plot(time, log["base_vel_x"], label='measured')
        if log["command_x"]: a.plot(time, log["command_x"], label='commanded')
        a.set(xlabel='time [s]', ylabel='base lin vel [m/s]', title='Base velocity x')
        a.legend()
        # plot base vel y
        a = axs[0, 1]
        if log["base_vel_y"]: a.plot(time, log["base_vel_y"], label='measured')
        if log["command_y"]: a.plot(time, log["command_y"], label='commanded')
        a.set(xlabel='time [s]', ylabel='base lin vel [m/s]', title='Base velocity y')
        a.legend()
        # plot base vel yaw
        a = axs[0, 2]
        if log["base_vel_yaw"]: a.plot(time, log["base_vel_yaw"], label='measured')
        if log["command_yaw"]: a.plot(time, log["command_yaw"], label='commanded')
        a.set(xlabel='time [s]', ylabel='base ang vel [rad/s]', title='Base velocity yaw')
        a.legend()
        # plot base vel z
        a = axs[1, 2]
        if log["base_vel_z"]: a.plot(time, log["base_vel_z"], label='measured')
        a.set(xlabel='time [s]', ylabel='base lin vel [m/s]', title='Base velocity z')
        a.legend()
        # plot contact forces
        a = axs[2, 0]
        if log["contact_forces_z"]:
            forces = np.array(log["contact_forces_z"])
            for i in range(forces.shape[1]):
                a.plot(time, forces[:, i], label=f'force {i}')
        a.set(xlabel='time [s]', ylabel='Forces z [N]', title='Vertical Contact forces')
        a.legend()
        # plot torque/vel curves
        a = axs[2, 1]
        if log["dof_vel"]!=[] and log["dof_torque"]!=[]: a.plot(log["dof_vel"], log["dof_torque"], 'x', label='measured')
        a.set(xlabel='Joint vel [rad/s]', ylabel='Joint Torque [Nm]', title='Torque/velocity curves')
        a.legend()
        # plot torques
        a = axs[2, 2]
        if log["dof_torque"]!=[]: a.plot(time, log["dof_torque"], label='measured')
        a.set(xlabel='time [s]', ylabel='Joint Torque [Nm]', title='Torque')
        a.legend()

        nb_rows = 4
        nb_cols = 5
        fig, axs = plt.subplots(nb_rows, nb_cols)
        # plot joint targets and measured positions
        dof_pos_all = np.array(log["dof_pos_all"])
        dof_pos_target_all = np.array(log["dof_pos_target_all"])
        for i in range(len(DOF_NAMES)):
            a = axs[int(i/5), i%5]
            if log["dof_pos_all"]: a.plot(time, dof_pos_all[:,i], label='measured')
            if log["dof_pos_target_all"]: a.plot(time, dof_pos_target_all[:,i], label='target')
            if log["dof_pos_limits_lower"]: a.axhline(y=log["dof_pos_limits_lower"][0][i], label='lower',c="r")
            if log["dof_pos_limits_upper"]: a.axhline(y=log["dof_pos_limits_upper"][0][i], label='upper',c="r")
            # if log["dof_pos_target"]: a.plot(time, log["dof_pos_target"], label='target')
            a.set(ylabel='Position [rad]', title='{:} Position'.format(DOF_NAMES[i]))
            a.legend()


        nb_rows = 4
        nb_cols = 5
        fig, axs = plt.subplots(nb_rows, nb_cols)
        # plot joint targets and measured positions
        dof_vel_all = np.array(log["dof_vel_all"])
        dof_vel_target_all = np.array(log["dof_vel_target_all"])
        for i in range(len(DOF_NAMES)):
            a = axs[int(i/5), i%5]
            if log["dof_vel_all"]: a.plot(time, dof_vel_all[:,i], label='measured')
            if log["dof_vel_limits"]: a.axhline(y=log["dof_vel_limits"][0][i], label='lower',c="r")
            if log["dof_vel_limits"]: a.axhline(y=-log["dof_vel_limits"][0][i], label='upper',c="r")
            if log["dof_vel_target_all"]: a.plot(time, dof_vel_target_all[:,i], label='target')
            a.set(ylabel='Vel [rad/s]', title='{:} Velocity'.format(DOF_NAMES[i]))
            a.legend()

        nb_rows = 4
        nb_cols = 5
        fig, axs = plt.subplots(nb_rows, nb_cols)
        # plot joint targets and measured positions
        dof_torque_all = np.array(log["dof_torque_all"])
        for i in range(len(DOF_NAMES)):
            a = axs[int(i/5), i%5]
            if log["dof_torque_all"]: a.plot(time, dof_torque_all[:,i], label='measured')
            if log["dof_torque_limits"]: a.axhline(y=log["dof_torque_limits"][0][i], label='lower',c="r")
            if log["dof_torque_limits"]: a.axhline(y=-log["dof_torque_limits"][0][i], label='upper',c="r")
            # if log["dof_pos_target"]: a.plot(time, log["dof_pos_target"], label='target')
            a.set(ylabel='Torque [Nm]', title='{:} Torque'.format(DOF_NAMES[i]))
            a.legend()

        nb_rows = 4
        nb_cols = 4
        fig, axs = plt.subplots(nb_rows, nb_cols)
        dof_vel_all = np.array(log["dof_vel_all"])
        dof_torque_all = np.array(log["dof_torque_all"])
        joint_gear_ratio = [1,1,2,1]*4

        plt.subplots_adjust(wspace=0.3, hspace=0.3)  # Reduce spacing between subplots
        for i in range(len(DOF_NAMES)):
            a = axs[int(i/4), i%4]
            a.plot(abs(dof_vel_all[:,i]), abs(dof_torque_all[:,i]), 'x', label='measured')
            a.set(xlabel='Joint vel [rad/s]', ylabel='Joint Torque [Nm]', title=DOF_NAMES[i])
            if log["dof_vel_limits"]:
                vel_limit = log["dof_vel_limits"][0][i]
                a.set_xlim([0, vel_limit+5])
            if log["dof_torque_limits"]:
                torque_limit = log["dof_torque_limits"][0][i]
                a.set_ylim([0, torque_limit+5])
            
            # Draw torque limit curve
            vel_points = np.linspace(0, vel_limit+5, 20)
            torque_limits = np.array([self.torque_limit_curve(joint_gear_ratio[i], v) for v in vel_points])
            a.plot(vel_points, torque_limits, 'r-', label='torque vel balanced limit')
            
            a.legend()

        plt.show()
    
    def torque_limit_curve(self,gear_ratio,current_dof_vel):
        if current_dof_vel*gear_ratio<13.5:
            max_torque = 40*gear_ratio
        else:
            max_torque = np.clip(40*gear_ratio-(current_dof_vel*gear_ratio-13.5)*9.0619,0,40*gear_ratio*1.1)
        return max_torque

    def print_rewards(self):
        print("Average rewards per second:")
        for key, values in self.rew_log.items():
            mean = np.sum(np.array(values)) / self.num_episodes
            print(f" - {key}: {mean}")
        print(f"Total number of episodes: {self.num_episodes}")
    
    def __del__(self):
        if self.plot_process is not None:
            self.plot_process.kill()