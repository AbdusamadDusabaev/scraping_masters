import datetime
import time
import requests
from config import addresses, categories
from connect import get_data, record_data
from send_email import send_email


ua_chrome = " ".join(["Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                      "AppleWebKit/537.36 (KHTML, like Gecko)",
                      "Chrome/108.0.0.0 Safari/537.36"])
headers = {"user-agent": ua_chrome}


def get_index_from_category(address, category, profile_id):
    address = addresses[address]
    category = categories[category]
    category_id = category.split("&")[0]
    job_draft_guid = category.split("&")[1]
    funnel_id = category.split("&")[2]
    today_full = str(datetime.date.today())
    today = str(datetime.date.today()).split("-")[-1]
    if category != 'category_id=1107&job_draft_guid=89c49c70-ea9c-4a2b-8ec6-0d5523984ad8&funnel_id=d271469f-ea6b-458f-b45a-c3f782d8c743_1672009327204':
        universal_keyword = f"vehicle_requirement=none&job_size=small&{funnel_id}&description=.&today_enabled=true&job_type=Template&is_recos_page=true&form_referrer=homepage_smart_search_v2_initial_dropdown&{job_draft_guid}"
    else:
        universal_keyword = f"vehicle_requirement=none&job_size=small&{funnel_id}&description=.&today_enabled=true&schedule%5Bdates%5D%5B%5D%5Bdate%5D={today_full}&schedule%5Bdates%5D%5B%5D%5Bdisabled%5D=false&schedule%5Bdates%5D%5B%5D%5Blabel%5D={today}&schedule%5Bdates%5D%5B%5D%5Bsameday%5D=false&job_type=Template&is_recos_page=true&form_referrer=homepage_smart_search_v2_initial_dropdown&{job_draft_guid}"
    url = f"https://www.taskrabbit.com/api/v3/jobs/post/bootstrap_multiday_recommend?{category_id}&{address}&{universal_keyword}"
    response = requests.get(url=url, headers=headers)
    json_object = response.json()
    master_objects = json_object["multiday_recommendations"]["recommendations"]["items"]
    index = 0
    for master_object in master_objects:
        index += 1
        master_id = master_object["slug"]
        if master_id == profile_id:
            return index


def main():
    print("[INFO] Программа запущена")
    while True:
        data = get_data()
        for client_request in data:
            client_address = client_request["address"]
            client_categories = client_request["categories"].split(", ")
            client_id = client_request["url"].split("/")[-1]
            client_email = client_request["email"]
            result = "<p>"
            for client_category in client_categories:
                client_category = client_category.strip()
                index = get_index_from_category(address=client_address, category=client_category, profile_id=client_id)
                if index is None:
                    index = "category is not active"
                sub_result = f"{client_category}: {index}"
                result = f"{result}<br>{sub_result}"
            result = result.strip()
            result = f"{result}</p></body></html>"
            send_email(client_email=client_email, data=result)
            record_data(result=client_request)
        time.sleep(2)


if __name__ == "__main__":
    main()
