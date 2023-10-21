from pytube import YouTube, request
import ttkbootstrap as ttb
from ttkbootstrap import Style
import tkinter as ttk
from tkinter import filedialog
from tkinter import PhotoImage
import os
import threading
def start_download():
    search_frame_var.set("Wait for the download to finish...")
    youtube_link_info_frame.pack(fill='x',pady=15)
    pre_notif.config(text="Fetching data...")
    try:
        video_url = url_var.get()
        yt = YouTube(video_url,on_progress_callback=on_progress)

        # Get the video title
        video_title = yt.title
        title_formatted=video_title[0:40]
        vidTitle.set(title_formatted+"...")

        # Get the video duration
        video_length = yt.length
        video_duration_formatted = str(int(video_length // 3600)).zfill(2) + ":" + str(int((
            video_length % 3600) // 60)).zfill(2) + ":" + str(int(video_length % 60)).zfill(2)
        vidDuration.set(video_duration_formatted)

        # get publish date
        date_publish = str(yt.publish_date)
        vid_publish_var.set(date_publish)

        # get the file_size
        stream = yt.streams.first()
        vid_size=stream.filesize_mb
        vid_file_size_var.set(str(vid_size)+" mb")

        # Ask the user where to save the video with the default filename set to the video title
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            initialfile=f"{video_title}.mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        pre_notif.config(text="")

        loading_frame.pack(fill='x',padx=15)

        youtube_info_frame.pack(fill='x',padx=15)

        if file_path:
            # The user selected a file path, so we can save the video there
            # Get the highest resolution stream and download the video
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=file_path)
    except Exception as e:
        download_status.config(text=str(e),
                               fg="#dc3545")
        youtube_info_frame.pack_forget()

def start_download_thread():
    # Create a thread for the download function
    download_thread = threading.Thread(target=start_download)

    # Start the thread
    download_thread.start()

def check_entry_contents(*args):
    if url_var.get():
        search_btn.config(state="normal")
    else:
        search_btn.config(state="disabled")

def on_progress(stream, chunks, bytes_remaining):
    total_size=stream.filesize
    bytes_downloaded=total_size - bytes_remaining
    percent_of_completion= bytes_downloaded/total_size*100
    per=str(int(percent_of_completion))
    loading_subtitle.config(text=per + '%')

    if per=="100":
        search_frame_var.set("Insert YouTube Link")
        search_entry.config(state="normal")
        loading_subtitle.config(text="FINISH!")
        # search_btn.pack_forget()
        downloading_label_var.set("Downloaded")
        loading_frame.pack_forget()
        download_finish.pack(fill='x',pady=5)
    else:
        search_entry.config(state="disabled")
        downloading_label_var.set("Downloading...")

    url_var.set("")
    loading_subtitle.update()


# window
window=ttb.Window()
window.title("YouTube Downloader")
window.geometry("700x600")
window.resizable(False, False)
window.iconbitmap("icons/online-video.ico")

# style
style=Style(theme="darkly")
background_color="#181818"
fg="#ffffff"

# main_frame
main_frame=ttb.Frame(window)
main_frame.pack(fill='x')
# main_frame

# header_frame
header_frame=ttk.Frame(main_frame)
header_frame.config(bg=background_color)
header_frame.pack(fill='x', ipadx=15, ipady=10)
# header_frame


# header_icon

new_width=40
new_height=40

icon_path = os.path.abspath("icons/online-video.png")
window.iconphoto(True, ttk.PhotoImage(file=icon_path))
header_icon=PhotoImage(file="icons/online-video.png")

header_icon=header_icon.subsample(int(header_icon.width()/new_width), int(header_icon.height()/new_height))
header_icon_label=ttb.Label(header_frame, image=header_icon)
header_icon_label.pack(side="left", padx=15)
# header_icon

# header_title
header_title=ttk.Label(header_frame, text="YouTube Downloader", font="Arial 16 bold")
header_title.config(bg=background_color, fg="#FFFFFF")
header_title.pack(side="left", fill='x')
# header_title

# search_frame
search_frame=ttb.Frame(main_frame)
search_frame.pack(fill='x',padx=15, pady=20)
# search_frame

# search_frame_label
search_frame_var=ttk.StringVar()
search_frame_var.set("Insert Youtube Link")
search_frame_label=ttb.Label(search_frame, textvariable=search_frame_var)
search_frame_label.pack(fill='x')
# search_frame_label

# search_entry
url_var=ttk.StringVar()
url_var.trace("w", check_entry_contents)
search_entry=ttb.Entry(search_frame, style="darkly", font="Arial 12", textvariable=url_var)
search_entry.pack(fill='x', pady=10, ipady=10)
# search_entry

# download_status
download_status=ttk.Label(search_frame, text="", font="Arial 9 bold")
# download_status

# search_btn
search_btn=ttb.Button(search_frame, text="Download", style="danger", width=20, command=start_download_thread,
                      state="disabled")
search_btn.pack(ipady=7,pady=10)
# search_btn

# pre_notif
pre_notif=ttb.Label(search_frame, text="")
pre_notif.pack(fill='x')
# pre_notif

# loading_frame
loading_frame=ttb.Frame(search_frame)
# loading_frame.pack()
# loading_frame

# downloading_label
downloading_label_var=ttk.StringVar()
downloading_label=ttb.Label(loading_frame, textvariable=downloading_label_var)
downloading_label.pack(fill='x')
# downloading_label

# loading_bar
loading_bar=ttb.Progressbar(loading_frame, style="danger", mode="determinate", maximum=100, length=200)
loading_bar.pack(fill='x',pady=5, ipady=5)
# loading_bar

# loading_subtitle
loading_subtitle=ttb.Label(loading_frame, text="0%", style="success")
loading_subtitle.pack(fill='x')
# loading_subtitle

# youtube_info_frame
youtube_info_frame=ttb.Frame(main_frame)
youtube_info_frame.pack(fill='x', padx=15)
# youtube_info_frame


# youtube_link_info_frame
youtube_link_info_frame=ttb.Frame(youtube_info_frame)
youtube_link_info_frame.pack(fill='x', pady=5)
# youtube_link_info_frame

# youtube_data
youtube_data=ttb.Frame(youtube_info_frame)
youtube_data.pack(fill='x')
# youtube_data

# youtube_link_metadata
youtube_link_metadata=ttb.Frame(youtube_data)
youtube_link_metadata.pack(side="left", fill='x')
# youtube_link_metadata

# vid_title
vidTitle=ttk.StringVar()
# vidTitle.set("Lorem ipssum dolor sit amit consicutor")
vid_title=ttb.Label(youtube_data, textvariable=vidTitle, font="Arial 10 bold")
vid_title.pack(fill='x')
# vid_title

# vid_duration
vidDuration=ttk.StringVar()
# vidDuration.set("05:00")
vid_duration=ttb.Label(youtube_data, textvariable=vidDuration)
vid_duration.pack(fill='x')
# vid_duration

# vid_publish_date
vid_publish_var=ttk.StringVar()
# vid_publish_var.set("2023-10-19")
vid_publish_date=ttb.Label(youtube_data, textvariable=vid_publish_var)
vid_publish_date.pack(fill='x')
# vid_publish_date

# vid_file_size
vid_file_size_var=ttk.StringVar()
# vid_file_size_var.set("100tb")
vid_file_size=ttb.Label(youtube_data, textvariable=vid_file_size_var)
vid_file_size.pack(fill='x')
# vid_file_size

# download_finish
download_finish=ttb.Label(youtube_data, text="Completed ✓", style="success")
# download_finish

# left_side_content

# footer
footer=ttk.Frame(window)
footer.config(bg=background_color)
footer.pack(side="bottom",fill='x')
# footer

# developer
developer=ttk.Label(footer, text="Developed by TEPHDY TECH")
developer.config(fg="#FA8714", bg=background_color)
developer.pack(fill='x', pady=10)
# developer

# run
window.mainloop()

# no code must be written below!