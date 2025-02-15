
<h1>Port Canaveral Ships</h1>
<h2>Creating port_canaveral_ships and moving files</h2>
<li>Locate the custom_components directory (folder) and create a new folder called port_canaveral_ships.</li>
<li>Download all the files from the custom_components/port_canaveral_ships/ directory (folder) in this repository.</li>
<li>Place the files you downloaded in the new directory (folder) you created in Home Assistant</li>
<li>Restart Home Assistant</li>

<h2>Installing Solution</h2>
<li>From Home Assistant, go to Settings, Devices & services</li>
<li>Look for the blue "Add Integration" button and click it</li>
<li>In search brand, type in "Ships" and locate Port Canaveral Ships</li>
<li>Answer questions about which Statuses to track, and retrieval interval</li>

<h2>About the update interval</h2>
We recommend that you use the default of 20 minutes. The mininum is 20 minutes, and the solution will not allow anything less than this to avoid any issue wtih uncessary retrievals. 

<h2>Data Source Might Not Change</h2>
The _async_update_data function fetches ship data from an external website (data_fetcher.fetch_ship_schedule()).
If the external data has not changed, the coordinator does not create a new update event.
The last_updated timestamp in Home Assistant is only updated if the fetched data changes.
Instead of last_updated, another property has been created called last_checked. This property will indicate when the solution <b>checked</b> for updates, but data may or may not of <b>changed</b>. To sense a change, we recommend using last_updated. 

