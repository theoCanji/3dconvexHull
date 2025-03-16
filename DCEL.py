import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class DCEL:
    def __init__(self):
        self.vertices = [] #vertex, coordinates, edge
        self.edges = [] 
        self.faces = [] #face, edge
    
    def create_edge(self, v1, v2):
        # edge, start, end, face, twin, next, prev
        # need to create a new edge and its twin and update the next and prev pointers for both faces
        edge1 = Edge(v1, v2, None, None, None, None)
        edge2 = Edge(v2, v1, None, None, None, None)

        edge1.twin = edge2
        edge2.twin = edge1

        self.edges.append(edge1)  
        self.edges.append(edge2)

        return edge1, edge2
    
    def create_face(self, edges):
        face = Face(edges[0])
        for i, edge in enumerate(edges):
            edge.face = face
            edge.next = edges[(i+1)%len(edges)] 
            edge.prev = edges[i-1]
        
        self.faces.append(face)

    #def create_twins():
        

    def create_tetrahedron(self, p1, p2, p3, p4):
        # Create vertices for the tetrahedron
        v1 = Vertex(p1, None)
        v2 = Vertex(p2, None)
        v3 = Vertex(p3, None)
        v4 = Vertex(p4, None)
        self.vertices.extend([v1, v2, v3, v4])

        # Create edges for the tetrahedron (six edges in total)
        e1, e2 = self.create_edge(v1, v2)
        e3, e4 = self.create_edge(v2, v3)
        e5, e6 = self.create_edge(v3, v1)
        e7, e8 = self.create_edge(v1, v4)
        e9, e10 = self.create_edge(v2, v4)
        e11, e12 = self.create_edge(v3, v4)
        
        # Create faces using the edges
        self.create_face([e1, e3, e5])  # Face 1 (p1, p2, p3)
        self.create_face([e2, e4, e6])  # Face 2 (p2, p3, p1)
        self.create_face([e1, e7, e9])  # Face 3 (p1, p2, p4)
        self.create_face([e3, e5, e11])  # Face 4 (p3, p1, p4)



class Edge: 
    def __init__(self, start, end, face, twin, next, prev):
        self.start = start
        self.end = end
        self.twin = None  # The opposite edge
        self.next = None  # Next edge in the face cycle
        self.prev = None  # Previous edge in the face cycle
        self.face = None  # The face that this edge belongs to


class Vertex:
    def __init__(self, coordinates, edge):
        self.coordinates = coordinates
        self.edge = edge

class Face:
    def __init__(self, edge):
        self.outer_edge = edge



# Function to plot the tetrahedron
def plot_tetrahedron():
    # Define 4 points in 3D space (the vertices of the tetrahedron)
    p1 = (0, 0, 0)
    p2 = (1, 0, 0)
    p3 = (0, 1, 0)
    p4 = (0, 0, 1)
    
    # List of vertices
    vertices = [p1, p2, p3, p4]
    
    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the vertices
    ax.scatter([v[0] for v in vertices], 
               [v[1] for v in vertices], 
               [v[2] for v in vertices], color='b', s=100)
    
    # Labels for the vertices
    for i, (x, y, z) in enumerate(vertices):
        ax.text(x, y, z, f'V{i+1}', color='r', fontsize=12)

    # Define the edges (pairs of vertices)
    edges = [
        (p1, p2), (p2, p3), (p3, p1),  # Triangle face 1
        (p1, p4), (p2, p4), (p3, p4)   # Triangle face 2
    ]
    
    # Plot the edges
    for edge in edges:
        x_vals = [edge[0][0], edge[1][0]]
        y_vals = [edge[0][1], edge[1][1]]
        z_vals = [edge[0][2], edge[1][2]]
        ax.plot(x_vals, y_vals, z_vals, color='g')
    
    # Set the labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set equal scaling for all axes
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    
    # Show the plot
    plt.show()

# Call the function to plot the tetrahedron
plot_tetrahedron()
