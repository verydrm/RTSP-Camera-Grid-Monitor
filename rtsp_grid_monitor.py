import sys
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime

if sys.platform == "win32":
    import win32gui
    import win32con
    import ctypes

# -------------------------------
GRID_ROWS = 3
GRID_COLS = 3
# -------------------------------

mainstream_urls = [
    "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/301",
    "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/201",
    "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101",
    "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/401",
    "rtsp://admin:password@192.168.1.101:554/Streaming/Channels/101",
    "rtsp://admin:password@192.168.1.102:554/Streaming/Channels/101",
    "rtsp://admin:password@192.168.1.103:554/Streaming/Channels/101",
    "rtsp://admin:password@192.168.1.104:554/Streaming/Channels/101",
    "rtsp://admin:password@192.168.1.105:554/Streaming/Channels/101",
]

fullscreen_processes = []

def myprint(msg):
    print(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        msg,
        flush=True
    )
    
def start_fullscreen_ffplay(strURL):
    global fullscreen_processes

    fullscreen_processes = [p for p in fullscreen_processes if p.poll() is None]
    if fullscreen_processes:
        myprint("[Overlay] Fullscreen already running.")
        return

    myprint(f"[Overlay] Fullscreen requested for: {strURL}")
    try:

        p = subprocess.Popen([
            'ffplay', '-fs', '-noborder', '-loglevel', 'quiet',
            '-fflags', 'nobuffer+discardcorrupt', '-flags', 'low_delay', '-framedrop',
            '-probesize', '32', '-analyzeduration', '0',
            '-rtsp_transport', 'tcp', '-max_delay', '50000', '-an', strURL
        ])
        fullscreen_processes.append(p)
    except Exception as e:
        myprint(f"[Overlay] Failed to launch fullscreen ffplay: {e}")


class VideoWidget(QFrame):
    def __init__(self, index, sub_url, main_url, main_window=None):
        super().__init__()
        self.index = index
        self.sub_url = sub_url
        self.main_url = main_url
        self.main_window = main_window
        self.process = None
        self.ffplay_hwnd = None

        self.setAttribute(Qt.WA_NativeWindow)
        self.setStyleSheet("background-color: black;")

        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.check_process_health)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            myprint(f"[VideoWidget #{self.index}] Double click captured! Opening fullscreen main stream.")
            start_fullscreen_ffplay(self.main_url)
        super().mouseDoubleClickEvent(event)

    def start(self):
        myprint(f"[VideoWidget #{self.index}] Starting ffplay for: {self.sub_url}")
        self.launch_ffplay()
        self.monitor_timer.start(5000) 


    def launch_ffplay(self):
            self.cleanup_process()
            
            cmd = [
                'ffplay', 
                '-loglevel', 'quiet',
                #'-stimeout', '5000000',               
                '-fflags', 'nobuffer+discardcorrupt', 
                '-flags', 'low_delay',                
                '-framedrop',                         
                '-probesize', '32', 
                '-analyzeduration', '0', 
                '-rtsp_transport', 'tcp',             
                '-max_delay', '50000',                
                '-an',                                
                '-left', '-9999', '-top', '-9999',    
                '-window_title', f"ffplay_embed_{id(self)}",
                self.sub_url
            ]
            try:
                self.process = subprocess.Popen(cmd)
                QTimer.singleShot(200, self.embed_ffplay_window)
            except Exception as e:
                myprint(f"[VideoWidget #{self.index}] Launch ffplay failed: {e}")


    def embed_ffplay_window(self):
        if sys.platform != "win32" or not self.process or self.process.poll() is not None:
            return

        target_title = f"ffplay_embed_{id(self)}"
        hwnd = win32gui.FindWindow(None, target_title)
        
        if not hwnd:
            QTimer.singleShot(100, self.embed_ffplay_window)
            return

        self.ffplay_hwnd = hwnd
        qt_hwnd = int(self.winId())

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        style &= ~win32con.WS_CAPTION
        style &= ~win32con.WS_SYSMENU
        style &= ~win32con.WS_THICKFRAME
        style |= win32con.WS_CHILD   
        
        style |= win32con.WS_DISABLED 
        
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)


        win32gui.SetParent(hwnd, qt_hwnd)
        self.resize_embedded_window()
        myprint(f"[VideoWidget #{self.index}] embed_ffplay_window successful.")


    def resize_embedded_window(self):
        if self.ffplay_hwnd and sys.platform == "win32":
            win32gui.MoveWindow(self.ffplay_hwnd, 0, 0, self.width(), self.height(), True)


    def check_process_health(self):
            is_dead = self.process is None or self.process.poll() is not None
            
            if not is_dead and self.ffplay_hwnd:
                try:
                    if ctypes.windll.user32.IsHungAppWindow(self.ffplay_hwnd):
                        myprint(f"[HealthCheck] ffplay widget #{self.index} window is HUNG (frozen)!")
                        is_dead = True
                except Exception as e:
                    myprint(f"[HealthCheck] Check window hung error: {e}")

            if is_dead:
                myprint(f"[HealthCheck] ffplay widget #{self.index} disconnected or frozen, auto restarting...")
                self.launch_ffplay()


    def cleanup_process(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except Exception:
                try: self.process.kill()
                except: pass
            self.process = None
            self.ffplay_hwnd = None

    def resizeEvent(self, event):
        self.resize_embedded_window()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.cleanup_process()
        super().closeEvent(event)


class MonitorGrid(QWidget):
    def __init__(self, sub_urls, main_urls):
        super().__init__()
        self.setWindowTitle(f"{GRID_ROWS}x{GRID_COLS} ffplay Ultra-Low Latency Monitor (Double-Click for Fullscreen)")
        self.setGeometry(100, 100, 1280, 720)

        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.widgets = []
        self.main_urls = main_urls
        self.sub_urls = sub_urls

        total_cells = GRID_ROWS * GRID_COLS
        for i in range(total_cells):
            if i < len(self.sub_urls):
                vw = VideoWidget(i, self.sub_urls[i], self.main_urls[i], self)
                layout.addWidget(vw, i // GRID_COLS, i % GRID_COLS)  
                self.widgets.append(vw)
            else:
                empty = QFrame()
                empty.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333;")
                layout.addWidget(empty, i // GRID_COLS, i % GRID_COLS)

        self.showMaximized()
        QTimer.singleShot(500, self.start_all)
        
    def start_all(self):
        self.start_index = 0
        self.start_next()

    def start_next(self):
        if self.start_index >= len(self.widgets):
            return
        self.widgets[self.start_index].start()
        self.start_index += 1

        QTimer.singleShot(1500, self.start_next)
        
    def keyPressEvent(self, event):
        key = event.key()

        if Qt.Key_1 <= key <= Qt.Key_9:
            index = key - Qt.Key_1
            if 0 <= index < len(self.widgets):
                start_fullscreen_ffplay(self.widgets[index].main_url)

        elif key == Qt.Key_Escape:
             global fullscreen_processes
             fullscreen_processes = [p for p in fullscreen_processes if p.poll() is None]
             for p in fullscreen_processes:
                 p.terminate()

    def closeEvent(self, event):
        for w in self.widgets:
            w.close()
        super().closeEvent(event)


def convert_to_substream(urls, timeout=1):
    substream_urls = []
    import socket
    for url in urls:
        if re.search(r'Channels/\d01', url):
            new_url = re.sub(r'(Channels/\d)01', r'\g<1>02', url)
        elif re.search(r'ch\d+_0\.h264', url):
            new_url = re.sub(r'(ch\d+)_0(\.h264)', r'\1_1\2', url)
        else:
            new_url = url  

        ip_port_match = re.match(r'.*://(?:[^@:]+:)?(?:[^@]+@)?([\d.]+):(\d+)', new_url)
        if ip_port_match:
            ip = ip_port_match.group(1)
            port = int(ip_port_match.group(2))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                sock.connect((ip, port))
                substream_urls.append(new_url)
            except Exception:
                substream_urls.append(url)
            finally:
                sock.close()
        else:
            substream_urls.append(url)
    return substream_urls
    

if __name__ == '__main__':
    myprint("[Main] Launcher initialized. Anti-lag parameters active.")
    substream_urls = convert_to_substream(mainstream_urls)
    
    try:
        app = QApplication(sys.argv)
        grid = MonitorGrid(substream_urls, mainstream_urls)
        sys.exit(app.exec_())
    except Exception as e:
        myprint(f"[Main] Critical Application error: {e}")
