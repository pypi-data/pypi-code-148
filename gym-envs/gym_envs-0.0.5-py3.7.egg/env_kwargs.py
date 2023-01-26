kwargs_dicts = {
    'widowx_reacher-v250': {
        'random_position' : False,
        'random_orientation': False,
        'moving_target': False,
        'target_type': "sphere",
        'goal_oriented' : False,
        'obstacle': None,
        'obs_type' : 1,
        'reward_type' : 1,
        'action_type' : 1,
        'joint_limits' : "large",
        'action_min': [-1, -1, -1, -1, -1, -1],
        'action_max': [1, 1, 1, 1, 1, 1],
        'alpha_reward': 0.1,
        'reward_coeff': 1,
        'lidar': False,
        'camera_sensor': False,
        'frame_skip': 5,
        'pybullet_action_coeff': 1,
        'widowx_type': "normal"
        }

}
