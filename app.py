import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube

class GUI():
    def __init__(self):
        ''' Ana pencere '''
        self.window = Tk()
        self.window.title('YouTube Downloader')
        self.window.geometry('700x250')

        ''' Video bağlantısı giriş satırı '''
        self.url_label = Label(self.window, text='Video bağlantısı (Ctrl+V): ', font=(None, 12))
        self.url_label.place(x=40, y=20)
        self.url_entry = Entry(self.window, width=50)
        self.url_entry.place(x=210, y=21)

        ''' İndirme yolu satırı '''
        self.path_label = Label(self.window, text='Kaydetmek istediğiniz yer: ', font=(None, 12))
        self.path_label.place(x=40, y=50)
        self.path_entry = Entry(self.window, width=50)
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))  # Varsayılan yolu ayarla
        self.path_entry.configure(state="readonly")  # Girişi salt okunur yap
        self.path_entry.place(x=240, y=51)
        
        self.path_button = Button(self.window, text='Gözat', command=self.select_folder)
        self.path_button.place(x=520, y=50)

        ''' İndirme tipi seçenek kutusu '''
        self.download_type_label = Label(self.window, text='İndirme Türü: ', font=(None, 12))
        self.download_type_label.place(x=40, y=80)
        self.download_type = ttk.Combobox(self.window, values=['Video', 'Ses (MP3)'])
        self.download_type.place(x=210, y=81)
        self.download_type.set('Ses (MP3)')

        ''' İndirme düğmesi '''
        self.down_button = Button(self.window, text='İndir', command=self.pressed)
        self.down_button.place(x=40, y=120)

        ''' Yapıştır düğmesi '''
        self.paste_button = Button(self.window, text='Yapıştır', command=self.paste_text)
        self.paste_button.place(x=520, y=20)

        self.progress = ttk.Progressbar(self.window, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress.place(x=40, y=150)

        self.window.mainloop()

    def download(self, link, path, download_type):
        try:
            yt = YouTube(link)
            self.title = yt.title

            if download_type == 'Video':
                stream = yt.streams.get_highest_resolution()
                os.makedirs(path, exist_ok=True)
                video_filename = f'{self.title}.mp4'
                video_path = os.path.join(path, video_filename)
                stream.download(output_path=path, filename=video_filename)
                return True, video_path
            elif download_type == 'Ses (MP3)':
                stream = yt.streams.filter(only_audio=True).first()
                os.makedirs(path, exist_ok=True)
                artist = yt.author
                mp3_filename = f'{artist} - {self.title}.mp3'
                mp3_path = os.path.join(path, mp3_filename)
                stream.download(output_path=path, filename=mp3_filename)
                return True, mp3_path
        except Exception as e:
            return False, str(e)

    def update_progress(self, stream, chunk, file_handle, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        percent = (bytes_downloaded / file_size) * 100
        self.progress["value"] = percent
        self.window.update_idletasks()

    def pressed(self):
        self.progress["value"] = 0
        self.progress.start()

        def callback():
            self.url = self.url_entry.get()
            self.dir = self.path_entry.get()
            self.download_type_val = self.download_type.get()

            if self.url and (self.url.startswith('http') or self.url.startswith('www')):
                try:
                    self.down_button['state'] = 'disabled'
                    yt = YouTube(self.url, on_progress_callback=self.update_progress)
                    self.title = yt.title
                    success, message = self.download(self.url, self.dir, self.download_type_val)
                    self.progress.stop()
                    if success:
                        messagebox.showinfo(title='Başarılı', message=f'İndirme tamamlandı! Şurada kaydedildi: {message}')
                    else:
                        messagebox.showerror(title='Hata', message=message)
                    self.down_button['state'] = 'normal'
                except Exception as e:
                    self.progress.stop()
                    messagebox.showerror(title='Hata', message=str(e))
            else:
                self.progress.stop()
                messagebox.showerror(title='Hata', message='Geçersiz URL')

        self.t = threading.Thread(target=callback)
        self.t.start()

    def paste_text(self):
        clipboard_text = self.window.clipboard_get()
        self.url_entry.delete(0, 'end')
        self.url_entry.insert(0, clipboard_text)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder_path)
            self.path_entry.configure(state="readonly")

if __name__ == '__main__':
    GUI()
