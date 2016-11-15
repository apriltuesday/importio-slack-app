#LUNCHBOT RUNBOOK

If lunchbot stops responding:
* log on to `algo-server`
* do `screen -r slack` to get the screen session
* the screen session should already be in the correct directory but if necessary do `cd ~/projects/importio-slack-app`
* restart the bot by running `python lunchbot.py`

If terrible unknown things start happening:
* you can just turn it off, it _is_ just lunch after all...
* but if you must, the code is on the `dev` branch of [this repo](https://github.com/apriltuesday/importio-slack-app/tree/dev), have fun