[![Test Coverage](https://codeclimate.com/github/setokinto/slack-bomber/badges/coverage.svg)](https://codeclimate.com/github/setokinto/slack-bomber/coverage)
[![Code Climate](https://codeclimate.com/github/setokinto/slack-bomber/badges/gpa.svg)](https://codeclimate.com/github/setokinto/slack-bomber)
[![Issue Count](https://codeclimate.com/github/setokinto/slack-bomber/badges/issue_count.svg)](https://codeclimate.com/github/setokinto/slack-bomber)
[![CircleCI](https://circleci.com/gh/setokinto/slack-bomber.svg?style=svg)](https://circleci.com/gh/setokinto/slack-bomber)

# slack-bomber
It's a bomb. Just a bomb.

# Try it with Docker
`docker run --env API_TOKEN="<Your Slack Bot Token>" setokinto/slack-bomber`

# How to use
1. Create a Bot https://your-team-name.slack.com/apps/A0F7YS25R-bots
1. Copy config file cp bomber.env.default bomber.env
1. Replace your api key with your bot from slack
1. `docker-compose up`
1. @bot-name start with @username1, @username2 and @username3
