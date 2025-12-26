import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageSequence
import io

class ButtonMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("88x31 Button Maker")
        self.root.geometry("800x650")
        self.root.configure(bg='#c0c0c0')
        
        # Variables
        self.bg_image = None
        self.bg_frames = []
        self.is_gif = False
        self.bg_color = '#0066cc'
        self.text = tk.StringVar(value='YOUR BUTTON')
        self.text_color = '#ffffff'
        self.font_size = tk.IntVar(value=10)
        self.font_family = tk.StringVar(value='Arial')
        self.text_x = tk.IntVar(value=44)
        self.text_y = tk.IntVar(value=16)
        self.border_color = '#000000'
        self.border_thickness = tk.IntVar(value=1)
        self.show_border = tk.BooleanVar(value=True)
        self.preview_image = None
        self.current_frame = 0
        
        self.setup_ui()
        self.update_preview()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#c0c0c0', relief='groove', bd=2)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#000080', relief='raised', bd=2)
        title_frame.pack(fill='x', padx=2, pady=2)
        tk.Label(title_frame, text='88x31 Button Maker', bg='#000080', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Content frame
        content = tk.Frame(main_frame, bg='#c0c0c0')
        content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Controls
        left_panel = tk.Frame(content, bg='#c0c0c0')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Background Image
        self.create_group(left_panel, "Background Image", [
            ('button', 'Choose Image/GIF', self.load_image),
            ('button', 'Remove Image', self.remove_image),
        ])
        
        # Background Color
        bg_frame = self.create_group(left_panel, "Background Color", [])
        tk.Button(bg_frame, text='Pick Color', command=self.pick_bg_color, 
                 relief='raised', bd=2, bg='#e0e0e0').pack(pady=2)
        self.bg_color_label = tk.Label(bg_frame, text=self.bg_color, bg=self.bg_color, 
                                       relief='sunken', bd=2, width=15)
        self.bg_color_label.pack(pady=2)
        
        # Text
        text_frame = self.create_group(left_panel, "Text", [])
        tk.Entry(text_frame, textvariable=self.text, relief='sunken', bd=2).pack(fill='x', pady=2)
        
        tk.Label(text_frame, text='Font:', bg='#c0c0c0').pack(anchor='w')
        fonts = ['Arial', 'Times New Roman', 'Courier New', 'Verdana', 'Georgia', 
                'Comic Sans MS', 'Impact', 'Trebuchet MS']
        ttk.Combobox(text_frame, textvariable=self.font_family, values=fonts, 
                    state='readonly').pack(fill='x', pady=2)
        
        tk.Label(text_frame, text='Size:', bg='#c0c0c0').pack(anchor='w')
        tk.Scale(text_frame, from_=6, to=20, variable=self.font_size, orient='horizontal',
                command=lambda x: self.update_preview(), bg='#c0c0c0').pack(fill='x')
        
        tk.Label(text_frame, text='Color:', bg='#c0c0c0').pack(anchor='w')
        tk.Button(text_frame, text='Pick Color', command=self.pick_text_color,
                 relief='raised', bd=2, bg='#e0e0e0').pack(pady=2)
        self.text_color_label = tk.Label(text_frame, text=self.text_color, bg=self.text_color,
                                        relief='sunken', bd=2, width=15)
        self.text_color_label.pack(pady=2)
        
        # Position
        pos_frame = self.create_group(left_panel, "Text Position", [])
        tk.Label(pos_frame, text='X Position:', bg='#c0c0c0').pack(anchor='w')
        tk.Scale(pos_frame, from_=0, to=88, variable=self.text_x, orient='horizontal',
                command=lambda x: self.update_preview(), bg='#c0c0c0').pack(fill='x')
        
        tk.Label(pos_frame, text='Y Position:', bg='#c0c0c0').pack(anchor='w')
        tk.Scale(pos_frame, from_=0, to=31, variable=self.text_y, orient='horizontal',
                command=lambda x: self.update_preview(), bg='#c0c0c0').pack(fill='x')
        
        # Border
        border_frame = self.create_group(left_panel, "Border", [])
        tk.Checkbutton(border_frame, text='Show Border', variable=self.show_border,
                      command=self.update_preview, bg='#c0c0c0').pack(anchor='w')
        
        tk.Label(border_frame, text='Color:', bg='#c0c0c0').pack(anchor='w')
        tk.Button(border_frame, text='Pick Color', command=self.pick_border_color,
                 relief='raised', bd=2, bg='#e0e0e0').pack(pady=2)
        self.border_color_label = tk.Label(border_frame, text=self.border_color, 
                                          bg=self.border_color, relief='sunken', bd=2, width=15)
        self.border_color_label.pack(pady=2)
        
        tk.Label(border_frame, text='Thickness:', bg='#c0c0c0').pack(anchor='w')
        tk.Scale(border_frame, from_=0, to=5, variable=self.border_thickness, orient='horizontal',
                command=lambda x: self.update_preview(), bg='#c0c0c0').pack(fill='x')
        
        # Download

        # Right panel - Preview
        right_panel = tk.Frame(content, bg='#c0c0c0')
        right_panel.pack(side='right', fill='both')
        
        # Actual size preview
        actual_frame = tk.LabelFrame(right_panel, text='Preview (Actual Size)', 
                                     bg='#c0c0c0', relief='groove', bd=2)
        actual_frame.pack(pady=5)
        preview_container = tk.Frame(actual_frame, bg='#808080', relief='sunken', bd=2)
        preview_container.pack(padx=5, pady=5)
        self.preview_label = tk.Label(preview_container, bg='#808080')
        self.preview_label.pack()
        
        # Large preview
        large_frame = tk.LabelFrame(right_panel, text='Large Preview (4x)', 
                                    bg='#c0c0c0', relief='groove', bd=2)
        large_frame.pack(pady=5)
        large_container = tk.Frame(large_frame, bg='#808080', relief='sunken', bd=2)
        large_container.pack(padx=5, pady=5)
        self.large_preview_label = tk.Label(large_container, bg='#808080')
        self.large_preview_label.pack()
# Download section (RIGHT PANEL - under preview)
        download_frame = tk.LabelFrame(
            right_panel,
            text='Download',
            bg='#c0c0c0',
            relief='groove',
            bd=2
        )
        download_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(
            download_frame,
            text='Save as PNG',
            command=lambda: self.download('png'),
            bg='#90ee90',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        ).pack(fill='x', pady=3)

        tk.Button(
            download_frame,
            text='Save as JPG',
            command=lambda: self.download('jpg'),
            bg='#90ee90',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        ).pack(fill='x', pady=3)

        tk.Button(
            download_frame,
            text='Save as GIF',
            command=lambda: self.download('gif'),
            bg='#90ee90',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        ).pack(fill='x', pady=3)
                
        
        # Bind text changes
        self.text.trace('w', lambda *args: self.update_preview())
        self.font_family.trace('w', lambda *args: self.update_preview())
        
    def create_group(self, parent, title, items):
        frame = tk.LabelFrame(parent, text=title, bg='#c0c0c0', relief='groove', bd=2)
        frame.pack(fill='x', pady=5)
        
        for item_type, *params in items:
            if item_type == 'button':
                tk.Button(frame, text=params[0], command=params[1], 
                         relief='raised', bd=2, bg='#e0e0e0').pack(fill='x', padx=5, pady=2)
        
        return frame
    
    def load_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            try:
                img = Image.open(filename)
                self.is_gif = filename.lower().endswith('.gif')
                
                if self.is_gif:
                    # Extract all frames
                    self.bg_frames = []
                    try:
                        for frame in ImageSequence.Iterator(img):
                            frame_copy = frame.copy().convert('RGBA')
                            frame_copy = frame_copy.resize((88, 31), Image.Resampling.LANCZOS)
                            self.bg_frames.append(frame_copy)
                    except Exception:
                        # If frame extraction fails, use single frame
                        self.bg_frames = [img.convert('RGBA').resize((88, 31), Image.Resampling.LANCZOS)]
                else:
                    self.bg_image = img.convert('RGBA').resize((88, 31), Image.Resampling.LANCZOS)
                    self.bg_frames = []
                
                self.update_preview()
                if self.is_gif:
                    self.animate_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def remove_image(self):
        self.bg_image = None
        self.bg_frames = []
        self.is_gif = False
        self.current_frame = 0
        self.update_preview()
    
    def pick_bg_color(self):
        color = colorchooser.askcolor(self.bg_color)
        if color[1]:
            self.bg_color = color[1]
            self.bg_color_label.config(bg=self.bg_color, text=self.bg_color)
            self.update_preview()
    
    def pick_text_color(self):
        color = colorchooser.askcolor(self.text_color)
        if color[1]:
            self.text_color = color[1]
            self.text_color_label.config(bg=self.text_color, text=self.text_color)
            self.update_preview()
    
    def pick_border_color(self):
        color = colorchooser.askcolor(self.border_color)
        if color[1]:
            self.border_color = color[1]
            self.border_color_label.config(bg=self.border_color, text=self.border_color)
            self.update_preview()
    
    def create_button_image(self, scale=1):
        w, h = 88 * scale, 31 * scale
        
        # Create base image
        if self.is_gif and self.bg_frames:
            img = self.bg_frames[self.current_frame].copy().resize((w, h), Image.Resampling.NEAREST)
        elif self.bg_image:
            img = self.bg_image.copy().resize((w, h), Image.Resampling.LANCZOS)
        else:
            img = Image.new('RGBA', (w, h), self.bg_color)
        
        draw = ImageDraw.Draw(img)
        
        # Draw border
        if self.show_border.get() and self.border_thickness.get() > 0:
            thickness = self.border_thickness.get() * scale
            for i in range(int(thickness)):
                draw.rectangle([i, i, w-1-i, h-1-i], outline=self.border_color)
        
        # Draw text
        if self.text.get():
            try:
                font = ImageFont.truetype(f"{self.font_family.get()}.ttf", self.font_size.get() * scale)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", self.font_size.get() * scale)
                except:
                    font = ImageFont.load_default()
            
            # Text shadow
            shadow_offset = 1 * scale
            draw.text((self.text_x.get() * scale + shadow_offset, self.text_y.get() * scale + shadow_offset), 
                     self.text.get(), fill='#000000', font=font, anchor='mm')
            # Main text
            draw.text((self.text_x.get() * scale, self.text_y.get() * scale), 
                     self.text.get(), fill=self.text_color, font=font, anchor='mm')
        
        return img
    
    def update_preview(self):
        # Actual size
        img = self.create_button_image(1)
        photo = ImageTk.PhotoImage(img)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo
        
        # Large preview
        large_img = self.create_button_image(4)
        large_photo = ImageTk.PhotoImage(large_img)
        self.large_preview_label.config(image=large_photo)
        self.large_preview_label.image = large_photo
    
    def animate_preview(self):
        if self.is_gif and self.bg_frames:
            self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            self.update_preview()
            self.root.after(100, self.animate_preview)
    
    def download(self, format):
        filename = filedialog.asksaveasfilename(
            defaultextension=f'.{format}',
            filetypes=[(f'{format.upper()} files', f'*.{format}')]
        )
        
        if filename:
            try:
                if format == 'gif' and self.is_gif and self.bg_frames:
                    # Save as animated GIF
                    frames = []
                    for i in range(len(self.bg_frames)):
                        self.current_frame = i
                        frame = self.create_button_image(1)
                        frames.append(frame.convert('RGB').convert('P', palette=Image.ADAPTIVE))
                    
                    frames[0].save(filename, save_all=True, append_images=frames[1:], 
                                  duration=100, loop=0, optimize=False)
                else:
                    # Save as static image
                    img = self.create_button_image(1)
                    if format == 'jpg':
                        img = img.convert('RGB')
                    img.save(filename)
                
                messagebox.showinfo("Success", f"Button saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ButtonMaker(root)
    root.mainloop()