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

    ri.Translate(0, 0, 4)
    ri.Rotate(-40, 1, 0, 0)
    ri.Rotate(30, 0, 1, 0)

    # Lights
    ri.AttributeBegin()
    ri.Rotate(-90, 1, 0, 0)
    ri.Translate(0, 10, 0)

    # Cafe
    ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                         'float intensity': [0.5],
                                         "string lightColorMap": "comfy_cafe_2k.tx"})

    # Kitchen
    # ri.Rotate(120, 0, 0, 1)
    # ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
    #                                      'float intensity': [0.3],
    #                                      "string lightColorMap": "kitchen.tx"})

    # # Hotel
    # # ri.Rotate(120, 0, 0, 1)
    # ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
    #                                      'float intensity': [0.1],
    #                                      "string lightColorMap": "hotel.tx"})
    ri.AttributeEnd()

    # Geometry
    # Table
    ri.TransformBegin()
    ri.Translate(0, -2.0, 0)
    ri.Pattern('wood', 'wood_shader', {"color Cin": [0.4, 0.2, 0.0],
                                       "float scale": 3,
                                       "float freq": 4,
                                       "float variation": 0.04})
    ri.Bxdf('PxrDisney',
            'bxdf',
            {
                'reference color baseColor': ['wood_shader:Cout']
            })
    primitivesFn.draw_cube(ri, scale=[10, 1, 10])
    ri.TransformEnd()

    # Yakult
    ri.TransformBegin()
    yakult.draw_scene(ri)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(-90, 1, 0, 0)
    ri.Translate(2.5, -1, 0)
    ri.Rotate(-90, 0, 1, 0)
    yakult.draw_scene(ri)
    ri.TransformEnd()

    ri.WorldEnd()
    ri.End()


if __name__ == "__main__":
    main(recompile_shaders=True, resolution=(720, 576))
