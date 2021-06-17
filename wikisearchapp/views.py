from django.shortcuts import render, HttpResponse
from django.contrib import messages
import wikipedia
import requests
import json


# "&list=search&srsearch=porto seguro"
# "prop=pageimages"

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages|imageinfo&format=json&piprop=thumbnail&pithumbsize=800&titles='


# WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&&piprop=thumbnail&pithumbsize=800&titles='


def index(request):
	if request.method == 'POST':
		search = request.POST['search']
		
		try:
			result = wikipedia.page(search, auto_suggest=True, redirect=True)  # No of sentences to output
			# result1 = wikipedia.search(search, results=3)
			wikipedia.set_lang('en')
			# wikipedia.set_lang('pt')
			title = result.title
			response = requests.get(WIKI_REQUEST + title)
			json_data = json.loads(response.text)
			feat = list(json_data['query']['pages'].values())[0]['thumbnail']['source']
			
			# for mykey in json_data:
			# 	if json_data[mykey] == "":
			# 		return messages.error(request, 'No search result found!')
			# 	else:
			# 		pass
			if response.ok:
				messages.info(request, title)
			else:
				messages.error(request, 'No search result found!')
		except:
			return HttpResponse('No search result found!')
		return render(request, 'index.html', {'result': result, 'feat': feat})
	return render(request, 'index.html')
