# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 20:03:54 2022

@author: Rjjam
"""

import numpy as np
import open3d as o3d
import plotly.graph_objects as go

def main():
    cloud = o3d.io.read_point_cloud("data/obj/ivysaur.obj", True) 
    print(cloud)
    o3d.visualization.draw_geometries([cloud])  


def main2():
    mesh = o3d.io.read_triangle_mesh("assets/Pokemon XY/Ivysaur/ivysaur.obj", True)
    #img = cv2.imread('C:/Users/Rjjam/OneDrive/Documents/GitHub/Pokemon/assets/Pokemon XY/Ivysaur/images/pm0002_00_BodyA1.png')
    
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])


def main4():
    mesh = o3d.io.read_triangle_mesh("assets/Pokemon XY/Ivysaur/ivysaur.ply")
    #img = cv2.imread('C:/Users/Rjjam/OneDrive/Documents/GitHub/Pokemon/assets/Pokemon XY/Ivysaur/images/pm0002_00_BodyA1.png')
    print(mesh.has_vertex_colors())
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])
    
def main5():
    mesh = o3d.io.read_triangle_mesh("assets/Pokemon XY/Bulbasaur/bulbasaur.ply")
    vert = np.asarray(mesh.vertices)
    tri = np.asarray(mesh.triangles)

    #print(mesh.has_vertex_colors())
    mesh.compute_vertex_normals()
    
    clr = None

    if mesh.has_triangle_normals():
        clr = np.asarray(mesh.vertex_colors)
        #clr = tuple(map(tuple, clr))
    else:
        clr = (1.0, 0.0, 0.0)
    mesh.compute_vertex_normals()
    
    mesh = go.Mesh3d(x=vert[:,0], y=vert[:,1], z=vert[:,2], 
             i=tri[:,0], j=tri[:,1], k=tri[:,2],vertexcolor=clr, opacity=1)
    
    graph_obj = []
    graph_obj.append(mesh)
    
    fig = go.Figure(
  #use data from graph objects array i.e. point cloud and mesh
      data=graph_obj, 
   #Layout of the plot
   layout=dict(
            scene=dict(
           #Disable axes’ display
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            )
        )
    )
    return fig

def model(model_name):
    
    cap_model_name = model_name.capitalize()
    mesh = o3d.io.read_triangle_mesh(f"assets/Pokemon XY/{cap_model_name}/{model_name}.obj")
    vert = np.asarray(mesh.vertices)
    tri = np.asarray(mesh.triangles)
    mesh.compute_vertex_normals()
    #print(mesh.textures)
    clr = None

    if mesh.has_triangle_normals():
        clr = (0.5, 0.5, 0.5) + np.asarray(mesh.triangle_normals) * 0.5
        clr = tuple(map(tuple, clr))
    else:
        clr = (1.0, 0.0, 0.0)

    mesh = go.Mesh3d(x=vert[:,0], y=vert[:,1], z=vert[:,2], 
             i=tri[:,0], j=tri[:,1], k=tri[:,2],facecolor=clr, opacity=1)
    

    """ 
    mesh = go.Mesh3d(x=vert[:,0], y=vert[:,1], z=vert[:,2], 
             i=tri[:,0], j=tri[:,1], k=tri[:,2], opacity=1)
    """
    graph_obj = []
    graph_obj.append(mesh)
    
    fig = go.Figure(
  #use data from graph objects array i.e. point cloud and mesh
      data=graph_obj, 
   #Layout of the plot
   layout=dict(
            scene=dict(
           #Disable axes’ display
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                camera = {"up":{"x":0, "y":1, "z":0}, "eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
                
            ),
            height = 400,
        )
    )
    return fig  #Display the figure 
        
    #o3d.visualization.draw_geometries([mesh])

#GLFW Error: WGL: Failed to make context current: The requested transformation operation is not supported.

if __name__ == "__main__":
    model()