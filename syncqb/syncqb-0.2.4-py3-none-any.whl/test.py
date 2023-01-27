import qb_client

def main():
    client = qb_client.get_client(True, creds={
        'QB_URL': 'https://rmcgroup.quickbase.com',
        'QB_USERTOKEN': 'b46fjf_ictm_0_c6ikfnbcer5zzpcvkhaynddjctsq'
    })

    response = client.add_field
    print(response)




if __name__ == '__main__':
    main()