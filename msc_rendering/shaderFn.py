import pathlib
import subprocess
from msc_rendering import Logger


def list_shader_files(shaders_dir: pathlib.Path) -> list:
    if not isinstance(shaders_dir, pathlib.Path):
        shaders_dir = pathlib.Path(shaders_dir)
    shader_gen = shaders_dir.glob('**/*.osl')
    osl_files = [f for f in shader_gen if f.is_file()]
    return osl_files


def compile_shaders(shaders_paths: list) -> None:
    if not shaders_paths:
        Logger.info("No shaders found")
        return
    for shader_source in shaders_paths:
        Logger.info("Compiling shader {0}".format(shader_source.name))
        out_file = shader_source.with_suffix(".oso")
        compile_command = "oslc -o {0} {1} ".format(out_file, shader_source)
        try:
            subprocess.check_output(compile_command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            Logger.error(err.output.decode("utf-8"))


def tx_textures(texture_dir: pathlib.Path, force: bool = False):
    valid_formats = [".tiff", ".exr", ".jpeg",
                     ".sgi", ".tga", ".mayaiff",
                     ".dpx", ".bmp", ".hdr",
                     ".png", ".gif", ".ppm", ".xpm"]
    for img_file in texture_dir.glob("*"):
        if img_file.suffix not in valid_formats:
            continue

        out_file = img_file.with_suffix(".tx")
        if out_file.is_file() and not force:
            continue
        Logger.info("Converting texture {0}...".format(img_file.name))
        compile_command = "txmake {0} {1}".format(img_file, out_file)
        try:
            subprocess.check_output(compile_command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            Logger.error(err.output.decode("utf-8"))


if __name__ == '__main__':
    pass
