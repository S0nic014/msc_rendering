import prman
import pathlib
from msc_rendering import Logger
import msc_rendering.shaderFn as shaderFn
import msc_rendering.primitivesFn as primitivesFn
import msc_rendering.yakult as yakult
import msc_rendering.table as table


ARCHIVES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'archives'
SHADERS_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'shaders'
TEXTURES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'textures'


def main(recompile_shaders=True, resolution=(720, 576), render_to_file: bool = False, hdri="cafe"):
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
    file_name = 'yakult.exr'
    if render_to_file:
        output = 'openexr'
    else:
        output = 'it'

    ri.Display(file_name, output, "rgba")
    ri.Format(*resolution, 1)

    # Raytrace /integrators
    ri.DepthOfField(20, 1.5, 2.5)
    ri.ShadingRate(10)
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

    # Cafe
    if hdri == "cafe":
        ri.Rotate(-40, 0, 0, 1)
        ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                             'float intensity': [0.8],
                                             "string lightColorMap": "comfy_cafe_2k.tx"})
    elif hdri == "kitchen":
        ri.Rotate(120, 0, 0, 1)
        ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                             'float intensity': [0.5],
                                             "string lightColorMap": "kitchen.tx"})
    elif hdri == "hotel":
        ri.Rotate(-120, 0, 0, 1)
        ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                             'float intensity': [0.1],
                                             "string lightColorMap": "hotel.tx"})
    else:
        Logger.error("Invalid HDRI name")
        raise ValueError

    ri.AttributeEnd()

    # Geometry
    # Table
    ri.TransformBegin()
    ri.Rotate(-20, 0, 1, 0)
    table.draw_scene(ri)
    ri.TransformEnd()

    # Yakult
    ri.TransformBegin()
    ri.Translate(0, -0.2, 0)
    yakult.draw_scene(ri)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(-90, 1, 0, 0)
    ri.Translate(2.5, -1, 0)
    ri.Rotate(120, 0, 1, 0)
    yakult.draw_scene(ri)
    ri.TransformEnd()

    ri.WorldEnd()
    ri.End()


if __name__ == "__main__":
    # main(recompile_shaders=True, resolution=(720, 576))
    main(recompile_shaders=True, resolution=(1920, 1080), render_to_file=False)
    # main(recompile_shaders=True, resolution=(3840, 2160), render_to_file=True)
