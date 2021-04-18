import prman

# Interface
ri = prman.Ri()
out_rib_path = 'output.rib'

# Setup renderer
ri.Begin('__render')
ri.ArchiveRecord(ri.COMMENT, "Example comment")
ri.Display("speaker_out.exr", "it", "rgba")
ri.Format(720, 576, 1)
ri.Projection(ri.PERSPECTIVE)

# World descrition
ri.WorldBegin()
ri.Translate(0, 0, 2)
ri.Sphere(1, -1, 1, 180)
ri.WorldEnd()

ri.End()
