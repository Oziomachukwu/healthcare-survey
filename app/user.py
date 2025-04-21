class User:
    def __init__(self, data):
        self.age = data.get('age')
        self.gender = data.get('gender')
        self.income = data.get('income')
        self.expenses = data.get('expenses', {})
    
    def to_csv_row(self):
        return [
            self.age,
            self.gender,
            self.income,
            self.expenses.get('utilities', 0),
            self.expenses.get('entertainment', 0),
            self.expenses.get('school_fees', 0),
            self.expenses.get('shopping', 0),
            self.expenses.get('healthcare', 0)
        ]
    
    @staticmethod
    def csv_header():
        return ['Age', 'Gender', 'Income', 'Utilities', 
                'Entertainment', 'School Fees', 'Shopping', 'Healthcare']