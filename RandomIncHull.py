from collections import deque
import helpers
from DCEL import DCEL, Vertex
import random

class RandomIncrementalHull3D:
    def __init__(self, points):
        """
        Initializes the Random Incremental Hull object and creates the hull

        Args:
            points (3 dimensional tuples): A list of points that the user wants a hull made from
        """
        self.points = list(map(lambda x: Vertex(x), points))
        self.hull = DCEL()
        random.shuffle(points) ## randomized insertion order
        self.conflict_faces = {} ## face: [vertices that use it as a conflict face]
        self.conflict_vertices = {} ## vertex: [face]
        self.hull.create_tetrahedron(self.points[0], self.points[1], self.points[2], self.points[3])
        self.needs_update = []
        self.new_faces = []

        self.get_conflicts(self.points[4:], self.hull.faces)
        
        for point in self.points[4:]: 
            self.add_point(point)
            
    def get_hull(self):
        """
        Function to get the DCEL hull from the Object itself

        Returns:
            DCEL: The DCEL representing the hull
        """
        return self.hull

    def plot(self):
        """
        Function to plot the hull from the Object itself
        """
        self.hull.plot()
        
    def get_conflicts(self, points, faces):
        """
        A function to update the conlict graph with new faces and vertices

        Args:
            points (List(Vetex)): The list of points that need new conflict faces
            faces (List): The list of new faces that replaced the old faces of the above points
        """
        points = set(points) ## O(n) for O(1) removal
        for face in faces:
            verts = self.hull.get_face_vertices(face)
            points_to_remove = []
            for point in points:
                if helpers.determine_visibility(verts[0], verts[1], verts[2], point):
                    self.conflict_vertices[point] = face
                    if face in self.conflict_faces:
                        self.conflict_faces[face].append(point)
                    else:
                        self.conflict_faces[face] = [point]
                    points_to_remove.append(point)
            for point in points_to_remove:
                points.remove(point)
        for point in points:
            self.conflict_vertices[point] = None

                    
    def add_point(self, point):
        """
        A function to add a point to the hull incrementally, finding the horizon, and forming new faces
        with every point on the horizon with the new point

        Args:
            point (Vertex): The next point to incrementally add to the hull

        Returns:
            None: No return type, simply updates the DCEL representing the hull
        """
        if point not in self.conflict_vertices or self.conflict_vertices[point] is None:
            self.hull.get_or_create_vertex(point)
            return ## point is not in conflict, so it is indside the hull
        
        face = self.conflict_vertices[point]
        horizon = self.get_horizon(face, point)
        for edge in horizon:
            self.new_faces.append(self.hull.create_face([edge.start, edge.end, point]))
        

        self.get_conflicts(self.needs_update, self.new_faces)
            
        self.needs_update = []
        self.new_faces = []

    def get_horizon(self, face, point):
        """
        Finds the horizon of visibility for a given point in the hull and removes the faces within
        the horizon to prepare for the addition of new faces

        Args:
            face (Face): The first face found in the visibility graph for the point
            point (Vertex): The point to add to the hull, to find the horizon of its visibility

        Returns:
            List: A not neccesarly ordered list of edges that form the horizon of the visibility of the point
        """
        horizon_edges = set()  
        visited_faces = set()  # explored faces
        queue = deque()  
        to_remove = []

        # Start BFS from first visible face (from conflict graph)
        queue.append(face)
        visited_faces.add(face)
        while queue:
            face = queue.popleft()
            edges = self.hull.get_face_edges(face)
            visited_count = 0
            for edge in edges:
                twin_face = edge.twin.face
                if twin_face is not None:
                    p1,p2,p3 = self.hull.get_face_vertices(twin_face)
                    next_vis = helpers.determine_visibility(p1,p2,p3, point)
                else:
                    next_vis = False
                
                if twin_face is None or not next_vis:  # It's a boundary edge or we can't see it
                    horizon_edges.add(edge)
                    if face in self.conflict_faces:
                        self.needs_update += self.conflict_faces[face]
                    to_remove.append(face)
                    
                elif twin_face not in visited_faces and next_vis:
                    queue.append(twin_face)
                    visited_faces.add(twin_face)
                    if face in self.conflict_faces:
                        self.needs_update += self.conflict_faces[face]
                    to_remove.append(face)
                else:
                    visited_count += 1
                    if visited_count == 3: # stranded face
                        if face in self.conflict_faces:
                            self.needs_update += self.conflict_faces[face]
                        to_remove.append(face)
            
        for face in to_remove:
            if face in self.conflict_faces:
                del self.conflict_faces[face]
            self.hull.remove_face(face)
        return list(horizon_edges)

RandomIncrementalHull3D(helpers.generate_random_points(100))