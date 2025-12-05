"""
Report Sub-Pages Module
Individual report view widgets.
"""
from .sale_report import SaleReportView
from .purchase_report import PurchaseReportView
from .all_transactions import AllTransactionsView
from .day_book import DayBookView
from .profit_loss import ProfitLossView
from .bill_wise_profit import BillWiseProfitView
from .cash_transactions import CashTransactionsView
from .balance_report import BalanceReportView

__all__ = [
    'SaleReportView',
    'PurchaseReportView',
    'AllTransactionsView',
    'DayBookView',
    'ProfitLossView',
    'BillWiseProfitView',
    'CashTransactionsView',
    'BalanceReportView'
]
