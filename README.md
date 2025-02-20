
<h1>Port Canaveral Ships</h1>
<h2>Creating port_canaveral_ships and moving files</h2>
<li>Locate the custom_components directory (folder) and create a new folder called pc_ships.</li>
<li>Download all the files from the custom_components/pc_ships/ directory (folder) in this repository.</li>
<li>Place the files you downloaded in the new directory (folder) you created in Home Assistant</li>
<li>Restart Home Assistant</li>

<h2>Installing Solution</h2>

<h3>HACS (Preferred and easy)</h3>

<li>From Home Assistant, go to HACS.</li>
<li>From the HACS community store, use the search bar and use "Port Canaveral Ships" in the search. The solution will show in the "Available for download" or "New" section.</li>
<li>Click on Download</li>

<li>From Home Assistant, go to Settings, Devices & services</li>
<li>Look for the blue "Add Integration" button and click it</li>
<li>In search brand, type in "Ships" and locate Port Canaveral Ships</li>
<li>Answer questions about which Statuses to track, retrieval intervals, and number of ships to track for each status (In Port, Departed, Confirmed, Scheduled)</li>

<h3>Manual</h3>

<li>Download all the items in /custom_components/pc_ships_hacs and put them on your Home Assistant instance in /custom_components/pc_ships_hacs</li>
<li>From Home Assistant, go to Settings, Devices & services</li>
<li>Look for the blue "Add Integration" button and click it</li>
<li>In search brand, type in "Ships" and locate <b>Port Canaveral Ships</b></li>
<li>Answer questions about which Statuses to track, retrieval intervals, and number of ships to track for each status (In Port, Departed, Confirmed, Scheduled)

<h2>Entities Created</h2>
<p>Depending on what status/es you selected (In Port, Confirmed, Scheduled, Departed), as well as number of sensors for each class, will determine how many entities and naming. </p>
<p>For example, if you chose just "In Port" and "Confirmed", with number of sensors for each Status to track at 2, then you will end up with these entities:</p>

<li>sensor.port_canaveral_ships_in_port_1
<li>sensor.port_canaveral_ships_in_port_2
<li>sensor.port_canaveral_ships_confirmed_1
<li>sensor.port_canaveral_ships_confirmed_2


<h2>Attributes created for each entity</h2>
<p>The following attributes are available for each entity: </p>

<li>Status Type: (Values available: In Port, Confirmed, Departed, Scheduled)
<li>Sensor Slot: (1 - whatever number of sensors you requested)
<li>Last Updated: (Long Date and Time ex: February 20, 2025 at 10:07:00 AM)
<li>Vessel: (Vessel Name)
<li>Status: Same as Status Type (above)
<li>Cargo Type: (What cargo is aboard the ship)
<li>Vessel class: (Cargo or Pessenger)
<li>Flag: (Country of registration)
<li>Berth: (Berth assigned at port)
<li>Arrival Date: (Format: 02/21/2025)
<li>Arrival Time: (Format: 03:00 24 hour time)
<li>Departure Date: (Format: 02/21/2025)
<li>Daparture Time: (Format: 03:00 24 hour time)
<li>Is tug boat: (Checks if Vessel name starts with TG=true or not start with TG=false)
<li>Others: Last Changed and Last Updated</li>


<h2>About the update interval</h2>
We recommend that you use the default of 20 minutes. The mininum is 15 minutes, and the solution will not allow anything less than this to avoid any issue wtih uncessary retrievals. 
<p>Note the lovelace_card_example.yaml file for an example card configuration for your lovelace card. It uses vertical-stack with conditionals. </p>






