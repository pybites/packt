## Packt Free Learning Notifier 

Set the following env variables in `venv/bin/activate` locally or as _Config Vars_ when [deploying to Heroku](https://devcenter.heroku.com/articles/git):

1. Heroku

		export CHROME_DRIVER=/app/.chromedriver/bin/chromedriver
		export GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google-chrome

(after adding Heroku `heroku/chromedriver` and heroku/google-chrome` _buildpacks_)

2. Post to Slack

		export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/abc/def/ghi

(after request app - admin approval - install app - "incoming webhook")

3. Post to Twitter

		export CONSUMER_KEY=abc
		export CONSUMER_SECRET=def
		export ACCESS_TOKEN=ghi
		export ACCESS_SECRET=jkl

(after creating an app via Twitter API)
