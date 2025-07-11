'''
@Author  ：skywoodsz
@Date    ：2025/7/11 17:29 
'''
import torch
import torch.optim as optim
from rsl_rl.modules import *
from copy import copy, deepcopy

def play():
    load_teacher_path = "../../logs/parkour_new/aaa-gg/model_15000.pt"
    load_student_path = "../../logs/parkour_new/bbb-kk-sirius_student_pitch_down_camera/model_10000.pt"
    save_cat_path = "../../logs/parkour_new/model_0.pt"


    n_priv_explicit = 3 + 3 + 3
    n_priv_latent = 4 + 1 + 12 + 12
    num_scan = 132
    num_actions = 12
    n_proprio = 3 + 2 + 3 + 4 + 36 + 4 + 1
    history_len = 10
    num_obs = n_proprio + num_scan + history_len * n_proprio + n_priv_latent + n_priv_explicit

    depth_resized = (87, 58)
    device = torch.device('cuda:0')

    policy_cfg = {
        'init_noise_std': 1.0,
        'continue_from_last_std': True,
        'scan_encoder_dims': [128, 64, 32],
        'actor_hidden_dims': [512, 256, 128],
        'critic_hidden_dims': [512, 256, 128],
        'priv_encoder_dims': [64, 20],
        'activation': 'elu',
        'rnn_type': 'lstm',
        'rnn_hidden_size': 512,
        'rnn_num_layers': 1,
        'tanh_encoder_output': False
    }

    estimator_cfg = {
        "train_with_estimated_states": True,
        "learning_rate": 1e-4,
        "hidden_dims": [128, 64],
        "priv_states_dim": n_priv_explicit,
        "num_prop": n_proprio,
        "num_scan": num_scan
    }

    depth_encoder_cfg = {
        "if_depth": True,
        "depth_shape": depth_resized,
        "buffer_len": 2,
        "hidden_dims": 512,
        "learning_rate": 1e-3,
        "num_steps_per_env": 5 * 24
    }

    cfg = {
        "policy_class_name": "ActorCritic",
        "algorithm_class_name": "PPO",
        "num_steps_per_env": 24,
        "max_iterations": 15001,

        # logging
        "save_interval": 100,
        "experiment_name": "sirius_parkour",
        "run_name": "",

        # resume / checkpoint
        "resume": False,
        "load_run": -1,
        "checkpoint": -1,
        "resume_path": None
    }

    teacher_policy_actor_critic : ActorCriticRMA = ActorCriticRMA(n_proprio,
                                                      num_scan,
                                                      num_obs,
                                                      n_priv_latent,
                                                      n_priv_explicit,
                                                      history_len,
                                                      num_actions,
                                                      **policy_cfg).to(device)
    teacher_policy_estimator = Estimator(input_dim=n_proprio, output_dim=n_priv_explicit,
                          hidden_dims=[128, 64]).to(device)
    teacher_optimizer = optim.Adam(teacher_policy_actor_critic.parameters(), lr=1e-3)

    depth_backbone = DepthOnlyFCBackbone58x87(None,
                                              32,
                                              512
                                              )
    student_depth_encoder = RecurrentDepthBackbone(depth_backbone, None).to(device)
    student_depth_actor = deepcopy(teacher_policy_actor_critic.actor)

    print(f"Loading teacher model from: {load_teacher_path}")
    teacher_loaded_dict = torch.load(load_teacher_path, map_location=device)
    teacher_policy_actor_critic.load_state_dict(teacher_loaded_dict['model_state_dict'])
    teacher_policy_estimator.load_state_dict(teacher_loaded_dict['estimator_state_dict'])
    teacher_optimizer.load_state_dict(teacher_loaded_dict['optimizer_state_dict'])

    print(f"Loading student model from: {load_student_path}")
    student_loaded_dict = torch.load(load_student_path, map_location=device)
    student_depth_encoder.load_state_dict(student_loaded_dict['depth_encoder_state_dict'])
    student_depth_actor.load_state_dict(student_loaded_dict['depth_actor_state_dict'])

    state_dict = {
        'model_state_dict': teacher_policy_actor_critic.state_dict(),
        'estimator_state_dict': teacher_policy_estimator.state_dict(),
        'optimizer_state_dict': teacher_optimizer.state_dict(),
        'depth_encoder_state_dict': student_depth_encoder.state_dict(),
        'depth_actor_state_dict': student_depth_actor.state_dict()
    }

    torch.save(state_dict, save_cat_path)

    print("Finished saving models.")

if __name__ == "__main__":
    play()