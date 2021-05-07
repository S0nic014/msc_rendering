import prman
import pathlib
import msc_rendering.shaderFn as shaderFn
import msc_rendering.primitivesFn as primitivesFn
import msc_rendering.yakult as yakult

ARCHIVES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'archives'
SHADERS_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'shaders'
TEXTURES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'textures'


def main(recompile_shaders=True, resolution=(720, 576)):
    shaderFn.tx_textures(TEXTURES_DIR)
    if recompile_shaders:
        shaderFn.compile_shaders(shaders_paths=shaderFn.list_shader_files(SHADERS_DIR))

    # Interface
    ri = prman.Ri()
    ri.Option('rib', {'string asciistyle': 'indented'})
    out_rib_path = 'output.rib'

    # Setup render
    ri.Begin('__render')
    # Paths
    ri.Option('searchpath', {'string archive': ARCHIVES_DIR.as_posix()})
    ri.Option('searchpath', {'string shader': SHADERS_DIR.as_posix()})
    ri.Option('searchpath', {'string texture': TEXTURES_DIR.as_posix()})
    # Display
    ri.Display("result_render.exr", "it", "rgba")
    ri.Format(*resolution, 1)

    # Raytrace /integrators
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.PixelVariance(0.01)
    ri.Integrator("PxrPathTracer", "integrator")
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 90})

    # World descrition
    ri.WorldBegin()

    ri.Translate(0, 0, 5)
    ri.Rotate(-40, 1, 0, 0)
    ri.Rotate(30, 0, 1, 0)

    # Lights
    ri.AttributeBegin()
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(30, 0, 0, 1)
    ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                         "string lightColorMap": "comfy_cafe_2k.tx"})
    ri.AttributeEnd()

    # Geometry
    # Table
    ri.TransformBegin()
    ri.Translate(0, -2.0, 0)
    ri.Pattern('wood', 'colourShader', {"color Cin": [0.4, 0.2, 0.0],
                                        "float scale": 2,
                                        "float freq": 10,
                                        "float variation": 0.04})
    ri.Bxdf('PxrDisney',
            'bxdf',
            {
                'reference color baseColor': ['colourShader:Cout']
            })
    primitivesFn.draw_cube(ri, scale=[10, 1, 10])
    ri.TransformEnd()

    # Yakult
    ri.TransformBegin()
    yakult.draw_scene(ri)

    ri.TransformEnd()

    ri.WorldEnd()
    ri.End()


if __name__ == "__main__":
    main(recompile_shaders=True, resolution=(720, 576))
