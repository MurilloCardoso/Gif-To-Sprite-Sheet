import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Função para aplicar o efeito pixelado na imagem
def pixelate_image(img, pixel_size=10):
    # Redimensiona a imagem para aplicar o efeito pixelado
    img_small = img.resize(
        (img.width // pixel_size, img.height // pixel_size), 
        resample=Image.NEAREST
    )
    
    # Redimensiona novamente para o tamanho original
    img_pixelated = img_small.resize(img.size, Image.NEAREST)
    
    return img_pixelated

# Função para exibir a imagem com a pixelização ajustada em tempo real
def update_image_display():
    pixel_size = pixel_size_var.get()
    if original_img:
        img_pixelated = pixelate_image(original_img, pixel_size)
        
        # Redimensionar a imagem para se ajustar à interface
        img_resized = img_pixelated.resize((img_pixelated.width // 3, img_pixelated.height // 3), Image.Resampling.LANCZOS)
        img_display = ImageTk.PhotoImage(img_resized)

        image_label.config(image=img_display)
        image_label.image = img_display


# Função para abrir a janela de seleção de arquivo para a imagem
def import_image():
    global original_img
    file_path = filedialog.askopenfilename(
        title="Selecione a imagem", 
        filetypes=[("Todos os arquivos de imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp;*.ico")]
    )
    
    if file_path:
        original_img = Image.open(file_path)
        update_image_display()

# Função para salvar a imagem pixelada
def save_image():
    if original_img:
        output_image_path = filedialog.asksaveasfilename(
            title="Salvar imagem pixelada", 
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("Todos os arquivos", "*.*")]
        )
        
        if output_image_path:
            pixel_size = pixel_size_var.get()
            img_pixelated = pixelate_image(original_img, pixel_size)
            img_pixelated.save(output_image_path)
            messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhuma imagem foi carregada.")

# Função para criar a interface gráfica
def create_gui():
    global image_label, pixel_size_var, original_img

    # Variável global para armazenar a imagem original
    original_img = None
    
    # Cria a janela principal
    root = tk.Tk()
    root.title("Pixelização de Imagem")

    # Cria o frame principal
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Cria o painel para o menu
    menu_panel = tk.Frame(main_frame)
    menu_panel.grid(row=1, column=0, sticky="nsew")

    # Botão para importar a imagem
    import_button = tk.Button(menu_panel, text="Importar Imagem", command=import_image)
    import_button.grid(row=0, column=0, pady=10)

    # Label para exibir a imagem
    image_label = tk.Label(menu_panel)
    image_label.grid(row=1, column=0, pady=10)

    # Texto de instrução
    label = tk.Label(menu_panel, text="Ajuste o tamanho do pixel:")
    label.grid(row=2, column=0, pady=5)

    # Variável para controlar o valor do slider (tamanho do pixel)
    pixel_size_var = tk.IntVar(value=10)

    # Slider para ajustar o tamanho do pixel
    slider = tk.Scale(menu_panel, from_=1, to_=50, orient=tk.HORIZONTAL, label="Tamanho do Pixel", variable=pixel_size_var)
    slider.grid(row=3, column=0)

    # Função para chamar a atualização da imagem ao clicar
    update_button = tk.Button(menu_panel, text="Atualizar Imagem", command=update_image_display)
    update_button.grid(row=4, column=0, pady=10)

    # Botão para salvar a imagem pixelada
    save_button = tk.Button(menu_panel, text="Salvar Imagem", command=save_image)
    save_button.grid(row=5, column=0, pady=10)

    # Ajuste para responsividade
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    menu_panel.grid_rowconfigure(0, weight=1)
    menu_panel.grid_columnconfigure(0, weight=1)

    # Inicia o loop da interface gráfica
    root.mainloop()

# Chama a função para criar a interface gráfica
create_gui()
