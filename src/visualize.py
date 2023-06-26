import open3d as o3d
from tqdm import tqdm
from src.bboxes import get_bounding_boxes
from src.cluster import down_segment_cluster

def get_frames(point_clouds, params, end=3331, interval=100):

    frames = list()
    for i in tqdm(range(0, end, interval)):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_clouds[i])
        labels, pcd_down, pcd = down_segment_cluster(pcd, **params)
        bbox = get_bounding_boxes(labels, pcd_down)
        frames.append([bbox, labels, pcd_down])
    return frames

def visualize(frames, lines):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    source = o3d.geometry.PointCloud()
    source.points = frames[0][-1].points
    source.colors = frames[0][-1].colors

    line_set = o3d.geometry.LineSet()
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.points = frames[0][0][10].get_box_points()

    vis.add_geometry(source)
    vis.add_geometry(line_set)

    try:
        for frame_count in range(len(frames)):
            
            source.points = frames[frame_count][-1].points
            source.colors = frames[frame_count][-1].colors
            
            line_set.lines = o3d.utility.Vector2iVector(lines)
            line_set.points = frames[frame_count][0][10].get_box_points()
            
            vis.update_geometry(source)
            vis.update_geometry(line_set)
            
            vis.poll_events()
            vis.update_renderer()

            vis.capture_screen_image(r"D:\DL-CV-ML Projects\3D Object Detection\data\output\temp_%04d.jpg" % frame_count)
    finally:
        vis.destroy_window()