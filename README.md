Something for monitor internet connection
I made this because I'm tired of being f***ed by my ISP, I'm running this in a Raspberry Pi

<h2>**REQUIREMENTS**</h2>
- 	Python 2.6+
- 	APScheduler	(pip install apscheduler)

First configure the DB variable(in internetMonitor.py) to set your sqlite database, you can use absolute paths

Just run internetMonitor.py (if you can as a service or daemon), every minute will write in your database and in data.js if the internet was recheable

In chart.html you can see a nice pie chart with the data
