import tkinter as tk
from tkinter import ttk, messagebox
import threading 

# Import the functions directly from your individual script files
from yt_vid_downloader import download_video
from video_splicer import splice_all_videos
from image_uploader import upload_to_roboflow

class AimDataDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎯 Aim Telemetry Pipeline Console")
        self.geometry("500x400")
        self.configure(bg="#1e1e1e")
        
        # Style layout configurations
        style = ttk.Style()
        style.theme_use('clam')
        
        # Status Display Label
        self.status_label = tk.Label(self, text="System Status: Idle", bg="#1e1e1e", fg="#ffffff", font=("Arial", 12))
        self.status_label.pack(pady=20)
        
        # --- STAGE 1: DOWNLOAD PANEL ---
        tk.Label(self, text="YouTube Source URL:", bg="#1e1e1e", fg="#aaaaaa").pack()
        self.url_input = tk.Entry(self, width=50, bg="#2d2d2d", fg="#ffffff", insertbackground="white")
        self.url_input.insert(0, "https://www.youtube.com/watch?v=mjxGYCzzcSM")
        self.url_input.pack(pady=5)
        
        self.btn_download = tk.Button(self, text="🚀 Run Video Downloader", command=self.start_download_thread, bg="#24a0ed", fg="white", width=35)
        self.btn_download.pack(pady=10)
        
        # --- STAGE 2: SPLICER PANEL ---
        self.btn_splice = tk.Button(self, text="🎬 Run Video Splicer", command=self.start_splicer_thread, bg="#00b300", fg="white", width=35)
        self.btn_splice.pack(pady=10)
        
        # --- STAGE 3: UPLOADER PANEL ---
        self.btn_upload = tk.Button(self, text="☁️ Run Roboflow Cloud Uploader", command=self.start_uploader_thread, bg="#ff9900", fg="white", width=35)
        self.btn_upload.pack(pady=10)

        # --- RUN FULL AUTOMATION ---
        self.btn_all = tk.Button(self, text="⚡ Run Full Sequential Pipeline", command=self.start_full_pipeline_thread, bg="#7842f5", fg="white", width=35, font=("Arial", 10, "bold"))
        self.btn_all.pack(pady=25)

    # ==========================================
    # THREAD MANAGEMENT LAYERS
    # ==========================================

    def start_download_thread(self):
        # Disables button immediately so user can't accidentally double-click it while running
        self.btn_download.config(state="disabled")
        url = self.url_input.get()
        self.status_label.config(text="Status: Downloading from YouTube...", fg="#24a0ed")
        
        # Dispatches the synchronous network call onto a separate track
        threading.Thread(target=self.worker_download, args=(url,), daemon=True).start()

    def worker_download(self, url):
        try:
            download_video(url)
            self.status_label.config(text="Status: Download Complete!", fg="#00b300")
            messagebox.showinfo("Success", "Video downloaded and stored successfully!")
        except Exception as e:
            self.status_label.config(text="Status: Download Error", fg="#ff3333")
            messagebox.showerror("Error", f"Failed download task:\n{str(e)}")
        finally:
            self.btn_download.config(state="normal")

    def start_splicer_thread(self):
        self.btn_splice.config(state="disabled")
        self.status_label.config(text="Status: Splicing frames...", fg="#00b300")
        
        threading.Thread(target=self.worker_splicer, daemon=True).start()

    def worker_splicer(self):
        try:
            splice_all_videos(data_dir_path="better_training", output_dir_path="raw_dataset", frame_splice=60)
            self.status_label.config(text="Status: Splicing Matrix Constructed!", fg="#00b300")
            messagebox.showinfo("Success", "Frames successfully extracted to raw_dataset folder!")
        except Exception as e:
            self.status_label.config(text="Status: Splicer Error", fg="#ff3333")
            messagebox.showerror("Error", f"Splicer operation encountered a flaw:\n{str(e)}")
        finally:
            self.btn_splice.config(state="normal")

    def start_uploader_thread(self):
        self.btn_upload.config(state="disabled")
        self.status_label.config(text="Status: Syncing with Roboflow APIs...", fg="#ff9900")
        
        threading.Thread(target=self.worker_uploader, daemon=True).start()

    def worker_uploader(self):
        try:
            upload_to_roboflow()
            self.status_label.config(text="Status: Cloud Sync Successful!", fg="#00b300")
            messagebox.showinfo("Success", "All unique batch images securely uploaded to Roboflow cloud!")
        except Exception as e:
            self.status_label.config(text="Status: Upload Error", fg="#ff3333")
            messagebox.showerror("Error", f"Cloud transaction aborted:\n{str(e)}")
        finally:
            self.btn_upload.config(state="normal")

    def start_full_pipeline_thread(self):
        self.btn_all.config(state="disabled")
        url = self.url_input.get()
        self.status_label.config(text="Status: Executing Full Pipeline Sequence...", fg="#7842f5")
        
        threading.Thread(target=self.worker_full_pipeline, args=(url,), daemon=True).start()

    def worker_full_pipeline(self, url):
        """Runs all operations sequentially in the background thread"""
        try:
            self.status_label.config(text="Status: Running Step 1/3 (Downloader)...", fg="#7842f5")
            download_video(url)
            
            self.status_label.config(text="Status: Running Step 2/3 (Splicer)...", fg="#7842f5")
            splice_all_videos(data_dir_path="better_training", output_dir_path="raw_dataset", frame_splice=60)
            
            self.status_label.config(text="Status: Running Step 3/3 (Uploader)...", fg="#7842f5")
            upload_to_roboflow()
            
            self.status_label.config(text="Status: Entire Pipeline Finished!", fg="#00b300")
            messagebox.showinfo("Pipeline Status", "Sequence Finished! Video downloaded, sliced, and batch exported to Roboflow seamlessly.")
        except Exception as e:
            self.status_label.config(text="Status: Pipeline Crashed", fg="#ff3333")
            messagebox.showerror("Pipeline Failure", f"Automation pipeline failed at execution step:\n{str(e)}")
        finally:
            self.btn_all.config(state="normal")

if __name__ == "__main__":
    app = AimDataDashboard()
    app.mainloop()