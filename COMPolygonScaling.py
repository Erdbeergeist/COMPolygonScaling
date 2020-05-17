import numpy as np
import matplotlib.pyplot as plt

class polygon():

    def __init__(self, nodes):

        #((x1,y1),...,(xn,yn))
        self.nodes = np.array(nodes)
        self.com = self.calculate_com(self.nodes)
        self.t_matrix = self.get_transformation_matrix()
        self.com_node_distances = self.calculate_com_nodes_distances()
        self.create_figure()

    def l2_distance(self, p1, p2):
        return np.sqrt(np.sum([(p1[i] - p2[i])**2 for i in range(len(p1))]))

    def calculate_com_nodes_distances(self):
        return np.array([self.l2_distance(self.com, node) for node in self.nodes])

    def calculate_com(self, nodes):
        return np.sum(nodes, axis = 0)/nodes.shape[0]

    def get_transformation_matrix(self):

        self.com = self.calculate_com(self.nodes)
        slopes = (self.nodes[...,1] - self.com[1]) / (self.nodes[...,0] - self.com[0])
        offsets = self.nodes[...,1] - slopes * self.nodes[...,0]
        # (slope, offset)
        self.t_matrix = np.column_stack((slopes, offsets))

        return self.t_matrix

    def update_nodes(self, new_nodes):

        self.nodes = new_nodes
        self.com = calculate_com(self.nodes)
        self.t_matrix = self.t_matrix


    def get_scaled_nodes(self, scaling, plot = False):
        #We solve the following equation for the new x coordinate on the line
        #connecting the com and the node, with the condition that the
        #new_com_node_l2_distance = scaling * old_com_node_l2_distance
        new_nodes = []
        for i, node in enumerate(self.nodes):
            slope = self.t_matrix[i, 0]
            offset = self.t_matrix[i, 1]
            old_distance = self.com_node_distances[i]
            cx = self.com[0]
            cy = self.com[1]
            if cx >= node[0]:
                xnew = (2*cx - 2*offset*slope + 2*cy*slope
                    - np.sqrt((-2*cx + 2*slope*offset -2*cy*slope)**2 - 4*(1+slope**2)
                    * (offset**2 + cx**2 - 2*offset*cy + cy**2 - old_distance**2 * scaling**2)))/(2*(1+slope**2))
            else:
                xnew = (2*cx - 2*offset*slope + 2*cy*slope
                    + np.sqrt((-2*cx + 2*slope*offset -2*cy*slope)**2 - 4*(1+slope**2)
                    * (offset**2 + cx**2 - 2*offset*cy + cy**2 - old_distance**2 * scaling**2)))/(2*(1+slope**2))
            ynew = slope * xnew + offset
            new_nodes.append([xnew, ynew])
        new_nodes = np.array(new_nodes)

        if plot:
            self.ax.plot(new_nodes[...,0], new_nodes[...,1], 'bo--')
            self.ax.plot([new_nodes[-1][0], new_nodes[0][0]], [new_nodes[-1][1], new_nodes[0][1]], 'bo--')
        return new_nodes

    def plot_polygon(self, close_polygon = False):

        self.line = self.ax.plot(self.nodes[...,0], self.nodes[...,1], 'bo-')
        self.line_end = self.ax.plot([self.nodes[-1][0], self.nodes[0][0]], [self.nodes[-1][1], self.nodes[0][1]], 'bo-')
        self.com_line = self.ax.plot(self.com[0], self.com[1], 'ro-')

    def plot_com_rays(self):

        self.get_transformation_matrix()
        xmin = 0.8 * np.min(self.nodes[...,0])
        xmax = 1.1 * np.max(self.nodes[...,0])
        self.ray_endpoints = np.array([[xmin, slope_offset[0] * xmin + slope_offset[1]] if self.nodes[i,0] <= self.com[0] else [xmax, slope_offset[0] * xmax + slope_offset[1]] for i, slope_offset in enumerate(self.t_matrix)])
        self.ray_lines = [self.ax.plot(np.append(self.com[0], ray_points[0]), np.append(self.com[1], ray_points[1]), 'r') for ray_points in self.ray_endpoints]

    def create_figure(self):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def show_fig(self):
        plt.show()
