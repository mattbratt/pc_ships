<!-- Icon at the top -->
<div align="center">
  <img src="https://github.com/mattbratt/pc_ships/blob/main/images/icon.png" alt="Port Canaveral Ships Icon" width="100"><h1>Port Canaveral Ships</h1>
</div>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/mattbratt/pc_ships?style=flat-square)
![HACS Compatible](https://img.shields.io/badge/HACS-Compatible-brightgreen?style=flat-square)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-blue?style=flat-square)

---

## About

**Port Canaveral Ships** fetches real-time data from Port Canaveral, Florida — one of the busiest cruise ship ports in the world. Track cargo ships, passenger ships, or both, tailored to your preferences. Know who is leaving first, arriving next, and which berth they're using — right in your smart home. A full visual **PC Ships** dashboard is automatically installed, complete with ship images and flag icons.

It is tightly integrated with [Home Assistant](https://www.home-assistant.io/) and most easily installed through [HACS](https://hacs.xyz/).

<img src="https://github.com/mattbratt/pc_ships/blob/main/images/port_canaveral_map.png" alt="Port Canaveral Ships Icon" width="400">

### Configuration Options
During setup, customize your tracking with these options:

<div align="center">
  <img src="https://github.com/mattbratt/pc_ships/blob/main/images/pc_ships_config.png" alt="Config Screenshot" width="400">
</div>

Stick with the defaults for simplicity, or customize them—such as selecting all statuses instead of just "In Port" and "Confirmed." Here's what each status means:

- **In Port**: Ships currently docked at a berth.
- **Confirmed**: Ships with validated arrivals.
- **Scheduled**: Ships slated to arrive, aiding berth management.
- **Departed**: Ships that recently left the port.

---

## PC Ships Dashboard

When you configure the integration, a **PC Ships** Lovelace dashboard is automatically written to Home Assistant storage and registered in your sidebar. It shows ships grouped by status — Departing Next (hero card), In Port, and Confirmed Arrivals — with ship photos, flag images, berth assignments, and schedule details.

> [!IMPORTANT]
> After completing setup, you **must restart Home Assistant once** for the PC Ships dashboard to appear in the sidebar.
> Home Assistant will **not** prompt you to do this — it is a required but silent step.
> Go to **Settings → System → Restart** to trigger it.

### Dashboard Prerequisites

The dashboard requires two **HACS Frontend** plugins — install both via HACS before using the dashboard:

| Plugin | HACS Name | Used for |
|---|---|---|
| [Button Card](https://github.com/custom-cards/button-card) | `button-card` | Ship card layout |
| [Card Mod](https://github.com/thomasloven/lovelace-card-mod) | `card-mod` | Card styling |

### How It Works

- Ship images are loaded from `/pc_ships/images/ships/` — matched automatically by vessel name (uppercase, no spaces)
- Flag images are loaded from `/pc_ships/images/flags/` — matched by the sensor's `flag_code` attribute (ISO-2 country code)
- Slots with no ship data are hidden automatically
- The dashboard is never overwritten or removed when you uninstall the integration — any customizations you make are preserved

### Ship Images

Images are included for most passenger ships that regularly visit Port Canaveral. However, not all ships are covered — new vessels are added to the fleet and existing ships are sometimes repositioned to other ports. To add a missing ship, place a `.png` file named after the vessel (uppercase, spaces removed) in `custom_components/pc_ships/www/images/ships/`.

---

## Installation

### Option 1: HACS (Highly Recommended)
The easiest way to get started:

> **Before you begin:** Install [Button Card](https://github.com/custom-cards/button-card) and [Card Mod](https://github.com/thomasloven/lovelace-card-mod) from HACS **Frontend** — the PC Ships dashboard requires both.

1. Open **HACS** in Home Assistant.
2. Search for *"Port Canaveral Ships"* in the Integrations section (check "Available for download" or "New").
3. Click **Download**.
4. Navigate to **Settings > Devices & Services** in Home Assistant.
5. Click the blue **+ Add Integration** button.
6. Search for "Ships," then select **Port Canaveral Ships**.
7. Configure your preferences: statuses, retrieval intervals, and ship counts per status.
8. **Restart Home Assistant** — go to **Settings → System → Restart**. The PC Ships dashboard will appear in your sidebar after the restart. Home Assistant will not prompt you for this — the restart is required but silent.

### Option 2: Manual Installation
For the hands-on folks:

1. Download all files from `/custom_components/pc_ships` in this repo.
2. Place them in your Home Assistant's `/custom_components/pc_ships` directory.
3. Go to **Settings > Devices & Services**.
4. Click **+ Add Integration**, search "Ships," and select **Port Canaveral Ships**.
5. Set up statuses, intervals, and ship counts (e.g., defaults: In Port: 15, Confirmed: 15, Scheduled: 15, Departed: 15).

---

## Entities Created

Entities vary based on your chosen statuses and sensor counts. For example, selecting "In Port" and "Confirmed" with 2 sensors each creates:

- `sensor.port_canaveral_ships_in_port_1`
- `sensor.port_canaveral_ships_in_port_2`
- `sensor.port_canaveral_ships_confirmed_1`
- `sensor.port_canaveral_ships_confirmed_2`

---

## Entity Attributes

Each sensor comes packed with details:

| Attribute          | Description                          | Example Value            |
|--------------------|--------------------------------------|--------------------------|
| **Status Type**    | Ship's status category              | In Port, Confirmed, etc. |
| **Sensor Slot**    | Sensor number                       | 1, 2, etc.              |
| **Last Updated**   | Timestamp of last update            | Feb 22, 2025, 10:07 AM  |
| **Vessel**         | Ship name                           | Icon of the Seas        |
| **Status**         | Matches Status Type                 | In Port                 |
| **Cargo Type**     | Cargo onboard                       | Containers              |
| **Vessel Class**   | Ship type                           | Cargo or Passenger      |
| **Flag**           | Country of registration             | Bahamas                 |
| **Flag Code**      | ISO-2 country code for flag image   | bs, us, pa              |
| **Berth**          | Assigned berth                      | CT-10                   |
| **Arrival Date**   | Date of arrival                     | 02/21/2025              |
| **Arrival Time**   | Time of arrival (24-hour)           | 03:00                   |
| **Departure Date** | Date of departure                   | 02/21/2025              |
| **Departure Time** | Time of departure (24-hour)         | 03:00                   |
| **Is Tug Boat**    | Tug boat indicator (TG prefix)      | True / False            |
| **Others**         | Additional metadata                 | Last Changed, etc.      |

---

## Update Interval

The default update interval is **20 minutes**, with a minimum of **15 minutes** enforced to avoid overloading the system. Adjust as needed during setup.

The auto-installed **PC Ships** dashboard is the recommended way to visualize your ship data — see the [PC Ships Dashboard](#pc-ships-dashboard) section above.

---

<div align="center">
  <strong>---</strong>
</div>
