Something for monitor internet connection

<H1>**REQUIREMENTS**</H1>
- 	Python 2.6+
- 	APScheduler	(pip install apscheduler)

First configure the DB variable(in internetMonitor.py) to set your sqlite database, you can use absolute paths

Just run internetMonitor.py (if you can as a service or daemon), every minute will write in your database and in data.js if the internet was recheable

In chart.html you can see a nice pie chart with the data
