from legged_gym.envs.base.base_config import BaseConfig

class LeggedRobotCfg( BaseConfig ):
    class play:
        load_student_config = False
        mask_priv_obs = False
    class env:
        num_envs = 4096  # origin: 6144; teacher: 4096; only used for teacher policy

        n_scan = 132
        n_priv = 3 + 3 + 3
        n_priv_latent = 4 + 1 + 12 + 12  # mass + CoM + Motor strength
        n_proprio = 3 + 2 + 3 + 4 + 36 + 5  # todo: means
        history_len = 10

        num_observations = n_proprio + n_scan + history_len * n_proprio + n_priv_latent + n_priv  # n_scan + n_proprio + n_priv #187 + 47 + 5 + 12
        num_privileged_obs = None  # if not None a priviledge_obs_buf will be returned by step() (critic obs for assymetric training). None is returned otherwise
        num_actions = 12
        env_spacing = 3.  # not used with heightfields/trimeshes
        send_timeouts = True  # send time out information to the algorithm
        episode_length_s = 20  # episode length in seconds
        obs_type = "og" # unused

        history_encoding = True
        reorder_dofs = True  # unused

        # action_delay_range = [0, 5]

        # additional visual inputs
        include_foot_contacts = True

        ## random domain
        randomize_start_pos = False
        randomize_start_vel = False
        randomize_start_yaw = False
        rand_yaw_range = 1.2
        randomize_start_y = False
        rand_y_range = 0.5
        randomize_start_pitch = False
        rand_pitch_range = 1.6

        contact_buf_len = 100

        next_goal_threshold = 0.2  # 完成距离阈值
        reach_goal_delay = 0.1  # 完成时间
        num_future_goal_obs = 2

    class depth:  ## camera setting only used in student policy
        use_camera = False
        camera_num_envs = 64  # origin: 192 # only used for student policy
        camera_terrain_num_rows = 10  ## unused
        camera_terrain_num_cols = 20  ## unused

        position = [0.27, 0, 0.03]  # front camera ## Notes: camera position w.r.t. body frame todo: need to tune
        angle = [-5, 5]  # positive pitch down; random angle in pitch

        update_interval = 5  # 5 works without retraining, 8 worse
        original = (106, 60) # 原分辨率
        resized = (87, 58) # resize后的分辨率
        horizontal_fov = 87
        buffer_len = 2
        # 死区参数
        near_clip = 0
        far_clip = 2
        dis_noise = 0.0

        scale = 1 ## unused
        invert = True ## unused

    class normalization:
        class obs_scales: # todo: need to tune
            lin_vel = 2.0
            ang_vel = 0.25
            dof_pos = 1.0
            dof_vel = 0.05
            height_measurements = 5.0

        clip_observations = 100.
        clip_actions = 2.4 # 100? a1: 1.2 with action_scale = 0.25

    class noise:
        add_noise = False
        noise_level = 1.0  # scales other values
        quantize_height = True

        class noise_scales:
            rotation = 0.0
            dof_pos = 0.01
            dof_vel = 0.05
            lin_vel = 0.05
            ang_vel = 0.05
            gravity = 0.02
            height_measurements = 0.02

    class terrain:  ## Notes: need to tune
        mesh_type = 'trimesh'  # "heightfield" # none, plane, heightfield or trimesh
        hf2mesh_method = "grid"  # grid or fast
        max_error = 0.1  # for fast
        max_error_camera = 2

        y_range = [-0.4, 0.4]

        edge_width_thresh = 0.05  ## 距离edge多少起跳

        horizontal_scale = 0.05  # 0.1 [m] influence computation time by a lot
        horizontal_scale_camera = 0.1
        vertical_scale = 0.005  # [m]
        border_size = 5  # [m]
        height = [0.02, 0.06]
        simplify_grid = False
        gap_size = [0.02, 0.1]
        stepping_stone_distance = [0.02, 0.08]
        downsampled_scale = 0.075
        curriculum = True

        all_vertical = False
        no_flat = True

        static_friction = 1.0
        dynamic_friction = 1.0
        restitution = 0.
        measure_heights = True
        measured_points_x = [-0.45, -0.3, -0.15, 0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05,
                             1.2]  # 1mx1.6m rectangle (without center line)
        measured_points_y = [-0.75, -0.6, -0.45, -0.3, -0.15, 0., 0.15, 0.3, 0.45, 0.6, 0.75]
        measure_horizontal_noise = 0.0

        selected = False  # select a unique terrain type and pass all arguments
        terrain_kwargs = None  # Dict of arguments for selected terrain
        max_init_terrain_level = 5  # starting curriculum state
        terrain_length = 18
        terrain_width = 4
        num_rows = 10  # number of terrain rows (levels)  # spreaded is benifitiall !
        num_cols = 40  # number of terrain cols (types)

        # 训练地形占比
        terrain_dict = {"smooth slope": 0.,
                        "rough slope up": 0.0,
                        "rough slope down": 0.0,
                        "rough stairs up": 0.,
                        "rough stairs down": 0.,
                        "discrete": 0.,
                        "stepping stones": 0.0,
                        "gaps": 0.,
                        "smooth flat": 0,
                        "pit": 0.0,
                        "wall": 0.0,
                        "platform": 0.,
                        "large stairs up": 0.,
                        "large stairs down": 0.,
                        "parkour": 0.2,
                        "parkour_hurdle": 0.2,
                        "parkour_flat": 0.2,
                        "parkour_step": 0.2,
                        "parkour_gap": 0.2,
                        "demo": 0.0, }
        terrain_proportions = list(terrain_dict.values())

        # trimesh only:
        slope_treshold = 1.5  # slopes above this threshold will be corrected to vertical surfaces
        origin_zero_z = True

        num_goals = 8 # 每个地形的goal数

    class commands:
        curriculum = False
        max_curriculum = 1.
        num_commands = 4  # default: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        resampling_time = 6.  # time before command are changed[s]
        heading_command = True  # if true: compute ang vel command from heading error

        lin_vel_clip = 0.2
        ang_vel_clip = 0.4

        # Easy ranges
        class ranges: # unused
            lin_vel_x = [0., 1.5]  # min max [m/s]
            lin_vel_y = [0.0, 0.0]  # min max [m/s]
            ang_vel_yaw = [0, 0]  # min max [rad/s]
            heading = [0, 0]

        # Easy ranges
        class max_ranges: # todo: need to tune
            lin_vel_x = [0.3, 0.8]  # min max [m/s]
            lin_vel_y = [-0.3, 0.3]  # [0.15, 0.6]   # min max [m/s]
            ang_vel_yaw = [-0, 0]  # min max [rad/s]
            heading = [-1.6, 1.6]

        class crclm_incremnt:
            lin_vel_x = 0.1 # min max [m/s]
            lin_vel_y = 0.1  # min max [m/s]
            ang_vel_yaw = 0.1    # min max [rad/s]
            heading = 0.5

        waypoint_delta = 0.7

    class init_state:
        pos = [0.0, 0.0, 1.]  # x,y,z [m]
        rot = [0.0, 0.0, 0.0, 1.0]  # x,y,z,w [quat]
        lin_vel = [0.0, 0.0, 0.0]  # x,y,z [m/s]
        ang_vel = [0.0, 0.0, 0.0]  # x,y,z [rad/s]
        default_joint_angles = {  # target angles when action = 0.0
            "joint_a": 0.,
            "joint_b": 0.}

    class control:
        control_type = 'P'  # P: position, V: velocity, T: torques
        # PD Drive parameters:
        stiffness = {'joint_a': 10.0, 'joint_b': 15.}  # [N*m/rad]
        damping = {'joint_a': 1.0, 'joint_b': 1.5}  # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.5 # 放缩actions and 改变相应的clip
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4

    class asset:
        file = ""
        foot_name = "None"  # name of the feet bodies, used to index body state and contact force tensors
        penalize_contacts_on = []
        terminate_after_contacts_on = []
        disable_gravity = False
        collapse_fixed_joints = True  # merge bodies connected by fixed joints. Specific fixed joints can be kept by adding " <... dont_collapse="true">
        fix_base_link = False  # fixe the base of the robot
        default_dof_drive_mode = 3  # see GymDofDriveModeFlags (0 is none, 1 is pos tgt, 2 is vel tgt, 3 effort)
        self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter
        replace_cylinder_with_capsule = True  # replace collision cylinders with capsules, leads to faster/more stable simulation
        flip_visual_attachments = False  # Some .obj meshes must be flipped from y-up to z-up ## Notes: must false, otherwise robot collapse

        density = 0.001
        angular_damping = 0.
        linear_damping = 0.
        max_angular_velocity = 1000.
        max_linear_velocity = 1000.
        armature = 0.
        thickness = 0.01

    class domain_rand:
        randomize_friction = True
        friction_range = [0.6, 2.]
        randomize_base_mass = True
        added_mass_range = [0., 3.]
        randomize_base_com = True
        added_com_range = [-0.2, 0.2]
        push_robots = True
        push_interval_s = 8
        max_push_vel_xy = 0.5

        randomize_motor = True
        motor_strength_range = [0.8, 1.2]  # limit

        delay_update_global_steps = 24 * 8000 # for actor delay
        action_delay = False
        action_curr_step = [1, 1]
        action_curr_step_scratch = [0, 1]
        action_delay_view = 1
        action_buf_len = 8

    class rewards:
        class scales:
            # tracking rewards
            tracking_goal_vel = 1.5
            tracking_yaw = 0.5
            # regularization rewards
            lin_vel_z = -1.0
            ang_vel_xy = -0.05
            orientation = -1.
            dof_acc = -2.5e-7
            collision = -10.
            action_rate = -0.1
            delta_torques = -1.0e-7
            torques = -0.00001
            hip_pos = -0.5
            dof_error = -0.04
            feet_stumble = -1
            feet_edge = -1

        only_positive_rewards = True # if true negative total rewards are clipped at zero (avoids early termination problems)
        tracking_sigma = 0.2 # tracking reward = exp(-error^2/sigma)
        soft_dof_pos_limit = 1. # percentage of urdf limits, values above this limit are penalized
        soft_dof_vel_limit = 1
        soft_torque_limit = 0.4 # unused
        base_height_target = 1. # unused
        max_contact_force = 40. # forces above this value are penalized # unused

    # viewer camera:
    class viewer:
        ref_env = 0
        pos = [10, 0, 6]  # [m]
        lookat = [11., 5, 3.]  # [m]

    class sim:
        dt = 0.005
        substeps = 1
        gravity = [0., 0., -9.81]  # [m/s^2]
        up_axis = 1  # 0 is y, 1 is z

        class physx:
            num_threads = 10
            solver_type = 1  # 0: pgs, 1: tgs
            num_position_iterations = 4
            num_velocity_iterations = 0
            contact_offset = 0.01  # [m]
            rest_offset = 0.0  # [m]
            bounce_threshold_velocity = 0.5  # 0.5 [m/s]
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2 ** 23  # 2**24 -> needed for 8000 envs and more
            default_buffer_size_multiplier = 5
            contact_collection = 2  # 0: never, 1: last sub-step, 2: all sub-steps (default=2)

    class video_logger:
        sampled_env_id = 50
        enable_video_logger = True
        video_log_interval = 50 # 100
        video_length_in_sec = 5
        env_dt = 0.02
        canvas_size = [368, 240]

class SiruisParkourCfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.45] # x,y,z [m]
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            'LF_HAA': 0.1,  # [rad]
            'LH_HAA': 0.1,  # [rad]
            'RF_HAA': -0.1,  # [rad]
            'RH_HAA': -0.1,  # [rad]

            'LF_HFE': 0.4,  # [rad]
            'LH_HFE': -0.4,  # [rad]
            'RF_HFE': 0.4,  # [rad]
            'RH_HFE': -0.4,  # [rad]

            'LF_KFE': -1.2,  # [rad]
            'LH_KFE': 1.2,  # [rad]
            'RF_KFE': -1.2,  # [rad]
            'RH_KFE': 1.2,  # [rad]
        }

    class control(LeggedRobotCfg.control):
        control_type = 'P'
        stiffness = {'HAA': 80, "HFE": 80, "KFE": 80}  # [N*m/rad]
        damping = {'HAA': 2.0, "HFE": 2.0, "KFE": 2.0}  # [N*m*s/rad]
        action_scale = 0.5 # todo: need to tune a1: 0.25
        decimation = 4

    class asset(LeggedRobotCfg.asset):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/sirius/urdf/sirius_diff.urdf'
        foot_name = "FOOT"
        penalize_contacts_on = ["thigh", "shank", "base_link"]
        terminate_after_contacts_on = ["base_link"]
        self_collisions = 1  # 1 to disable, 0 to enable...bitwise filter

    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.45

####################################################
####################### PPO ########################
####################################################
class LeggedRobotCfgPPO(BaseConfig):
    seed = 1
    runner_class_name = 'OnPolicyRunner'

    class policy:
        init_noise_std = 1.0
        continue_from_last_std = True
        scan_encoder_dims = [128, 64, 32]
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]
        priv_encoder_dims = [64, 20]
        activation = 'elu'  # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid
        # only for 'ActorCriticRecurrent':
        rnn_type = 'lstm'
        rnn_hidden_size = 512
        rnn_num_layers = 1

        tanh_encoder_output = False

    class algorithm:
        # training params
        value_loss_coef = 1.0
        use_clipped_value_loss = True
        clip_param = 0.2
        entropy_coef = 0.01
        num_learning_epochs = 5
        num_mini_batches = 4  # mini batch size = num_envs*nsteps / nminibatches
        learning_rate = 2.e-4  # 5.e-4
        schedule = 'adaptive'  # could be adaptive, fixed
        gamma = 0.99
        lam = 0.95
        desired_kl = 0.01
        max_grad_norm = 1.
        # dagger params
        dagger_update_freq = 20
        priv_reg_coef_schedual = [0, 0.1, 2000, 3000]
        priv_reg_coef_schedual_resume = [0, 0.1, 0, 1]

    class depth_encoder:
        if_depth = LeggedRobotCfg.depth.use_camera
        depth_shape = LeggedRobotCfg.depth.resized
        buffer_len = LeggedRobotCfg.depth.buffer_len
        hidden_dims = 512
        learning_rate = 1.e-3
        num_steps_per_env = LeggedRobotCfg.depth.update_interval * 24

    class estimator:
        train_with_estimated_states = True
        learning_rate = 1.e-4
        hidden_dims = [128, 64]
        priv_states_dim = LeggedRobotCfg.env.n_priv
        num_prop = LeggedRobotCfg.env.n_proprio
        num_scan = LeggedRobotCfg.env.n_scan

    class runner:
        policy_class_name = 'ActorCritic'
        algorithm_class_name = 'PPO'
        num_steps_per_env = 24  # per iteration
        max_iterations = 10001  # number of policy updates origin: 50000, teacher:15001，student may be 15000 better, because I reduce the camera_num_envs from 192 to 64

        # logging
        save_interval = 100  # check for potential saves every this many iterations
        experiment_name = 'sirius_parkour'
        run_name = ''
        # load and resume
        resume = False
        load_run = -1  # -1 = last run
        checkpoint = -1  # -1 = last saved model
        resume_path = None  # updated from load_run and chkpt

class SiriusParkourCfgPPO( LeggedRobotCfgPPO ):
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'sirius_parkour'