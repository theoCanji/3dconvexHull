import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class DCEL:
    def __init__(self):
        self.vertices = []  # List of vertices
        self.edges = {}  # Hash table for edges (key: (start, end), value: Edge object)
        self.faces = []  # List of faces

    def get_or_create_vertex(self, coordinates):
        for vertex in self.vertices:
            if vertex.coordinates == coordinates:
                return vertex  # Return existing vertex
        v = Vertex(coordinates)
        self.vertices.append(v)
        return v

    def get_or_create_edge(self, v1, v2):
        key = (v1.coordinates, v2.coordinates)
        twin_key = (v2.coordinates, v1.coordinates)

        # Check if the edge already exists
        if key in self.edges:
            return self.edges[key]  # Return existing edge

        # Create new edges
        edge = Edge(v1, v2)
        twin = Edge(v2, v1)

        edge.twin = twin
        twin.twin = edge

        # Store edges in hash table
        self.edges[key] = edge
        self.edges[twin_key] = twin

        return edge

    def create_face(self, points): # assume points are in ccw order
        if len(points) < 3:
            raise ValueError("A face must have at least 3 vertices.")

        vertices = [self.get_or_create_vertex(p) for p in points]

        edges = []
        for i in range(len(vertices)):
            v1, v2 = vertices[i], vertices[(i + 1) % len(vertices)]
            edge = self.get_or_create_edge(v1, v2)
            edges.append(edge)

        # Create and assign face
        face = Face(edges[0])  
        for i in range(len(edges)):
            edges[i].face = face
            edges[i].next = edges[(i + 1) % len(edges)]
            edges[i].prev = edges[i - 1]

        self.faces.append(face)

        # Update twin edges if their face was previously None
        for edge in edges:
            if edge.twin.face is None:
                edge.twin.face = face  # Assign adjacent face     

    def create_tetrahedron(self, p1, p2, p3, p4):
        v1, v2, v3, v4 = Vertex(p1), Vertex(p2), Vertex(p3), Vertex(p4)
        self.vertices.extend([v1, v2, v3, v4])

        self.create_face([p1, p2, p3])  # Base face
        self.create_face([p1, p3, p4])  # Side face 1
        self.create_face([p1, p4, p2])  # Side face 2
        self.create_face([p2, p4, p3])  # Side face 3

        
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ## Plot vertices
        for vertex in self.vertices:
            ax.scatter(vertex.coordinates[0], vertex.coordinates[1], vertex.coordinates[2], color='b', s=50)

        ## Plot edges
        for edge in self.edges.values():
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
        for edge in dcel.edges.values():
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
    def __init__(self, start, end, face = None, twin = None , next = None, prev = None):
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
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.edge = None
        
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