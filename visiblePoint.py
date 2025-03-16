import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define the vector class
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot_product(self, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z  

    def cross_product(self, v2):
        return Vector(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )

def determine_visibility(p1, p2, p3, q):
    # Compute vectors on the plane
    v1 = Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    v2 = Vector(p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
    
    normal_vector = Vector.cross_product(v1, v2)
    #double check the normal vector is correct
    query_vector = Vector(q.x-p1.x, q.y-p1.y, q.z-p1.z)
    dot_product = Vector.dot_product(query_vector, normal_vector)
    if dot_product > 0:
        return True
    else:
        return False


# Define the vertices of a polygon (half-plane)
# These are the vertices in 2D
x = np.array([1, 4, 4, 1])
y = np.array([1, 1, 4, 4])

# assign z value for 3D display
z = np.array([1,2,2,1])

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#plot the point


#create vectors 
q = Vector(2-x[0],8-y[0],-4-z[0]) # query point
v1 = Vector(x[1]-x[0], y[1]-y[0], z[1]-z[0]) # vector from point 1 to point 2
v2 = Vector(x[2]-x[0], y[2]-y[0], z[2]-z[0]) # vector from point 1 to point 3
ax.scatter(q.x, q.y, q.z, color='b')
print(q.x, q.y, q.z)

# Create the faces of the polygon (which could be a quad or triangle, etc.)
verts = [[(x[i], y[i], z[i]) for i in range(len(x))]]
#determine if the point is visible
visible = determine_visibility(Vector(x[0], y[0], z[0]), Vector(x[1], y[1], z[1]), Vector(x[2], y[2], z[2]), Vector(2-x[0],8-y[0],-4-z[0]))
print(visible)
#display points that form the vectors on the graph and label them
ax.text(x[0], y[0], z[0], 'p1', color='y')
ax.text(x[1], y[1], z[1], 'p2', color='r')
ax.text(x[2], y[2], z[2], 'p3', color='g')
ax.scatter(x[0], y[0], z[0], color='y')
ax.scatter(x[1], y[1], z[1], color='r')
ax.scatter(x[2], y[2], z[2], color='g')
ax.scatter(q.x, q.y, q.z, color='b')

#draw the vectors used 
ax.quiver(x[0], y[0], z[0], v1.x, v1.y, v1.z, color='r')
ax.quiver(x[0], y[0], z[0], v2.x, v2.y, v2.z, color='r')
ax.quiver(x[0], y[0], z[0], q.x-x[0], q.y-y[0], q.z-z[0], color='b')

#draw the normal vector
normal_vector =  Vector.cross_product(v1, v2)
ax.quiver(x[0], y[0], z[0], normal_vector.x, normal_vector.y, normal_vector.z, color='g')

# Plot the polygon as a 3D object
poly3d = Poly3DCollection(verts, alpha=0.25, linewidths=1, edgecolors='r')
ax.add_collection3d(poly3d)

# Set the labels and limits
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set the limits for the axes
ax.set_xlim([0, 5])
ax.set_ylim([0, 5])
ax.set_zlim([0, 5])

plt.show()
