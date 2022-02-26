## Python Telegram Tail Bot

A simple Python Telegram Tail Bot, or _pttb_ for short, that:

* Tails the syslog logstream from one or more files, ie `/var/log/ipng.log`
* Pattern matches on loglines, after which an `incident` is created
* Waits for a predefined number of seconds (which may be zero) to see if more loglines match, adding them to
  the incident
* Holds the incident against a list of known regular expression `silences`, throwing away those which
  aren't meant to be distributed
* Sending to a predefined Telegram group chat, those incidents which aren't silenced


## Building

```
sudo apt install python3-pip
pip install pyinstaller
pip install argparse
pip install pyyaml
pip install python-telegram-bot --upgrade
pyinstaller pttb --onefile
vi pttb-example.yaml ## or emacs if you're so inclined; add your token and chat-id from Telegram
dist/pttb --config ./pttb-example.yaml
```

## Install

Instructions below are for Debian/Ubuntu only. The bot will work on other operating systems, but persistent
startup and config management are beyond the scope of this README. The `pttb.service` file runs the binary
as `nobody:adm` so to enable config persistence (when users add triggers and silences), make sure that the
config file is writable by either user=nobody or group=adm (or both).

```
sudo mkdir -p /usr/local/bin /etc/pttb/
sudo cp pttb /usr/local/bin/
sudo cp pttb.service /lib/systemd/system/
sudo cp pttb-example.yaml /etc/pttb/pttb.yaml
sudo chmod 664 /etc/pttb/pttb.yaml
sudo chown nobody:adm /etc/pttb/pttb.yaml
sudo vi /etc/pttb/pttb.yaml ## or emacs, add your production token and chat-id from Telegram
systemctl enable pttb
systemctl start pttb
```

## Details

The bot should allow for the following features, based on a YAML configuration file, which will allow it to be
restarted and upgraded:

* A (mandatory) `TOKEN` to interact with Telegram API
* A (mandatory) single `chat-id` - incidents will be sent to this Telegram group chat
* An (optional) list of logline triggers, consisting of:
  * regular expression to match in the logstream
  * grace period to coalesce additional loglines of the same trigger into the incident
* AN (optional) list of silences, consisting of:
  * regular expression to match any incident message data in
  * an expiry timestamp

The bot will start up, announce itself on the `chat-id` Telegram group, and then listen on Telegram for the following
commands:

* **/help** - a list of available commands
* **/trigger** - without parameters, list the current triggers
* **/trigger add &lt;regexp&gt; [duration] [&lt;message&gt;]** - with one parameter set a trigger on a regular expression.
  Optionally, add a duration in seconds between [0..3600>, within which additional matched loglines will be added to the
  same incident, and an optional message to include in the Telegram alert.
* **/trigger del &lt;idx&gt;** - with one parameter, remove the trigger with that index (use /trigger to see the list).
* **/silence** - without parameters, list the current silences.
* **/silence add &lt;regexp&gt; [duration] [&lt;reason&gt;]** - with one parameter, set a default silence for 1d; optionally
  add a duration in the form of `[1-9][0-9]*([hdm])` which defaults to hours (and can be days or minutes), and an optional 
  reason for the silence.
* **/silence del &lt;idx&gt;** - with one parameter, remove the silence with that index (use /silence to see the list).
* **/stfu [duration]** - a shorthand for a silence with regular expression `.*`, will suppress all notifications, with a
  duration similar to the **/silence add** subcommand.
* **/stats** - shows some runtime statistics, notably how many loglines were processed, how many incidents created,
  and how many were sent or suppressed due to a silence.

It will save its configuration file any time a silence or trigger is added or deleted, so make sure that the user running
the bot has write access to its configurationfile. The bot will (obviously) start sending incidents that are not silenced
to the `chat-id` group-chat when they occur.

## Notes

This software is not done :-) This README describes the intended endstate, not the current state. Several functions do not
work at the moment, but they should be done in Q1'2022. 

If you file feature request issues, please expect the response "contributions welcome", which means that I am not able or
willing to satisfy external needs beyond critical bugreports that affect my own use cases. If you'd like to extend this
FOSS software, please send a PR with working code and accompanied by an explanation in a github issue. If you feel entitled
to support, feel free to mail sales@ipng.ch for a quote.
