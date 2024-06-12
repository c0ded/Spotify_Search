#-*-coding:utf8;-*-

import sys
import time
from datetime import datetime
import requests
import webbrowser as wb


### ADD WHILE LOOP TO KEEP ASKING
### TO RUN URLS!!
### OPEN:
### TRACK/ARTIST/ALBUM/SHOW/EPISODE URL!!!!


class spotifySearch():
	
	def __init__(self):
		
		self.time_start = time.process_time()

	def searchInput(self):
		
		search_input = self.searchInputData(data_info="input")
		search_type = self.searchInputData(data_info="type")
		
		self.searchOutput("\n*** Searching Spotify (" +  search_type.capitalize() + "s) For: " + "\"" + search_input + "\"" " ***\n")
		
		self.apiAuth(search_input, search_type)


	def searchInputData(self, data_info, type=None):

		s_type = type

		if data_info == "input":
			for i_retry in range(5):
				s_input = input("Spotify Search Input: ")
				if s_input:
					return s_input
					break
				else:
					if i_retry <= 3:
						self.searchOutput("[ERROR] No Search Input Entered!")
			else:
				self.searchOutput("[END] 5 Fails! Bye.")
				sys.exit()

		if data_info == "type":
			for t_retry in range(5):
				if t_retry == 0:
					self.searchOutput("Type Options: (\"track\" (\"1\"), \"artist\" (\"2\"), \"album\" (\"3\"), \"show\" (\"4\"), \"episode\"|\"podcast\" (\"5\"), )")
				s_type = input("Spotify Search Type: ")
				if s_type:
					s_type = s_type.lower()
					if s_type in ["track", "artist", "album", "show", "episode", "podcast", "pod", "1", "2", "3", "4", "5"]:
						s_type = s_type.replace("1", "track").replace("2", "artist").replace("3", "album").replace("4", "show").replace("5", "episode").replace("podcast", "episode").replace("pod", "episode")
						return s_type
						break
					else:
						if t_retry <= 3:
							self.searchOutput("[ERROR] Type Options: (\"track\" (\"1\"), \"artist\" (\"2\"), \"album\" (\"3\"), \"show\" (\"4\"), \"episode\"|\"podcast\"|\"pod\" (\"5\"), )")
				else:
					if t_retry <= 3:
						self.searchOutput("[ERROR] No Search Type Entered!")
			else:
				self.searchOutput("[END] 5 Fails! Bye.")
				sys.exit()
				
		if data_info == "url_run":
			for u_retry in range(5):
				u_num = input("Open Spotify URL (" + s_type + ") [#1-20] [\"no\"\\\"exit\"]: ")
				if u_num:
					if u_num.lower() not in ["no", "exit"]:
						if u_num.isdigit():
							if 1 <= int(u_num) <= 20:
								return u_num
								break
							else:
								if u_retry <= 3:
									self.searchOutput("[ERROR] Enter Number [#1-20] To Open URL Or [\"no\"\\\"exit\"].")
						else:
							if u_retry <= 3:
								self.searchOutput("[ERROR] Enter Number [#1-20] To Open URL Or [\"no\"\\\"exit\"].")
					else:
						self.searchOutput("[END] Program Quit.")
						sys.exit()
				else:
					if u_retry <= 3:
						self.searchOutput("[ERROR] No URL Number Entered!")
			else:
				self.searchOutput("[END] 5 Fails! Bye.")
				sys.exit()

		if data_info == "full_desc":
			for d_retry in range(5):
				d_num = input("See Spotify Full Description (" + s_type + ") [#1-20] [\"no\"\\\"exit\"]: ")
				if d_num:
					if d_num.lower() not in ["no", "exit"]:
						if d_num.isdigit():
							if 1 <= int(d_num) <= 20:
								return d_num
								break
							else:
								if d_retry <= 3:
									self.searchOutput("[ERROR] Enter Number [#1-20] To See Full Description Or [\"no\"\\\"exit\"].")
						else:
							if d_retry <= 3:
								self.searchOutput("[ERROR] Enter Number [#1-20] To See Full Description Or [\"no\"\\\"exit\"].")
					else:
						break
				else:
					break
			else:
				self.searchOutput("[END] 5 Fails! Next Question...")

	def apiAuth(self, input, type):
		
		s_input = input
		s_type = type

		client_id = 'b5aae5acb4b9414db6bff815437031a8'
		client_secret = '58b86f3852ef47e697164142d9ae1b21'
		
		requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
	
		auth_url = 'https://accounts.spotify.com/api/token'
		data = {
		    'grant_type': 'client_credentials',
  	  	'client_id': client_id,
 	 	  'client_secret': client_secret,
		}
		auth_response = requests.post(auth_url, data=data)
		auth_response_data = auth_response.json()
		access_token = auth_response_data['access_token']
		api_url = 'https://api.spotify.com/v1/'
		headers = {
   		 'Authorization': 'Bearer {token}'.format(token=access_token)
		}
		params = {'q': s_input, 'type': s_type, 'market': 'US'}
		info_request = requests.get(api_url + 'search', headers = headers, params = params)
		info_request_data = info_request.json()
		
		self.searchData(info_request_data, s_type)


	def searchData(self, data, type):

		s_data = data
		s_type = type
		dt = datetime.now()

		if s_type == "track":
			count = 0
			url_list = []
			results = list(self.dataFindInfo(s_data, 'items'))
			self.searchOutput("RESULTS:\n\n")
			for result in results[count]:
				title = list(self.dataFindInfo(result, 'name'))
				url = list(self.dataFindInfo(result, 'spotify'))
				popularity = list(self.dataFindInfo(result, 'popularity'))
				type = list(self.dataFindInfo(result, 'type'))
				search_time = dt.strftime("%m/%d/%Y - %I:%M:%S%p")
			
				s_artist = title[2]
				s_title = title[0]
				s_album = title[1]
				s_url = url[-1]
				s_pop = str(popularity[0])
				s_type = type[0].capitalize()
				s_time = search_time

				a_list_full = title[3::]
				a_list = []
			
				self.searchOutput("#" + str(count + 1) + "\n")
			
				for name in a_list_full:
					if name != s_artist:
						if name not in a_list:
							a_list.append(name)
							
				a_list_names = ", ".join(a_list)
				if a_list_names:
					if s_artist.lower() == "various artists":
						a_list_output = "(" + a_list_names + ")"
					else:
						a_list_output = "(feat. " + a_list_names + ")"
					self.searchOutput("TRACK ARTIST: " + s_artist + " " + a_list_output)
					url_info = [s_url, s_title, s_artist + " " + a_list_output, s_album]
					url_list.append(url_info)
				else:
					self.searchOutput("TRACK ARTIST: " + s_artist)
					url_info = [s_url, s_title, s_artist, s_album]
					url_list.append(url_info)
					
				self.searchOutput("TRACK TITLE: " + s_title)
				self.searchOutput("TRACK ALBUM: " + s_album)
				self.searchOutput("TRACK URL: " + s_url)
				self.searchOutput("TRACK POPULARITY: " + s_pop)
				self.searchOutput("TRACK TYPE: " + s_type)
				self.searchOutput("SEARCH TIME: " + s_time)
				self.searchOutput('\n')
				
				count += 1
			
			self.searchOpenURL(url_list, s_type)
				
		if s_type == "artist":
			count = 0
			url_list = []
			results = list(self.dataFindInfo(s_data, 'items'))
			self.searchOutput("RESULTS:\n\n")
			for result in results[count]:
				artist = list(self.dataFindInfo(result, 'name'))
				url = list(self.dataFindInfo(result, 'spotify'))
				follow = list(self.dataFindInfo(result, 'total'))
				popularity = list(self.dataFindInfo(result, 'popularity'))
				type = list(self.dataFindInfo(result, 'type'))
				search_time = dt.strftime("%m/%d/%Y - %I:%M:%S%p")
				
				s_artist = artist[0]
				s_url = url[0]
				s_flwrs = str(follow[0])
				s_pop = str(popularity[0])
				s_time = search_time
				s_type = type[0].capitalize()
				
				self.searchOutput("#" + str(count + 1) + "\n")
				
				url_info = [s_url, s_artist]
				url_list.append(url_info)				
				
				self.searchOutput("ARTIST NAME: " + s_artist)
				self.searchOutput("ARTIST URL: " + s_url)
				self.searchOutput("ARTIST FOLLOWERS: " + s_flwrs)
				self.searchOutput("TRACK POPULARITY: " + s_pop)
				self.searchOutput("SEARCH TIME: " + s_time)
				self.searchOutput('\n')
				
				count += 1
				
			self.searchOpenURL(url_list, s_type)
				
		if s_type == "album":
			count = 0
			url_list = []
			results = list(self.dataFindInfo(s_data, 'items'))
			self.searchOutput("RESULTS:\n\n")
			for result in results[count]:
				album = list(self.dataFindInfo(result, 'name'))
				atype = list(self.dataFindInfo(result, 'album_type'))
				url = list(self.dataFindInfo(result, 'spotify'))
				date = list(self.dataFindInfo(result, 'release_date'))
				tracks = list(self.dataFindInfo(result, 'total_tracks'))
				type = list(self.dataFindInfo(result, 'type'))
				search_time = dt.strftime("%m/%d/%Y - %I:%M:%S%p")

				s_artist = album[1]
				s_album = album[0]
				s_url = url[-1]
				try:
					s_date = datetime.strptime(date[0].replace("-", ""), '%Y%m%d')
					s_date = s_date.strftime('%m/%d/%Y')
				except:
					s_date = date[0]
				s_tracks = str(tracks[0])
				s_atype = atype[0].capitalize()
				s_time = search_time
				
				a_list_full = album[2::]
				a_list = []				
				
				self.searchOutput("#" + str(count + 1) + "\n")
				
				for name in a_list_full:
					if name != s_artist:
						if name not in a_list:
							a_list.append(name)
			
				a_list_names = ", ".join(a_list)
				if a_list_names:
					if s_artist.lower() == "various artists":
						a_list_output = "(" + a_list_names + ")"
					else:
						a_list_output = "(feat. " + a_list_names + ")"
					self.searchOutput("ALBUM ARTIST: " + s_artist + " " + a_list_output)
					url_info = [s_url, s_artist + " " + a_list_output, s_album]
					url_list.append(url_info)
				else:
					self.searchOutput("ALBUM ARTIST: " + s_artist)
					url_info = [s_url, s_artist, s_album]
					url_list.append(url_info)				
				self.searchOutput("ALBUM TITLE: " + s_album)
				self.searchOutput("ALBUM URL: " + s_url)
				self.searchOutput("ALBUM DATE: " + s_date)
				self.searchOutput("ALBUM TRACKS: " + s_tracks)
				self.searchOutput("ALBUM TYPE: " + s_atype)
				self.searchOutput("SEARCH TIME: " + s_time)
				self.searchOutput('\n')
	
				count += 1
				
			self.searchOpenURL(url_list, s_type)
			
		if s_type == "show":
			count = 0
			url_list = []
			results = list(self.dataFindInfo(s_data, 'items'))
			self.searchOutput("RESULTS:\n\n")
			for result in results[count]:
				show = list(self.dataFindInfo(result, 'name'))
				url = list(self.dataFindInfo(result, 'spotify'))
				description = list(self.dataFindInfo(result, 'description'))
				episodes = list(self.dataFindInfo(result, 'total_episodes'))
				type = list(self.dataFindInfo(result, 'type'))
				search_time = dt.strftime("%m/%d/%Y - %I:%M:%S%p")
				
				s_show = show[0]
				s_url = url[0]
				s_desc_full = description[0]
				if len(s_desc_full) > 175:
					s_desc = s_desc_full[:175] + "..."
				else:
					s_desc = s_desc_full
				s_eps = str(episodes[0])
				s_time = search_time
				s_type = type[0].capitalize()
				
				self.searchOutput("#" + str(count + 1) + "\n")
				
				url_info = [s_url, s_show, s_desc_full]
				url_list.append(url_info)				
				
				self.searchOutput("SHOW NAME: " + s_show)
				self.searchOutput("SHOW DESCRIPTION: " + s_desc)
				self.searchOutput("SHOW URL: " + s_url)
				self.searchOutput("SHOW EPISODES: " + s_eps)
				self.searchOutput("SHOW TYPE: " + s_type)
				self.searchOutput("SEARCH TIME: " + s_time)
				self.searchOutput('\n')
				
				count += 1
				
			self.searchFullDescription(url_list, s_type)
				
		if s_type == "episode":
			count = 0
			url_list = []
			results = list(self.dataFindInfo(s_data, 'items'))
			self.searchOutput("RESULTS:\n\n")
			for result in results[count]:
				ep = list(self.dataFindInfo(result, 'name'))
				url = list(self.dataFindInfo(result, 'spotify'))
				description = list(self.dataFindInfo(result, 'description'))
				date = list(self.dataFindInfo(result, 'release_date'))
				duration = list(self.dataFindInfo(result, 'duration_ms'))
				type = list(self.dataFindInfo(result, 'type'))
				search_time = dt.strftime("%m/%d/%Y - %I:%M:%S%p")
				
				s_ep = ep[0]
				s_url = url[0]
				s_desc_full = description[0]
				if len(s_desc_full) > 175:
					s_desc = s_desc_full[:175] + "..."
				else:
					s_desc = s_desc_full
				try:
					s_date = datetime.strptime(date[0].replace("-", ""), '%Y%m%d')
					s_date = s_date.strftime('%m/%d/%Y')
				except:
					s_date = date[0]
				s_dur = str(duration[0])
				ms = int(s_dur)
				secs = int((ms/1000)%60)
				mins = int((ms/(1000*60))%60)
				hours = (ms/(1000*60*60))%24
				s_dur = "%02d:%02d:%02d" % (hours, mins, secs)
				s_time = search_time
				s_type = type[0].capitalize()
				
				self.searchOutput("#" + str(count + 1) + "\n")
				
				url_info = [s_url, s_ep, s_desc_full]
				url_list.append(url_info)				
				
				self.searchOutput("EPISODE TITLE: " + s_ep)
				self.searchOutput("EPISODE DESCRIPTION: " + s_desc)
				self.searchOutput("EPISODE URL: " + s_url)
				self.searchOutput("EPISODE DATE: " + s_date)
				self.searchOutput("EPISODE DURATION: " + s_dur + " (Run Time)")
				self.searchOutput("EPISODE TYPE: " + s_type)
				self.searchOutput("SEARCH TIME: " + s_time)
				self.searchOutput('\n')
				
				count += 1
				
			self.searchFullDescription(url_list, s_type)


	def dataFindInfo(self, data, kv):
		
		if isinstance(data, list):
			for i in data:
				for x in self.dataFindInfo(i, kv):
					yield x
		elif isinstance(data, dict):
			if kv in data:
				yield data[kv]
			for j in data.values():
				for x in self.dataFindInfo(j, kv):
					yield x


	def searchFullDescription(self, url_list, type):
		
		u_list = url_list
		u_type = type
		
		u_run = self.searchInputData(data_info="full_desc", type=u_type)
		
		if u_type.lower() == "show":
			if u_run:
				u_url = u_list[int(u_run) - 1][0]
				u_title = u_list[int(u_run) - 1][1]
				u_desc = u_list[int(u_run) - 1][2]
				
				self.searchOutput('\n')
				self.searchOutput("SHOW TITLE: " + u_title)
				self.searchOutput("SHOW DESCRIPTION: " + u_desc)
				self.searchOutput("SHOW URL: " + u_url)
				self.searchOutput('\n')
				self.searchOpenURL(u_list, u_type)
			else:
				self.searchOpenURL(u_list, u_type)
		
		if u_type.lower() == "episode":
			if u_run:
				u_url = u_list[int(u_run) - 1][0]
				u_title = u_list[int(u_run) - 1][1]
				u_desc = u_list[int(u_run) - 1][2]
				
				self.searchOutput('\n')
				self.searchOutput("EPISODE TITLE: " + u_title)
				self.searchOutput("EPISODE DESCRIPTION: " + u_desc)
				self.searchOutput("EPISODE URL: " + u_url)
				self.searchOutput('\n')
				self.searchOpenURL(u_list, u_type)
			else:
				self.searchOpenURL(u_list, u_type)
				
				
	def searchOpenURL(self, url_list, type):
		
		u_list = url_list
		u_type = type
		
		u_run = self.searchInputData(data_info="url_run", type=u_type)
		
		if u_type.lower() == "track":
			u_url = u_list[int(u_run) - 1][0]
			u_title = u_list[int(u_run) - 1][1]
			u_artist = u_list[int(u_run) - 1][2]
			u_album = u_list[int(u_run) - 1][3]			

			self.searchOutput("\n*** OPENING URL (" +  u_type.capitalize() + ") [#" + u_run + "]:\n")
			self.searchOutput("TRACK ARTIST: " + u_artist)
			self.searchOutput("TRACK TITLE: " + u_title)
			self.searchOutput("TRACK ALBUM: " + u_album)
			self.searchOutput("TRACK URL: " + u_url)
			
			#wb.open(u_url, new=2, autoraise=True)
			#import urllib.request
			#urllib.request.urlopen(u_url)
			
			#import androidhelper 

			#url = "http://www.Google.com"
			#androidhelper.Android().startActivity("android.intent.action.VIEW", url)
				
			#import android
			#url = "http://www.Google.com"
			#android.Android().startActivity("android.intent.action.VIEW", url)

			wb.open(u_url, new=1, autoraise=True)

		if u_type.lower() == "artist":
			u_url = u_list[int(u_run) - 1][0]
			u_artist = u_list[int(u_run) - 1][1]

			self.searchOutput("\n*** OPENING URL (" +  u_type.capitalize() + ") [#" + u_run + "]:\n")
			self.searchOutput("ARTIST NAME: " + u_artist)
			self.searchOutput("ARTIST URL: " + u_url)
			
			#wb.open(u_url, new=2, autoraise=True)
			#import urllib.request
			#urllib.request.urlopen(u_url)
			
			#import androidhelper 

			#url = "http://www.Google.com"
			#androidhelper.Android().startActivity("android.intent.action.VIEW", url)
				
			#import android
			#url = "http://www.Google.com"
			#android.Android().startActivity("android.intent.action.VIEW", url)

			wb.open(u_url, new=1, autoraise=True)

		if u_type.lower() == "album":
			u_url = u_list[int(u_run) - 1][0]
			u_artist = u_list[int(u_run) - 1][1]
			u_album = u_list[int(u_run) - 1][2]			

			self.searchOutput("\n*** OPENING URL (" +  u_type.capitalize() + ") [#" + u_run + "]:\n")
			self.searchOutput("ALBUM ARTIST: " + u_artist)
			self.searchOutput("ALBUM TITLE: " + u_album)
			self.searchOutput("ALBUM URL: " + u_url)
			
			#wb.open(u_url, new=2, autoraise=True)
			#import urllib.request
			#urllib.request.urlopen(u_url)
			
			#import androidhelper 

			#url = "http://www.Google.com"
			#androidhelper.Android().startActivity("android.intent.action.VIEW", url)
				
			#import android
			#url = "http://www.Google.com"
			#android.Android().startActivity("android.intent.action.VIEW", url)

			wb.open(u_url, new=1, autoraise=True)
			
		if u_type.lower() == "show":
			u_url = u_list[int(u_run) - 1][0]
			u_title = u_list[int(u_run) - 1][1]
			u_desc_full = u_list[int(u_run) - 1][2]
			if len(u_desc_full) > 175:
				u_desc = u_desc_full[:175] + "..."
			else:
				u_desc = u_desc_full

			self.searchOutput("\n*** OPENING URL (" +  u_type.capitalize() + ") [#" + u_run + "]:\n")
			self.searchOutput("SHOW TITLE: " + u_title)
			self.searchOutput("SHOW DESCRIPTION: " + u_desc)
			self.searchOutput("SHOW URL: " + u_url)
			
			#wb.open(u_url, new=2, autoraise=True)
			#import urllib.request
			#urllib.request.urlopen(u_url)
			
			#import androidhelper 

			#url = "http://www.Google.com"
			#androidhelper.Android().startActivity("android.intent.action.VIEW", url)
				
			#import android
			#url = "http://www.Google.com"
			#android.Android().startActivity("android.intent.action.VIEW", url)

			wb.open(u_url, new=1, autoraise=True)
			
			
		if u_type.lower() == "episode":
			u_url = u_list[int(u_run) - 1][0]
			u_title = u_list[int(u_run) - 1][1]
			u_desc_full = u_list[int(u_run) - 1][2]
			if len(u_desc_full) > 175:
				u_desc = u_desc_full[:175] + "..."
			else:
				u_desc = u_desc_full

			self.searchOutput("\n*** OPENING URL (" +  u_type.capitalize() + ") [#" + u_run + "]:\n")
			self.searchOutput("EPISODE TITLE: " + u_title)
			self.searchOutput("EPISODE DESCRIPTION: " + u_desc)
			self.searchOutput("EPISODE URL: " + u_url)
			
			#wb.open(u_url, new=2, autoraise=True)
			#import urllib.request
			#urllib.request.urlopen(u_url)
			
			#import androidhelper 

			#url = "http://www.Google.com"
			#androidhelper.Android().startActivity("android.intent.action.VIEW", url)
				
			#import android
			#url = "http://www.Google.com"
			#android.Android().startActivity("android.intent.action.VIEW", url)

			wb.open(u_url, new=1, autoraise=True)
			
			
	def searchOutput(self, output):
		
		output_line = output
		print(output_line)
		
		if "SEARCH TIME: " in output:
			self.time_end = time.process_time()
			self.time_run = round((self.time_end - self.time_start), 2)
			if self.time_run < 1:
				trace_output = "TRACE TIME: " + str(self.time_run) + " sec"
			else:
				trace_output = "TRACE TIME: " + str(self.time_run) + " min"
			print(trace_output)


if __name__ == '__main__':

	spotifySearch().searchInput()
