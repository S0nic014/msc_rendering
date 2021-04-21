import prman
import msc_rendering.shaderFn as shaderFn
import pathlib

SHADERS_DIR = pathlib.Path.cwd() / 'prman_tests' / 'shaders'


def main(recompile_shaders=True):
    if recompile_shaders:
        shaderFn.compile_shaders(shaders_paths=shaderFn.list_shader_files(SHADERS_DIR))

    # Interface
    ri = prman.Ri()
    out_rib_path = 'output.rib'

    # Setup renderer
    ri.Begin('__render')

    ri.ArchiveRecord(ri.COMMENT, "Example comment")
    ri.Display("HelloWorld.exr", "it", "rgba")
    ri.Format(720, 576, 1)
    ri.Projection(ri.PERSPECTIVE)

    # World descrition
    ri.WorldBegin()
    ri.Pattern('colour', 'colourShader')
    ri.Bxdf('PxrDiffuse',
            'bxdf',
            {
                'reference color diffuseColor': ['colourShader:Cout']
            })

    ri.Translate(0, 0, 2)
    ri.TransformBegin()
    ri.Rotate(90, 1, 1, 1)
    colours = [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    ri.Sphere(1, -1, 1, 360, {'Cs': colours})
    ri.TransformEnd()
    ri.WorldEnd()

    ri.End()


if __name__ == '__main__':
    main(recompile_shaders=True)
