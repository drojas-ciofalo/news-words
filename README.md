# Creating Telegram Channel: News&Words

Get an image showing the most relevant words on the day's news: US, Mexico, and Germany news. By: drojas.ciofalo

## Steps used

* Connect to news API to download the day's news
* Create a word cloud from the contents in the response
* Connect to Telegram API to send the plot created
* Use crontab from terminal to send the pics every day to te channel

Be sure to start the cron deamon before:
`systemctl status crond.service `
`systemctl start crond.service `
