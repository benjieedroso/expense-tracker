from flask_restx import Resource, Namespace
from .models import Budget, Expense, Category
from .extensions import db
from .expense_ns import calculate_total_expenses
from .api_models import summary_model

summary_ns = Namespace('summary', description='Summary related operations')

@summary_ns.route('/')
class SummaryResource(Resource):
    @summary_ns.marshal_with(summary_model)
    def get(self):
        expenses = Expense.query.all()
        budgets = Budget.query.all()
        categories = Category.query.all()

        total_expenses = sum([expense.amount for expense in expenses])
        total_budgets = sum([budget.amount for budget in budgets])

        return {"expenses": expenses, "total_expenses": total_expenses, "budgets":budgets, "total_budgets": total_budgets, "categories": categories}, 200
    

@summary_ns.route('/<int:month>/<int:year>')
class MonthlySummaryResource(Resource):
    @summary_ns.marshal_with(summary_model)
    def get(self, month, year):
        expenses = Expense.query.filter(db.extract('month', Expense.date) == month, db.extract('year', Expense.date) == year).all()
        total_expenses = sum([expense.amount for expense in expenses])
        budgets = Budget.query.filter_by(month=month, year=year).all()
        total_budgets = sum([budget.amount for budget in budgets])
        categories = Category.query.all()

        return {
            "expenses": expenses,
            "total_expenses": total_expenses,
            "budgets": budgets,
            "total_budgets": total_budgets,
            "categories": categories
        }, 200
    
@summary_ns.route('/<string:category_id>/<int:month>/<int:year>')
class CategoryMonthlySummaryResource(Resource):
    @summary_ns.marshal_with(summary_model)
    def get(self, category_id, month, year):
        expenses = Expense.query.filter(
            Expense.category == category_id,
            db.extract('month', Expense.date) == month,
            db.extract('year', Expense.date) == year
        ).all()
        total_expenses = sum([expense.amount for expense in expenses])
        budgets = Budget.query.filter_by(month=month, year=year).all()
        total_budgets = sum([budget.amount for budget in budgets])
        categories = Category.query.all()

        return {
            "expenses": expenses,
            "total_expenses": total_expenses,
            "budgets": budgets,
            "total_budgets": total_budgets,
            "categories": categories
        }, 200
    
@summary_ns.route('/<string:category_id>')
class CategorySummaryResource(Resource):
    @summary_ns.marshal_with(summary_model)
    def get(self, category_id):
        expenses = Expense.query.filter(Expense.category == category_id).all()
        total_expenses = sum([expense.amount for expense in expenses])
        budgets = Budget.query.all()
        total_budgets = sum([budget.amount for budget in budgets])
        categories = Category.query.all()

        return {
            "expenses": expenses,
            "total_expenses": total_expenses,
            "budgets": budgets,
            "total_budgets": total_budgets,
            "categories": categories
        }, 200





        
