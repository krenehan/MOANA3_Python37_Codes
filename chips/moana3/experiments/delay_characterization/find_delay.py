from includes import *

def find_delay(t, y1, y2):
    
    y = (y1, y2)
    
    # Check input length
    if len(y) != 2:
        raise Exception("y must be a touple of 2 curves")
        
    # Check that t matches y
    if len(y[0]) != len(t):
        raise Exception("y and t must be of equal length")
    
    # Half max value
    y_hm = [max(y[i]) / 2 for i in range(2)]
    
    # Get the point first point where the data crosses
    y_val_after_rise = [y[i][np.where(y[i]>y_hm[i])][0] for i in range(2)]
    y_val_before_fall = [y[i][np.where(y[i]>=y_hm[i])][-1] for i in range(2)]
    
    # Find the index of those two points
    y_idx_after_rise = [np.where(np.isclose(y[i], y_val_after_rise[i])==True)[0][0] for i in range(2)]
    y_idx_before_fall = [np.where(np.isclose(y[i], y_val_before_fall[i])==True)[0][0] for i in range(2)]
    
    # Get the index of the other two points
    y_idx_before_rise = [y_idx_after_rise[i] - 1 for i in range(2)]
    y_idx_after_fall = [y_idx_before_fall[i] + 1 for i in range(2)]
    
    # Get the values of these points
    y_val_before_rise = [y[i][y_idx_before_rise[i]] for i in range(2)]
    y_val_after_fall = [y[i][y_idx_after_fall[i]] for i in range(2)]
    
    # Get the times associated with these points
    t_before_rise = [t[y_idx_before_rise[i]] for i in range(2)]
    t_after_rise = [t[y_idx_after_rise[i]] for i in range(2)]
    t_before_fall = [t[y_idx_before_fall[i]] for i in range(2)]
    t_after_fall = [t[y_idx_after_fall[i]] for i in range(2)]
    
    # Find time of crossing the y_hm
    m_rise = [(y_val_after_rise[i] - y_val_before_rise[i]) / (t_after_rise[i] - t_before_rise[i]) for i in range(2)]
    t_rise = [(y_hm[i] - y_val_before_rise[i]) / m_rise[i] + t_before_rise[i] for i in range(2)]
    
    # Find time of falling edge crossing the y_hm
    # m_fall = (y_val_before_fall - y_val_after_fall) / (t_before_fall - t_after_fall)
    # t_fall = (y_hm - y_val_before_fall) / m_fall + t_before_fall
    
    # Calculate delay
    delay = t_rise[1] - t_rise[0]
    return delay


def mean_time(t, y1, y2):
    
    y = (y1, y2)
    
    # Calculate mean time of each curve
    mt = [np.average(t, weights=y[i]) for i in range(2)]
    
    delay = mt[1] - mt[0]
    return delay