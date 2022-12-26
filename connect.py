import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


api_json = {
  "type": "service_account",
  "project_id": "tally-so",
  "private_key_id": "19859acac092450ec553487ce79d30054025a22f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDhBXfkJksPKNLI\nfUkMEU4e2iG1GBKH/fnVcDSaB1ASxfBAt+O0cl+zk+MPfWBIeDJHjKWX8VWb4Xfj\nvfBtYS8PXRm22Dce8st4/+WWY2kfnOLdK1N/2iEUxmIvJpyDuV2LALfq06JILaxW\ngfq4KwM4SMRtUjwg6xDKHeytBHd59kHk1V/SU/Rccy1sQMKfSuDw44XztyeBznrk\nnhtgXfyzW/67ANQByNkqK18tmq5854id0oBHDcF/qkv1SZZLqJVJE48b5JsU1rBl\nSpwLWi2DPRcUNZPpEPwS7f6C3gd1/8J96pJ2tl3IRUYfHX5ctWEK8Veiu5tBTtug\nkU7Ah8z/AgMBAAECggEABUZmisT8X3eahrQBLAo/0D4Bf52ihD5HnAxMVLa1LCt9\nuAFXki8C3/0ohoAZlg6onGrHUFTfp+QqNlQz4wHd44361gF4O/5/F0VlxsJqgCDi\nZJg+azHcMqt6jmu+TDbijX6lJm5y+x7ZpRGDpMuaq2LGpWAXJBe+m1kGPQFszOwW\nBZtYywwocb7s59HowNtjXYF9JfRi5jmw9dBa9jaoMjZbTPfa/0vmWPhFmz5w/2hk\nMoOYnP+XLQNBL3ytDSYLLsAsAsYC7cUovFvmCaQZlFORt70kesZubJMi2aKNLepo\n7Sd5VQDeJD4L31RG1oUYYPfh29NV+KxoNJt4u3p9cQKBgQDzqOWNyk9n9ULNG7oe\n5UErpObpAyP+L3hsWTyuB2ctyhjJoKwVC/pCpcCa8Z3rt0f3dxZ3f1iR2az1AfaW\nQpAnAUBcHbvsJ5KQ4PCcn7SaviYb/Y0k02hJf3ZUTGGqUxJh+H1kpPnXj1YLF+XG\nX1DH8kHiFnGoKwSqHNF3JzdTtwKBgQDsauuy+OsHDyV+BGgbLyfUzsKu6uA5fnNM\nHRL7RwgRzq0ZVSAm6YyM7hGUKKZ2JaYTaqShF6gMf/tOm0Fb0pdnUPxzxABMGIUU\ni0zEkMhOjAWWnVGVQbhFp3sX5NNSAWRSbiSAqouCwqar8Ot8NA8T8rSnTuGBjfqC\nN4q91cOg+QKBgHfo2m9Y7JMAhAtkZcfmkpfj4y8wuHnS6rSHhfEu+3vxRRmU1JrW\n9iXuZEbcORdTbzs9g/Ty2qeMNC2u9ackwsQvPXkXuO+S2fIqgL7TaZHtmduUf+1r\njJr++0CpBjdIAnfsTelFtx56D6IN9KoXJi3/7qRQ30YfRYBiBkNZLUUpAoGBAICO\nf455pqvXA6cr1ER79ufUaq7dD4KUDTQlVy4GaQ/t19i/nlUqiIAV8L8k/6edP1qt\nkcn7aCkr6sbKy9aXhDbtJen5ecPnTW5ndR4qMJHtuBg3gaZs7zwJH3lVt8eO9DOS\nqwzAME6xdBppTlPipxRM1QlpblyZjNAETdB+jftZAoGBAOUqbTD/+Elafm3S9qVX\nLwM3+7k10SKjeMGQ8gIAT7ltFxLC6iz3CnsX89BHJZTZ0QxrNx/GZA/eTwEVGQE3\nhoa3NLDfZyc4qddr9SRkhoZG1hO9S1eWSEq/emoPkjl/1rm/KKQHnZ8x4yBPbtt7\nFQDfqrJ6887Qeli1bQi4L+Op\n-----END PRIVATE KEY-----\n",
  "client_email": "tally-so-master-index-checker@tally-so.iam.gserviceaccount.com",
  "client_id": "108774980116330337063",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tally-so-master-index-checker%40tally-so.iam.gserviceaccount.com"
}
sheet_id = "1AL2qXbJekvOIIAb6xsi3AHLdAfXaBnDr-XLmb6hvXg4"


def get_service_sacc():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_service = ServiceAccountCredentials.from_json_keyfile_dict(api_json, scopes=scopes).authorize(httplib2.Http())
    return build(serviceName="sheets", version="v4", http=creds_service)


def get_data():
    service = get_service_sacc()
    sheet = service.spreadsheets()
    response = sheet.values().get(spreadsheetId=sheet_id, range=f"Requests!A2:AS100000").execute()
    result = list()
    index = 1
    for element in response["values"]:
        index += 1
        if element[5] != "ВЫПОЛНЕНО":
            sub_result = dict()
            sub_result["address"] = element[3]
            sub_result["categories"] = element[4]
            sub_result["url"] = element[43]
            sub_result["email"] = element[44]
            sub_result["index"] = index
            result.append(sub_result)
    return result


def record_data(result):
    service = get_service_sacc()
    sheet = service.spreadsheets()
    index = result["index"]
    values = [["ВЫПОЛНЕНО", result["url"], result["email"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
               "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]
    body = {"values": values}
    sheet.values().update(spreadsheetId=sheet_id, range=f"Requests!F{index}:AS{index}",
                          valueInputOption="RAW", body=body).execute()
    print(f"[INFO] Данные о клиенте {result['email']} были перезаписаны в Google Sheets")


if __name__ == "__main__":
    get_data()
