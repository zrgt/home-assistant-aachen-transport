// Aachen Transport Timetable Card

class AachenTransportTimetableCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({
            mode: 'open'
        });
    }

    /* This is called every time sensor is updated */
    set hass(hass) {

        const config = this.config;
        const maxEntries = config.max_entries || 10;
        const showStopName = config.show_stop_name || true;
        const entityIds = config.entity ? [config.entity] : config.entities || [];

        let content = "";

        for (const entityId of entityIds) {
            const entity = hass.states[entityId];
            if (!entity) {
                throw new Error("Entity State Unavailable");
            }

            if (showStopName) {
                content += `<div class="stop">${entity.attributes.friendly_name}</div>`;
            }

            const timetable = entity.attributes.departures.slice(0, maxEntries).map((departure) => 
                `<div class="departure">
                    <div class="line">
                        <div class="line-icon" style="background-color: ${departure.color}">${departure.line_name}</div>
                    </div>
                    <div class="direction">${departure.direction}</div>
                    <div class="delay">+${departure.delay}</div>
                    <div class="time">${departure.time}</div>
                    <div class="minutes_left">${departure.minutes_left}min</div>
                </div>`
            );

            content += `<div class="departures">` + timetable.join("\n") + `</div>`;
        }

       this.shadowRoot.getElementById('container').innerHTML = content;
    }

    /* This is called only when config is updated */
    setConfig(config) {
        const root = this.shadowRoot;
        if (root.lastChild) root.removeChild(root.lastChild);

        this.config = config;

        const card = document.createElement('ha-card');
        const content = document.createElement('div');
        const style = document.createElement('style')
  
        style.textContent = `
            .container {
                padding: 10px;
                font-size: 100%;
                line-height: 1.5em;
            }
            .stop {
                opacity: 0.6;
                font-weight: 400;
                width: 100%;
                text-align: left;
                padding: 10px 10px 5px 5px;
            }      
            .departures {
                width: 100%;
                font-weight: 400;
                line-height: 1.5em;
                padding-bottom: 20px;
            }
            .departure {
                padding-top: 10px;
                display: flex;
                flex-direction: row;
                flex-wrap: nowrap;
                align-items: flex-start;
                gap: 20px;
            }
            .line {
                min-width: 70px;
                text-align: right;
            }
            .line-icon {
                display: inline-block;
                border-radius: 20px;
                padding: 7px 10px 5px;
                font-size: 120%;
                font-weight: 700;
                line-height: 1em;
                color: #FFFFFF;
                text-align: center;
            }
            .direction {
                align-self: center;
                flex-grow: 1;
            }
            .minutes_left {
                align-self: flex-start;
                font-weight: 700;
                line-height: 2em;
                padding-right: 10px;
                min-width: 40px;
                text-align: right;
            }
            .delay {
                align-self: flex-start;
                font-weight: 100;
                line-height: 2em;
                font-size: 70%;
            }
            .time {
                align-self: flex-start;
                font-weight: 700;
                line-height: 2em;
            }
        `;
     
        content.id = "container";
        content.className = "container";
        card.header = config.title;
        card.appendChild(style);
        card.appendChild(content);

        root.appendChild(card);
      }
  
    // The height of the card.
    getCardSize() {
      return 5;
    }
}
  
customElements.define('aachen-transport-timetable-card', AachenTransportTimetableCard);
