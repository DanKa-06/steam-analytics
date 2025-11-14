import open3d as o3d
import numpy as np

def apply_gradient(mesh, axis=2):
    """Применяем градиент по выбранной оси (0=X,1=Y,2=Z)"""
    points = np.asarray(mesh.vertices)
    min_val, max_val = points[:, axis].min(), points[:, axis].max()
    colors = np.array([[(p[axis]-min_val)/(max_val-min_val), 0, 1-(p[axis]-min_val)/(max_val-min_val)] for p in points])
    mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
    return mesh

# -------------------------
# Step 1: Loading and Visualization
# -------------------------
mesh = o3d.io.read_triangle_mesh("dragon.ply")
if not mesh.has_vertex_colors():
    mesh.paint_uniform_color([0.7, 0.7, 0.7])  # временно серый
mesh = apply_gradient(mesh)
print("=== Step 1: Original Mesh ===")
print("Number of vertices:", np.asarray(mesh.vertices).shape[0])
print("Number of triangles:", np.asarray(mesh.triangles).shape[0])
print("Has vertex colors:", mesh.has_vertex_colors())
print("Has vertex normals:", mesh.has_vertex_normals())

o3d.visualization.draw_geometries([mesh], window_name="Step 1: Original Mesh")

# -------------------------
# Step 2: Conversion to Point Cloud
# -------------------------
pcd = mesh.sample_points_uniformly(number_of_points=50000)
pcd_colors = np.asarray(mesh.vertex_colors)
pcd.paint_uniform_color([0.7, 0.7, 0.7])  # временно
# применяем градиент к point cloud по Z
points = np.asarray(pcd.points)
z_min, z_max = points[:, 2].min(), points[:, 2].max()
colors = np.array([[(p[2]-z_min)/(z_max-z_min), 0, 1-(p[2]-z_min)/(z_max-z_min)] for p in points])
pcd.colors = o3d.utility.Vector3dVector(colors)

print("\n=== Step 2: Point Cloud ===")
print("Number of points:", np.asarray(pcd.points).shape[0])
print("Has colors:", pcd.has_colors())

o3d.visualization.draw_geometries([pcd], window_name="Step 2: Point Cloud")

# -------------------------
# Step 3: Surface Reconstruction (Poisson)
# -------------------------
mesh_recon, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
bbox = pcd.get_axis_aligned_bounding_box()
mesh_recon = mesh_recon.crop(bbox)
mesh_recon = apply_gradient(mesh_recon)

print("\n=== Step 3: Reconstructed Mesh ===")
print("Number of vertices:", np.asarray(mesh_recon.vertices).shape[0])
print("Number of triangles:", np.asarray(mesh_recon.triangles).shape[0])
print("Has vertex colors:", mesh_recon.has_vertex_colors())

o3d.visualization.draw_geometries([mesh_recon], window_name="Step 3: Reconstructed Mesh")

# -------------------------
# Step 4: Voxelization
# -------------------------
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)
print("\n=== Step 4: Voxel Grid ===")
print("Number of voxels:", len(voxel_grid.get_voxels()))
print("Has colors:", voxel_grid.has_colors())
o3d.visualization.draw_geometries([voxel_grid], window_name="Step 4: Voxel Grid")

# -------------------------
# Step 5: Adding a Plane
# -------------------------
bbox = mesh_recon.get_axis_aligned_bounding_box()
center = bbox.get_center()
extent = bbox.get_extent()
plane = o3d.geometry.TriangleMesh.create_box(width=extent[0]*2, height=0.01, depth=extent[2]*2)
plane.paint_uniform_color([0.8, 0.8, 0.8])
plane.translate([center[0]-extent[0], center[1], center[2]-extent[2]])

print("\n=== Step 5: Plane Added ===")
o3d.visualization.draw_geometries([mesh_recon, plane], window_name="Step 5: Mesh with Plane")

# -------------------------
# Step 6: Surface Clipping
# -------------------------
y_plane = center[1]
vertices = np.asarray(mesh_recon.vertices)
mask = vertices[:, 1] <= y_plane
triangles = np.asarray(mesh_recon.triangles)
mask_tri = np.all(mask[triangles], axis=1)
triangles_clipped = triangles[mask_tri]

mesh_clipped = o3d.geometry.TriangleMesh()
mesh_clipped.vertices = o3d.utility.Vector3dVector(vertices)
mesh_clipped.triangles = o3d.utility.Vector3iVector(triangles_clipped)
mesh_clipped = apply_gradient(mesh_clipped)

print("\n=== Step 6: Clipped Mesh ===")
print("Number of vertices:", np.asarray(mesh_clipped.vertices).shape[0])
print("Number of triangles:", np.asarray(mesh_clipped.triangles).shape[0])
o3d.visualization.draw_geometries([mesh_clipped, plane], window_name="Step 6: Clipped Mesh")

# -------------------------
# Step 7: Gradient and Extremes
# -------------------------
mesh_recon = apply_gradient(mesh_recon)
points = np.asarray(mesh_recon.vertices)
min_z_idx = np.argmin(points[:, 2])
max_z_idx = np.argmax(points[:, 2])
min_point = points[min_z_idx]
max_point = points[max_z_idx]

sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
sphere_min.translate(min_point)
sphere_min.paint_uniform_color([1, 0, 0])

sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
sphere_max.translate(max_point)
sphere_max.paint_uniform_color([0, 1, 0])

print("\n=== Step 7: Gradient and Extremes ===")
print("Minimum point (Z-axis):", min_point)
print("Maximum point (Z-axis):", max_point)

o3d.visualization.draw_geometries([mesh_recon, sphere_min, sphere_max], window_name="Step 7: Gradient and Extremes")
