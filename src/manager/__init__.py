import inquirer

from manager_api import Business



class ManagerFunctions():
    business = None

    def __init__(self):
        # Open the business. NOTE: Always use a test business first!
        self.business = Business("http://localhost:55667", "apiuser", "password", "Test Business")

    def menu_main(self):
        options = []
        options.append(("Testing functions", self.menu_testing))
        options.append(("Back", None))
        questions = [
            inquirer.List('action',
                          message="What do you want to do?",
                          choices=options,
                          ),
        ]

        while True:
            answers = inquirer.prompt(questions)
            if answers["action"] is None:
                return
            answers["action"]()

    def menu_testing(self):
        options = []
        options.append(("List all suppliers", self.cmd_list_suppliers))
        options.append(("Back", None))
        questions = [
            inquirer.List('action',
                          message="What do you want to do?",
                          choices=options,
                          ),
        ]

        while True:
            answers = inquirer.prompt(questions)
            if answers["action"] is None:
                return
            answers["action"]()

    def cmd_list_suppliers(self):
        suppliers = self.business.Supplier.list()
        for supplier in suppliers:
            print(supplier.Name)
