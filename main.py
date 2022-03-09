import requests
import pandas as pd
from decouple import config

apiKey = config('apiKey', default='')

baseurl = "https://developer.dacast.com/"
endpoint = 'v2/vod'


headers = {
  'X-Api-Key': apiKey,
  'X-Format': "default"
}

def list_videos(baseurl, endpoint, x, q='', sort='created_at', order='asc', page=1, per_page=100, tag="", category_id=None):
  """
  This function takes in a baseurl, an endpoint, and a page number, and returns a list of videos
  
  :param baseurl: the base url of the API
  :param endpoint: /videos
  :param x: The page number
  :param q: A search term
  :param sort: The field to sort by, defaults to created_at (optional)
  :param order: asc or desc, defaults to asc (optional)
  :param page: The page number of the results to retrieve, defaults to 1 (optional)
  :param per_page: The number of objects to return per page, defaults to 100 (optional)
  :param tag: The tag you want to search for
  :param category_id: The ID of the category you want to filter by
  :return: The response is a list of dictionaries. Each dictionary contains the metadata for a video.
  """
 
  response = requests.get(baseurl + endpoint + f'?page={x}&perpage=100', headers=headers)

  return response.json()

def next_page(response):
  """
  Given a response from the API, return the URL for the next page of results
  
  :param response: the response object returned by the API call
  :return: The next page of results.
  """
  return response['paging']['next']

def parse_json(response):
  """
  This function takes a response from the API and parses it into a list of dictionaries. Each
  dictionary contains the following information:
  
  title
  id
  asset_id
  duration
  filename
  password
  video_height
  video_width
  thumbnail
  share_code
  subtitles
  folder
  folder_year
  
  :param response: the response from the API
  :return: A list of dictionaries. Each dictionary is a video.
  """
  videolist = []

  try:
    
    for x in range(0,100):
      try:
        dict = {
                'title': response['data'][x]['title'],
                'id': response['data'][x]['id'],
                'asset_id': response['data'][x]['asset_id'],
                'duration': response['data'][x]['duration'],
                'filename': response['data'][x]['filename'],
                'password': response['data'][x]['password'],
                'video_height': response['data'][x]['video_height'],
                'video_width': response['data'][x]['video_width'],
              }
      except:
        print(f"Something went wrong on page {x}")

      finally:
      
        try: 
          if response['data'][x]['pictures']['thumbnail'] != None:
            dict['thumbnail'] = response['data'][x]['pictures']['thumbnail'][0]
            
        except:
          print("no thumbnail")
          dict['thumbnail'] = ""
          
        try: 
          if response['data'][x]['share_code']['facebook'] != None:
            dict['share_code'] = response['data'][x]['share_code']['facebook'] 
            
        except:
          print("no videoURL")
          dict['share_code'] = ""
          
        try: 
          if response['data'][x]['subtitles'][0]['url'] != None:
            dict['subtitles'] = response['data'][x]['subtitles'][0]['url']
            
        except:
          # print("no subtitles")
          dict['subtitles'] = ""
        try: 
          if response['data'][x]['folders'][0]['path'] != None:
            dict['folder'] = response['data'][x]['folders'][0]['path']
            
        except:
          print("not in a folder")
          dict['folder'] = ""
        try: 
          if response['data'][x]['folders'][0]['name'] != None:
            dict['folder_year'] = response['data'][x]['folders'][0]['name']
            
        except:
          print("not in a folder year")
          dict['folder_year'] = ""
        try:  
          videolist.append(dict)
        except:
          print("Couldn't append videos on this page to dictionary")
  except:
    print(f'error in page: id {x} - failed')
  finally:
    print(f'Page complete')

  return videolist
 
superlist = []
for x in range(0,106):
  print(f"Scanning page {x}")
  superlist.extend(parse_json(list_videos(baseurl, endpoint, x)))

print("Length of superlist is " + str(len(superlist)))

df = pd.DataFrame(superlist)
df.to_csv('dacast.csv', index=True)

