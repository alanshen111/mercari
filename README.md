# Overview

My girlfriend complained to me about scalpers buying out all the nice clothes on Mercari, so I created this web app to beat out those scalpers.

# How it works

![](Example.jpg)

This web app uses Flask. The frontend will provide a simple passcode login before bring you to the root page, where a search bar is provided. Once you submit a query, the scraper search it on https://jp.mercari.com and collect the 5 most recent items every 60 seconds and update the page.

# How to run

1. Create a `.env` in the root and add the line `PASSWORD=yourpassword123`
2. Install `requirements.txt`
3. Run `app.py`
4. Enjoy!