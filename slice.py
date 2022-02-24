import re
import os
import logging


class Slice:

    def __init__(self):
        for i in self.get_files():
            file = self.get_main_py(i)
            if not file: continue
            files = self.slice(file.split('\n'))
            self.write_files(i, files)

    def get_main_py(self, path: str):
        if os.path.isfile(f'{path}/main.py'):
            with open(f'{path}/main.py') as f:
                file = f.read()
            return file
        logging.warning(f'{path}/main.py does not exist')

    def get_files(self):
        files_path = [i for i in os.listdir() if not re.match(r'.*\..*', string=i) and re.match(r'^\d.*', string=i)]
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
            with open(f'{path}/{name}', 'w') as f:
                f.write(file)

    def get_code(self, file, target, line_skip=1, is_end=False):
        start = None
        for index, i in enumerate(file):
            if i.startswith(target):
                start = index + line_skip
                if is_end:
                    return '\n'.join(file[index + line_skip:])
            if start and index > start and i == "'''":
                return '\n'.join(file[start:index])


if __name__ == "__main__":
    Slice()
