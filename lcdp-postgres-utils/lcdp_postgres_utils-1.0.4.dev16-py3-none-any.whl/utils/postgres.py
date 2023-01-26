from .ssm import fetch_password_from_ssm
import pg8000


def get_connection(db_name, endpoint, user_name, ssm_db_password_path):
    """
        Method to establish the connection.
    """
    try:
        print("Connecting to database")
        # Read the environment variables to get DB EndPoint
        db_password = fetch_password_from_ssm(ssm_db_password_path)

        # Establishes the connection with the server using the token generated as password
        conn = pg8000.connect(
            host=endpoint,
            user=user_name,
            database=db_name,
            password=db_password
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print("While connecting failed due to :{0}".format(str(e)))
        return None
