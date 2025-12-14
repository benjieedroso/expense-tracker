from flask_restx import fields
from .extensions import api


category_model = api.model('Category', {
    'id': fields.String,
    'name': fields.String,
})

expense_model = api.model('Expense', {
    'id': fields.String,
    'description': fields.String,
    'amount': fields.Float,
    'category': fields.String,
    'date': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
})

create_expense_model = api.model('CreateExpense', {
    'amount': fields.Float,
    'description': fields.String,
    'category': fields.String,
    'date': fields.String,
})

budget_model = api.model('Budget', {
    'id': fields.String,
    'amount': fields.Float,
    'month': fields.Integer,
    'year': fields.Integer,
    'status': fields.String,
    'spent': fields.Float,
    'created_at': fields.String,
    'updated_at': fields.String,
})

create_budget_model = api.model('CreateBudget', {
    'amount': fields.Float,
    'month': fields.Integer,
    'year': fields.Integer,
})

summary_model = api.model('Summary', {
    'expenses': fields.Nested(expense_model),
    'total_expenses': fields.Float,
    'budgets': fields.Nested(budget_model),
    'total_budgets': fields.Float,
    'categories': fields.Nested(category_model),
})