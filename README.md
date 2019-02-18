## Packt Free Learning Notifier 

Set the following env variables in `venv/bin/activate` locally or as _Config Vars_ when [deploying to Heroku](https://devcenter.heroku.com/articles/git):

1. Heroku

	Add Heroku `heroku/chromedriver` and `heroku/google-chrome` _buildpacks_, then set:

		export CHROME_DRIVER=/app/.chromedriver/bin/chromedriver
		export GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google-chrome

2. Post to Slack

	Create app (API) - admin approval - install app into workspace - add "incoming webhook", then set:

		export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/abc/def/ghi


3. Post to Twitter

	Create an app via the Twitter API, then set:

		export CONSUMER_KEY=abc
		export CONSUMER_SECRET=def
		export ACCESS_TOKEN=ghi
		export ACCESS_SECRET=jkl
