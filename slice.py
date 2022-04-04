import logging
import os
import re
import sys
import subprocess


class Slice:

    def __init__(self, path=None, force=False):
        self.force = force
        self.dir_name = None
        self.pre_code = None
        self.sample_code = None
        self.sol_code = None
        self.expectation_code = None

        if path:
            self.run_path(path)
        else:
            self.run_all()

    def run_path(self, path):
        file = self.get_main_py(path)
        files = self.slice(file.split('\n'))
        self.write_files(path, files)

    def run_all(self):
        for dir_name in self.get_files():
            self.dir_name = dir_name
            file = self.get_main_py(dir_name)
            if not file: continue
            files = self.slice(file.split('\n'))

            if not self.force and (False in {*self.valid_comment()} or not self.valid_test()):
                breakpoint()
                files = self.slice(self.get_main_py(dir_name).split('\n'))
            self.write_files(dir_name, files)

    def get_main_py(self, path: str):
        if os.path.isfile(f'{path}/main.py'):
            with open(f'{path}/main.py') as f:
                file = f.read()
            return file
        print(f'{path}/main.py does not exist')

    def get_files(self):
        files_path = [i for i in sorted(os.listdir()) if
                      not re.match(r'.*\..*', string=i) and re.match(r'^\d.*', string=i)]
        return files_path

    def slice(self, file):
        self.pre_code = self.get_code(file, '# pre_code', 2)
        self.sample_code = self.get_code(file, '# sample_code', 2)
        self.sol_code = self.get_code(file, '# solution')
        self.expectation_code = self.get_code(file, '# expectation', is_end=True)
        return self.pre_code, self.sample_code, self.sol_code, self.expectation_code

    def write_files(self, path, files):
        names = 'pre_exercise_code.py', 'sample_code.py', 'solution.py', 'expectation.py'
        for file, name in zip(files, names):
            try:
                with open(f'{path}/{name}', 'w') as f:
                    f.write(file)

                subprocess.call(['python', '-m', 'black', f'{self.dir_name}/{name}'])
            except TypeError:
                logging.warning(f'ОШИБКА ЧТЕНИЯ ФАЙЛА {path + "/main.py"}')

    def get_code(self, file, target, line_skip=1, is_end=False):
        start = None
        for index, i in enumerate(file):
            if i.startswith(target):
                start = index + line_skip
                if is_end:
                    return '\n'.join(file[index + line_skip:])
            if start and index > start and i == "'''":
                return '\n'.join(file[start:index])

    def valid_comment(self):
        for sam, sol in zip(self.get_comments(self.sample_code), self.get_comments(self.sol_code)):
            if sam != sol:
                print(f"\n Комментарий не совпадает: {self.dir_name}\n{sam}\n{sol}")
                yield False
            elif re.search(r'#\s*[а-я]|\.\s*$', sam):
                print(f"\n Комментарий с маленькой буквы или точка в конце: {self.dir_name} - {sam}\n")
                yield False
            yield True

    def valid_test(self):
        print(f"Тест: {self.dir_name}/main.py")
        os.chdir(self.dir_name)
        proc = subprocess.call(['pytest', 'main.py'])
        os.chdir('../')
        if proc == 2:
            print(f"\n Ошибка ожиданий: {self.dir_name}\n")
            return False
        return True

    @staticmethod
    def get_comments(code: str) -> list:
        comments = []
        for line in code.split("\n"):
            comment = re.search(r"#.*", line)
            if comment:
                comments.append(comment.string.rstrip(" ").rstrip("\r"))
        return comments


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-f":
        Slice(force=True)
    elif len(sys.argv) == 2:
        Slice(path=sys.argv[1])
    else:
        Slice()
