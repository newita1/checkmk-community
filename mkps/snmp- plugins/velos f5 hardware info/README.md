# CheckMK Plugin Velos F5

This Checkmk plugin is designed to monitor and gather key metrics from the hardware of Velos F5 devices, providing visibility into the status and performance of their main components. The plugin ensures the health and availability of the system by actively tracking the following elements:

    CPU: Information about processor usage and performance.
    Memory: Data regarding memory consumption to identify potential resource issues.
    Power Supply: Status of power supply units to ensure redundancy and continuous power delivery.
    Temperature: Monitoring of thermal sensors to prevent overheating.
    Disk IO Summary: Monitoring of Write and Read Latency(ms), Bytes and IOPs .

# Integration with WATO

To facilitate configuration and customization, the plugin includes a ruleset called "Velos F5 thresholds". This ruleset allows administrators to define specific threshold values directly from the WATO interface, tailoring the monitoring behavior to match the operational requirements of their Velos F5 hardware.
