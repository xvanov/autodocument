import sys
import datetime
from pyhocon import ConfigFactory

def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

def parse_conf(confName):
    conf = ConfigFactory.parse_file(f'./conf/{confName}')
    address = conf.get_string('address')
    owner = conf.get_string('owner')
    tenant = conf.get_string('tenant')
    price = conf.get_string('price')
    deposit = conf.get_string('deposit')
    return address, owner, tenant, price, deposit




def generate_sublet_agreement(outputFile, first, last, confName, contBool):
    address, owner, tenant, price, deposit = parse_conf(confName)
    fmt = '%m/%d/%Y'
    depositReturn = datetime.datetime.strftime(last + datetime.timedelta(days=6), fmt)
    first = datetime.datetime.strftime(first, fmt)
    last = datetime.datetime.strftime(last, fmt)
    if contBool:
        contClause = '(already paid)'
    else:
        contClause = ''
    agreement = f"""Sublease Agreement


{owner} is subleasing one bedroom at {address} to {tenant} (sub-licensee) from {first}, until {last}. The sub-licensee agrees to pay:

        1. returnable security deposit of ${deposit} {contClause}
        2. ${price} due {first}
        3. 1/6th of utilities (water, electricity and gas) for the utility billing period due {last}

                The security deposit will be refunded by {depositReturn}, unless items or furniture are missing, broken, or the room and common areas were not left in a clean condition. The sub-licensee is required to respect the rules and regulations of the original license agreement as well as keeping the common areas clean and being respectful in sharing the house with the rest of the occupants. The sub-licensee is responsible for cleaning the room, the bathroom and kitchen after use. No smoking or pets are allowed on the premises. The house is fully furnished with wireless internet, washer and dryer use included in the rent. The sub-licensee will provide  own household consumables. The sub-licensee will be solely responsible for ensuring that the payments are made as stated in this agreement.



{tenant}\t\t\t________________\t\t__________
(sub-licensee)\t\t\t\t(signature)\t\t\t(date)



{owner}\t\t\t\t________________\t\t_________
(sub-licensor)\t\t\t\t(signature)\t\t\t(date)

    """
    with open(outputFile, 'w') as f:
        print(agreement, file=f)

if __name__ == '__main__':
    day = sys.argv[1]
    confPath = sys.argv[2]
    contBool = True if sys.argv[3]=='continue' else False

    fmt = '%Y-%m-%d'
    first = datetime.datetime.strptime(day, fmt)
    last = last_day_of_month(first)
    outputFile = f'/home/alex/cur/8_lgx/house/tenants/{confPath.split(".")[0]}_{day}.txt'
    generate_sublet_agreement(outputFile, first, last, confPath, contBool)




