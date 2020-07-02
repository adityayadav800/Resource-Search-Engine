from django.shortcuts import render
from django.http import HttpResponse
import requests




def  home(request):
	return render(request,'index.html',{})

def buttonClicked(request):
	if request.method=="GET":
		field=request.GET['field']
		subject=request.GET['subject']
		topic=request.GET['topic']
		classl=request.GET['class']
		keyWords=[field,subject,topic,classl]
		links_list=search(keyWords)
		read=links_list[0]
		video=links_list[1]
		book=links_list[2]
		print(read)
		print(video)
		print(book)
	#Add the whole Code here! import the modules at th beginning!
	return render(request,'index.html',{'links':read,'video':video,'book':book})

def search(keywords_list, is_book_or_paper=False, number_of_links_required=55):
	import os
	from bs4 import BeautifulSoup
	import googlesearch
	import requests
	final=[[]]
	query=""
	video_query="https://www.youtube.com/results?search_query="
	pdf_query=query+"filetype:pdf"
	for keyword in keywords_list:
		query=query+keyword
		video_query=video_query+"+"+keyword
	links_generator=googlesearch.search(query,tld="com",lang="en",num=number_of_links_required,start=0,stop=None,pause=2.0)
	links_list=[]
	try:
		while True:
			links_list.append(next(links_generator))
	except:
		pass
	print(links_list)
	final.append(links_list)
	content=requests.get(video_query).content
	youtube_soup=BeautifulSoup(content)
	video_links=[]
	for tag in youtube_soup.find_all("a"):
		if 'watch?v=' in tag.get('href'):
			video_links.append("https://www.youtube.com"+tag.get('href'))
	if number_of_links_required < len(video_links):
		video_links=video_links[:number_of_links_required]
	print(video_links)
	final.append(video_links)
	pdf_links=[]
	links_generator=googlesearch.search(query,tld="com",lang="en",num=number_of_links_required,start=0,stop=None,pause=2.0)
	try:
		while True:
			print("Iterating...")
			pdf_links.append(next(links_generator))
	except:
		pass
	print(pdf_links)
	final.append(pdf_links)
	print(final)
	return final