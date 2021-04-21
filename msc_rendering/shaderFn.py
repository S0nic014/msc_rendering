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
        # out_file = shader_source.with_suffix(".oso")
        # compile_command = "oslc.exe -o {0} {1} ".format(out_file, shader_source)
        compile_command = "oslc.exe {0}".format(shader_source)
        try:
            subprocess.check_output(compile_command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            Logger.error(err.output.decode("utf-8"))


if __name__ == '__main__':
    pass
