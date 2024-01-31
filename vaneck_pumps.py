# %%
import requests
from sqlalchemy import create_engine, Integer, String, Column, MetaData, Table
import sqlalchemy
import pandas as pd
import pangres

eng = create_engine("postgresql://postgres:password@host:port/crypto")

webhook = "..."

cookies = {
    "sitelanguage": "{e}rst//sV1seTScheIS0uYQg==",
    "ve-country": "{e}K//5iC/vzt/hgyIRNerqy6E01n/ToIg8GGm4TFtFSJ/kZu+iSO5csb630fUQ75bi",
    "visitortype": "{e}lJwKBgBBGx/cejr8N9tp/w==",
    "banner-promo": "{e}Ba2FvSYi53I9eod/mFaA05oZjdX8OfT/yR7eBrDqgvQ=",
    "ve-country-us": "{e}O2uYcr3+77V9gb0waBp5IYgcfJ+T9xl14hVIZDIsH9lc7f32xRLaokCUV0svBo2JFBCIXtymp11qEKTqIzF3iUiHQD7N+lmk9c0jdFByIiBbaAaLncRwWWGsZclkRM1oPutvL+gWxVUjnTbR18WrEhEIF6//MJs/SevadibCTo5NZDB0ctKPRo9MajCm3b0TTZd3JR0FsShL7vhSSNhzAsGJcEAZtYxenrNm4ofiSvaU7XvKu0TTU1Qt4ERn4Eo3c2tQPR/jBjVWE+GHrRLHBA==",
    ".EPiForm_BID": "95b5349f-1eca-4e7a-a250-638e0f9fb5f7",
    ".EPiForm_VisitorIdentifier": "95b5349f-1eca-4e7a-a250-638e0f9fb5f7:",
    "__RequestVerificationToken": "PRzd6UeiAwQ5ldKYVBM6QKqF_8MN8y_PTibnP5sQkXXsurUgaAHeshk6LlzpE1THO5xIyQOMgUB_oQ6zdqB_HN-tegolEZC-cXgKUhZut9s1",
    "ASP.NET_SessionId": "t3scyb2w5mffuucgy4km5diz",
}

headers = {
    "authority": "www.vaneck.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    # 'cookie': 'sitelanguage={e}rst//sV1seTScheIS0uYQg==; ve-country={e}K//5iC/vzt/hgyIRNerqy6E01n/ToIg8GGm4TFtFSJ/kZu+iSO5csb630fUQ75bi; visitortype={e}lJwKBgBBGx/cejr8N9tp/w==; banner-promo={e}Ba2FvSYi53I9eod/mFaA05oZjdX8OfT/yR7eBrDqgvQ=; ve-country-us={e}O2uYcr3+77V9gb0waBp5IYgcfJ+T9xl14hVIZDIsH9lc7f32xRLaokCUV0svBo2JFBCIXtymp11qEKTqIzF3iUiHQD7N+lmk9c0jdFByIiBbaAaLncRwWWGsZclkRM1oPutvL+gWxVUjnTbR18WrEhEIF6//MJs/SevadibCTo5NZDB0ctKPRo9MajCm3b0TTZd3JR0FsShL7vhSSNhzAsGJcEAZtYxenrNm4ofiSvaU7XvKu0TTU1Qt4ERn4Eo3c2tQPR/jBjVWE+GHrRLHBA==; .EPiForm_BID=95b5349f-1eca-4e7a-a250-638e0f9fb5f7; .EPiForm_VisitorIdentifier=95b5349f-1eca-4e7a-a250-638e0f9fb5f7:; __RequestVerificationToken=PRzd6UeiAwQ5ldKYVBM6QKqF_8MN8y_PTibnP5sQkXXsurUgaAHeshk6LlzpE1THO5xIyQOMgUB_oQ6zdqB_HN-tegolEZC-cXgKUhZut9s1; ASP.NET_SessionId=t3scyb2w5mffuucgy4km5diz',
    "origin": "https://www.vaneck.com",
    "referer": "https://www.vaneck.com/us/en/insights/digital-assets/",
    "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

data = {
    "pageNumber": "0",
    "pageSize": "6",
    "QueryFormat": "All",
    "Author": "",
    "Category": "34669",
    "TopicalTags": "",
    "ContentTypeTags": "",
    "LocationTags": "",
    "FundTags": "",
    "SiteContext": "1",
    "Lang": "en",
}

response = requests.post(
    "https://www.vaneck.com/Main/RelatedMediaUsBlock/GetMediaWithPaging",
    cookies=cookies,
    headers=headers,
    data=data,
)
# %%
df = pd.DataFrame(response.json()["Result"]["GridCardDetails"])


def send_to_discord(new_df):
    # Placeholder for the actual implementation of sending to Discord
    # Loop through each row in the DataFrame and send a message
    for index, row in new_df.iterrows():
        # Create an embed object for the Discord message
        data = {
            "embeds": [
                {
                    "title": row["Title"],
                    "description": row["Description"],
                    "color": 5814783,  # You can change the color of the embed here
                    "image": {"url": "https://www.vaneck.com" + row["Image"]},
                    "url": "https://www.vaneck.com" + row["MediaLink"],
                }
            ]
        }

        # Make a POST request to the Discord webhook URL
        response = requests.post(
            # Put your discord webhook in here
            webhook,
            json=data,
        )

        # Check the response
        if response.status_code == 204:
            print(f"Message {index} sent successfully")
        else:
            print(
                f"Failed to send message {index}: {response.status_code}, {response.text}"
            )


def check_new_ids_and_send(df, engine):
    # Retrieve the existing Ids from the table
    existing_ids = pd.read_sql('SELECT "Id" FROM vaneck_pumps', engine)

    # Find new Ids by checking which are in `df` but not in `existing_ids`
    new_ids = df[~df["Id"].isin(existing_ids["Id"])]

    if len(new_ids.index) == 0:
        return []

    df = df.set_index("Id")

    pangres.upsert(eng, df, "vaneck_pumps", if_row_exists="ignore")

    return new_ids["Id"].tolist()


# %%
new_ids = check_new_ids_and_send(df, eng)
if new_ids == []:
    print("No new posts")
else:
    new_df = df[df["Id"].isin(new_ids)]
    send_to_discord(new_df)

# %%
