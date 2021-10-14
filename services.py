
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import func
from models import TokenHoldings
from dbconfig import SessionLocal, engine, Base
import datetime

session = SessionLocal()
Base.metadata.create_all(bind=engine)


def saveTokenHoldings2(tk):
    oTk = session.query(TokenHoldings).filter(and_(TokenHoldings.address == tk.address,
                                                   TokenHoldings.symbol == tk.symbol, TokenHoldings.date == tk.date)).first()
    if oTk:
        print('finded..')
        oTk.name = tk.name
        oTk.balance = tk.balance
        oTk.price = tk.price
        oTk.totalvalue = tk.totalvalue
        oTk.updatetime = datetime.datetime.now()
    else:
        session.add(tk)
    session.commit()
    session.close()


def saveTokenHoldings(address, name, symbol, balances, prices, totalvalues):
    address = address
    name = name
    symbol = symbol
    date = datetime.date.today().strftime('%Y-%m-%d')
    balance = round(float(balances), 2)
    price = round(float(prices), 2)
    totalvalue = round(float(totalvalues), 2)
    updatetime = datetime.datetime.now()
    tk = TokenHoldings(address=address, name=name, symbol=symbol, date=date,
                       balance=balance, price=price, totalvalue=totalvalue, updatetime=updatetime)
    saveTokenHoldings2(tk)


# select symbol , sum(t.balance) ,max(t.price), sum(t.totalvalue) from TokenHoldings t where t.name='ParaFi' and t.date='2021-10-14' group by t.symbol order by  sum(t.totalvalue) desc
def queryAssertByAddressDao(addresslist, date):
    return session.query(TokenHoldings.symbol, func.sum(TokenHoldings.balance).label('balance'), func.max(TokenHoldings.price).label('price'), func.sum(
        TokenHoldings.totalvalue).label('totalvalue')).filter(and_(TokenHoldings.address.in_(addresslist), TokenHoldings.date == date)).group_by(TokenHoldings.symbol).order_by(desc(func.max(TokenHoldings.totalvalue))).all()


def queryTotalValueByAddressDao(addresslist, date):
    return session.query(func.sum(
        TokenHoldings.totalvalue).label('totalvalue')).filter(and_(TokenHoldings.address.in_(addresslist), TokenHoldings.date == date)).first()


def queryTotalValueByAddress(addresslist, date):
    tks = queryAssertByAddressDao(addresslist, date)
    totalvalue = queryTotalValueByAddressDao(addresslist, date).totalvalue
    for tk in tks:
        ntk = {}
        ntk['symbol'] = tk.symbol
        ntk['balance'] = round(tk.balance, 2)
        ntk['price'] = round(tk.price, 2)
        ntk['totalvalue'] = round(tk.totalvalue, 2)
        ntk['rate'] = "%.2f%%" % (tk.totalvalue*100/totalvalue)
        yield ntk


def queryTotalValueByAddress2(addresslist):
    date = datetime.date.today().strftime('%Y-%m-%d')
    tks = queryTotalValueByAddress(addresslist, date)
    results = []
    i = 1
    for tk in tks:
        result = []
        result.append(str(i))
        result.append(tk['symbol'])
        result.append(tk['balance'])
        result.append(tk['price'])
        result.append(tk['totalvalue'])
        result.append(tk['rate'])
        results.append(result)
        i = i+1

    return results


if __name__ == '__main__':
    """
    address = '0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363'
    name = 'ParaFi'
    symbol = 'ETH3'
    date = datetime.date.today().strftime('%Y-%m-%d')
    balance = 49.71
    price = 3488.66
    totalvalue = 173652.48
    updatetime = datetime.datetime.now()
    tk = TokenHoldings(address=address, name=name, symbol=symbol, date=date,
                       balance=balance, price=price, totalvalue=totalvalue, updatetime=updatetime)
    saveTokenHoldings(tk)
    symbol = 'ETH2'
    tk = TokenHoldings(address=address, name=name, symbol=symbol, date=date,
                       balance=balance, price=price, totalvalue=totalvalue, updatetime=updatetime)
    saveTokenHoldings(tk)
    print('ok')
    """

    address = "0x5028d77b91a3754fb38b2fbb726af02d1fe44db6;0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363;0xd9b012a168fb6c1b71c24db8cee1a256b3caa2a2"
    list = address.split(';')
    tks = queryTotalValueByAddress2(list)
    for tk in tks:
        print(tk)
