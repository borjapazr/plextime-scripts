# 🤖⏰ Plextime scripts ![GitHub CI Workflow Status](https://github.com/borjapazr/plextime-scripts/workflows/CI/badge.svg)

Scripts for automatic clocking in and out on Plextime platform written in Python and scheduled using schedule (Python library) or Ofelia (Docker)

## 🧩 Requirements

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Make

## 🧑‍🍳 Configuration

Before deploying the service it is necessary to configure it. To do so, it is enough to create an .env file with the content of the corresponding .env.template. You can also use the `make env` command.

There are two ways to configure the service for automatic clocking. The first one is based on the scheduling of clockings from each employee's timetable (`INTERNAL_SCHEDULING` to `true`). The second one allows to set the scheduling using a service called [Ophelia](https://github.com/mcuadros/ofelia). To use it, just copy the content of the `docker-compose-ofelia.yml` file into the `docker-compose.yml` file and review its configuration to understand how it works. It is very simple. Just set the environment variables `CHECKIN_CRON_EXPRESSION`, `CHECKOUT_FULL_DAY_CRON_EXPRESSION` and `CHECKOUT_HALF_DAY_CRON_EXPRESSION` with the cron expressions that match the employee's timetable.

### Environment variables that need to be configured

- `INTERNAL_SCHEDULING`: Enables or disables the scheduling of automatic clockings based on the user's timetable. `true` or `false` (default)
- `PLEXTIME_USER`: Plextime user
- `PLEXTIME_PASSWORD`: Plextime user's password
- `PLEXTIME_JOURNAL_OPTION`: Type of clocking to be performed. For example, telework, office, client, etc. The default value is telework (`8`). To find out the different identifiers available, please fill in your username and password and run the command `make journal-options`.
- `CHECKIN_CRON_EXPRESSION`: Check-in cron expression. For example, `0 0 8 * * MON-FRI`
- `CHECKOUT_FULL_DAY_CRON_EXPRESSION`: Check-out cron expression for full working days. For example, `0 0 19 * * MON,WED`
- `CHECKOUT_HALF_DAY_CRON_EXPRESSION`: Check-out Cron expression for half working days. For example, `0 0 15 * * TUE,THU,FRI`
- `CHECKIN_RANDOM_MARGIN`: Maximum value (in seconds) for the random timeout for check-in process. For example, `900`. Default is `0`
- `CHECKOUT_RANDOM_MARGIN`: Maximum value (in seconds) for the random timeout for check-out process. For example, `1800`. Default is `0`
- `TELEGRAM_NOTIFICATIONS`: Enable or disable Telgram notifications. `true` or `false`
- `TELEGRAM_BOT_TOKEN`: Telegram bot token for notifications
- `TELEGRAM_CHANNEL_ID`: Telegram channel to receive notifications
- `TZ`: Timezone. For example, `Europe/Madrid`

## 🏗️ Installation

```bash
make install
```

## 🧙 Usage

```txt
Usage: make TARGET [ARGUMENTS]

Targets:
  build              Build all or c=<name> containers
  checkin            Checkin
  checkout           Checkout
  destroy            Destroy all or c=<name> containers
  disable            Disable service
  down               Down all or c=<name> containers
  enable             Enable service
  env                Create .env file from .env.template
  health             Get service health
  install            Start all containers in background
  journal-options    List available journal options
  logs               Show logs for all or c=<name> containers
  restart            Restart all or c=<name> containers
  start              Start all or c=<name> containers
  status             Show status of containers
  stop               Stop all or c=<name> containers
  uninstall          Stop all containers and remove all data
  up                 Up all or c=<name> containers
```

## ⚖️ License

The MIT License (MIT). Please see [License](LICENSE) for more information.
