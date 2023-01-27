import qb_client

def main():
    client = qb_client.get_client(True, creds={
        'QB_URL': 'https://rmcgroup.quickbase.com',
        'QB_USERTOKEN': 'b46fjf_ictm_0_c6ikfnbcer5zzpcvkhaynddjctsq'
    })
    data = [
        {
            '3': 113,
            '6': '4'
        },
        {
            '3': '112',
            '6': ''
        }
    ]



    response = client.do_query(database='bnj3ts22e', query='{3.GT.50}', columns=[3])
    print(response)




if __name__ == '__main__':
    main()