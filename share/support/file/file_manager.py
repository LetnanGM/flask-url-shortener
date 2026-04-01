import shutil
import os
from share.shared.logger.print import Logger


class filf:
    writeln = Logger()


class MovableFile:
    def __init__(self):
        pass

    @staticmethod
    def move(from_path: str, to_path: str) -> bool:
        """
        moving file from old path to new path.

        Params:
            from_path: mean old path or which file to move?.
            to_path: new path location for move.

        Returns:
            'True' if file successfully moved.
        """
        try:
            shutil.move(from_path, to_path)
            filf.writeln.silent(
                f"(File) Move file from {from_path} to {to_path} => Success"
            )
            return True
        except Exception as e:
            filf.writeln.silent(
                f"(File) Move file from {from_path} to {to_path} => Failed | reason: {e}"
            )
            return False

    @staticmethod
    def copy(from_path: str, to_path: str) -> bool:
        try:
            shutil.copy(from_path, to_path)
            filf.writeln.silent(
                f"(File) Copy file from {from_path} to {to_path} => Success"
            )

            return True
        except PermissionError:
            shutil.copy(from_path, to_path)
            filf.writeln.silent(
                f"(File) Move file from {from_path} to {to_path} => Success"
            )
            return True

        except Exception as e:
            filf.writeln.silent(
                f"(File) Copy file from {from_path} to {to_path} => Failed | reason: {e}"
            )
            return False

    @staticmethod
    def remove(path_file: str) -> bool:
        try:
            filf.writeln.silent(f"(File) Deleted {path_file} => Success")
            os.remove(path_file)
            return True
        except Exception:
            filf.writeln.silent(f"(File) Deleted {path_file} => Failed")
            return False

    @staticmethod
    def replace(from_path: str, to_path: str) -> bool:
        if not from_path or not os.path.exists(from_path):
            filf.writeln.error(f"(File) Source file '{from_path}' not found.")
            return False

        try:
            # Read content from source file
            filf.writeln.silent(f"(File) Reading data of file {from_path}..")
            with open(from_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Write to destination file (overwrite)
            filf.writeln.silent(f"(File) Writing data to {to_path}..")
            with open(f"./{to_path}", "w", encoding="utf-8") as file:
                file.write(content)

            # Delete source file
            os.remove(from_path)
            filf.writeln.silent(
                f"(File) Replaced and deleted {from_path} successfully."
            )
            return True

        except PermissionError:
            filf.writeln.error(f"(File) Permission denied when accessing {to_path}.")
            filf.writeln.debug("(File) Trying alternative method..")
            try:
                shutil.move(from_path, f"./{to_path}")
            except FileExistsError:
                namefile = from_path.split("\\")
                filf.writeln.error(
                    f"(File) File named '{namefile}' are exists in {to_path}"
                )

            if os.path.exists(to_path):
                filf.writeln.info(f"(File) Success moved file to {to_path}")

                return True
            return False
        except Exception as e:
            filf.writeln.error(f"(File) Failed to replace file: {e}")
            return False
