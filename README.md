# Aachen (AVV) transport widget for Home Assistant

Custom sensor component and lovelace card that displays upcoming departures from your defined public transport stops for Aachen.

![](./docs/screenshots/timetable-card.jpg)

## 🧑‍ Credits

This widget was forked from [vas3k](https://github.com/vas3k)'s [repository](https://github.com/vas3k/home-assistant-berlin-transport) and adopted to work for Aachen


## 💿 Installation

The component consists of two parts:

1. A sensor, which tracks departures via [AVV Widget Service](https://abfahrt.avv.de) every 30 seconds
2. A widget (card) for the lovelace dashboard, which displays upcoming transport in a nice way

We will look at the installation of each of them separately below. But first, let's learn how to find the Stop IDs.

### How do I find my `avv_widget_id`?

- Go to this URL: **https://abfahrt.avv.de/**
- Choose your stop and desired lines
- Copy the value at the and of the link in `Anzeigelink` 
  - https://abfahrt.avv.de/index.php?v=VALUE_TO_COPY


### Install sensor component

**1.** Copy the whole [aachen_transport](./custom_components/) directory to the `custom_components` folder of your Home Assistant installation. If you can't find the `custom_components` directory at the same level with your `configuration.yml` — simply create it yourself and put `aachen_transport` there.

**2.** Go to Home Assistant web interface -> `Developer Tools` -> `Check and Restart` and click "Restart" button. It will reload all components in the system.

**3.** Now you can add your new custom sensor to the corresponding section in the `configuration.yml` file.

```yaml
sensor:
  - platform: aachen_transport
    departures:
      - name: "Ponttor" # free-form name, only for display purposes
        avv_widget_id: fIha9h4yt78VWMfViwcBLlPSLh5oYAee # actual AVV widget id for the API
      - name: "Aachen Bushof" # you can add more that one stop to track
        avv_widget_id: rhAYAkp7I0xEi5DwWuFB6SjaR23fgWO5
        
        # Optional parameter with track id that show only transport, which stops at the defined track
        # track: 1 
```

**4.** Restart Home Assistant core again and you should now see two new entities (however, it may take some time for them to fetch new data). If you don't see anything new — check the logs (Settings -> System -> Logs). Some error should pop up there.

### Add the lovelace card

When sensor component is installed and working you can add the new fancy widget for your dashboard.

**1.** Copy the [aachen-transport-timetable-card.js](./www) card module to the `www` directory of your Home Assistant. The same way you did for the sensor above. If it doesn't exist — create one.

**2.** Go to your Home Assistant dashboard, click "Edit dashboard" at the right top corner and after that in the same top right corner choose "Manage resources".

**3.** Add new resource with URL: `/local/aachen-transport-timetable-card.js` and click create. Go back to your dashboard and refresh the page.

**4.** Now you can add the custom card and integrate it with your sensor. Click "Add card -> Manual" or just go to "Raw configuration editor" and use this config.

```yaml
- type: custom:aachen-transport-timetable-card
  show_stop_name: true # show or hide the name of your stop in card title
  max_entries: 8 # number of upcoming departures to show (max: 10)
  entities:
    - sensor.stop_id_900110001 # use your entity IDs here
    - sensor.stargarder_str # they might be different from mine
```

## 🎨 Styling

If you want to change any styles, font size or layout — the easiest way is to use [card_mod](https://github.com/thomasloven/lovelace-card-mod) component. It allows you to change any CSS classes to whatever you want.

## ❤️ Contributions

Contributions are welcome. Feel free to [open a PR](https://github.com/zrgt/home-assistant-aachen-transport/pulls) and send it to review. If you are unsure, [open an Issue](https://github.com/zrgt/home-assistant-aachen-transport/issues) and ask for advice.

## 🐛 Bug reports and feature requests

Since this is my small hobby project, I cannot guarantee you a 100% support or any help with configuring your dashboards. I hope for your understanding.

- **If you find a bug** - open [an Issue](https://github.com/zrgt/home-assistant-aachen-transport/issues) and describe the exact steps to reproduce it. Attach screenshots, copy all logs and other details to help me find the problem.
- **If you're missing a certain feature**, describe it in Issues and try to code it yourself. It's not hard. 

## 👮‍♀️ License

- [MIT](./LICENSE.md)
