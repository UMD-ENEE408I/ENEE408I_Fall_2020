# This is a python file you need to have in the same directory as your code so you can import it
import gather_keys_oauth2 as Oauth2
import fitbit
import pandas as pd 
import datetime
# You will need to put in your own CLIENT_ID and CLIENT_SECRET as the ones below are fake
CLIENT_ID='CLIENT_ID'
CLIENT_SECRET='CLIENT_SECRET'

server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)

# This is the date of data that I want. 
# You will need to modify for the date you want
oneDate = pd.datetime(year = 2020, month = 10, day = 31)
oneDayData = auth2_client.intraday_time_series('activities/heart',
                                               base_date=oneDate,
                                               detail_level='1sec')

df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])

print(df)

filename = oneDayData['activities-heart'][0]['dateTime'] +'_intradata'

# Export file to csv
df.to_csv(filename + '.csv', index = False)
df.to_excel(filename + '.xlsx', index = False)


