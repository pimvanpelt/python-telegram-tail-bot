## Python Telegram Tail Bot

A simple Python Telegram Tail Bot, or _pttb_ for short, that:

* Tails the syslog logstream from one or more files, ie `/var/log/ipng.log`
* Pattern matches on loglines, after which an `incident` is created
* Waits for a predefined number of seconds (which may be zero) to see if more loglines match, adding them to
  the `incident`
* Holds the `incident` against a list of known regular expression `silences`, throwing away those which
  aren't meant to be distributed
* Sending to a predefined group chat, those incidents which aren't silenced


## Install

```
sudo apt install python3-pip
pip install pyinstaller
pip install argparse
pip install python-telegram-bot --upgrade
./pttb --config ./pttconfig.yaml
```

## Details

The bot should allow for the following features, based on a YAML configuration file, which will allow it to be
restarted and upgraded:

* A (mandatory) `TOKEN` to interact with Telegram API
* A (mandatory) single `chat-id` - messages will be sent to this Telegram group chat
* An (optional) list of logline triggers, consisting of:
  * regular expression to match in the logstream
  * grace period to coalesce additional loglines of the same trigger into the incident
* AN (optional) list of silences, consisting of:
  * regular expression to match any incident message data in
  * an expiry timestamp

The bot will start up, announce itself on the `chat-id` group, and then listen on Telegram for the following
commands:

* **/help** - a list of available commands
* **/trigger** - without parameters, list the current triggers
* **/trigger add &lt;regexp&gt; [duration]** - with one parameter set a trigger on a regular expression. Optionally,
  add a duration in seconds between [0..3600>, within which additional matched loglines will be added to the
  same incident.
* **/trigger del &lt;idx&gt;** - with one parameter, remove the trigger with that index (use /trigger to see the list).
* **/silence** - without parameters, list the current silences
* **/silence add &lt;regexp&gt; [duration]** - with one parameter, set a default silence for 1d; optionally
  add a duration in the form of `[1-9][0-9]*([hdm])` which defaults to hours (and can be days or minutes).
* **/silence del &lt;idx&gt;** - with one parameter, remove the silence with that index (use /silence to see the list).

It will save its configuration file any time a silence or trigger is added or deleted, so make sure that the user running
the bot has write access to its configurationfile. The bot will (obviously) start sending incidents that are not silenced
to the `chat-id` group-chat when they occur.
