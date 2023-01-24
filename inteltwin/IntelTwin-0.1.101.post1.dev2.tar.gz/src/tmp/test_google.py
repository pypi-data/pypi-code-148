from src.thirdparty_api.google_gmail import GMailService

gmail = GMailService()

gmail.init_auth()

gmail.print_labels()
