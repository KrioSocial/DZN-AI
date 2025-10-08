# Routes package initialization
# Imports all route blueprints for easy registration

from . import auth_routes
from . import client_routes
from . import project_routes
from . import design_routes
from . import product_routes
from . import invoice_routes
from . import marketing_routes
from . import calendar_routes
from . import dashboard_routes

__all__ = [
    'auth_routes',
    'client_routes',
    'project_routes',
    'design_routes',
    'product_routes',
    'invoice_routes',
    'marketing_routes',
    'calendar_routes',
    'dashboard_routes'
]

