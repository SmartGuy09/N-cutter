# i wrote this thing around 17 months ago 
# comments by chatgpt! & me

from tkinter import *
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


class VideoTrimmer:    

    def __init__(self):
        self.window = Tk()        
        self.window.title("N-cutter")
        # screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # width and height
        window_width = 600
        window_height = 500

        # the math
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the window geometry
        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        # File input section
        file_frame = Frame(self.window)
        file_frame.pack(pady=10)

        file_label = Label(file_frame, text="Choose a video file:")
        file_label.pack(side=LEFT)

        self.file_entry = Entry(file_frame, width=30)
        self.file_entry.pack(side=LEFT, padx=10)

        file_button = Button(file_frame, text="Browse", command=self.browse_file)
        file_button.pack(side=LEFT)

        # Parts input section
        parts_frame = Frame(self.window)
        parts_frame.pack(pady=10)

        parts_label = Label(parts_frame, text="Enter the number of parts:")
        parts_label.pack(side=LEFT)

        self.parts_entry = Entry(parts_frame, width=10)
        self.parts_entry.pack(side=LEFT, padx=10)

        # Folder input section
        folder_frame = Frame(self.window)
        folder_frame.pack(pady=10)

        folder_label = Label(folder_frame, text="Choose a folder to save the trimmed videos:")
        folder_label.pack(side=LEFT)        

        self.folder_entry = Entry(folder_frame, width=10)
        self.folder_entry.pack(side=LEFT, padx=5)

        folder_button = Button(folder_frame, text="Choose Folder", command=self.browse_folder)
        folder_button.pack(side=LEFT)

        # Trim button
        trim_button = Button(self.window, text="Trim", command=self.trim_video)
        trim_button.pack(pady=20)

        info_lable = Label(self.window, text="Made By - Smart Guy", fg='green')
        info_lable.pack(side=BOTTOM)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Jo video katna h wo choose kar!",
                                              filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, filename)

    def browse_folder(self):
        foldername = filedialog.askdirectory(initialdir="/", title="folder lele")
        if not foldername:
            self.show_error("No folder selected. Please choose a folder.")
            return

        self.folder_entry.delete(0, END)
        self.folder_entry.insert(0, foldername)

    def trim_video(self):
        # Get the input values
        filename = self.file_entry.get()
        parts = self.parts_entry.get()
        foldername = self.folder_entry.get()

        print(f"Filename: {filename}, Parts: {parts}, Foldername: {foldername}")

        # Check if all fields are filled
        if not filename or not parts or not foldername:
            print("Error: Some fields are empty")
            self.show_error("BKL kuch to entry kar.")
            return

        try:
            parts = int(parts)
        except ValueError:
            print("Error: Invalid number of parts")
            self.show_error("jyada ganith aari kya?.")
            return

        # Load the video file
        video = VideoFileClip(filename)

        # Trim the video and save each part to the selected folder
        duration = video.duration
        part_duration = duration / parts

        for i in range(parts):
            start_time = i * part_duration
            end_time = min((i + 1) * part_duration, duration)
            part = video.subclip(start_time, end_time)
            part_title = os.path.splitext(os.path.basename(filename))[0] + "_part" + str(i+1) + ".mp4"
            part_path = os.path.join(foldername, part_title)
            part.write_videofile(part_path)

        # Close the video file
        video.reader.close()

    def show_error(self, message):
        error_window = Toplevel(self.window)
        error_window.title("Error")

        # the shit again
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()

        window_width = 300
        window_height = 150

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        error_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Display the error message
        error_label = Label(error_window, text=message)
        error_label.pack(padx=20, pady=10)

        # OK button to close the error window
        samjha_button = Button(error_window, text="sorry!", command=error_window.destroy)
        samjha_button.pack(pady=10)

if __name__ == "__main__":
    app = VideoTrimmer()
    app.window.mainloop()
