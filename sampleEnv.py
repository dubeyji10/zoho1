# jitendra.seo@exportgenius.in  - TEG!N$kuty%85
#removed redirect_url

# config = {
#     "apiBaseUrl":"https://www.zohoapis.com",
#     "apiVersion":"v2",
#     "currentUserEmail":"info@exportgenius.in",
#     "sandbox":"False",
#     "applicationLogFilePath":"./log",
#     "client_id":"1000.YJMLLC9IJTQI2732MQJ1QOQIQ60ETU",
#     "client_secret":"c397c14e66b370e81897ffde73023c2812674ace4c",
#     "redirect_uri":"http://localhost:800/some_path",
#     "accounts_url":"https://accounts.zoho.in",
#     "token_persistence_path":"",
#     "access_type":"online"
# }
import zcrmsdk


config = {
    "apiBaseUrl":"https://www.zohoapis.in",
    "apiVersion":"v2",
    "currentUserEmail":"info@exportgenius.in",
    "sandbox":"False",
    "applicationLogFilePath":"./log",
    "client_id":"1000.YJMLLC9IJTQI2732MQJ1QOQIQ60ETU",
    "client_secret":"c397c14e66b370e81897ffde73023c2812674ace4c",
    "accounts_url":"https://accounts.zoho.in",
    "token_persistence_path":"",
    "access_type":"online"
}
    
zcrmsdk.ZCRMRestClient.initialize(config)
oauth_client = zcrmsdk.ZohoOAuth.get_client_instance()
grant_token = "1000.a5837d4344c8fca409aa41c08989a8ba.dfced0931753bf753e24472345df9877"
oauth_tokens = oauth_client.generate_access_token(grant_token)
    
print(oauth_tokens)

print("works")