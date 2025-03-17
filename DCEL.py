import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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
        if len(edges) < 3:
            raise ValueError("A face must have at least 3 edges.")

        face = Face(edges[0])
        print(edges)
        for i, edge in enumerate(edges):
            edge.face = face
            edge.next = edges[(i+1)%len(edges)] 
            edge.prev = edges[i-1]
        
        self.faces.append(face)        

    def create_tetrahedron(self, p1, p2, p3, p4):
        v1, v2, v3, v4 = Vertex(p1), Vertex(p2), Vertex(p3), Vertex(p4)
        self.vertices.extend([v1, v2, v3, v4])

        # Create edges for the tetrahedron (six edges in total)
        print(v1, v2, v3, v4)
        e1, e2 = self.create_edge(v1, v2)
        e3, e4 = self.create_edge(v2, v3)
        e5, e6 = self.create_edge(v3, v1)
        e7, e8 = self.create_edge(v4, v1)
        e9, e10 = self.create_edge(v4, v2)
        e11, e12 = self.create_edge(v4, v3)

        # Create faces 
        self.create_face([e1, e3, e5])  # Base: (p1, p2, p3)
        self.create_face([e2, e9, e8])  # Side 1: (p1, p2, p4)
        self.create_face([e7, e2, e10]) # Side 2: (p1, p3, p4)
        self.create_face([e4, e12, e10])# Side 3: (p2, p3, p4)

        
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ## Plot vertices
        for vertex in self.vertices:
            ax.scatter(vertex.coordinates[0], vertex.coordinates[1], vertex.coordinates[2], color='b', s=50)

        ## Plot edges
        for edge in self.edges:
            x_vals = [edge.start.coordinates[0], edge.end.coordinates[0]]
            y_vals = [edge.start.coordinates[1], edge.end.coordinates[1]]
            z_vals = [edge.start.coordinates[2], edge.end.coordinates[2]]
            ax.plot(x_vals, y_vals, z_vals, color='r')

        ## Plot faces
        for face in self.faces:
            verts = []
            edge = face.outer_edge
            first_edge = edge  ## find when we make a cycle, ie. the face is closed
            while True:
                verts.append(edge.start.coordinates)
                edge = edge.next
                if edge == first_edge:
                    break # cycle complete
                
            print(verts)
            ax.add_collection3d(Poly3DCollection([verts], edgecolor='k', alpha=.5)) 

        ## Set labels and aspect ratio
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_box_aspect([1, 1, 1])
        
        plt.show()
        
    def test_dcel(self):
        dcel = DCEL()

        # Define tetrahedron vertices
        p1 = (0, 0, 0)
        p2 = (1, 0, 0)
        p3 = (0, 1, 0)
        p4 = (0, 0, 1)

        # Construct the tetrahedron
        dcel.create_tetrahedron(p1, p2, p3, p4)

        # Print DCEL structure
        print("\nVertices:")
        for vertex in dcel.vertices:
            print(vertex.coordinates)

        print("\nEdges:")
        for edge in dcel.edges:
            print(f"Edge from {edge.start.coordinates} to {edge.end.coordinates}")

        print("\nFaces:")
        for face in self.faces:
            e = face.outer_edge
            print(f"Face with edges:")
            edge_cycle = e
            while True:
                print(f"  {edge_cycle.start.coordinates} -> {edge_cycle.end.coordinates}")
                edge_cycle = edge_cycle.next
                if edge_cycle == e:
                    break

        # Plot the DCEL
        dcel.plot()

class Edge: 
    def __init__(self, start, end, face, twin, next, prev):
        self.id = random.randint(0, 1000) # Unique identifier
        self.start = start
        self.end = end
        self.twin = None  # The opposite edge
        self.next = None  # Next edge in the face cycle
        self.prev = None  # Previous edge in the face cycle
        self.face = None  # The face that this edge belongs to
        
    def __repr__(self): ## for degbugging
        return f'Edge: ({self.start}, {self.end}) id: {self.id}'
    
    def __str__(self):
        return f'Edge: ({self.start}, {self.end})'

class Vertex:
    def __init__(self, coordinates, edge=None):
        self.coordinates = coordinates
        self.edge = edge
        
    def __repr__(self): ## for degbugging
        return f'Vertex: ({self.coordinates})'
    
    def __str__(self):
        return f'Vertex: ({self.coordinates})'

class Face:
    def __init__(self, edge):
        self.outer_edge = edge
        
    def __repr__(self): ## for degbugging
        return f'Face: {self.outer_edge})'
    
    def __str__(self):
        return f'Face: {self.outer_edge})'

# Run the test
dcel = DCEL()
dcel.test_dcel()