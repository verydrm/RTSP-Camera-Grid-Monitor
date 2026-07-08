# RTSP-Camera-Grid-Monitor
Ultra-low latency 3×3 RTSP Multi-Camera RTSP Viewe with embedded ffplay, automatic reconnect, and one-click fullscreen.

# RTSP Camera Grid Monitor

<p align="center">

<img src="screenshots/logo.png" width="180">

</p>

<p align="center">

A lightweight, ultra-low latency RTSP camera viewer for Windows.

Display multiple IP cameras in a responsive **3×3 camera grid**, powered by **PyQt5** and **ffplay**.

Designed for home surveillance, small offices, workshops, warehouses, and DIY monitoring systems.

</p>

---

<p align="center">

<img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue">

<img alt="Platform" src="https://img.shields.io/badge/Platform-Windows-success">

<img alt="RTSP" src="https://img.shields.io/badge/Protocol-RTSP-green">

<img alt="License" src="https://img.shields.io/badge/License-MIT-yellow">

<img alt="ffplay" src="https://img.shields.io/badge/Backend-FFplay-red">

</p>

---

# Screenshot

## Camera Grid

![Grid](screenshots/grid.png)

Display up to **9 RTSP cameras simultaneously** in a responsive 3×3 layout.

Each camera runs independently, allowing automatic recovery if a stream disconnects.

---

## Fullscreen Mode

![Fullscreen](screenshots/fullscreen.png)

Double-click any camera to instantly open the corresponding **main stream** in fullscreen mode.

The camera grid continues running in the background.

---

# Why This Project?

Many IP camera applications suffer from one or more of the following problems:

- High latency
- Heavy CPU usage
- Large memory footprint
- Complicated installation
- Expensive commercial licenses
- Poor support for multiple cameras
- Slow stream recovery after disconnects

This project was created to solve these problems while remaining lightweight and easy to use.

Instead of implementing another video decoder, this application leverages the highly optimized **ffplay** player and embeds each player window directly into a PyQt interface.

The result is a fast and responsive multi-camera monitoring application with extremely low latency.

---

# Key Features

## ✔ 3×3 Camera Grid

Display up to nine RTSP cameras simultaneously.

The grid layout automatically resizes with the application window.

Perfect for:

- Home surveillance
- Office monitoring
- Factory monitoring
- Garage security
- Warehouse surveillance
- Workshop cameras
- Retail stores
- DIY CCTV systems

---

## ✔ Ultra-Low Latency

The application uses carefully tuned ffplay parameters to reduce buffering as much as possible.

Typical latency:

- approximately 100–300 ms on a local network

Much lower than many traditional surveillance applications.

---

## ✔ Embedded ffplay Windows

Unlike launching multiple standalone ffplay windows,

each ffplay instance is embedded directly inside the Qt interface.

Benefits include:

- cleaner interface
- automatic resizing
- native window management
- lower desktop clutter

---

## ✔ Double-Click Fullscreen

Double-click any camera to immediately open its **main stream** in fullscreen.

This is especially useful when:

- someone rings the doorbell
- motion is detected
- checking package deliveries
- monitoring visitors

---

## ✔ Automatic Main/Sub Stream Switching

Most IP cameras provide:

- Main Stream (high resolution)
- Sub Stream (lower bandwidth)

The application automatically attempts to use the sub stream for the grid.

When fullscreen is requested, it switches to the corresponding main stream.

This significantly reduces:

- network traffic
- CPU usage
- decoding workload

while maintaining high image quality when needed.

---

## ✔ Automatic Camera Recovery

Each camera runs independently.

If one stream disconnects:

- only that camera restarts
- other cameras continue running normally

This makes the system much more reliable than restarting the entire application.

---

## ✔ Frozen Window Detection

A process can remain alive even when video decoding has stopped.

On Windows, the application periodically checks whether an embedded ffplay window has become unresponsive.

If a frozen window is detected, it is automatically restarted.

This greatly improves long-term stability.

---

## ✔ Keyboard Shortcuts

Press:

| Key | Function |
|------|----------|
| 1-9 | Open camera in fullscreen |
| ESC | Close all fullscreen windows |

Fast keyboard control makes the application convenient for daily monitoring.

---

## ✔ Sequential Camera Startup

Opening multiple RTSP streams simultaneously may overload:

- cameras
- switches
- routers
- Wi-Fi

Instead, cameras are started one by one with a configurable delay.

Benefits include:

- smoother startup
- fewer connection failures
- reduced network bursts

---

## ✔ Lightweight

The application itself performs very little video processing.

Most decoding work is handled by ffplay.

As a result:

- low memory usage
- low CPU overhead
- excellent stability

---

# Typical Use Cases

This application is suitable for:

- Home security
- Apartment monitoring
- Office surveillance
- Small businesses
- Warehouses
- Workshops
- Farms
- Shops
- Parking lots
- Hobby CCTV projects

It also works well for anyone wanting a lightweight RTSP monitor without installing a full NVR system.

---

# Design Philosophy

The goal of this project is **simplicity**.

Instead of building another complex surveillance platform, it focuses on doing one thing well:

> Display multiple RTSP cameras with the lowest possible latency.

No cloud services.

No subscriptions.

No user accounts.

No vendor lock-in.

Just open your cameras and monitor them.

---

# Core Technologies

- Python
- PyQt5
- ffplay
- FFmpeg
- Win32 API
- RTSP
- TCP Transport

These technologies combine to provide excellent responsiveness while keeping the codebase relatively small and easy to understand.

---


## Installation

### Prerequisites

Before running the application, make sure the following software is installed:

* Python 3.9 or later
* FFmpeg (including **ffplay**)
* Windows 10 or Windows 11

---

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:

```text
PyQt5
pywin32
```

---

### Install FFmpeg

Download FFmpeg from the official website:

https://ffmpeg.org/

Make sure **ffplay.exe** is available from your system PATH.

You can verify the installation by running:

```bash
ffplay -version
```

If the version information is displayed, the installation was successful.

---

## Project Structure

```text
rtsp-camera-grid-monitor/
│
├── rtsp_grid_monitor.py
├── config.py
├── sample_config.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
└── screenshots/
    ├── grid.png
    ├── fullscreen.png
    └── logo.png
```

Project files:

| File                 | Description                       |
| -------------------- | --------------------------------- |
| rtsp_grid_monitor.py | Main application                  |
| config.py            | Your private camera configuration |
| sample_config.py     | Example configuration             |
| requirements.txt     | Python dependencies               |
| screenshots          | Images used by this README        |

---

## Configuration

Camera information is intentionally stored outside the main program.

This prevents accidentally publishing passwords or private IP addresses.

Create a file named:

```text
config.py
```

Example:

```python
CAMERAS = [

    "rtsp://username:password@192.168.0.100:554/Streaming/Channels/101",

    "rtsp://username:password@192.168.0.101:554/Streaming/Channels/101",

    "rtsp://username:password@192.168.0.102:554/Streaming/Channels/101",

]
```

The application imports this list automatically.

Never commit your own `config.py` to GitHub.

Instead, commit:

```
sample_config.py
```

and add `config.py` to `.gitignore`.

---

## Running the Application

Start the application with:

```bash
python rtsp_grid_monitor.py
```

The application will:

1. Load camera URLs
2. Detect sub streams
3. Build the camera grid
4. Start cameras one at a time
5. Monitor stream health continuously

---

## User Interface

The interface is intentionally simple.

```
+-------------------------------+
| Camera | Camera | Camera |
+-------------------------------+
| Camera | Camera | Camera |
+-------------------------------+
| Camera | Camera | Camera |
+-------------------------------+
```

Unused cells remain empty.

The layout automatically scales when resizing the window.

---

## Camera Startup Sequence

Instead of opening every RTSP stream simultaneously, the application starts cameras gradually.

```
Camera 1

↓

Camera 2

↓

Camera 3

↓

...

↓

Camera 9
```

This approach helps avoid:

* Network congestion
* Camera overload
* Connection failures
* Startup lag

The startup interval can be adjusted in the source code.

---

## Automatic Sub Stream Detection

Many surveillance cameras provide two streams:

Main Stream

* High resolution
* Higher bandwidth
* Better image quality

Sub Stream

* Lower resolution
* Lower bandwidth
* Faster decoding

The application automatically converts common RTSP URLs to their corresponding sub stream whenever available.

Examples:

```
Streaming/Channels/101
↓

Streaming/Channels/102
```

or

```
ch0_0.h264

↓

ch0_1.h264
```

If a sub stream cannot be reached, the application automatically falls back to the original stream.

No manual configuration is required.

---

## Fullscreen Mode

Each camera has two stream URLs:

* Grid stream
* Fullscreen stream

The grid displays the lightweight stream.

Double-clicking opens the higher-quality stream.

Benefits:

* Better image quality
* Lower CPU usage
* Lower network traffic
* Faster grid rendering

---

## Embedded ffplay Windows

Instead of displaying separate player windows, ffplay is embedded inside each Qt widget.

```
+------------------------+

| Qt Widget |

| |

| Embedded ffplay |

| |

+------------------------+
```

Advantages:

* Native window resizing
* Cleaner desktop
* Better user experience
* Independent camera management

---

## Automatic Recovery

Each camera has its own monitoring logic.

```
Camera

↓

Running

↓

Disconnected?

↓

YES

↓

Restart ffplay

↓

Continue monitoring
```

Only the failed camera is restarted.

Other cameras remain unaffected.

---

## Health Monitoring

A running process does not always mean a healthy video stream.

The application periodically checks:

* Process status
* Window availability
* Frozen window detection (Windows)

If a problem is detected:

```
Terminate process

↓

Start new ffplay instance

↓

Re-embed window

↓

Continue playback
```

This enables long-term unattended operation.

---

# Low Latency Optimization

The application uses carefully selected FFmpeg parameters.

These parameters are chosen specifically for real-time monitoring instead of media playback.

Current options include:

```text
-fflags nobuffer+discardcorrupt
-flags low_delay
-framedrop
-probesize 32
-analyzeduration 0
-rtsp_transport tcp
-max_delay 50000
-an
```

Each parameter contributes to reducing playback delay.

---

### nobuffer

Disables unnecessary buffering.

Result:

* Lower latency
* Faster live response

---

### discardcorrupt

Automatically ignores damaged packets.

Benefits:

* Smoother playback
* Better stability

---

### low_delay

Enables FFmpeg's low latency decoding mode.

Designed specifically for live streams.

---

### framedrop

If decoding falls behind, old frames are skipped.

This prevents playback from accumulating delay.

Live monitoring is generally more important than displaying every frame.

---

### analyzeduration 0

Skips long stream analysis.

Playback begins much faster.

---

### probesize 32

Reduces startup probing.

The player starts almost immediately.

---

### rtsp_transport tcp

Uses TCP transport.

Compared with UDP:

Advantages:

* More reliable
* Better through firewalls
* Fewer packet losses

---

### max_delay

Limits buffering delay.

Smaller values produce faster response.

---

### Audio Disabled

Audio is disabled intentionally.

Reasons:

* Lower CPU usage
* Lower bandwidth
* Reduced synchronization delay

The application focuses entirely on video monitoring.

---

# Performance

The application is designed to remain responsive even when monitoring multiple cameras simultaneously.

Actual performance depends on:

* Camera resolution
* Camera frame rate
* Network bandwidth
* CPU performance
* GPU acceleration (if enabled by FFmpeg)
* RTSP server implementation

For best results, use the **sub stream** for the grid and reserve the **main stream** for fullscreen viewing.

---

# Resource Usage

Compared with many traditional NVR applications, this project aims to minimize resource consumption.

Typical characteristics:

* Low Python CPU usage
* Low memory overhead
* Independent player processes
* Fast startup
* Quick recovery after disconnects

Because video decoding is handled by **ffplay**, the Python application mainly manages windows, layouts, and process monitoring.

---

# Supported Cameras

Any camera providing a standard RTSP stream should work.

Examples include cameras from many popular manufacturers that expose RTSP URLs.

The project does not rely on proprietary SDKs or vendor-specific APIs.

If your camera can be opened by **ffplay**, it will usually work with this application.

---

# Supported RTSP URL Formats

The automatic sub-stream conversion currently recognizes common formats such as:

```text
Streaming/Channels/101
Streaming/Channels/201
Streaming/Channels/301
Streaming/Channels/401
```

and converts them to:

```text
Streaming/Channels/102
Streaming/Channels/202
Streaming/Channels/302
Streaming/Channels/402
```

It also supports URL styles similar to:

```text
ch0_0.h264
```

which become:

```text
ch0_1.h264
```

If no matching pattern is found, the original RTSP URL is used without modification.

---

# Application Architecture

The application follows a simple layered design.

```text
                    User

                      │

                      ▼

           PyQt User Interface

                      │

                      ▼

              Monitor Grid

                      │

        ┌─────────────┼─────────────┐

        ▼             ▼             ▼

   VideoWidget   VideoWidget   VideoWidget

        │             │             │

        ▼             ▼             ▼

     ffplay        ffplay        ffplay

        │             │             │

        ▼             ▼             ▼

          RTSP Camera Streams
```

Each camera is completely independent.

A failure in one stream does not affect any other stream.

---

# Why Use ffplay?

Many Python RTSP viewers decode video directly inside Python.

While this approach works, it often introduces additional complexity and higher CPU usage.

This project intentionally uses **ffplay** because it offers:

* Excellent RTSP compatibility
* Mature FFmpeg decoding
* Stable playback
* Low latency
* Simple deployment
* Proven reliability

Rather than reinventing a media player, the application focuses on providing a better monitoring experience.

---

# Why PyQt?

PyQt provides:

* Native desktop windows
* Responsive layouts
* Easy event handling
* Efficient resizing
* Mature Windows support

It is well suited for embedding native application windows such as ffplay.

---

# Keyboard Shortcuts

| Key | Action                       |
| --- | ---------------------------- |
| 1   | Fullscreen Camera 1          |
| 2   | Fullscreen Camera 2          |
| 3   | Fullscreen Camera 3          |
| 4   | Fullscreen Camera 4          |
| 5   | Fullscreen Camera 5          |
| 6   | Fullscreen Camera 6          |
| 7   | Fullscreen Camera 7          |
| 8   | Fullscreen Camera 8          |
| 9   | Fullscreen Camera 9          |
| ESC | Close all fullscreen windows |

---

# Recommended Camera Configuration

For the best user experience:

Grid View

* Use sub stream
* Lower resolution
* Lower bitrate
* Lower bandwidth

Fullscreen View

* Use main stream
* Higher resolution
* Higher bitrate
* Better image quality

This configuration provides a good balance between responsiveness and image quality.

---

# Troubleshooting

## Black Screen

Possible causes:

* Incorrect RTSP URL
* Camera offline
* Firewall blocking the connection
* Invalid username or password

Verify the stream using:

```bash
ffplay rtsp://...
```

before running the application.

---

## ffplay Cannot Be Found

Ensure FFmpeg has been installed and `ffplay.exe` is available in your system PATH.

Running:

```bash
ffplay -version
```

should display the installed version.

---

## Camera Disconnects Frequently

Possible reasons include:

* Weak Wi-Fi signal
* Network congestion
* Camera reboot
* Power instability

The application automatically attempts to reconnect whenever a stream becomes unavailable.

---

## High CPU Usage

Suggestions:

* Reduce camera resolution
* Lower frame rate
* Use sub streams
* Enable hardware acceleration in your FFmpeg build if available

---

# Frequently Asked Questions

## Does this application record video?

No.

This project is a live monitoring viewer only.

---

## Does it support ONVIF?

Not currently.

Future versions may include optional ONVIF device discovery.

---

## Does it support Linux?

The current implementation targets Windows because it relies on Win32 APIs to embed ffplay windows.

Porting to Linux would require a different window embedding mechanism.

---

## Does it support macOS?

Not at the moment.

---

## Does it support more than nine cameras?

Yes.

The grid size can be modified in the source code.

For example:

```python
GRID_ROWS = 4
GRID_COLS = 4
```

allows up to sixteen cameras.

---

# Roadmap

Future ideas include:

* ONVIF device discovery
* Drag-and-drop camera layout
* Camera names
* Camera snapshots
* Motion detection integration
* Hardware decoding options
* Multi-monitor support
* Camera grouping
* Automatic layout saving
* Dark and light themes
* Stream statistics
* Recording support (optional)
* Cross-platform support
* Docker development environment

Contributions and suggestions are welcome.

---

# Contributing

Bug reports, feature requests, and pull requests are appreciated.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your code.
5. Submit a pull request.

Please keep the code clean, readable, and well documented.

---

# About VeryDRM

This project is developed and maintained by **VeryDRM**.

VeryDRM focuses on digital content protection and document security solutions, including:

* PDF DRM Protection
* Secure Document Distribution
* Content Security Platform
* Dynamic Watermarking
* Video DRM
* Audio DRM
* eBook Protection
* Secure File Sharing

While this project is open source and focused on RTSP camera monitoring, it reflects the same engineering principles that guide our commercial software:

* Reliability
* Simplicity
* Performance
* Security
* Practical design

Learn more about VeryDRM at:

**https://verydrm.com**

---

# License

This project is released under the MIT License.

You are free to:

* Use
* Modify
* Distribute
* Incorporate into commercial projects

Please refer to the `LICENSE` file for complete details.

---

# Acknowledgements

Special thanks to the open-source community and the projects that make this application possible:

* Python
* PyQt5
* FFmpeg
* ffplay
* pywin32

Without these excellent projects, this application would not have been possible.

---

# Star History

If you find this project useful, please consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.

---

# Contact

Questions, suggestions, and pull requests are always welcome.

If you discover a bug or have an idea for a new feature, please open a GitHub Issue.

---

# Final Notes

This project was created to provide a simple, fast, and reliable RTSP monitoring solution without the complexity of a full NVR system.

Whether you are monitoring a home, office, workshop, warehouse, or laboratory, the goal is the same:

> **Open your cameras instantly, monitor them with minimal latency, and keep the interface clean and responsive.**

Happy monitoring!


---

# Comparison

Many RTSP monitoring applications focus on providing a complete Network Video Recorder (NVR) solution.

This project has a different goal.

| Feature                   | RTSP Camera Grid Monitor | Typical NVR Software |
| ------------------------- | ------------------------ | -------------------- |
| Lightweight               | ✅                        | ❌                    |
| Open Source               | ✅                        | Varies               |
| Ultra-Low Latency         | ✅                        | Usually Higher       |
| Embedded ffplay           | ✅                        | ❌                    |
| Automatic Camera Recovery | ✅                        | Varies               |
| Fast Startup              | ✅                        | ❌                    |
| Easy to Customize         | ✅                        | ❌                    |
| Cloud Dependency          | None                     | Often Required       |
| Subscription              | None                     | Sometimes            |
| Vendor Lock-in            | None                     | Possible             |

Instead of replacing a professional NVR platform, this project focuses on providing a fast and responsive multi-camera viewer.

---

# Security

This application never sends camera data to any remote server.

All RTSP streams remain inside your local network unless your cameras are configured otherwise.

The project does not:

* Upload videos
* Upload snapshots
* Collect analytics
* Require user accounts
* Require cloud services

Your camera credentials remain stored locally in `config.py`.

For security reasons:

* Never commit `config.py` to GitHub.
* Always use strong passwords for your cameras.
* Consider placing cameras on an isolated VLAN or dedicated network if possible.

---

# Privacy

Privacy is one of the design goals of this project.

Unlike many commercial surveillance solutions, this application operates entirely on your own computer.

No telemetry.

No tracking.

No advertising.

No cloud login.

No hidden background services.

---

# Customization

The project is intentionally designed to be easy to modify.

Examples of common customizations include:

* 2×2 camera layout
* 4×4 camera layout
* 5×5 camera layout
* Camera labels
* Different startup delays
* Custom keyboard shortcuts
* Alternative fullscreen behavior
* Camera grouping
* Multiple monitor support

Because the project is written in Python, these modifications are straightforward.

---

# Ideas for Future Contributions

Community contributions are welcome.

Possible enhancements include:

* ONVIF auto-discovery
* PTZ control
* Hardware acceleration options
* Recording support
* Snapshot support
* Camera name overlays
* FPS display
* Bitrate display
* Recording schedules
* Motion event integration
* AI object detection
* Face recognition integration
* License plate recognition
* MQTT notifications
* Home Assistant integration
* Frigate integration
* Docker development environment
* Linux support
* macOS support

---

# Why Open Source?

This project is released as open source because practical tools improve through community feedback.

By making the code available, developers can:

* Learn from the implementation
* Customize it for their own needs
* Fix bugs
* Add features
* Share improvements

Open source encourages collaboration and long-term maintainability.

---

# Related Projects

If you are interested in document security and digital content protection, you may also want to explore **VeryDRM**.

VeryDRM develops commercial solutions for protecting digital content, including:

* Secure PDF distribution
* PDF DRM protection
* Dynamic watermarking
* Content Security Platform
* Secure document sharing
* Video DRM
* Audio DRM
* eBook protection
* Intellectual property protection

These products focus on protecting sensitive business documents, educational materials, training content, and other valuable digital assets.

More information is available at:

https://verydrm.com

---

# GitHub Topics

Consider adding these repository topics on GitHub:

```text
rtsp
camera
ip-camera
cctv
surveillance
video-wall
multicam
ffplay
ffmpeg
pyqt5
python
home-security
home-surveillance
low-latency
video-monitor
rtsp-viewer
camera-grid
security-camera
desktop-application
windows
```

These topics can improve discoverability within GitHub.

---

# SEO Keywords

The following keywords are naturally associated with this project:

* RTSP Camera Viewer
* RTSP Camera Grid
* RTSP Monitor
* Multi Camera Viewer
* IP Camera Viewer
* CCTV Viewer
* Home Surveillance Software
* Ultra Low Latency RTSP
* RTSP Video Wall
* FFplay RTSP
* FFmpeg RTSP
* PyQt RTSP Viewer
* Embedded ffplay
* Open Source Surveillance
* Security Camera Viewer
* Desktop Camera Monitor
* Windows RTSP Viewer
* Camera Matrix Viewer
* RTSP Dashboard
* Camera Wall

---

# Support the Project

If this project saves you time or helps with your home or office surveillance setup, please consider supporting it by:

* ⭐ Starring the repository
* 🍴 Forking the project
* 🐞 Reporting bugs
* 💡 Suggesting new features
* 🔧 Submitting pull requests
* 📢 Sharing it with others

Community support helps the project continue to grow.

---

**Thank you for using RTSP Camera Grid Monitor!**
