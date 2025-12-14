from flask_restx import Resource, Namespace
from .models import Budget, Expense
from .api_models import budget_model, create_budget_model
from .extensions import db
budget_ns = Namespace('budgets', description='Budget related operations')
@budget_ns.route('/')
class BudgetListResource(Resource):
    @budget_ns.marshal_list_with(budget_model)
    def get(self):
        budgets  = Budget.query.all()
        return budgets, 200

    @budget_ns.expect(create_budget_model)
    @budget_ns.marshal_with(budget_model)
    def post(self):

        month = budget_ns.payload['month']
        year = budget_ns.payload['year']

        expenses_spent = Expense.query.with_entities(Expense.amount).filter(db.extract('month', Expense.date) == month, db.extract('year', Expense.date) == year).all()
        total_spent = sum([expense.amount for expense in expenses_spent])

        if total_spent > budget_ns.payload['amount']:
            status = 'Budget Exceeded!'
        else:
            status = 'On Track!'

        budget = Budget(
            amount=budget_ns.payload['amount'],
            month=budget_ns.payload['month'],
            year=budget_ns.payload['year'],
            status=status
        )
        db.session.add(budget)
        db.session.commit()
        return budget, 201