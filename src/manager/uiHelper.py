import inquirer
from decimal import Decimal

class UiHelper():
    def prompt_for_obj(self, prompt, obj_lis):
        options = []
        for obj in obj_lis:
            options.append((obj.Name(), obj))
        options.append(("None", None))
        questions = [
            inquirer.List('selection',
                          message=prompt,
                          choices=options,
                          ),
        ]
        answers = inquirer.prompt(questions)
        return answers["selection"]

    def get_decimal_value(self, prompt, default):
        questions = [
            inquirer.Text('main',
                          message=prompt,
                          default=default
                          ),
        ]
        answers = inquirer.prompt(questions)
        return Decimal(answers["main"])

