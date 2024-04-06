# Shelly HT Push Exporter

A middleware HTTP forwarder that reformats Shelly HT HTTP actions to a format compatible with the Prometheus pushgateway.

## Configuration

Enter the following in the Shelly HT Action configuration.

`http://<url_to_this_server>/?instance=<instance_name>&temperature=$temperature`

For humidity replace temperature with humidity in the above example.


