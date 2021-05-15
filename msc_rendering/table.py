import prman
import msc_rendering.primitivesFn as primitivesFn


def draw_scene(ri: prman.Ri):
    ri.TransformBegin()
    ri.Translate(0, -2.0, 0)

    # Patterns
    ri.Pattern('PxrTexture', 'diffuse_tx', {'string filename': ['wood_diffuse.tx']})
    ri.Pattern('PxrTexture', 'rough_tx', {'string filename': ['wood_roughness.tx']})
    ri.Pattern('PxrTexture', 'normal_tx', {'string filename': ['wood_normal.tx']})
    ri.Pattern('PxrBump', 'nbump', {'reference normal inputN': ['normal_tx:resultRGB']})

    # Material
    ri.Bxdf('PxrDisney', 'table_surface', {'reference color baseColor': 'diffuse_tx:resultRGB',
                                           'reference float roughness': 'rough_tx:resultA',
                                           'reference normal bumpNormal': 'nbump:resultN'})

    # Draw
    primitivesFn.draw_cube(ri, scale=[10, 1, 10])
    ri.TransformEnd()
