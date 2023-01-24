from src.thirdparty_api.atlassian_jira import JiraAccess

print(".... initiating ....")
ja = JiraAccess()

print(".... authenticating ...")
ja.init_auth()

print(".... testing ...")
ja.test_jira()

