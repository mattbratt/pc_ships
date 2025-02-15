
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
<li>Answer questions about which Statuses to track, retrieval intervals, and number of ships to track for each status (In Port, Departed, Confirmed, Scheduled)</li>

<h2>About the update interval</h2>
We recommend that you use the default of 20 minutes. The mininum is 15 minutes, and the solution will not allow anything less than this to avoid any issue wtih uncessary retrievals. 

Note the lovelace_card_example.yaml file for an example card configuration for your lovelace card. It uses vertical-stack with conditionals. 






