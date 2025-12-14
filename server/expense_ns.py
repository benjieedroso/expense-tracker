from flask_restx import Resource, Namespace
from .models import Expense, Budget
from .api_models import expense_model, create_expense_model
from .extensions import db

expense_ns = Namespace('expenses', description='Expense related operations')

@expense_ns.route('/')
class ExpenseListResource(Resource):
    @expense_ns.marshal_list_with(expense_model)
    def get(self):
        expenses  = Expense.query.all()
        return expenses, 200

    @expense_ns.expect(create_expense_model)
    @expense_ns.marshal_with(expense_model)
    def post(self):
        expense = Expense(
            description=expense_ns.payload['description'],
            amount=expense_ns.payload['amount'],
            category=expense_ns.payload['category'],
            date=expense_ns.payload['date']
        )
        db.session.add(expense)
        db.session.commit()

        update_budget_status(
            month=expense.date.month,
            year=expense.date.year
        )

        update_spent(
            month=expense.date.month,
            year=expense.date.year
        )

        return expense, 201
    
@expense_ns.route('/<string:id>')
class ExpenseResource(Resource):
    @expense_ns.marshal_with(expense_model)
    def get(self, id):
        expense = Expense.query.get_or_404(id)
        return expense, 200

    @expense_ns.expect(create_expense_model)
    @expense_ns.marshal_with(expense_model)
    def put(self, id):
        expense = Expense.query.get_or_404(id)
        expense.description = expense_ns.payload['description']
        expense.amount = expense_ns.payload['amount']
        expense.category = expense_ns.payload['category']
        expense.date = expense_ns.payload['date']
        db.session.commit()
        return expense, 200

    def delete(self, id):
        expense = Expense.query.get_or_404(id)
        db.session.delete(expense)
        db.session.commit()
        return '', 204
    

def calculate_total_expenses(month, year):
    expenses = Expense.query.with_entities(Expense.amount).filter(db.extract('month', Expense.date) == month, db.extract('year', Expense.date) == year).all()
    total = sum([expense.amount for expense in expenses])
    return total

def update_budget_status(month, year):
    budget = Budget.query.filter_by(month=month, year=year).first()
    if not budget:
        return

    total_expenses = calculate_total_expenses(month, year)

    if total_expenses > budget.amount:
        budget.status = 'Budget Exceeded!'
    else:
        budget.status = 'On Track!'

    db.session.commit()

def update_spent(month, year):
    total_expenses = calculate_total_expenses(month, year)
    budget = Budget.query.filter_by(month=month, year=year).first()
    if budget:
        budget.spent = total_expenses
        db.session.commit()
    return total_expenses