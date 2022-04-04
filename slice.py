import logging
import os
import re
import sys
import subprocess


class Slice:

    def __init__(self, path=None):
        self.dir_name = None
        self.sample_code = None
        self.solution = None
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
            self.checked_comment()
            self.checked_test()
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
        pre_code = self.get_code(file, '# pre_code', 2)
        sample_code = self.get_code(file, '# sample_code', 2)
        sol_code = self.get_code(file, '# solution')
        expectation_code = self.get_code(file, '# expectation', is_end=True)
        return pre_code, sample_code, sol_code, expectation_code

    def write_files(self, path, files):
        names = 'pre_exercise_code.py', 'sample_code.py', 'solution.py', 'expectation.py'
        for file, name in zip(files, names):
            try:
                with open(f'{path}/{name}', 'w') as f:
                    f.write(file)
                subprocess.call(['python3.8', '-m', 'black', f'{self.dir_name}/{name}'])
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
                if target == "# sample_code":
                    self.sample_code = file[start:index]
                elif target == "# solution":
                    self.solution = file[start:index]
                return '\n'.join(file[start:index])

    def checked_comment(self):
        for sam, sol in zip(self.sample_code, self.solution):
            if (re.search(r'#\s*', sam) and not re.search(r'\--$', sam)) \
                    and (re.search(r'#\s*', sol) and not re.search(r'\--$', sol)):
                res = [sam, sol]
                if len(set(res)) > 1:
                    print(f"\n Комментарий не совпадает: {self.dir_name} - {set(res)}\n")
                    breakpoint()
                elif re.search(r'#\s*[а-я]|#\s*[а-я]\s*\.|\.$', sam):
                    print(
                        f"\n Комментарий с маленькой буквы или точка в конце: {self.dir_name} - {sam}\n")
                    breakpoint()

    def checked_test(self):
        print(f"Тест: {self.dir_name}/main.py")
        proc = subprocess.call(['pytest', f'{self.dir_name}/main.py'])
        if proc == 2:
            print(f"\n Ошибка ожиданий: {self.dir_name}\n")
            breakpoint()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Slice(path=sys.argv[1])
    else:
        Slice()
