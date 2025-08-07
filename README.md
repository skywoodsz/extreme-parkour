This project builds upon [Extreme Parkour](https://github.com/chengxuxin/extreme-parkour), aiming to enable parkour with a wheel-legged robot.


### Key Differences from *Extreme Parkour*

#### 1. Basic Configuration and Logger

- The wheel-legged robot is added under  
  `/legged_gym/resources/robot/sirius_wheel`.

- The gym environment for the wheel-legged robot is added under  
  `/legged_gym/legged_gym/envs/sirius_wheel`.

**Note:** For readability, `LeggedRobotCfg` and `LeggedRobot` are defined directly in `/legged_gym/legged_gym/envs/sirius_wheel` rather than inheriting from `/legged_gym/legged_gym/envs/base`.  Only this environment is registered in the `envs` package; registering other environments that inherit from the base may result in errors.

- Modified `LeggedRobotCfg` and `SiruisWheelParkourCfg` based on [diff_whl_legged_gym](https://github.com/CUHKSiriusLeggedRobotTeam/diff_whl_legged_gym), and added `"thigh"`, `"calf"`, and `"trunk"` to `penalize_contacts_on`.

- Modified the `_compute_torques` method in the `LeggedRobot` class, though **serial torques** are still used rather than **differential torques**.

- Added a debugging `wandb_logger` to log:
  - Agent 0's velocity and torque  
  - Terrain curriculum progression  
  - Reset conditions

- Modified the joint order of network observations and actions to match the wheel-legged SDK.  See methods `reindex` and `reindex_feet`.


#### 2. New Terrains

- Added two new terrains:
  - `parkour_wall2`: jump area **without a gap**
  - `parkour_wall_gap2`: jump area **with a gap**

- In `parkour_wall2`:
  - Wall size: 5 m tall × 1 m wide × 10 m long  
  - Randomly placed on the left or right side of the submap  
  - Y-axis offset from the robot: randomly sampled between 0.3 m and 0.6 m

- There are three **goals**:
  1. **Takeoff point** – 4 m in front of the starting position  
  2. **Landing point** – randomly placed 0.4 m–2 m ahead of the takeoff point (increases with difficulty)  
  3. **Task completion point** – 2 m ahead of the landing point

- Two custom areas:
  - `terminate_mask`: area representing the gap; contact here triggers termination
  - `wall_contact_area`: wall section between goal 1 and 2; encourages foot contact during jump

- `parkour_wall_gap2` is identical to `parkour_wall2` except it includes a gap with a depth randomly sampled from 0.1 m to 5 m.

- During visualization (`play` mode):
  - `terminate_mask`: shown in **red points**
  - `wall_contact_area`: shown in **green points**

**Known issue:** The visualization currently fixes all points at height 0 (flat). This does not affect simulation logic.

- The method `check_contact_in_terminate_masks` in `LeggedRobot` terminates the episode upon contact with `terminate_mask`.

- `_reward_contact_wheel` encourages foot contact with `wall_contact_area` during jumps.


#### 3. Additional Sampling and Rewards

- `_reward_jump_height`:  
  - Target height = **1 m** when jumping to the second goal (landing point)  
  - Target height = **0.5 m** otherwise

- `_reward_dof_error` and `_reward_hip_pos`:  
  - Penalize joint positions generally  
  - Rewards set to **0** when targeting the second goal, allowing more joint motion exploration during jumping

- The observation space includes a flag indicating whether the current target is the second goal — encoding jump timing explicitly.

- In `reset_idx`:  
  - Agents are randomly initialized at either the origin or mid-jump  
  - Mid-jump agents receive a random initial velocity between **0.1m/s** and **1.6m/s**


### Installation ###
```bash
conda create -n parkour python=3.8
conda activate parkour
cd
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
git clone git@github.com:chengxuxin/extreme-parkour.git
cd extreme-parkour
# Download the Isaac Gym binaries from https://developer.nvidia.com/isaac-gym 
# Originally trained with Preview3, but haven't seen bugs using Preview4.
cd isaacgym/python && pip install -e .
cd ~/extreme-parkour/rsl_rl && pip install -e .
cd ~/extreme-parkour/legged_gym && pip install -e .
pip install "numpy<1.24" pydelatin wandb tqdm opencv-python ipdb pyfqmr flask colorama scikit-image imageio-ffmpeg imageio
```

### Usage ###
`cd legged_gym/scripts`
1. Train base policy:  
```bash
python train.py --exptid xxx-xx-WHATEVER --device cuda:0 --headless 
```
Train 10-15k iterations (8-10 hours on 3090) (at least 15k recommended).

2. Train distillation policy:
```bash
python train.py --exptid yyy-yy-WHATEVER --device cuda:0 --resume --resumeid xxx-xx --delay --use_camera --headless 
```
Train 5-10k iterations (5-10 hours on 3090) (at least 5k recommended). 
>You can run either base or distillation policy at arbitary gpu # as long as you set `--device cuda:#`, no need to set `CUDA_VISIBLE_DEVICES`.

3. Play base policy:
```bash
python play.py --exptid xxx-xx
```
No need to write the full exptid. The parser will auto match runs with first 6 strings (xxx-xx). So better make sure you don't reuse xxx-xx. Delay is added after 8k iters. If you want to play after 8k, add `--delay`

4. Play distillation policy:
```bash
python play.py --exptid yyy-yy --delay --use_camera
```


### Viewer Usage
Can be used in both IsaacGym and web viewer.
- `ALT + Mouse Left + Drag Mouse`: move view.
- `[ ]`: switch to next/prev robot.
- `Space`: pause/unpause.
- `F`: switch between free camera and following camera.

### Arguments
- --exptid: string, can be `xxx-xx-WHATEVER`, `xxx-xx` is typically numbers only. `WHATEVER` is the description of the run. 
- --device: can be `cuda:0`, `cpu`, etc.
- --delay: whether add delay or not.
- --checkpoint: the specific checkpoint you want to load. If not specified load the latest one.
- --resume: resume from another checkpoint, used together with `--resumeid`.
- --seed: random seed.
- --no_wandb: no wandb logging.
- --use_camera: use camera or scandots.
- --web: used for playing on headless machines. It will forward a port with vscode and you can visualize seemlessly in vscode with your idle gpu or cpu. [Live Preview](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server) vscode extension required, otherwise you can view it in any browser.

