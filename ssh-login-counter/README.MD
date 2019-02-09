## AlphaServer

A simple service (simple web-app or data query client) that can show all the metrices sent to it by various AlphaClients (as
described later). The stats displayed by it have metrices mapped to AlphaClients from where it was reported.

#### [Implementation Readme](server/README.md)

## AlphaClient

Any utility that can report the metrices of number of ssh log-in attempts (on the machine it is running) to AlphaServer. As soon as the ssh log-in attempt happens it should get reported to the AlphaServer.

#### [Implementation Readme](agent/README.md)

### Example:
Say, AlphaClient is running on 2 machines (nodeABC and nodeXYZ).
- 3 ssh log-in attempts were made at nodeABC
- 2 ssh log-in attempts were made at nodeXYZ

Then AlphaServer shows a web-page or console message similar to

```
Metrics for ssh log-in attempts
* nodeABC had 3 attempt
* nodeXYZ had 2 attempt
```