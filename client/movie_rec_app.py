
from appdata import AppData
import predictionio
import sys

from app_config import APP_KEY, API_URL

ENGINE_NAME = 'movie-rec'
SIM_ENGINE_NAME = 'movie-sim'

class App:

	def __init__(self):
		self._app_data = AppData()
		self._client = predictionio.Client(APP_KEY, 1, API_URL)

	def run(self):
		state = "[Main Menu]"

		prompt = "\n"\
			"%s\n"\
			"%s\n"\
			"Please input selection:\n"\
			" 0: Quit application.\n"\
			" 1: Get personalized recommendation.\n"\
			" 2: Display user's data.\n"\
			" 3: Display movie data.\n" % (state, '-'*len(state)) 

		while True:
			print prompt
			choice = raw_input().lower()
			if choice == '0':
				print "\nGood Bye!\n"
				break
			elif choice == '1':
				self.recommend_task(state)
			elif choice == '2':
				self.display_user_task(state)
			elif choice == '3':
				self.get_similar_movies_task(state)
			else:
				print '[Error] \'%s\' is not a valid selection.' % choice

		self._client.close()

	def recommend_task(self, prev_state):
		state = prev_state + " / [Get Recommendations]"
		prompt = "\n"\
			"%s\n"\
			"%s\n"\
			"Please enter user id:" % (state, '-'*len(state))

		while True:
			print prompt
			choice = raw_input().lower()
			u = self._app_data.get_user(choice)
			if u:
				n = 10
				print "[Info] Getting top %s item recommendations for user %s..." % (n, u.uid)
				try:
					self._client.identify(u.uid)
					rec = self._client.get_itemrec_topn(ENGINE_NAME, n)
					u.rec = rec['pio_iids']
					self.display_items(u.rec)
				except predictionio.ItemRecNotFoundError:
					print "[Info] Recommendation not found"

				print "[Info] Go back to previous menu..."
				break
			else:
				print "[Error] invalid user id %s. Go back to previous menu..." % choice
				break

	def get_similar_movies_task(self, prev_state):
		state = prev_state + " / [Get Similar Movies]"
		prompt = "\n"\
			"%s\n"\
			"%s\n"\
			"Please enter movie id:" % (state, '-'*len(state))

		while True:
			print prompt
			choice = raw_input().lower()
			i = self._app_data.get_item(choice)
			if i:
				n = 10
				self.display_items((i.iid,), all_info=False)
				print "\n[Info] People who liked this may also liked..."
				try:
					rec = self._client.get_itemsim_topn(SIM_ENGINE_NAME, i.iid, n, { 'pio_itypes' : i.genres })
					self.display_items(rec['pio_iids'], all_info=False)
				except predictionio.ItemSimNotFoundError:
					print "[Info] Similar movies not found"

				print "[Info] Go back to previous menu..."
				break
			else:
				print "[Error] invalid item id %s. Go back to previous menu..." % choice
				break

	def display_user_task(self, prev_state):
		state = prev_state + " / [Display User]"
		prompt = "\n"\
			"%s\n"\
			"%s\n"\
			"Please enter user id:" % (state, '-'*len(state))

		while True:
			print prompt
			choice = raw_input().lower()
			u = self._app_data.get_user(choice)
			if u:
				print "[Info] User %s:" % u.uid
				n = 10
				topn_rate_actions = self._app_data.get_top_rate_actions(u.uid, n)
				print "\n[Info] Top %s movies rated by this user:" % n
				self.display_rate_actions(topn_rate_actions)

				print "\n[Info] Getting New Recommendation..."
				n = 10
				try:
					self._client.identify(u.uid)
					rec = self._client.get_itemrec_topn(ENGINE_NAME, n)
					u.rec = rec['pio_iids']
				except predictionio.ItemRecNotFoundError:
					print "[Info] Recommendation not found"

				print "\n[Info] Movies recommended to this user:"
				self.display_items(u.rec)

				self.wait_for_ack()
				print "\n[Info] Go back to previous menu..."
				break
			else:
				print "[Error] invalid user id %s. Go back to previous menu..." % choice
				break
	
	def display_items(self, iids, all_info=False):
		"""print item info for each iid in the list
		"""
		if iids:
			for iid in iids:
				item = self._app_data.get_item(iid)
				if item:
					if all_info:
						print "[Info] %s" % item
					else:
						print "[Info] (%s) %s %s" % (item.iid, item.name, item.release_date.strftime("%d-%b-%Y"))
				else:
					print "[Error] Invalid item id %s" % iid
		else:
			print "[Info] Empty."

	def display_rate_actions(self, actions):
		"""print iid and rating
		"""
		if actions:
			for a in actions:
				item = self._app_data.get_item(a.iid)
				if item:
					print "[Info] (%s) %s, rating = %s" % (item.iid, item.name, a.rating)
				else:
					print "[Error] Invalid item id %s" % a.iid
		else:
			print "[Info] Empty."

	def wait_for_ack(self):

		prompt = "\nPress enter to continue..."
		print prompt
		choice = raw_input().lower()


if __name__ == '__main__':

	print "\nWelcome To PredictionIO Python-SDK Demo App!"
	print "============================================\n"
	
	my_app = App()
	my_app.run()
