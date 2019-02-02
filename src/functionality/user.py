class User:
    def __init__(self, name, salary, additional_inc, state, filing_status, post_tax_funds, post_tax_monthly_funds):
        self.name = name
        self.salary = salary
        self.additional_inc = additional_inc
        self.state = state
        self.filing_status = filing_status
        self.post_tax_funds = post_tax_funds
        self.post_tax_monthly_funds = post_tax_monthly_funds

    def __repr__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.name, self.salary, self.additional_inc, self.state, self.filing_status, self.post_tax_funds, self.post_tax_monthly_funds)
