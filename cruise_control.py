import pandas as pd


m_car = 300  # kg
max_F = 8000  # N
min_F = -8000  # N
delay_factor = 0.5
cda = 0.4  # drag coefficient
rf = 0.05  # rolling resistance

Kp = 2
Ki = 0.1
max_error_int = 10
target_speed_list = [50, 100, 0, 70] # km/h

dt = 0.1  # sec
responce = 5 # How often does the system respond (once per responce)
sim_time = 15  # sec
responce_period = responce * dt

target_speed_mode = 1
state_log =[]


def main():
    df = None
    error_int = 0
    state = {
        'time': 0,
        'speed': 0,
        'force': 0,
        'acc': 0,
        'force_drag': 0
    }
    count = 0
    target_speed_base = target_speed_list[count % 4]
    break_time = sim_time
    log_list = []
    score = 0
    
    current_responce = 0
    
    while count < 8:
        if state['time'] > break_time:
            break_time += sim_time
            count += 1
            target_speed_base = target_speed_list[count % 4]
        
        if state["time"]  >= current_responce:
            current_responce += responce_period
            target_speed = target_speed_base
            error = target_speed - state['speed']
            error_int += error * responce_period
            score += abs(error * responce_period)
            # error_int = max(min(error_int, max_error_int), -max_error_int)
            P_action = Kp * error
            I_action = Ki * error_int
            
            throttle = P_action + I_action
        
        target_force = throttle / 100 * max_F
        
        # car simulator
        state = sim_car(target_force, state)
        
        # log data
        log_dict = {
            **state,
            'error': error,
            'error_int': error_int,
            'P_action': P_action,
            'I_action': I_action,
            'target_force': target_force,
            'target_speed': target_speed
        }
        log_list.append(log_dict)
    
    
    
    key_list = []
    for key in log_dict.keys():
        key_list.append(key)
    pd.DataFrame(log_list, columns=key_list).to_csv("data.csv", header=key_list)
    
    print("The final score is: %f" % score)
    


def sim_car(target_force, state):
    
    # add delay factor to simulate engine
    force = state['force'] * delay_factor + target_force * (1 - delay_factor)
    force = max(min(force, max_F), min_F)
    
    velocity = state['speed'] / 3.6
    
    # drag force
    force_drag = (0.5 * 1.225 * velocity * velocity * cda + rf * m_car * 9.81) * sign(velocity)
    
    acc = (force - force_drag) / m_car
    velocity += acc * dt
    
    state['time'] += dt
    state['force'] = force
    state['speed'] = velocity * 3.6
    state['acc'] = acc
    state['force_drag'] = force_drag
    
    return state


def sign(x):
    return 1 if x >= 0 else -1


if __name__ == '__main__':
    main()
