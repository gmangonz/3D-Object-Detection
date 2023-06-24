import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tqdm import tqdm

params = {'voxel_size': 0.3,
          'distance_threshold': 0.2, 
          'ransac_n': 3, 
          'num_iterations': 500, 
          'eps': 0.9, 
          'min_points': 10}


def down_segment_cluster(pcd, voxel_size, distance_threshold, ransac_n, num_iterations, eps, min_points):
    
    # Segmentation of the road and objects
    _, inliers = pcd.segment_plane(distance_threshold=distance_threshold, ransac_n=ransac_n, num_iterations=num_iterations)
    inlier_cloud = pcd.select_by_index(inliers)
    pcd = pcd.select_by_index(inliers, invert=True)
    inlier_cloud.paint_uniform_color([1,0,0])
    pcd.paint_uniform_color([0,0,1])

    # Voxel downsample to remove uneccessary points
    pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
    
    # Clustering and Labeling
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(pcd_down.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))
    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd_down.colors = o3d.utility.Vector3dVector(colors[:, :3])
    
    return labels, pcd_down, pcd
  
  
shorter_frames = list()
for i in tqdm(range(0, 3331, 30)): ######################################################### Change 30 to 1 to process all the frames
    # Create Point Clouds
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_clouds[i])
    # Create Clusters
    labels, pcd_out, pcd = down_segment_cluster(pcd, **params)
    # Append labels and cloud to list
    shorter_frames.append([labels, pcd_out, pcd])
    # break