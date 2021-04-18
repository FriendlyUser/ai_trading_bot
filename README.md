# Ai Trading System

To run
```
python3.8 ai-trading-system/src/app.py
```

Discord is intended to contain all messages produced by the bot.

The standard way to log a message is, within a repository

```python
self._logger.info('Calculating forecast with the given data...')
```

In order to pass fields into discord, we need to pass a dict on the logger function,
for example

```python
self._logger.info("AI trading system starting...", {"version": __version__})
```



## Task List

- [x] Remove old references
- [x] discord module for logging. (4/11/2021)
- [] Basic trading algorthmic, trade if forecast returns promising data
- [] Various trading strategies that can be turned on and off

Deployed to `repl.it`@ https://aitradingbot.friendlyuser.repl.co

## References

Adding more content here
- https://towardsdatascience.com/how-to-create-a-fully-automated-ai-based-trading-system-with-python-708503c1a907
