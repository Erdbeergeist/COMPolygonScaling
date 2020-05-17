from COMPolygonScaling import polygon

p = polygon([[1,2],[1,4],[7,3],[2,-1]])
p.plot_polygon()
p.plot_com_rays()
p.get_scaled_nodes(0.6, True)
p.get_scaled_nodes(1.1, True)
p.show_fig()
