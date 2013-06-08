ClassBot v1.0
=============
Written by [Tarashish Mishra](http://tarashish.com) <sunu0000@gmail.com>

What is ClassBot?
-----------------

ClassBot is a simple IRCBot that helps you in managing Q&A sessions on IRC.

How to run ClassBot?
--------------------
ClassBot runs on python 2, not python 3. You can run ClassBot by
	
	python classbot.py

All the configuration like server, port, channel list, bot's nick is inside the classbot.py file.

How to use ClassBot on my IRC channel?
--------------------------------------

Add "#yourchannel" to CHANNELS in classbot.py.

Add your/bot operator's nick to OPERATORS in classbot.py.

To ask question the asker has to write:

	/msg <classbot's nick> <your question>

To get next question from the question queue, the operator has to write:

	<classbot's nick> next



