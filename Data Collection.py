import velodyne_decoder as vd
from tqdm import tqdm

model='VLP-16'
bagfile_loc = 'D:\EECE 5554\Project/2017-10-18-17-33-13_0.bag'
topics = '/ns1/velodyne_packets'

def get_cloud_arrays():
  
  config = vd.Config(model=model) 
  bagfile = bagfile_loc
  lidar_topics = topics # '/ns2/velodyne_packets'
  cloud_arrays = []
  for stamp, points, topic in tqdm(vd.read_bag(bagfile, config, lidar_topics)):
    cloud_arrays.append(points)
  return cloud_arrays

def cloud_arrays_to_point_clouds(cloud_arrays):
  
  """
  Convert cloud arrays to point cloud by extracting the first 3 indexes
  
  """
  
  point_clouds = list(map(lambda x: x[:, :3], cloud_arrays))
  return point_clouds