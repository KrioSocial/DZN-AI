# Database models initialization
# This file imports all models for easy access throughout the application

from .user import User
from .client import Client
from .project import Project
from .task import Task
from .message import Message
from .design import Design
from .product import Product
from .invoice import Invoice
from .marketing import MarketingContent
from .calendar import CalendarEvent
from .activity import ActivityLog

# Export all models
__all__ = [
    'User',
    'Client',
    'Project',
    'Task',
    'Message',
    'Design',
    'Product',
    'Invoice',
    'MarketingContent',
    'CalendarEvent',
    'ActivityLog'
]

