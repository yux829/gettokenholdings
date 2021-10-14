import requests
import services

def parseJson(json):
    if json:
        items = json.get('d').get('data')
        for index, item in enumerate(items):
            token = {}
            symbol = item.get('Symbol')
            if(symbol.find("<font color=''>") > -1):
                symbol = symbol[symbol.find(
                    "<font color=''>")+17:symbol.find('</font>')]
            token['Symbol'] = symbol
            balance = item.get('Balance')
            if(balance.find('<') > -1):
                balance = balance[balance.find('>')+1:balance.find('</')]
            if(balance.find('.') > -1):
                balance = balance[0:balance.find('.')+2]
            token['Balance'] = balance.replace('...', '')
            price = item.get('Price')
            if price.find('<') > -1:
                price = price[0:price.find('<')]
            token['Price'] = price.replace(',', '').replace(
                '$', '').replace('≈', '').replace('-', '0')
            value = item.get('Value')
            token['Value'] = value.replace(',', '').replace(
                '$', '').replace('≈', '').replace('-', '0')
            yield token


def getdata(address, startNo, url, proxy, cookies):
    params = '{"dataTableModel":{"draw":13,"columns":[{"data":"TokenName","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Symbol","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"ContractAddress","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"Balance","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Price","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Change24H","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"Value","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"More","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}}],"order":[{"column":6,"dir":"desc"}],"start":'+startNo+',"length":10,"search":{"value":"","regex":false}},"model":{"address":"'+address+'","hideZeroAssets":false,"filteredContract":""}}'
    # print(params)
    headers = {
        'Cookie': cookies,
        'origin': 'https://etherscan.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        # 'referer': 'https://etherscan.io/tokenholdings?a=0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363',
        'content-type': 'application/json'
    }
    try:
        r = requests.post(url, proxies=proxy,  headers=headers, data=params)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def getAllDatas(address, url, proxy, cookies):

    results1 = list(parseJson(getdata(address, "0", url, proxy, cookies)))
    results2 = list(parseJson(getdata(address, "10", url, proxy, cookies)))

    return results1+results2


def collet(name, address, url, proxy, cookies):
    addresslist = address.split(';')
    for adds in addresslist:
        print(adds)
        results = getAllDatas(adds, url, proxy, cookies)
        if len(results) == 0:
            print('find not datas ')
        for result in results:
            print(result)
            symbol = result['Symbol']
            balance = result['Balance']
            price = result['Price']
            value = result['Value']
            if(float(value) < 1000):
                continue
            services.saveTokenHoldings(
                adds, name, symbol, balance, price, value)


def  queryAsset(addersss,proxy,cookies):
    #url_en = 'https://etherscan.io/tokenholdingsnew.aspx/GetAssetDetails'
    url_cn = 'https://cn.etherscan.com/tokenholdingsnew.aspx/GetAssetDetails'
    collet('', addersss, url_cn, proxy, cookies)
    list = addersss.split(';')
    return services.queryTotalValueByAddress2(list)


if __name__ == '__main__':
    address = "0x4655b7ad0b5f5bacb9cf960bbffceb3f0e51f363"
    cookies_en = '_ga=GA1.2.1849702871.1624172453; __stripe_mid=39a0736d-0a17-4c30-98d4-3e4ed5f149243fca8e; _gid=GA1.2.1986308060.1633400568; etherscan_autologin=True; etherscan_userid=yux829; etherscan_pwd=4792:Qdxb:fcJNWoIaUOFfR/oK2gudIw==; amplitude_id_fef1e872c952688acd962d30aa545b9eetherscan.io=eyJkZXZpY2VJZCI6ImI3NDU4YWNiLTk0ZGUtNGVlMC04Y2EwLTQ5ZGE4Njk2YWFkNFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYzMzUxODY0NzM2NiwibGFzdEV2ZW50VGltZSI6MTYzMzUxOTQ5NDYyMiwiZXZlbnRJZCI6MTMsImlkZW50aWZ5SWQiOjEsInNlcXVlbmNlTnVtYmVyIjoxNH0=; etherscan_cookieconsent=True; ASP.NET_SessionId=apqyvubs4gbdkebf5kzagv2b; cf_clearance=J4c0RmrlRWgf5jEJkNw4UfmXD0HDteR6ThZxeM5fDBk-1634210041-0-250; __cflb=02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLUaLWvSFEVCCSx; __cf_bm=r0sXddKPa5Dcfv1i6BzsdsT._KwPKdVHszDTa0lbUVg-1634210043-0-AbwOhZHQhQfOKAAzltNEuSbwHB/l5RePfs6ys+QB9/bwpH075hItDX/BHC1PblS1SO8E1GB3arkG7EG4XcEnGhcrsdmgSeq6Toe6neXGEAKKcMbcr6faN5rE5k0P8dDP+w==; _gat_gtag_UA_46998878_6=1'
    proxy={"http": "http://127.0.0.1:11000","https": "http://127.0.0.1:11000" }
    results = queryAsset(address,proxy,cookies_en)
    for result in results:
        print(result)
