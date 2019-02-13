# Requirement
- Python 3.7
- Django 2.1.5
- babel
- django-cors-headers
- VueCDN

# Features
- Transaction (Income/Expense) Reports
- Wallet
- Reports Statistics
- Wishlist/Savings *addition*

# Pages
- Dashboard : show reports, add report, search reports by category
              view/update/delete report link, show wallet, show reports by month, link to statistics
- Report Edit : view, update and delete report
- Login : login page
- Statistics : most money spent by category, daily expenses amount, daily
              income amount

# Backend Function
- Reports : Create, Retrieve, Update, Delete
- Users' Wallet : Create*, Update
- Category : Create (along with report), Retrieve
- Statistic : Generator

# Tables
- Reports : id, amount, isExpense, category, transactionDate
- Category : id, name
- Wallet : id, total, savings, owner
