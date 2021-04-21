import prman
import msc_rendering.shaderFn as shaderFn
import pathlib
import random

SHADERS_DIR = pathlib.Path.cwd() / 'prman_tests' / 'shaders'
ARCHIVES_DIR = pathlib.Path.cwd() / 'prman_tests' / 'archives'


def main(recompile_shaders=True):
    if recompile_shaders:
        shaderFn.compile_shaders(shaders_paths=shaderFn.list_shader_files(SHADERS_DIR))

    # Interface
    ri = prman.Ri()
    ri.Option('rib', {'string asciistyle': 'indented'})
    out_rib_path = 'output.rib'

    # Setup renderer
    ri.Begin('__render')
    ri.Option('searchpath', {'string shader': SHADERS_DIR.as_posix()})
    ri.Option('searchpath', {'string archive': ARCHIVES_DIR.as_posix()})

    ri.ArchiveRecord(ri.COMMENT, "Example comment")
    ri.Display("TestPoints.exr", "it", "rgba")
    ri.Format(720, 576, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 90})

    # World descrition
    ri.WorldBegin()
    ri.Translate(0, 0, 4)

    ri.TransformBegin()
    points = []
    width = []
    colour = []
    normals = []

    for i in range(0, 20000):
        for ix in range(0, 3):
            colour.append(random.uniform(0, 1))
            points.append(random.uniform(-2, 2))
            # normals.append(random.uniform(0, 1))
        width.append(random.uniform(0.01, 0.2))

    ri.Pattern('colour', 'colourShader')
    ri.Bxdf('PxrDiffuse', 'bxdf', {'reference color diffuseColor': ['colourShader:Cout']})
    ri.Points({ri.P: points, ri.CS: colour, ri.WIDTH: width})
    ri.TransformEnd()

    ri.WorldEnd()

    ri.End()


if __name__ == '__main__':
    main(recompile_shaders=True)
