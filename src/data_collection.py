import velodyne_decoder as vd
from tqdm import tqdm


def get_cloud_arrays(model, bagfile_loc, topics):
  
  """
  Returns the cloud arrays given the path to bag file and topics. Model will be a Velodyne LidAR model to get the configuration
  
  """

  assert isinstance(topics, list), 'topics must be a list'
  
  config = vd.Config(model=model) 
  lidar_topics = topics # '/ns2/velodyne_packets'
  cloud_arrays = []
  for stamp, points, topic in tqdm(vd.read_bag(bagfile_loc, config, lidar_topics)):
    cloud_arrays.append(points)
  return cloud_arrays

def cloud_arrays_to_point_clouds(cloud_arrays):
  
  """
  Convert cloud arrays to point cloud by extracting the first 3 indexes
  
  """
  
  point_clouds = list(map(lambda x: x[:, :3], cloud_arrays))
  return point_clouds