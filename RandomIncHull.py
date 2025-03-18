from collections import deque
import helpers
from DCEL import DCEL, Vertex
import random

class RandomIncrementalHull3D:
    def __init__(self, points):
        self.points = list(map(lambda x: Vertex(x), points))
        self.hull = DCEL()
        random.shuffle(points)
        self.conflict_faces = {} ## face: [vertices that use it as a conflict face]
        self.conflict_vertices = {} ## vertex: [face]
        self.hull.create_tetrahedron(self.points[0], self.points[1], self.points[2], self.points[3])
        self.needs_update = []
        self.new_faces = []

        for point in self.points[4:]:
            self.get_conflicts(point, self.hull.faces)
        
        count = 0
        for point in self.points[4:]:
            count += 1
            self.add_point(point)

        self.hull.plot()

    def get_conflicts(self, point, faces):
        conflict_found = False
        for face in faces:
            verts = self.hull.get_face_vertices(face)
            if helpers.determine_visibility(verts[0], verts[1], verts[2], point):
                self.conflict_vertices[point] = face
                if face in self.conflict_faces:
                    self.conflict_faces[face].append(point)
                else:
                    self.conflict_faces[face] = [point]
                conflict_found = True
                break
        if not conflict_found:
            self.conflict_vertices[point] = None

                    
    def add_point(self, point):
        if point not in self.conflict_vertices or self.conflict_vertices[point] is None:
            return ## point is not in conflict, so it is indside the hull
        
        face = self.conflict_vertices[point]
        horizon = self.get_horizon(face, point)
        for edge in horizon:
            self.new_faces.append(self.hull.create_face([edge.start, edge.end, point]))
        
        for pointi in self.needs_update:
            self.get_conflicts(pointi, self.new_faces)
            
        self.needs_update = []
        self.new_faces = []

    def get_horizon(self, face, point):
        horizon_edges = set()  
        visited_faces = set()  # explored faces
        queue = deque()  
        to_remove = []

        # Start BFS from first visible face
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