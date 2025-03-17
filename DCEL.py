import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

import helpers

class DCEL:
    def __init__(self):
        self.vertices = []  # List of vertices
        self.edges = {}  # Hash table for edges (key: (start, end), value: Edge)
        self.faces = set()  # set of faces

    def get_or_create_vertex(self, v):
        for vertex in self.vertices:
            if vertex.coordinates == v.coordinates:
                return vertex  # Return existing vertex
        self.vertices.append(v)
        return v

    def get_or_create_edge(self, v1, v2):
        key = (v1.coordinates, v2.coordinates)
        twin_key = (v2.coordinates, v1.coordinates)

        # Check if the edge already exists
        if key in self.edges:
            edge = self.edges[key]  # Return existing edge
        else: 
            # Create new edges
            edge = Edge(v1, v2)
        
        if twin_key in self.edges:
            twin = self.edges[twin_key]
        else:   
            twin = Edge(v2, v1)

        edge.twin = twin
        twin.twin = edge

        # Store edges in hash table
        self.edges[key] = edge
        self.edges[twin_key] = twin

        return edge

    def create_face(self, points):
        if len(points) < 3:
            raise ValueError("A face must have at least 3 vertices.")

        ## Ensure we work with our DCEL vertices
        vertices = [self.get_or_create_vertex(p) for p in points]
        new_edges = []
        
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % len(vertices)]
            
            new_edge = Edge(v1, v2) ## make new edge
            
            twin_key = (v2.coordinates, v1.coordinates) ## check if there already is a twin, if not, make one
            if twin_key in self.edges:
                twin_edge = self.edges[twin_key]
                new_edge.twin = twin_edge
                twin_edge.twin = new_edge
            else:
                twin_edge = Edge(v2, v1)
                new_edge.twin = twin_edge
                twin_edge.twin = new_edge
            
            self.edges[(v1.coordinates, v2.coordinates)] = new_edge
            self.edges[(v2.coordinates, v1.coordinates)] = twin_edge
            new_edges.append(new_edge)
        
        for i, edge in enumerate(new_edges):
            edge.next = new_edges[(i + 1) % len(new_edges)]
            edge.prev = new_edges[i - 1]

        face = Face(new_edges[0])
        for edge in new_edges:
            edge.face = face

        self.faces.add(face)
        return face

                
    def remove_face(self, face):
        edge = face.outer_edge
        first_edge = edge
        self.faces.discard(face)  # Remove face from set   
        
        while True:
            twin_edge = edge.twin
            if (edge.start.coordinates, edge.end.coordinates) in self.edges:
                self.edges[(edge.start.coordinates, edge.end.coordinates)].face = None  # Remove edge from hash table
            
                # Check if the twin has a face, if not, remove it
                if twin_edge.face is None:
                    del self.edges[(edge.end.coordinates, edge.start.coordinates)]
                    del self.edges[(edge.start.coordinates, edge.end.coordinates)]
                            
            edge = edge.next
            if edge == first_edge:
                break  # Loop through face complete

    def create_tetrahedron(self, p1, p2, p3, p4):
        # Add vertices to the hull.
        self.vertices.extend([p1, p2, p3, p4])
        
        # Compute the centroid of the tetrahedron (strictly interior) to make sure evreything is oriented correctly
        centroid = helpers.Vector(
            (p1.x + p2.x + p3.x + p4.x) / 4.0,
            (p1.y + p2.y + p3.y + p4.y) / 4.0,
            (p1.z + p2.z + p3.z + p4.z) / 4.0
        )
        
        self.create_face(helpers.oriented_face([p1, p2, p3], centroid))  # Base face
        self.create_face(helpers.oriented_face([p1, p3, p4], centroid))  # Side face 1
        self.create_face(helpers.oriented_face([p1, p4, p2], centroid))  # Side face 2
        self.create_face(helpers.oriented_face([p2, p4, p3], centroid))  # Side face 3

        
    def get_face_vertices(self, face):
        verts = []
        edge = face.outer_edge
        first_edge = edge
        while True:
            verts.append(edge.start)
            edge = edge.next
            if edge == first_edge:
                break
        return verts

    def get_face_edges(self, face):
        edges = []
        edge = face.outer_edge
        first_edge = edge
        count = 0
        while True:
            count += 1
            if count == 6:
                print("breakpoint")
            edges.append(edge)
            edge = edge.next
            if edge == first_edge:
                break
        return edges

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

        for face in self.faces:
            verts = self.get_face_vertices(face)

            p1, p2, p3 = verts[0], verts[1], verts[2]
            v1 = helpers.Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
            v2 = helpers.Vector(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
            normal_vector = v1.cross_product(v2)
            
            for i in range(len(verts)):
                verts[i] = verts[i].coordinates
                
            centroid_face = np.mean(verts, axis=0)

            # Plot the normal vector 
            ax.quiver(centroid_face[0], centroid_face[1], centroid_face[2],
                    normal_vector.x, normal_vector.y, normal_vector.z,
                    color='g', length=10, normalize=True)

            ax.add_collection3d(Poly3DCollection([verts], edgecolor='k', alpha=.5))

        ## Set labels and aspect ratio
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_box_aspect([1, 1, 1])

        plt.show()
    
    def __repr__(self): ## for degbugging
        ret = f'DCEL: {len(self.vertices)} vertices, {len(self.edges)} edges, {len(self.faces)} faces'
        ret += '\nVertices:\n' + ',\n'.join([f"{v.coordinates}" for v in self.vertices])
        ret += '\nEdges:\n' + ',\n'.join([f"{str(e.start.coordinates)}->{str(e.end.coordinates)}" for e in self.edges.values()])
        ret += '\nFaces: ' + ', '.join([str(f) for f in self.faces])
        return ret

    def __str__(self):
        return self.__repr__()

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
        self.x, self.y, self.z = coordinates
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
