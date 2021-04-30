import pandas as pd
import plotly.graph_objs as go
import datetime
import numpy as np

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/robot_data.csv`

def prepare_data(filepath):
    """Returns cleaned and augmented data for visualization
    
        Args: 
            filepath: filepath to the dataset
        
        Returns: 
            df: dataframe of cleaned and augmented data
        
    """
    df = pd.read_csv(filepath)
    
    # convert datetimes column to datetime datatype
    df['datetimes'] = df['datetimes'].map(lambda x: datetime.datetime.strptime(x, "%d%m%y-%H:%M:%S.%f"))
    
    # create column of interval times
    intervals = np.zeros(df.shape[0])
    
    for i, dt in enumerate(df['datetimes']):
        if i == 0:
            prev_dt = dt
            continue

        intervals[i] = (intervals[i-1] + ((dt - prev_dt).microseconds / 1e6))

        prev_dt = dt
        
    # convert to series
    intervals = pd.Series(intervals)

    # create new column
    df.insert(0, "time", intervals)    
    
    # change to categorical feature
    def change_to_category(x):
        if x == 1:
            x = 'normal'
        elif x == 3:
            x = 'protective_stop'
        elif x == 8:
            x = 'violation'
        elif x == 9:
            x = 'fault'
        else:
            x = 'error'

        return x
        
    df['safety_mode'] = df['safety_mode'].apply(change_to_category)
    
    
    # get accelerations
    base_acc = np.zeros(df.shape[0])
    shoulder_acc = np.zeros(df.shape[0])
    elbow_acc = np.zeros(df.shape[0])
    wrist1_acc = np.zeros(df.shape[0])
    wrist2_acc = np.zeros(df.shape[0])
    wrist3_acc = np.zeros(df.shape[0])

    def get_acceleration(array, joint):
        for i, vel in enumerate(df[f'actual_qd_{joint}']):
            if i == 0:
                prev_vel = vel
                continue

            d_time = df['time'][i] - df['time'][i-1]
            
            if d_time == 0.0:
                d_time = 0.008
                
            d_vel = vel - prev_vel

            acc = d_vel / d_time

            array[i] = acc

            prev_vel = vel

        return array

    base_acc_series = pd.Series(get_acceleration(base_acc, 0))
    shoulder_acc_series = pd.Series(get_acceleration(shoulder_acc, 1))
    elbow_acc_series = pd.Series(get_acceleration(elbow_acc, 2))
    wrist1_acc_series = pd.Series(get_acceleration(wrist1_acc, 3))
    wrist2_acc_series = pd.Series(get_acceleration(wrist2_acc, 4))
    wrist3_acc_series = pd.Series(get_acceleration(wrist3_acc, 5))
    
    df.insert(13, 'actual_qdd_0', base_acc_series)
    df.insert(14, 'actual_qdd_1', shoulder_acc_series)
    df.insert(15, 'actual_qdd_2', elbow_acc_series)
    df.insert(16, 'actual_qdd_3', wrist1_acc_series)
    df.insert(17, 'actual_qdd_4', wrist2_acc_series)
    df.insert(18, 'actual_qdd_5', wrist3_acc_series)
    
    # drop unwanted columns, also drop datetimes
    df.drop(['datetimes', 'robot_mode'], axis=1, inplace=True)
    
    # drop duplicated data
    df = df.drop_duplicates()
    
    return df



def return_figures(df):
    """Creates four plotly visualizations

    Args:
        df: dataframe of cleaned and augmented data

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    
    time = df['time'].tolist()

    # first chart plots joint currents vs time as a line chart
    
    graph_one = []
    
    
    graph_one.append([
        
        go.Scatter(
            x = time,
            y = df['actual_current_0'].tolist(),
            mode = 'lines',
            name = 'Slide'),
        go.Scatter(
            x = time,
            y = df['actual_current_1'].tolist(),
            mode = 'lines',
            name = 'Lower'),
        go.Scatter(
            x = time,
            y = df['actual_current_2'].tolist(),
            mode = 'lines',
            name = 'Upper'),
        go.Scatter(
            x = time,
            y = df['actual_current_3'].tolist(),
            mode = 'lines',
            name = 'Rotation'),
        go.Scatter(
            x = time,
            y = df['actual_current_4'].tolist(),
            mode = 'lines',
            name = 'Bend'),
        go.Scatter(
            x = time,
            y = df['actual_current_5'].tolist(),
            mode = 'lines',
            name = 'Twist')
      
       
        ])

    layout_one = dict(title = 'Graph of Joint Currents vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Joint Currents (A)'),
                     )
    
    # second chart plots joint voltages vs time as a line chart
    graph_two = []
      
    graph_two.append([
        
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_0'].tolist(),
            mode = 'lines',
            name = 'Slide'),
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_1'].tolist(),
            mode = 'lines',
            name = 'Lower'),
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_2'].tolist(),
            mode = 'lines',
            name = 'Upper'),
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_3'].tolist(),
            mode = 'lines',
            name = 'Rotation'),
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_4'].tolist(),
            mode = 'lines',
            name = 'Bend'),
        go.Scatter(
            x = time,
            y = df['actual_joint_voltage_5'].tolist(),
            mode = 'lines',
            name = 'Twist')
      
       
    ])

    layout_two = dict(title = 'Graph of Joint Voltages vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Joint Voltages (A)'),
                     )
    
    # third chart plots joint temperatures vs time as a line chart
    graph_three = []
    
    graph_three.append([
        
        go.Scatter(
            x = time,
            y = df['joint_temperatures_0'].tolist(),
            mode = 'lines',
            name = 'Slide'),
        go.Scatter(
            x = time,
            y = df['joint_temperatures_1'].tolist(),
            mode = 'lines',
            name = 'Lower'),
        go.Scatter(
            x = time,
            y = df['joint_temperatures_2'].tolist(),
            mode = 'lines',
            name = 'Upper'),
        go.Scatter(
            x = time,
            y = df['joint_temperatures_3'].tolist(),
            mode = 'lines',
            name = 'Rotation'),
        go.Scatter(
            x = time,
            y = df['joint_temperatures_4'].tolist(),
            mode = 'lines',
            name = 'Bend'),
        go.Scatter(
            x = time,
            y = df['joint_temperatures_5'].tolist(),
            mode = 'lines',
            name = 'Twist')  
    ])

    layout_three = dict(title = 'Graph of Joint Temperatures vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Joint Temperatures (degC)'),
                     )
    
    # fourth chart plots joint speeds vs time as a line chart
    graph_four = []
    
    graph_four.append([
        
        go.Scatter(
            x = time,
            y = df['actual_qd_0'].tolist(),
            mode = 'lines',
            name = 'Slide'),
        go.Scatter(
            x = time,
            y = df['actual_qd_1'].tolist(),
            mode = 'lines',
            name = 'Lower'),
        go.Scatter(
            x = time,
            y = df['actual_qd_2'].tolist(),
            mode = 'lines',
            name = 'Upper'),
        go.Scatter(
            x = time,
            y = df['actual_qd_3'].tolist(),
            mode = 'lines',
            name = 'Rotation'),
        go.Scatter(
            x = time,
            y = df['actual_qd_4'].tolist(),
            mode = 'lines',
            name = 'Bend'),
        go.Scatter(
            x = time,
            y = df['actual_qd_5'].tolist(),
            mode = 'lines',
            name = 'Twist')  
    ])

    layout_four = dict(title = 'Graph of Joint Velocities vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Joint Velocities(rad/s)'),
                     )
    
    # fifth chart plots joint accelerations vs time as a line chart
    graph_five = []
    
    graph_five.append([
        
        go.Scatter(
            x = time,
            y = df['actual_qdd_0'].tolist(),
            mode = 'lines',
            name = 'Slide'),
        go.Scatter(
            x = time,
            y = df['actual_qdd_1'].tolist(),
            mode = 'lines',
            name = 'Lower'),
        go.Scatter(
            x = time,
            y = df['actual_qdd_2'].tolist(),
            mode = 'lines',
            name = 'Upper'),
        go.Scatter(
            x = time,
            y = df['actual_qdd_3'].tolist(),
            mode = 'lines',
            name = 'Rotation'),
        go.Scatter(
            x = time,
            y = df['actual_qdd_4'].tolist(),
            mode = 'lines',
            name = 'Bend'),
        go.Scatter(
            x = time,
            y = df['actual_qdd_5'].tolist(),
            mode = 'lines',
            name = 'Twist')  
    ])

    layout_five = dict(title = 'Graph of Joint Accelerations vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Joint Accelerations(rad/s2)'),
                     )
    
    # sixth chart plots tcp force vs time as a line chart
    graph_six = []
    
    graph_six.append(
        
        go.Scatter(
            x = time,
            y = df['tcp_force_scalar'].tolist(),
            mode = 'lines',
            name = 'force')
    )

    layout_six = dict(title = 'Graph of TCP Force vs Time',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'TCP Force(N)'),
                     )
    

    # seventh chart plots percentage of the different'safety mode' occurrences as a bar chart    
    graph_seven = []
    
    classes = df['safety_mode'].unique()
    
    safety_mode_list = []
    
    for label in classes:
        safety_mode_list.append(len(df[df['safety_mode']==label]) / len(df) * 100)

    graph_seven.append(
      go.Bar(
      x = classes,
      y = safety_mode_list,
      )
    )

    layout_seven = dict(title = 'Safety Mode Types Occurrence (%)',
                        xaxis = dict(title = 'Safety Mode Type',),
                        yaxis = dict(title = 'Occurrence (%)'),
                        )

    # eigth chart plots occurrence of protective stops vs time    
    graph_eight = []
    
    df = pd.get_dummies(df, columns=['safety_mode'])
    
    safety_mode_list = []
    

    graph_eight.append(
        
        go.Scatter(
            x = time,
            y = df['safety_mode_protective_stop'].tolist(),
            mode = 'lines',
            name = 'P.S.')
    )


    layout_eight = dict(title = 'Protective Stop Occurrences',
                        xaxis = dict(title = 'Time',),
                        yaxis = dict(title = 'Occurrence'),
                        )

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one[0], layout=layout_one))
    figures.append(dict(data=graph_two[0], layout=layout_two))
    figures.append(dict(data=graph_three[0], layout=layout_three))
    figures.append(dict(data=graph_four[0], layout=layout_four))
    figures.append(dict(data=graph_five[0], layout=layout_five))
    # only 1 scatter plot in graph 6, so no need to index 0
    figures.append(dict(data=graph_six, layout=layout_six))
    # only 1 bar plot
    figures.append(dict(data=graph_seven, layout=layout_seven))
    # only 1 scatter plot
    figures.append(dict(data=graph_eight, layout=layout_eight))

    return figures
