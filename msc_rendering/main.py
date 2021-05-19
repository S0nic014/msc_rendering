import prman
import pathlib
import json
from msc_rendering import Logger
import msc_rendering.shaderFn as shaderFn
import msc_rendering.yakult as yakult
import msc_rendering.table as table

CONFIG_PATH = pathlib.Path.cwd() / 'msc_rendering' / 'render_config.json'
ARCHIVES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'archives'
SHADERS_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'shaders'
TEXTURES_DIR = pathlib.Path.cwd() / 'msc_rendering' / 'textures'


def load_config() -> dict:
    config_dict = {}
    with CONFIG_PATH.open() as jsonfile:
        config_dict = json.load(jsonfile)
    return config_dict


def main():
    config = load_config()
    shaderFn.tx_textures(TEXTURES_DIR)
    if config.get('recompile_shaders', True):
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
    file_name = config.get('output_file', 'yakult.exr')
    if config.get('file_render', False):
        output = 'openexr'
    else:
        output = 'it'

    ri.Display(file_name, output, "rgba")
    ri.Format(*config.get('resolution', (720, 576)), 1)

    # Raytrace /integrators
    ri.DepthOfField(20, 1.5, 2.5)
    ri.ShadingRate(config.get('shading_rate', 10))
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.PixelVariance(config.get('pixel_variance', 0.01))
    ri.Integrator("PxrPathTracer", "integrator")
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: config.get('fov', 90)})

    # World descrition
    ri.WorldBegin()

    ri.Translate(0, 0, 4)
    ri.Rotate(-40, 1, 0, 0)
    ri.Rotate(30, 0, 1, 0)

    # Lights
    ri.AttributeBegin()
    ri.Rotate(-90, 1, 0, 0)

    # Cafe
    hdri = config.get('hdri', 'cafe')
    if hdri == "cafe":
        ri.Rotate(-40, 0, 0, 1)
        ri.Light('PxrDomeLight', 'skyDome', {'float exposure': [0],
                                             'float intensity': [0.8],
                                             "string lightColorMap": "cafe.tx"})
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
    main()
