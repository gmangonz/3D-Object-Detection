import pandas as pd

def get_bounding_boxes(labels, pcd):
    
    """
    Get the bounding boxes given the labels and the point cloud
    
    """
    
    obbs = []
    indexes = pd.Series(range(len(labels))).groupby(labels, sort=False).apply(list).tolist()

    Max_Points = 1000
    Min_Points = 10

    for i in range(0, len(indexes)):
        nb_pts = len(pcd.select_by_index(indexes[i]).points)
        if (nb_pts > Min_Points and nb_pts < Max_Points):
            sub_cloud = pcd.select_by_index(indexes[i])
            obb = sub_cloud.get_axis_aligned_bounding_box()
            obb.color=(0,0,1)
            obbs.append(obb)
            
    return obbs