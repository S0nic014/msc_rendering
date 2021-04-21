import prman
import msc_rendering.shaderFn as shaderFn
import pathlib
import random

SHADERS_DIR = pathlib.Path.cwd() / 'prman_tests' / 'shaders'
ARCHIVES_DIR = pathlib.Path.cwd() / 'prman_tests' / 'archives'


def generate_curves(width_x: float, width_z: float, inc: float, points: list, width_list: list, num_points_list: list, seed: int = 1):
    xmin = -width_x / 2.0
    xmax = width_x / 2.0
    zmin = -width_z / 2.0
    zmax = width_z / 2.0
    random.seed(seed)
    zpos = zmin
    plus = 0.1
    minus = -0.1
    while zpos < zmax:
        xpos = xmin
        while(xpos < xmax):
            points.append(xpos + random.uniform(minus, plus))
            points.append(0)
            points.append(zpos + random.uniform(minus, plus))

            points.append(xpos + random.uniform(minus, plus))
            points.append(0.2)
            points.append(zpos + random.uniform(minus, plus))

            points.append(xpos + random.uniform(minus, plus))
            points.append(0.4)
            points.append(zpos + random.uniform(minus, plus))

            points.append(xpos + random.uniform(minus, plus))
            points.append(0.8 + random.uniform(minus, plus))
            points.append(zpos + random.uniform(minus, plus))

            width_list.append(0.006)
            width_list.append(0.003)
            num_points_list.append(4)
            xpos += inc
        zpos += inc


def main(recompile_shaders=True):
    if recompile_shaders:
        shaderFn.compile_shaders(shaders_paths=shaderFn.list_shader_files(SHADERS_DIR))

    # Interface
    ri = prman.Ri()
    ri.Option('rib', {'string asciistyle': 'indented'})
    out_rib_path = 'output.rib'

    # Generate points
    points = []
    width = []
    num_points = []
    generate_curves(14, 14, 0.3, points, width, num_points, seed=1)

    # Setup renderer
    ri.Begin('__render')
    ri.ShadingRate(0.2)
    ri.Option('searchpath', {'string shader': SHADERS_DIR.as_posix()})
    ri.Option('searchpath', {'string archive': ARCHIVES_DIR.as_posix()})

    ri.ArchiveRecord(ri.COMMENT, "Example comment")
    ri.Display("TestMultiCurves.exr", "it", "rgba")
    ri.Format(1024, 720, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 80})

    # World descrition
    ri.WorldBegin()
    ri.Translate(0, 0, 10)
    ri.Rotate(-20, 1, 0, 0)

    ri.TransformBegin()
    ri.Bxdf('PxrDiffuse', 'bxdf', {'color diffuseColor': [0.5, 0.5, 0.5]})
    ri.Curves('cubic', num_points, 'noperiodic', {ri.P: points, ri.WIDTH: width})
    ri.TransformEnd()

    ri.WorldEnd()
    ri.End()


if __name__ == '__main__':
    main(recompile_shaders=False)
