import inventory, sales, expenses, loans, equity, other_assets
import datetime as dt

# Form states
form_state = None

BUY_INV_CASH_STATE = 'buy_inv_cash'
BUY_INV_CREDIT_STATE = 'buy_inv_credit'
SELL_INV_CASH_STATE = 'sell_inv_cash'
SELL_INV_CREDIT_STATE = 'sell_inv_credit'
USE_SUPPLY_STATE = 'use_supply_state'
PERSONAL_USE_SUPPLY_STATE = 'use_inventory_state'
INVEST_INV_STATE = 'invest_inventory_state'
PAY_VENDOR_STATE = 'pay_vendor_state'

RENT_EXP_STATE = 'rent_exp_state'
UTILIY_EXP_STATE = 'UTILIY_exp_state'
AD_EXP_STATE = 'ad_exp_state'
SALARY_EXP_STATE = 'salary_exp_state'
OTHER_EXP_STATE = 'rent_exp_state'

COLLECT_PAYMENT_STATE = 'collect_payment_state'

BORROW_STATE = 'borrow state'
PAY_INTEREST_STATE = 'pay-interest-state'
REPAY_LOAN = 'repay_loan'
GIVE_LOAN_STATE = 'give loan'
GET_INTEREST_STATE = 'get interest_state'
GET_BORROWER_REPAYMENT = 'receive borrower repayment'

TAKEOUT_CASH_STATE = 'takeout_cash_state'
INVEST_CASH_STATE = 'invest_cash_state'

BUY_EQUIP_STATE = 'buy equipment state'
DISPOSE_EQUIP_STATE = 'dispose equipment state'
EXCHANGE_EQUIP_STATE = 'exchange equipment state'
INVEST_PERSONAL_ASSET_STATE = 'invest personal asset state'
USE_ASSET_PERSONALLY = 'use asset personally'
#-----------------

DATE = 'date'
AMOUNT = 'amount'
NOTE = 'note'
QUANTITY ='quantity'
COST = 'cost'
INVENTORY_NAME = 'inv_name'
#--------------inventory related
SELLER_NAME = 'Seller name'
SELLER_PHONE = 'Seller phone'
INVENTORY_TYPE = 'inventory_type'
CUSTOMER_NAME = 'customer name'
CUSTOMER_PHONE = 'customer_phone'

#---------------------Loan related
LENDER_NAME = 'lender_name'
LOAN_TYPE = 'loan_type'
LOAN = 'loan'
BORROWER_NAME = 'borrower_name'

FOR_BUSINESS = 'for_business'
FOR_PERSONAL = 'for_personal'
BUSINESS_PERSONAL = 'business_personal'

#------------------Equipment
EQUIPMENT_NAME = 'equipment name'
EQUIPMENT = 'equipment'
USAGE_YEARS = 'usage years'
EQ_CASH_TAKEN = 'equipment cash taken'
EQ_CASH_GIVEN = 'equipment cash given'


def convert_to_date(str_date:str):
    return dt.datetime.strptime(str_date, "%m/%d/%Y").date()


#---------------These functions will connect form variables to transaction parameters
def exe_buy_inventory_cash(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    info = inventory.VendorInfo(data[SELLER_NAME], data[SELLER_PHONE])
    inv_name = data[INVENTORY_NAME]
    inv_type = data[INVENTORY_TYPE]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    amount = quantity * cost

    # print(date, type(date))
    inventory.buy_inventory_cash(date, note, amount,info, inv_name,
                                 inv_type, quantity, cost)


def exe_buy_inventory_credit(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    info = inventory.VendorInfo(data[SELLER_NAME], data[SELLER_PHONE])
    inv_name = data[INVENTORY_NAME]
    inv_type = data[INVENTORY_TYPE]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    amount = quantity * cost

    # print(date, type(date))
    inventory.buy_inventory_credit(date, note, amount,info, inv_name,
                                 inv_type, quantity, cost)


def exe_sell_inventory_cash(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    info = sales.CustomerInfo(data[CUSTOMER_NAME], data[CUSTOMER_PHONE])
    inv_name = data[INVENTORY_NAME]
    quantity = float(data[QUANTITY])
    amount = float(data[AMOUNT])

    # print(date, type(date))
    inventory.sale_inventory_cash(date, note, amount, info, inv_name, quantity)


def exe_sell_inventory_credit(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    info = sales.CustomerInfo(data[CUSTOMER_NAME], data[CUSTOMER_PHONE])
    inv_name = data[INVENTORY_NAME]
    quantity = float(data[QUANTITY])
    amount = float(data[AMOUNT])

    # print(date, type(date))
    inventory.sale_inventory_credit(date, note, amount, info, inv_name, quantity)

def exe_use_inventory(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    inv_name = data[INVENTORY_NAME]
    quantity = float(data[QUANTITY])

    # print(date, type(date))
    inventory.use_inventory(date, note, inv_name, quantity)
 
def exe_use_inventory_personally(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    inv_name = data[INVENTORY_NAME]
    quantity = float(data[QUANTITY])

    # print(date, type(date))
    inventory.use_personally(date, note, inv_name, quantity)
 
def exe_invest_inventory(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    inv_name = data[INVENTORY_NAME]
    inv_type = data[INVENTORY_TYPE]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    # amount = quantity * cost

    # print(date, type(date))
    inventory.invest_inventory(date, note, inv_name, inv_type, quantity, cost)
 
def exe_pay_vendor(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    name = data[SELLER_NAME]
    amount = float(data[AMOUNT])
    
    ven_info = inventory.VendorInfo.get_vendor(inventory.VendorInfo(name, None))
    # print(date, type(date))
    inventory.pay_vendor(date, note, ven_info, amount)


def exe_rent_expense(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    purpose = data[BUSINESS_PERSONAL]
    print('Purpose', purpose)
    if purpose == FOR_BUSINESS:
        expenses.rent_expense(date, note, amount)
    elif purpose == FOR_PERSONAL:
        expenses.personal_expense(date, note + '- Rent', amount)

def exe_utility_expense(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    purpose = data[BUSINESS_PERSONAL]
    print('Purpose', purpose)
    if purpose == FOR_BUSINESS:
        expenses.utility_expense(date, note, amount)
    elif purpose == FOR_PERSONAL:
        expenses.personal_expense(date, note + '- Utility', amount)


def exe_ad_expense(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    purpose = data[BUSINESS_PERSONAL]
    print('Purpose', purpose)
    if purpose == FOR_BUSINESS:
        expenses.advertising_expense(date, note, amount)
    elif purpose == FOR_PERSONAL:
        expenses.personal_expense(date, note + '- Ad', amount)


def exe_salaries_expense(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    purpose = data[BUSINESS_PERSONAL]
    print('Purpose', purpose)
    if purpose == FOR_BUSINESS:
        expenses.salaries_expense(date, note, amount)
    elif purpose == FOR_PERSONAL:
        expenses.personal_expense(date, note + '- Salaries', amount)


def exe_other_expense(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    purpose = data[BUSINESS_PERSONAL]
    print('Purpose', purpose)
    if purpose == FOR_BUSINESS:
        expenses.other_expense(date, note, amount)
    elif purpose == FOR_PERSONAL:
        expenses.personal_expense(date, note + '- Other', amount)

def exe_collect_payment(data):
    date = convert_to_date(data[DATE])
    amount = float(data[AMOUNT])
    cus_name = data[CUSTOMER_NAME]
    note = data[NOTE]
    sales.collect_on_credit_sales(date, note, amount, sales.CustomerInfo(cus_name, None))


def exe_borrow(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    name = data[LENDER_NAME]
    amount = float(data[AMOUNT])
    lt = data[LOAN_TYPE]

    loans.take_loan(date, note, name, amount, lt)


def exe_pay_interest(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    loan = data[LOAN]
    amount = float(data[AMOUNT])

    loan_id = float(loan.split(',')[0])

    loans.pay_interest(date, note, loan_id, amount)


def exe_repay_loan(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    loan = data[LOAN]
    amount = float(data[AMOUNT])

    loan_id = float(loan.split(',')[0])

    loans.pay_principal(date, note, loan_id, amount)


def exe_give_loan(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    name = data[BORROWER_NAME]
    amount = float(data[AMOUNT])
    lt = data[LOAN_TYPE]

    loans.give_loan(date, note, name, amount, lt)


def exe_get_interest(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    loan = data[LOAN]
    amount = float(data[AMOUNT])

    loan_id = float(loan.split(',')[0])

    loans.get_interest(date, note, loan_id, amount)


def exe_receive_loan_repayment(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    loan = data[LOAN]
    amount = float(data[AMOUNT])

    loan_id = float(loan.split(',')[0])

    loans.get_principal(date, note, loan_id, amount)


def exe_takeout_cash(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])
    equity.use_cash_personally(date, note, amount)


def exe_invest_cash(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    amount = float(data[AMOUNT])

    equity.invest_cash(date, note, amount)


def exe_buy_equip(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    name = data[EQUIPMENT_NAME]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    usage = float(data[USAGE_YEARS])

    other_assets.buy_asset(date, note, name, quantity, cost, usage)


def exe_dispose_asset(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    equip:str = data[EQUIPMENT]
    amount = float(data[AMOUNT])

    equipment_id = int(equip.split(',')[0])

    other_assets.dispose_asset(date, note, amount, equipment_id)



def exe_exchange_asset(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    old_equip = data[EQUIPMENT]
    cash_received = float(data[EQ_CASH_TAKEN])
    cash_given= float(data[EQ_CASH_GIVEN])
    name = data[EQUIPMENT_NAME]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    usage = float(data[USAGE_YEARS])

    cash = cash_received - cash_given

    equipment_id = int(old_equip.split(',')[0])

    other_assets.exchange_asset(date, note, equipment_id, name, quantity, cost, cash, usage)


def exe_invest_personal_asset(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    name = data[EQUIPMENT_NAME]
    quantity = float(data[QUANTITY])
    cost = float(data[COST])
    usage = float(data[USAGE_YEARS])

    other_assets.invest_equipment(date, note, name, quantity, cost, usage)


def exe_use_asset_personally(data):
    date = convert_to_date(data[DATE])
    note = data[NOTE]
    quantity = float(data[QUANTITY])
    equip:str = data[EQUIPMENT]
    
    equipment_id = int(equip.split(',')[0])

    other_assets.use_asset_personally(date, note, equipment_id, quantity)


def execute_transction(data):
    state_func = {
        BUY_INV_CASH_STATE: exe_buy_inventory_cash,
        BUY_INV_CREDIT_STATE: exe_buy_inventory_credit,
        SELL_INV_CASH_STATE: exe_sell_inventory_cash,
        SELL_INV_CREDIT_STATE: exe_sell_inventory_credit,
        USE_SUPPLY_STATE: exe_use_inventory,
        PERSONAL_USE_SUPPLY_STATE: exe_use_inventory_personally,
        INVEST_INV_STATE: exe_invest_inventory,
        PAY_VENDOR_STATE: exe_pay_vendor,
        RENT_EXP_STATE: exe_rent_expense,
        UTILIY_EXP_STATE: exe_utility_expense,
        AD_EXP_STATE: exe_ad_expense,
        SALARY_EXP_STATE: exe_salaries_expense,
        OTHER_EXP_STATE: exe_other_expense,
        COLLECT_PAYMENT_STATE: exe_collect_payment,
        BORROW_STATE: exe_borrow,
        PAY_INTEREST_STATE: exe_pay_interest,
        REPAY_LOAN: exe_repay_loan,
        GIVE_LOAN_STATE: exe_give_loan,
        GET_INTEREST_STATE: exe_get_interest,
        GET_BORROWER_REPAYMENT: exe_receive_loan_repayment,
        TAKEOUT_CASH_STATE: exe_takeout_cash,
        INVEST_CASH_STATE: exe_invest_cash,
        BUY_EQUIP_STATE: exe_buy_equip,
        DISPOSE_EQUIP_STATE: exe_dispose_asset,
        EXCHANGE_EQUIP_STATE: exe_exchange_asset,
        INVEST_PERSONAL_ASSET_STATE: exe_invest_personal_asset,
        USE_ASSET_PERSONALLY: exe_use_asset_personally
    }

    # try:
    func = state_func[form_state]
    func(data)
    # except Exception as e:
        # print(e)
        # raise e
    
    