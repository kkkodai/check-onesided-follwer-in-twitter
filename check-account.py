import tweepy
import pandas as pd
import time

def authorize():
    Consumer_key = '自分のAPI Key'
    Consumer_secret = '自分のAPI Secret Key'
    Access_token = '自分のAccess Token'
    Access_secret = '自分のAccess Secret Token'
    authorization = [Consumer_key, Consumer_secret, Access_token, Access_secret]
    return authorization


def get_myaccount_data(authorization):
    auth = tweepy.OAuthHandler(authorization[0], authorization[1])
    auth.set_access_token(authorization[2], authorization[3])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_friends_id(api):
    print("フォローしているユーザのidとnameを取得中...")
    df_friends = pd.DataFrame(columns=["id","name"])
    process_id = len(api.friends_ids())
    for i, user_id in enumerate(api.friends_ids()[:6]):
        if (i+1) % 5 == 0:
            print("Processd: ", round(((i+1)/process_id)*100,2),"%")
        time.sleep(1) # 必要ないかも。人数が多ければアンコメント
        user = api.get_user(user_id)
        user_info = [user.id_str, user.name]
        df_friends.loc[i,"id"] = user_info[0]
        df_friends.loc[i,"name"] = user_info[1]
    print("完了")
    print("\n")
    df_friends.to_csv("./friends_ids.csv", index=False, encoding='utf-8-sig')
    return df_friends


def get_followers_id(api):
    print("フォロワーのidとnameを取得中...")
    df_followers = pd.DataFrame(columns=["id","name"])
    process_id = len(api.followers_ids())
    for i, user_id in enumerate(api.followers_ids()[:6]):
        if (i+1) % 5 == 0:
            print("Processd: ", round(((i+1)/process_id)*100,2),"%")
        time.sleep(1) # 必要ないかも。人数が多ければアンコメント
        user = api.get_user(user_id)
        user_info = [user.id_str, user.name]
        df_followers.loc[i,"id"] = user_info[0]
        df_followers.loc[i,"name"] = user_info[1]
    print("完了")
    print("\n")
    df_followers.to_csv("./followers_ids.csv", index=False, encoding='utf-8-sig')
    return df_followers


def check_onesided_follow(df_friends, df_followers):
    print("片方フォローをチェック中...")
    # setに変換して、集合差を出すことで片方フォローをチェック
    friends = set(df_friends["id"])
    followers = set(df_followers["id"])
    # 1. フォローバックしてくれないユーザを一括表示
    diff1 = friends.difference(followers)
    diff1_list = list(diff1)
    print("フォローバックしてくれないユーザを一括表示\n")
    print(df_friends['name'][df_friends['id'].isin(diff1_list)])
    # 2. フォローしてくれたのに自分がフォローバックしていないユーザを一括表示
    diff2 = followers.difference(friends)
    diff2_list = list(diff2)
    print("フォローしてくれたのに自分がフォローバックしていないユーザを一括表示\n")
    print(df_followers['name'][df_followers['id'].isin(diff2_list)])
    print("完了")
    print("\n")

def main():
    #Twitter APIを使用するためのConsumerキー、アクセストークン設定
    authorization = authorize()
    #自分のアカウント情報をAPIで取得
    api = get_myaccount_data(authorization)
    # フレンド(こっちがフォローしたアカウント)のidとnameを一括取得
    df_friends = get_friends_id(api)
    # フォロワーのidとnameを一括取得
    df_followers = get_followers_id(api)
    # 片方フォロー(自分はフォローしたがフォローバックしてくれないorフォローしてくれたが自分はフォローしていない)の
    # ユーザー名をprint文で一括表示
    check_onesided_follow(df_friends, df_followers)
    
if __name__ == "__main__":
    main()