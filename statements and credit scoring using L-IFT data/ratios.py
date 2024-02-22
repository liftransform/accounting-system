import pandas as pd
import numpy as np
from utils import get_unique_months, get_unique_years, filter_by_year

def unformat_num(num_str:str) -> float:
    if num_str == '':
        return 0
    to_include = ['.']
    to_replace = {'(': '-'}
    new_form = ''
    for char in num_str:
        if char in to_replace:
            new_form += to_replace[char]
            continue
    
        if char.isdecimal() or char in to_include:
            new_form += char
            continue
    
    return float(new_form)


def get_acc_bal_from_statement(df: pd.DataFrame, acc_name:str) -> float:
    return float(df[df['Account'] == acc_name]['Balance'].apply(lambda x: unformat_num(x)).sum())


def check_ratio(func):
    def wrapper(inc_stat, bal_sheet):
        result = None
        try:
            result = func(inc_stat, bal_sheet)
        except ZeroDivisionError:
            pass
        
        if result == np.inf or result == -np.inf:
            return np.nan
        
        return result
    
    return wrapper

@check_ratio
def calc_current_ratio(inc_statement: pd.DataFrame, balance_sheet: pd.DataFrame) -> float:
    current_assets = 0
    for curr in ['Cash', 'Ar', 'Loans to employees', 'Informal loans given']:
        current_assets += get_acc_bal_from_statement(balance_sheet, curr)
        
    current_liab = 0
    for curr in ['Ap', 'Informal loan', 'Short term loan']:
         current_liab += get_acc_bal_from_statement(balance_sheet, curr)
        
    
    return current_assets / current_liab

@check_ratio
def calc_quick_ratio(inc_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
    current_assets = 0
    for curr in ['Cash', 'Ar']:
        current_assets += get_acc_bal_from_statement(balance_sheet, curr)
       
    current_liab = 0
    for curr in ['Ap', 'Informal loan', 'Short term loan']:
         current_liab += get_acc_bal_from_statement(balance_sheet, curr)
        
    return current_assets / current_liab

@check_ratio
def calc_FATO(inc_statement, bal_sheet: pd.DataFrame) -> float:
    fato = 0
    for item in ['Equipment', 'Building', 'Land']:
        fato += get_acc_bal_from_statement(bal_sheet, item)
    
    sales = get_acc_bal_from_statement(inc_statement, 'Sales')
    return sales / fato

@check_ratio
def calc_TATO(inc_statement:pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    sales = get_acc_bal_from_statement(inc_statement, 'Sales')
    tato = get_acc_bal_from_statement(bal_sheet, 'Total assets')
    return sales/tato

@check_ratio
def calc_debt_ratio(inc_statement:pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    debt = get_acc_bal_from_statement(bal_sheet, 'Total liabilities')
    assets = get_acc_bal_from_statement(bal_sheet, 'Total assets')
    return debt/assets

@check_ratio
def calc_EM(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    assets = get_acc_bal_from_statement(bal_sheet, 'Total assets')
    equity = get_acc_bal_from_statement(bal_sheet, 'Equity')
    return assets/equity

@check_ratio
def calc_PM(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    ni = get_acc_bal_from_statement(inc_statement, 'Net income')
    sales = get_acc_bal_from_statement(inc_statement, 'Sales')
    return ni / sales

@check_ratio
def calc_GP(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    purchases = get_acc_bal_from_statement(inc_statement, 'Purchases')
    sales = get_acc_bal_from_statement(inc_statement, 'Sales')
    return (sales + purchases) / sales

@check_ratio
def calc_ROA(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    ni = get_acc_bal_from_statement(inc_statement, 'Net income')
    assets = get_acc_bal_from_statement(bal_sheet, 'Total assets')
    return ni / assets

@check_ratio
def calc_ROE(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    ni = get_acc_bal_from_statement(inc_statement, 'Net income')
    equity = get_acc_bal_from_statement(bal_sheet, 'Equity')
    return ni / equity

@check_ratio
def calc_withdrawal_ratio(inc_statement: pd.DataFrame, bal_sheet: pd.DataFrame) -> float:
    ni = get_acc_bal_from_statement(inc_statement, 'Net income')
    payouts = get_acc_bal_from_statement(inc_statement, 'Withdrawal')
    return (-1 * payouts) / ni

