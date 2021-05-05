import prman
import msc_rendering.shaderFn as shaderFn
import pathlib

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
    ri.Display("TestSubdiv.exr", "it", "rgba")
    ri.Format(1024, 720, 1)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 90})

    # World descrition
    ri.WorldBegin()
    ri.Translate(0, 0, 4)
    ri.Rotate(-15, 1, 0, 0)

    # Checker
    expr = """
    $colour = c1;
    $c = floor(10 * $u) + floor(10 * $v);
    if(fmod($c, 2.0) < 1.0)
    {
        $colour=c2;
    }
    $colour
    """
    npolys = [4] * 6
    points = [-0.5, -0.5, -0.5,
              0.5, -0.5, -0.5,
              -0.5, 0.5, -0.5,
              0.5, 0.5, -0.5,
              -0.5, -0.5, 0.5,
              0.5, -0.5, 0.5,
              -0.5, 0.5, 0.5,
              0.5, 0.5, 0.5]
    indices = [0, 1, 3, 2,
               0, 4, 5, 1,
               0, 2, 6, 4,
               1, 5, 7, 3,
               2, 3, 7, 6,
               4, 6, 7, 5]
    ri.Pattern('PxrSeExpr', 'seTexture', {'color c1': [1, 1, 1],
                                          'color c2': [1, 0, 0],
                                          'string expression': [expr]})
    ri.Bxdf('PxrDiffuse', 'diffuse', {'reference color diffuseColor': ['seTexture:resultRGB']})

    ri.TransformBegin()
    ri.Translate(-1.5, 0, 0)
    ri.Rotate(45, 0, 1, 0)
    ri.SubdivisionMesh('catmull-clark',
                       npolys,
                       indices,
                       [ri.CREASE, ri.CREASE, ri.CREASE, ri.CREASE],
                       [5, 1, 5, 1, 5, 1, 5, 1], [4, 5, 7, 6, 4, 0, 1, 3, 2, 0, 0, 4, 6, 2, 0, 1, 5, 7, 3, 1],
                       [3, 3, 3, 3], {ri.P: points})

    ri.TransformEnd()
    ri.WorldEnd()

    ri.End()


if __name__ == '__main__':
    main(recompile_shaders=True)
