import prman


def draw_cube(ri: prman.Ri,
              translate=[0, 0, 0],
              rotation=[0, 0, 0],
              scale=[1, 1, 1],
              width=1,
              height=1,
              depth=1):
    ri.TransformBegin()
    ri.Translate(*translate)
    ri.Rotate(rotation[0], 1, 0, 0)
    ri.Rotate(rotation[1], 0, 1, 0)
    ri.Rotate(rotation[2], 0, 0, 1)
    ri.Scale(*scale)

    ri.ArchiveRecord(ri.COMMENT, '--Cube primitive--')
    w = width
    h = height
    d = depth
    # Rear
    face = [-w, -h, d, -w, h, d, w, -h, d, w, h, d]
    ri.Patch("bilinear", {'P': face})
    # Front
    face = [w, -h, -d, w, h, -d, -w, -h, -d, -w, h, -d]
    ri.Patch("bilinear", {'P': face})
    # Left
    face = [-w, -h, -d, -w, h, -d, -w, -h, d, -w, h, d]
    ri.Patch("bilinear", {'P': face})
    # Right
    face = [w, -h, d, w, h, d, w, -h, -d, w, h, -d]
    ri.Patch("bilinear", {'P': face})
    # Bottom
    face = [w, -h, d, w, -h, -d, -w, -h, d, -w, -h, -d]
    ri.Patch("bilinear", {'P': face})
    # Top
    face = [-w, h, d, -w, h, -d, w, h, d, w, h, -d]
    ri.Patch("bilinear", {'P': face})
    ri.ArchiveRecord(ri.COMMENT, '--End of Cube primitive--')

    ri.TransformEnd()
