<!-- Icon at the top -->
<img src="https://github.com/mattbratt/pc_ships/blob/main/images/icon.png" alt="Port Canaveral Ships Icon" style="max-width: 100px; display: block; margin: 0 auto;">

<h1>Port Canaveral Ships</h1>

<h2>About</h2>
<p><strong>Port Canaveral Ships</strong> is a <a href="https://hacs.xyz/" target="_blank">HACS</a> solution that retrieves data from Port Canaveral and integrates it into <a href="https://www.home-assistant.io/" target="_blank">Home Assistant</a>. It provides a convenient way to monitor cargo and passenger ships moving in and out of Port Canaveral, located on the central east coast of Florida. Users can customize the integration to track cargo ships, passenger ships, or both, based on their preferences.</p>
<p>During installation, users are presented with the following options:</p>

<img src="https://github.com/mattbratt/pc_ships/blob/main/images/pc_ships_config.png">

<p>It’s recommended to keep most options at their defaults, though a popular customization is to select all statuses (instead of just "In Port" and "Confirmed"). The statuses are defined as follows:</p>
<ul>
    <li><strong>In Port</strong> - Ships currently in port and at a berth.</li>
    <li><strong>Confirmed</strong> - Ships that have validated their arrival at the port.</li>
    <li><strong>Scheduled</strong> - Ships scheduled to arrive at the port, used for managing berthing, etc.</li>
    <li><strong>Departed</strong> - Ships that have recently departed.</li>
</ul>

<h2>Installing the Solution</h2>

<h3>HACS (Preferred and Easy)</h3>
<p>Install via the <strong>HACS</strong> community store for the simplest experience:</p>
<ol>
    <li>From Home Assistant, navigate to <strong>HACS</strong>.</li>
    <li>In the HACS store, search for <em>"Port Canaveral Ships"</em>. Look for it in the "Available for download" or "New" section.</li>
    <li>Click <strong>Download</strong>.</li>
    <li>In Home Assistant, go to <strong>Settings > Devices & Services</strong>.</li>
    <li>Click the blue <strong>+ Add Integration</strong> button.</li>
    <li>Search for "Ships" and select <strong>Port Canaveral Ships</strong>.</li>
    <li>Configure the integration by selecting statuses to track, retrieval intervals, and the number of ships to monitor for each status (In Port, Departed, Confirmed, Scheduled).</li>
</ol>





<h3>Manual Installation</h3>
<p>For advanced users preferring a manual setup:</p>
<ol>
    <li>Download all files from <code>/custom_components/pc_ships</code> and place them in your Home Assistant instance under <code>/custom_components/pc_ships</code>.</li>
    <li>In Home Assistant, go to <strong>Settings > Devices & Services</strong>.</li>
    <li>Click the blue <strong>+ Add Integration</strong> button.</li>
    <li>Search for "Ships" and select <strong>Port Canaveral Ships</strong>.</li>
    <li>Configure the integration by selecting statuses to track, retrieval intervals, and the number of ships to monitor for each status. Recommended defaults: In Port: 15, Confirmed: 15, Scheduled: 15, Departed: 15.</li>
</ol>

<h2>Entities Created</h2>
<p>The number and naming of entities depend on the selected statuses (In Port, Confirmed, Scheduled, Departed) and the number of sensors specified for each status.</p>
<p>For example, if you select "In Port" and "Confirmed" with 2 sensors per status, the following entities are created:</p>
<ul>
    <li><code>sensor.port_canaveral_ships_in_port_1</code></li>
    <li><code>sensor.port_canaveral_ships_in_port_2</code></li>
    <li><code>sensor.port_canaveral_ships_confirmed_1</code></li>
    <li><code>sensor.port_canaveral_ships_confirmed_2</code></li>
</ul>

<h2>Attributes Created for Each Entity</h2>
<p>Each entity includes the following attributes:</p>
<ul>
    <li><strong>Status Type</strong>: (Values: In Port, Confirmed, Departed, Scheduled)</li>
    <li><strong>Sensor Slot</strong>: (1 to the number of sensors requested)</li>
    <li><strong>Last Updated</strong>: (e.g., February 20, 2025 at 10:07:00 AM)</li>
    <li><strong>Vessel</strong>: (Vessel Name)</li>
    <li><strong>Status</strong>: (Matches Status Type)</li>
    <li><strong>Cargo Type</strong>: (Cargo aboard the ship)</li>
    <li><strong>Vessel Class</strong>: (Cargo or Passenger)</li>
    <li><strong>Flag</strong>: (Country of registration)</li>
    <li><strong>Berth</strong>: (Assigned berth at port)</li>
    <li><strong>Arrival Date</strong>: (e.g., 02/21/2025)</li>
    <li><strong>Arrival Time</strong>: (e.g., 03:00, 24-hour format)</li>
    <li><strong>Departure Date</strong>: (e.g., 02/21/2025)</li>
    <li><strong>Departure Time</strong>: (e.g., 03:00, 24-hour format)</li>
    <li><strong>Is Tug Boat</strong>: (True if vessel name starts with "TG", False otherwise)</li>
    <li><strong>Others</strong>: Last Changed and Last Updated</li>
</ul>

<h2>About the Update Interval</h2>
<p>We recommend using the default update interval of <strong>20 minutes</strong>. The minimum is <strong>15 minutes</strong>, and the solution enforces this limit to prevent unnecessary data retrievals.</p>
<p>See the <code>lovelace_card_example.yaml</code> file for a sample Lovelace card configuration. It uses a vertical stack with conditionals for a dynamic display.</p>
