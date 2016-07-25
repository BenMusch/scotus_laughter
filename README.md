Twitter bot + web site to keep track of every time "(Laughter.)" appears in
Supreme Court oral arguments.

Services:
 - Spider: scrapes the SCOTUS web site for oral argument data, because
   transcripts are posted much faster there than Oyez, then searches Oyez to
   track the times in the audio that the joke occurs
 - ETL: Parses the data from the scraper. Most notably, parses the PDF format of
   the oral arguments on the SCOTUS site
 - Web App: Schedules the spider, controls the Twitter bot, provides front-end
   for data
