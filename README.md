# LiDAR point-cloud based 3D object detection
Object detection is a key component in advanced driver assistance systems (ADAS), which allow cars to detect driving lanes and pedestrians to improve road safety. I took this project to learn how to perform 3D Object Detection using LiDAR data. The data comes from a Velodyne VLP-16 LiDAR sensor to capture real-time scenarios. Using Open3D, I perform the following: segmentation, RANSAC, DBSCAN, Voxel-Grid Downsampling, clustering, and detection using bounding boxes.

## Requirements
1. python 3.7
2. open3d
2. rosbag
3. velodyne-decoder
4. bagpy

Additional requirements listed in requirements.yaml file. (TODO)

### Velodyne-decoder

``bash
pip install rosbag --extra-index-url https://rospypi.github.io/simple/

``

## Data
Link to the rosbag can be found [here](https://drive.google.com/file/d/1MiPApz0QMdPGunLu2G9QBLTkUDTqGvDt/view?usp=drive_link):

Each packet contains the data from 24 firing sequences in 12 data blocks where each data block contains information from two firing sequences of 16 lasers.

# Methods

## 1. Voxel-Grid Down-sampling
After extraction, to reduce complexity and improve model efficiency, I use use Voxel grids, 3D boxes or cells that can hold multiple points, to downsample the data. The points present in each voxel (i.e., 3D box), are approximated with their centroid. This represents an accurate structure of the surface by points that are equidistant from each other. While retaining the essential features of the data set, I reduced the number of points seen in each frame to around 6,500 from the original 23,000 data points.

## 2. RANSAC: RANdom Sampling and Consensus
The RANSAC algorithm can be described as follows:
1. Select a random set of points (3 points to form a plane).
2. Calculate the parameters required for the plane equation.
3. Calculate the distance of all the points in the point cloud from the plane.
4. If the distance is within the THRESHOLD then add the point as an inlier.
5. Store the plane points and points having the maximum number of inliers.
6. Repeat the process again for MAX-ITERATIONS.

<img src="images\RANSAC1.png" width=700px>
<img src="images\RANSAC2.png" width=700px>
<img src="images\RANSAC3.png" width=700px>
After RANSAC is complete, the plane having the maximum number of inliers is the best estimate of the road plane. Using this algorithm, we can remove the road plane so that obstacles in the field of view of the sensor can be more efficiently localized and detected.

## 3. DBSCAN: Density-Based Spatial Clustering of Applications with Noise
The Density-Based Spatial Clustering of Applications with Noise algorithm can be summarized as follows:
1. Pick a point in the dataset (until all points have been visited).
2. If there are at least MINPOINTS points within a radius of EPS to the point selected, then we consider all these points to be part of the same cluster.
3. The clusters are then expanded by repeating this calculation for each neighboring point. DBSCAN is a robust mechanism for clustering by removing noise as outliers. Its advantages over other methods include being able to detect arbitrary clusters and being independent of the requirement to predefine the number of clusters like k-means clustering.

## 4. Bounding box Detection
To draw bounding boxes around the clusters of points, we get the labels of each cluster and group them together. Using these labels, we get the indices of the actual points to get the axis-aligned bounding boxes.

# Analysis of approach
After extracting the data using the velodyne-decoder package and using Open3d for point cloud processing, we can see the resulting point clouds of a single frame in the data. To segment the road plane out of the data, I use the previously described RANSAC algorithm. The road plane, labeled in red, is well-defined and can be separated from the data to reduce the complexity and possible noise.

  Initial point clouds of a single frame      |      Result after segmentation        |
:-------------------------:|:------------------------:|
| <img src="images\Downsampling.jpg" width=500px> | <img src="images\RANSAC.jpg" width=500px> |

Using Voxel downsampling, the number of points in a frame is reduce from 23,000 points to around 6,500 points. We can see a before and after. Despite reducing the complexity by a factor of 3, the contents seen in the point clouds are not affected as clusters of points are not affected.

   Before running voxel downsampling      |       After running voxel downsampling        |
:-------------------------:|:------------------------:|
| <img src="images\downsampling2.jpg" width=500px> | <img src="images\Downsampling1.jpg" width=500px> |

Finally, using DBSCAN, I cluster the points into objects. We can see the final objects detected. Given these clusters, I can place bounding boxes on the detected objects.

# Final Results
Using the algorithms described I can detect objects accurately in real time. As seen from the final results, it may not always be perfectly accurate but we can see the current results show that 3D detection can be achieved with satisfying results.

   Results after clustering      |       Clusters with bounding boxes        |
:-------------------------:|:------------------------:|
| <img src="images\Clustering.jpg" width=500px> | <img src="images\Bounding Box.jpg" width=500px> |

# References :
1. Velodyne lidar puck. https://www.amtechs.co.jp/product/VLP-16-Puck.pdf.
2. Downsampling a pointcloud using a voxelgrid filter. https://adioshun.gitbooks.io/pcl/content/Tutorial/Filtering/pcl-cpp-downsampling-a-pointcloud-using-a-voxelgrid-filter.html, 2022.
3. Downsampling a pointcloud using a voxelgrid filter — point cloud library 0.0 documentation. https://pcl.readthedocs.io/en/latest/voxel_grid.html, 2022.
4. What is lidar? learn how lidar works, velodyne lidar. https://velodynelidar.com/what-is-lidar/, 2022.
5. Nagesh Chauhan. Dbscan clustering algorithm in machine learning - kdnuggets. https://www.kdnuggets.com/2020/04/dbscan-clustering-algorithm-machine-learning.html, 2022.
6. Martin Simon, Stefan Milz, Karl Amende, and Horst-Michael Gross.Complex-yolo: Real-time 3d object detection on point clouds. arXiv, 2018.
7. Martin Valgur. Velodyne decoder. https://github.com/valgur/velodyne_decoder, 2022.
8. Leah A. Wasser. The basics of lidar - light detection and ranging - remote sensing. https://www.neonscience.org/resources/learning-hub/tutorials/lidar-basics, 2022.
9. Qian-Yi Zhou, Jaesik Park, and Vladlen Koltun. Open3D: A modern library for 3D data processing. arXiv:1801.09847, 2018.

