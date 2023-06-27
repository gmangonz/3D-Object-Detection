import open3d as o3d
from tqdm import tqdm
from src.bboxes import get_bounding_boxes
from src.cluster import down_segment_cluster

def get_frames(point_clouds, params, end=3331, interval=100):

    """
    Given the point clouds, it will perform downsampleing, segmentation, and clustering and will finnaly get the bounding boxes
    
    """

    frames = list()
    for i in tqdm(range(0, end, interval)):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_clouds[i])
        labels, pcd_down, pcd = down_segment_cluster(pcd, **params)
        bbox = get_bounding_boxes(labels, pcd_down)
        frames.append([bbox, labels, pcd_down])
    return frames

def visualize(frames, lines):

    """
    Visualize the list of frames
    Inputs:
        frames: list of list that contains the bounding boxes, labels and the point clouds
        line: used to draw the bounding boxes 
    
    """

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    source = o3d.geometry.PointCloud()
    source.points = frames[0][-1].points # set placeholder for points using the first frame's point cloud
    source.colors = frames[0][-1].colors # set placeholder for colors using the first frame's point cloud

    line_set = o3d.geometry.LineSet()
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.points = frames[0][0][10].get_box_points() # set placeholder for line's points using the first frame's 10th bounding box. Why 10? idk just randomly picked it

    vis.add_geometry(source)
    vis.add_geometry(line_set)

    try:
        for frame_count in range(len(frames)):
            
            source.points = frames[frame_count][-1].points
            source.colors = frames[frame_count][-1].colors
            
            line_set.lines = o3d.utility.Vector2iVector(lines)
            line_set.points = frames[frame_count][0][10].get_box_points() # TODO: Make the set of bboxes appear. Currently having problems with this
            
            vis.update_geometry(source)
            vis.update_geometry(line_set)
            
            vis.poll_events()
            vis.update_renderer()

            vis.capture_screen_image(r"D:\DL-CV-ML Projects\3D Object Detection\data\output\temp_%04d.jpg" % frame_count)
    finally:
        vis.destroy_window()