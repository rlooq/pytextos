# Pytextos

A general text manager. I would like to make it do the following:
- Create Text objects based on .txt files which
	a) store information: title, subtitle, body, author, date, source, text-type, genre.
	b) generate data about themselves: tokenization, word counts, paragraph counts,
	   word frequency, keywords, lexical diversity, vocabulary by CEFR level,
	   reading time, (POS frequency, gramamtical features, summary, topic, etc.*).

- Create Collection objects (collections of Text objects) to generate listings
  with different criteria and export them to .csv, .xlsx, etc. for persistence. 

- Create Extracts based on Text objects for exemplification, with similar features as texts.

- Create learning activities associated to Text objects. Not sure how to implement this yet.

- A database of said Text objects with queries to locate specific texts or features.

\* For now, no NLP frameworks are being used.