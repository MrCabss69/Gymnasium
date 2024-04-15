import plotly.graph_objects as go

class Renderer:
    def __init__(self, window_size):
        self.window_size = window_size
        self.fig = go.Figure()

    def render(self, trajectory, initial_pos, target_pos, wind_speed, wind_direction):
        # Plot trajectory
        if trajectory:
            self.fig.add_trace(go.Scatter(x=[pos[0] for pos in trajectory],
                                     y=[pos[1] for pos in trajectory],
                                     mode='lines+markers',
                                     name='Trajectory'))
        
        # Plot initial and target positions
        self.fig.add_trace(go.Scatter(x=[initial_pos[0], target_pos[0]],
                                 y=[initial_pos[1], target_pos[1]],
                                 mode='markers',
                                 marker=dict(size=[10, 15], color=['red', 'green']),
                                 name='Start & Target'))

        # Add wind direction indicator
        self.fig.add_annotation(x=initial_pos[0], y=initial_pos[1],
                           text=f'Wind: {wind_speed:.1f} m/s @{wind_direction:.0f}°',
                           showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='lightblue')

        # Update layout
        self.fig.update_layout(title='Projectile Trajectory Simulation',
                          xaxis_title='X Position',
                          yaxis_title='Y Position',
                          width=600, height=600)
        self.fig.show()

