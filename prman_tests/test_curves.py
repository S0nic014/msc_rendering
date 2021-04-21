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
    ri.Display("TestCurves.exr", "it", "rgba")
    ri.Format(720, 576, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 90})

    # World descrition
    ri.WorldBegin()
    ri.Translate(0, 0, 4)

    ri.TransformBegin()
    ri.Bxdf('PxrDiffuse', 'bxdf', {'color diffuseColor': [1, 0, 0]})
    points = [0, 0, 0, -1, -0.5, 1, 2, 0.5, 1, 1, 0, -1]
    width = [0.01, 0.04]
    ri.Curves('cubic', [4], 'noperiodic', {ri.P: points, ri.WIDTH: width})

    ri.Bxdf('PxrDiffuse', 'bxdf', {'color diffuseColor': [0, 0, 1]})
    points2 = [0, 0, 0, 3, 4, 5, -1, -0.5, 1, 2, 0.5, 1, 1, 0, -1]
    ri.Curves('linear', [5], 'nonperiodic', {ri.P: points2, ri.CONSTANTWIDTH: [0.075]})
    ri.TransformEnd()

    ri.WorldEnd()
    ri.End()


if __name__ == '__main__':
    main(recompile_shaders=False)
