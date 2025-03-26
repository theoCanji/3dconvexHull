# 3D Incremental COnvex Hull Project Overview

```
3DConvexHull
├── README.md
├── DCEL.py
├── RandIncHull.py
├── helpers.py
├── main.py
├── runtime.png
├── runtime.txt
```

**How to Run**

1. Open `main.py`.

2. In the `main()` function, select what to run by commenting/uncommenting the following functions:

   - **Runtime Analysis:**
     ```python
     time_algorithm(n_values, i, decrement_i=True)
     ```
     - Runs runtime tests to confirm expected complexity.
     - Displays runtime results in the console and plots a graph of runtimes.

   - **Convex Hull Visualization:**
     ```python
     visualize_hull(n, dis_inc=False)
     ```
     - Shows a 3D plot of the convex hull using Matplotlib.
     - Setting `dis_inc=True` enables incremental visualization:
       - Press **space** to incrementally add points, pausing at each step to show removed faces and the horizon.
       - Upon completion (adding all points or closing the plot), outputs to the console whether the hull is correctly convex with a boolean flag.

3. Adjust parameters in `main()`:
   - `n`: Number of points to generate and visualize.
   - `display_incrementally`: Set to `True` for step-by-step visualization in ``visualize_hull(n, dis_inc=False)``.

**Using in Your Own Project:**

You can use the convex hull in your own scripts as follows:

```python
from RandomIncHull import RandomIncrementalHull3D

# make a set of 3D points to create the hull from
points = [(x1, y1, z1), (x2, y2, z2), ...]
hull = RandomIncrementalHull3D(points)
```

**Files**

`DCEL.py` is where we made our DCEL class to hold the convex hull. It has additional classes like Vertex, Edge, and Face. The DCEL class contains the code to plot the hull and to update it as points are added.

`helpers.py` a file of helper primitives and functions that are used in the random incremental convex hull algorithm or in the DCEL. 

`RandIncHull.py` the file that holds the code for the random incremental convex hull class that runs the algorithm and holds the DCEL representing the hull.

`main.py` is the file that runs the tests for the random incremental convex hull algorithm, including runtime, visualizations, and correctness (is convex?).

`runtime.png` is the graph of the runtime of the algorithm for different values of n from 16000 to 1024000, averaged over 100 iterations per n.

`runtime.txt` is the data associated with `runtime.png`

`sample_output.png` is a sample output of the convex hull for 100 points.

`sample_input.png` is a sample input of 100 randomly generated points.

## Functions and Classes in `DCEL.py`
The main class for our Doubly Connected Edge List.

- **`__init__()`**  
  Initializes the DCEL object, storing our vertices, edges, and faces.

- **`get_or_create_vertex(v)`**  
  Function to get or create a vertex in the DCEL if one already exists.  

- **`create_face(points)`**  
  Makes a new face from a list of points (vertices). Creates new half-edges for this face, and uses twins if they already exist. If not, it makes them.  

- **`remove_face(face)`**  
  Removes a face from the DCEL, and removes the edges that belong to the face. If the twin is `None`, removes both edges; otherwise, sets its half-edge to `None`.  

- **`create_tetrahedron(p1, p2, p3, p4)`**  
  Builds the initial tetrahedron in the DCEL to use as a basis for the algorithm.  

- **`get_face_vertices(face)`**  
  Helper method to get the vertices for a given face.  

- **`get_face_edges(face)`**  
  Helper method to get the edges defining a face.  

- **`plot(normal_mode=False)`**  
  Method to plot the DCEL in `matplotlib`.  

- **`__repr__()`**  
  Debugging representation of the DCEL, showing the number of vertices, edges, and faces.  

- **`__str__()`**  
  Returns the `__repr__()` output.  

### `Edge`
Edge class to be held in the DCEL.

- **`__init__(start, end, face=None, twin=None, next=None, prev=None)`**  
  Initializes available variables for an edge.  

- **`__repr__()`**  
  Debugging representation of the Edge, showing the start and end vertices.  

- **`__str__()`**  
  Returns the `__repr__()` output.  

### `Vertex`
Vertex class to be held in the DCEL.

- **`__init__(coordinates)`**  
  Initializes a Vertex to hold a reference to an edge incident on it.  

- **`__repr__()`**  
  Debugging representation of the Vertex, showing its coordinates.  

- **`__str__()`**  
  Returns the `__repr__()` output.  

### `Face`
Face class to be held in the DCEL.

- **`__init__(edge)`**  
  Initializes the face to hold an edge incident on the face.  

- **`__repr__()`**  
  Debugging representation of the Face, showing its outer edge.  

- **`__str__()`**  
  Returns the `__repr__()` output.  

---

## Functions in `RandIncHull.py`

### `RandomIncrementalHull3D`
The class for running the random incremental convex hull algorithm.

- **`__init__(points)`**  
  Initializes the Random Incremental Hull object and creates the hull.  

  Args:
  - `points`: List of 3D points to create the hull from.
  - `dis_inc`: Flag to determine if the hull is to be displayed incrementally. Defaults to False.

- **`get_hull()`**  
  Retrieves the DCEL hull from the object.  

- **`start()`**  
  Starts the interactive incremental hull plotting.

- **`on_close()`**  
  Handles the close event for the incremental plotting,
  continues the algorithm and finds the rest of the hull from the point that the user closed the window.

- **`on_key_press(self, event)`**  
  Handles the key press event for the incremental plotting,
  adds the next point to the hull when the space key is pressed

  Args:
      event (KeyEvent): the matplotlib key press event

- **`redraw(self, highlight=None, title=None)`**  
  Helper function to redraw the hull with optional highlighting and title, 
  used for the incremental plotting mode.

  Args:
      highlight (list[Egde], optional): The edges within the hull to highlight, show in red. Defaults to None.
      title (String, optional): The title of the plot. Defaults to None.
  """

- **`plot()`**  
  Function to plot the hull from the object itself.

- **`get_conflicts(points, faces)`**  
  Updates the conflict graph with new faces and vertices.  

- **`add_point(point)`**  
  Incrementally adds a point to the hull, finding the horizon and forming new faces with every point on the horizon with the new point.  

- **`get_horizon(face, point)`**  
  Finds the horizon of visibility for a given point in the hull and removes the faces within the horizon to prepare for the addition of new faces.  

---

## Helper Functions in `helpers.py`

- **`determine_visibility(p1, p2, p3, q)`**  
  Checks if a point is visible from a given face.  

- **`oriented_face(points, centroid)`**  
  Ensures the initial tetrahedron's faces are oriented correctly in the DCEL (outward-facing normals).  

- **`generate_random_points(n)`**  
  Generates `n` random points for testing the algorithm.  

- **`is_convex(dcel)`**  
  Checks if a given DCEL represents a convex hull.  

---

## Functions in `main.py`

- **`time_algorithm(n_values, i, decrement_i=True)`**  
  Measures the runtime of the algorithm for different values of `n`. Ensures total runtime is >1 second for accurate timing.

  **Effect:**  
  - Prints runtime results  
  - Generates and saves a plot (`runtime.png`) showing the runtime of the algorithm  

- **`visualize_hull(n, dis_inc: Optional[bool])`**  
  Generates and visualizes the convex hull for a given number of points.
  If `dis_inc` is `True`, the hull will be displayed incrementally. Closing the matplotlib window will continue the algorithm on the next step.

- **`main()`**  
  Main function to show runtime, hull visualization, and correctness.  

---





