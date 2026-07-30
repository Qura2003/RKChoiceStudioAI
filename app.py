# ============================================
# RK Choice Studio AI
# app.py - Part 1
# ============================================

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading

import customtkinter as ctk

from background import BackgroundRemover


# ============================================
# APPLICATION SETTINGS
# ============================================

APP_NAME = "RK Choice Studio AI"
APP_VERSION = "MVP 1.0"


# ============================================
# APPEARANCE
# ============================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================
# MAIN APPLICATION
# ============================================

class RKChoiceStudioAI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("950x750")
        self.minsize(850, 700)

        self.resizable(True, True)

        # ----------------------------------------
        # Variables
        # ----------------------------------------

        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()

        self.white_background = tk.BooleanVar(
            value=True
        )

        self.processing = False

        self.remover = BackgroundRemover()

        # ----------------------------------------
        # Build Interface
        # ----------------------------------------

        self.create_interface()


    # ============================================
    # CREATE INTERFACE
    # ============================================

    def create_interface(self):

        # ----------------------------------------
        # Main Container
        # ----------------------------------------

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        # ----------------------------------------
        # Header
        # ----------------------------------------

        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.header_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )


        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=APP_NAME,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.title_label.pack(
            anchor="w"
        )


        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text=(
                "Bulk AI Background Remover "
                f"• {APP_VERSION}"
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        self.subtitle_label.pack(
            anchor="w",
            pady=(3, 0)
        )


        # ----------------------------------------
        # Folder Section
        # ----------------------------------------

        self.folder_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12
        )

        self.folder_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )


        # Input Label

        self.input_label = ctk.CTkLabel(
            self.folder_frame,
            text="Input Folder",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.input_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=(18, 8),
            sticky="w"
        )


        # Input Entry

        self.input_entry = ctk.CTkEntry(
            self.folder_frame,
            textvariable=self.input_folder,
            height=40,
            placeholder_text="Select folder containing photos..."
        )

        self.input_entry.grid(
            row=1,
            column=0,
            padx=(15, 8),
            pady=(0, 15),
            sticky="ew"
        )


        # Input Browse Button

        self.input_button = ctk.CTkButton(
            self.folder_frame,
            text="Browse",
            width=110,
            height=40,
            command=self.select_input_folder
        )

        self.input_button.grid(
            row=1,
            column=1,
            padx=(0, 15),
            pady=(0, 15)
        )


        # Output Label

        self.output_label = ctk.CTkLabel(
            self.folder_frame,
            text="Output Folder",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.output_label.grid(
            row=2,
            column=0,
            padx=15,
            pady=(5, 8),
            sticky="w"
        )


        # Output Entry

        self.output_entry = ctk.CTkEntry(
            self.folder_frame,
            textvariable=self.output_folder,
            height=40,
            placeholder_text="Select folder for processed photos..."
        )

        self.output_entry.grid(
            row=3,
            column=0,
            padx=(15, 8),
            pady=(0, 18),
            sticky="ew"
        )


        # Output Browse Button

        self.output_button = ctk.CTkButton(
            self.folder_frame,
            text="Browse",
            width=110,
            height=40,
            command=self.select_output_folder
        )

        self.output_button.grid(
            row=3,
            column=1,
            padx=(0, 15),
            pady=(0, 18)
        )


        self.folder_frame.grid_columnconfigure(
            0,
            weight=1
        )


        # ----------------------------------------
        # Options Section
        # ----------------------------------------

        self.options_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12
        )

        self.options_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )


        self.options_label = ctk.CTkLabel(
            self.options_frame,
            text="Output Options",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.options_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.white_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="White Background (JPG)",
            variable=self.white_background
        )

        self.white_checkbox.pack(
            anchor="w",
            padx=15,
            pady=(5, 15)
        )


        # ----------------------------------------
        # Status Section
        # ----------------------------------------

        self.status_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12
        )

        self.status_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )


        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.status_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )


        self.progress_bar = ctk.CTkProgressBar(
            self.status_frame,
            height=18
        )

        self.progress_bar.pack(
            fill="x",
            padx=15,
            pady=(5, 8)
        )

        self.progress_bar.set(0)


        self.progress_text = ctk.CTkLabel(
            self.status_frame,
            text="0%",
            font=ctk.CTkFont(
                size=12
            )
        )

        self.progress_text.pack(
            anchor="e",
            padx=15,
            pady=(0, 12)
        )


        # ----------------------------------------
        # Statistics
        # ----------------------------------------

        self.stats_label = ctk.CTkLabel(
            self.main_frame,
            text="Total: 0    Success: 0    Failed: 0",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.stats_label.pack(
            pady=(0, 10)
        )


        # ----------------------------------------
        # Buttons
        # ----------------------------------------

        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )


        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="START PROCESSING",
            height=48,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.start_processing
        )

        self.start_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )


        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="STOP",
            height=48,
            width=120,
            state="disabled",
            command=self.stop_processing
        )

        self.stop_button.pack(
            side="right",
            padx=(6, 0)
        )


# ============================================
# PART 1 END
# ============================================
# ============================================
# RK Choice Studio AI
# app.py - Part 2
# ============================================


    # ========================================
    # SELECT INPUT FOLDER
    # ========================================

    def select_input_folder(self):

        folder = filedialog.askdirectory(
            title="Select Input Folder"
        )

        if folder:

            self.input_folder.set(folder)

            # Automatically suggest Output folder
            # inside the selected Input folder

            input_path = Path(folder)

            suggested_output = (
                input_path.parent /
                f"{input_path.name}_Output"
            )

            self.output_folder.set(
                str(suggested_output)
            )


    # ========================================
    # SELECT OUTPUT FOLDER
    # ========================================

    def select_output_folder(self):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:
            self.output_folder.set(folder)


    # ========================================
    # UPDATE STATUS
    # ========================================

    def update_status(
        self,
        text
    ):

        self.after(
            0,
            lambda: self.status_label.configure(
                text=text
            )
        )


    # ========================================
    # UPDATE PROGRESS
    # ========================================

    def update_progress(
        self,
        index,
        total,
        percent,
        filename
    ):

        def update():

            value = percent / 100

            self.progress_bar.set(
                value
            )

            self.progress_text.configure(
                text=f"{percent:.1f}%"
            )

            self.status_label.configure(
                text=f"Processing: {filename}"
            )

        self.after(
            0,
            update
        )


    # ========================================
    # START PROCESSING
    # ========================================

    def start_processing(self):

        # ------------------------------------
        # Prevent duplicate processing
        # ------------------------------------

        if self.processing:

            return


        # ------------------------------------
        # Get folders
        # ------------------------------------

        input_folder = self.input_folder.get().strip()
        output_folder = self.output_folder.get().strip()


        # ------------------------------------
        # Validate Input
        # ------------------------------------

        if not input_folder:

            messagebox.showwarning(
                "Input Folder Required",
                "Please select an Input Folder."
            )

            return


        if not Path(input_folder).exists():

            messagebox.showerror(
                "Invalid Input Folder",
                "The selected Input Folder does not exist."
            )

            return


        # ------------------------------------
        # Validate Output
        # ------------------------------------

        if not output_folder:

            messagebox.showwarning(
                "Output Folder Required",
                "Please select an Output Folder."
            )

            return


        # ------------------------------------
        # Create Output Folder
        # ------------------------------------

        try:

            Path(output_folder).mkdir(
                parents=True,
                exist_ok=True
            )

        except Exception as e:

            messagebox.showerror(
                "Output Folder Error",
                str(e)
            )

            return


        # ------------------------------------
        # Reset UI
        # ------------------------------------

        self.progress_bar.set(0)

        self.progress_text.configure(
            text="0%"
        )

        self.status_label.configure(
            text="Preparing..."
        )

        self.stats_label.configure(
            text="Total: 0    Success: 0    Failed: 0"
        )


        # ------------------------------------
        # Change Processing State
        # ------------------------------------

        self.processing = True


        self.start_button.configure(
            state="disabled",
            text="PROCESSING..."
        )


        self.stop_button.configure(
            state="normal"
        )


        self.input_button.configure(
            state="disabled"
        )


        self.output_button.configure(
            state="disabled"
        )


        self.white_checkbox.configure(
            state="disabled"
        )


        # ------------------------------------
        # Start Worker Thread
        # ------------------------------------

        worker_thread = threading.Thread(
            target=self.process_images,
            args=(
                input_folder,
                output_folder,
                self.white_background.get()
            ),
            daemon=True
        )

        worker_thread.start()


    # ========================================
    # PROCESS IMAGES
    # ========================================

    def process_images(
        self,
        input_folder,
        output_folder,
        white_background
    ):

        try:

            self.update_status(
                "Scanning images..."
            )


            # --------------------------------
            # Process Folder
            # --------------------------------

            self.stop_requested = False
            success, result = (
                self.remover.process_folder(
                    input_folder=input_folder,
                    output_folder=output_folder,
                    white_background=white_background,
                    callback=self.update_progress
                )
            )


            # --------------------------------
            # Handle Result
            # --------------------------------

            if success:

                total = result.get(
                    "total",
                    0
                )

                successful = result.get(
                    "success",
                    0
                )

                failed = result.get(
                    "failed",
                    0
                )


                def completed():

                    self.progress_bar.set(
                        1
                    )

                    self.progress_text.configure(
                        text="100%"
                    )

                    self.status_label.configure(
                        text="Processing Completed"
                    )

                    self.stats_label.configure(
                        text=(
                            f"Total: {total}    "
                            f"Success: {successful}    "
                            f"Failed: {failed}"
                        )
                    )


                    self.processing_finished()


                    messagebox.showinfo(
                        "Processing Complete",
                        (
                            "Bulk processing completed.\n\n"
                            f"Total Images : {total}\n"
                            f"Success      : {successful}\n"
                            f"Failed       : {failed}"
                        )
                    )


                self.after(
                    0,
                    completed
                )


            else:

                error_message = str(
                    result
                )


                def failed_process():

                    self.status_label.configure(
                        text="Processing Failed"
                    )

                    self.processing_finished()


                    messagebox.showerror(
                        "Processing Error",
                        error_message
                    )


                self.after(
                    0,
                    failed_process
                )


        except Exception as e:

            error_message = str(e)


            def unexpected_error():

                self.status_label.configure(
                    text="Unexpected Error"
                )

                self.processing_finished()


                messagebox.showerror(
                    "Unexpected Error",
                    error_message
                )


            self.after(
                0,
                unexpected_error
            )


# ============================================
# PART 2 END
# ============================================# ============================================
# RK Choice Studio AI
# app.py - Part 3
# ============================================


    # ========================================
    # STOP PROCESSING
    # ========================================

    def stop_processing(self):

        if not self.processing:
            return

        answer = messagebox.askyesno(
            "Stop Processing",
            (
                "Are you sure you want to stop "
                "the current processing?"
            )
        )

        if not answer:
            return

        # ------------------------------------
        # Stop request
        # ------------------------------------

        self.stop_requested = True

        self.status_label.configure(
            text="Stopping..."
        )

        self.stop_button.configure(
            state="disabled",
            text="STOPPING..."
        )


    # ========================================
    # PROCESSING FINISHED
    # ========================================

    def processing_finished(self):

        self.processing = False

        self.stop_requested = False

        self.start_button.configure(
            state="normal",
            text="START PROCESSING"
        )

        self.stop_button.configure(
            state="disabled",
            text="STOP"
        )

        self.input_button.configure(
            state="normal"
        )

        self.output_button.configure(
            state="normal"
        )

        self.white_checkbox.configure(
            state="normal"
        )


    # ========================================
    # WINDOW CLOSE
    # ========================================

    def on_close(self):

        if self.processing:

            answer = messagebox.askyesno(
                "Processing in Progress",
                (
                    "Processing is currently running.\n\n"
                    "Do you really want to close "
                    "the application?"
                )
            )

            if not answer:
                return

            self.stop_requested = True

        self.destroy()


# ============================================
# APPLICATION START
# ============================================

def main():

    app = RKChoiceStudioAI()

    app.stop_requested = False

    app.protocol(
        "WM_DELETE_WINDOW",
        app.on_close
    )

    app.mainloop()


# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":

    main()