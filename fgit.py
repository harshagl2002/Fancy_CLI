from pyfiglet import Figlet
from plumbum import cli
from plumbum.cmd import ls, git
import questionary

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

def print_banner(text):
    print(Figlet(font='slant').renderText(text))

class FancyGitAdd(cli.Application):
    VERSION = "1.3"
    commit = cli.Flag(['c', 'commit'], help="Commits the added file.")

    def main(self):
        print_banner("Git fancy add")

        files = get_files()
        ls = []
        for file in files:
            if file[:1] != '_':
                ls.append(file)

        question = questionary.select("What would you like to add?", choices=ls)
        to_add = question.ask()
        git('add', to_add)
        if self.commit:
            git('commit', 'm', 'updates')
    
if __name__ == "__main__":
    FancyGitAdd()

def test_get_files():
    files = get_files()
    assert len(files) == 5

def test_generate_question():
    files = ["best.rb", "good.kt", "small.py"]
    question = generate_question(files)
    assert len(question) == 1, "has to be one question"
    assert question[0]['type'] == 'checkbox', "has to allow multiple selections"
    assert len(question[0]['choices']) == len(files), "same number of choices as files"
