import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

import helpers

class DCEL:
    def __init__(self):
        """
        Initializes the DCEL object, stores, our vertices, edges, and faces
        """
        self.vertices = set()  # List of vertices
        self.edges = {}  # Hash table for edges (key: (start, end), value: Edge)
        self.faces = set()  # set of faces

    def get_or_create_vertex(self, v):
        """
        Function to get or create a vertex in the DCEL, if one already exists

        Args:
            v (Vertex): The vertex to try and find

        Returns:
            Vertex: The Vertex, either new or already in DCEL
        """
        if v in self.vertices:
            return v
        self.vertices.add(v)
        return v

    def create_face(self, points):
        """
        Make a new face from a list of points (vertices).
        Creates new half edges for this face, and uses twins if they already exist
        if not, make them.

        Args:
            points (list[Vertex]): the ordered list of vertices that make up the face

        Raises:
            ValueError: not enough points to make a face

        Returns:
            Face: A new face in the DCEL
        """
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
        """
        Remove a face from the DCEL, and remove the edges that belong to the face, if the twin is None, remove bothe edges, if not, set its half edge to None.

        Args:
            face Face: the face to remove
        """
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
        """
        Build the initial tetrahedron in the DCEL to use as a basis for the algorithm

        Args:
            p1 (Vertex): A point to use to create the initial tetrahedron
            p2 (Vertex): A point to use to create the initial tetrahedron
            p3 (Vertex): A point to use to create the initial tetrahedron
            p4 (Vertex): A point to use to create the initial tetrahedron
        """
        # Add vertices to the hull.
        self.vertices.union([p1, p2, p3, p4])
        
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
        """
        Helper method to get the vertices for a given face

        Args:
            face (Face): The face to get vertices for

        Returns:
            list[Vertex]: the ordered list of vertices from the face
        """
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
        """
        Helper method to get the edges defining a face.

        Args:
            face (Face): The face to get edges for

        Returns:
            list[Edge]: the ordered list of edges from the face
        """
        edges = []
        edge = face.outer_edge
        first_edge = edge
        while True:
            edges.append(edge)
            edge = edge.next
            if edge == first_edge:
                break
        return edges

    def plot(self, normal_mode = False):
        """
        method to plot the DCEL in matplotlib

        Args:
            normal_mode (bool, optional): A boolean flag of whether or not to show the normals of the faces. Defaults to False.
        """
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
            
            if normal_mode:
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
            else:
                for i in range(len(verts)):
                    verts[i] = verts[i].coordinates

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
    """
    Edge class to be held in the DCEL
    """
    def __init__(self, start, end, face = None, twin = None , next = None, prev = None):
        """
        Initialize availible variables

        Args:
            start (Vertex): _description_
            end (Vertex): _description_
            face (Face, optional): The incident face. Defaults to None.
            twin (Edge, optional): the twin of the half edge. Defaults to None.
            next (Edge, optional): the next edge inident on the same face. Defaults to None.
            prev (Edge, optional): the previous edge incident on the same face. Defaults to None.
        """
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
    """
    Vertex class to be held in the DCEL
    """
    def __init__(self, coordinates):
        """
        Initialize Vertex to hold a reference to an edge incident on it.
        Args:
            coordinates (Vertex): the position of the vertex
        """
        self.coordinates = coordinates
        self.x, self.y, self.z = coordinates
        self.edge = None
        
    def __repr__(self): ## for degbugging
        return f'Vertex: ({self.coordinates})'
    
    def __str__(self):
        return f'Vertex: ({self.coordinates})'

class Face:
    """
    Face class to be held in the DCEL
    """
    def __init__(self, edge):
        """
        Initialize the face to hold a edge incident on the face, any edge that refers to this face as its face

        Args:
            edge (Edge): the edge that is indicent on the face
        """
        self.outer_edge = edge
        
    def __repr__(self): ## for degbugging
        return f'Face: {self.outer_edge})'
    
    def __str__(self):
        return f'Face: {self.outer_edge})'
