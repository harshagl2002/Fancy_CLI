from plumbum import cli 
from pyfiglet import Figlet
from plumbum.cmd import ls, git
from questionary import prompt

def print_banner(text: str):
    print(Figlet(font='slant').renderText(text))

def get_files():
    ls_output = ls().strip()
    files = ls_output.split("\n")
    return files

def generate_question(files):
    return [{
        'type': 'checkbox',
        'name': 'files',
        'message': 'What would you like to add?',
        'choices': [{'name': file.strip()} for file in files],   
    }]

class FancyGitAdd(cli.Application):
    VERSION = "1.3"
    commit = cli.Flag(['c', 'commit'], help="Commits the added files as well")
    def main(self):
        print_banner("Git Fancy add")
        files = get_files()
        
        question = generate_question(files)
        answers = prompt(question)
        git('add', answers['files'])
        if self.commit:
            git('commit', '-m', 'updates')

if __name__ == "__main__":
    FancyGitAdd()

### TESTS

def test_get_files():
    files = get_files()
    assert len(files) == 5, "There should be enough files"

def test_generate_question():
    files = ["best.rb", "good.kt", "small.py"]
    question = generate_question(files)
    assert len(question) == 1, "has to be one question"
    assert question[0]['type'] == 'checkbox', "has to allow multiple selections"
    assert len(question[0]['choices']) == len(files), "same number of choices as files"

