import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os

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

# Função para selecionar o GIF, o diretório de saída e o tamanho dos sprites
def select_files_for_sprite_sheet():
    # Selecionar GIF
    gif_path = filedialog.askopenfilename(title="Selecione o GIF", filetypes=[("GIF Files", "*.gif")])
    if not gif_path:
        return

    # Selecionar diretório de saída
    output_folder = filedialog.askdirectory(title="Selecione o diretório de saída")
    if not output_folder:
        return

    # Perguntar pela largura e altura desejada do sprite
    width = simpledialog.askinteger("Largura do Sprite", "Escolha a largura do sprite:")
    height = simpledialog.askinteger("Altura do Sprite", "Escolha a altura do sprite:")
    
    if not width or not height:
        print("Largura ou altura inválida.")
        return

    # Criar uma nova pasta para o projeto
    gif_name = os.path.splitext(os.path.basename(gif_path))[0]  # Nome do GIF sem extensão
    project_folder = os.path.join(output_folder, gif_name)  # Caminho da nova pasta do projeto
    os.makedirs(project_folder, exist_ok=True)  # Cria a pasta do projeto

    # Criar a pasta para os frames
    sprites_folder = os.path.join(project_folder, "sprites")  # Pasta para os sprites
    os.makedirs(sprites_folder, exist_ok=True)  # Cria a pasta "sprites"

    sprite_sheet_path = os.path.join(project_folder, f"{gif_name}_sprite_sheet.png")  # Caminho do sprite sheet
    
    # Extrair frames do GIF
    extract_frames(gif_path, sprites_folder, width, height)
    
    # Criar o sprite sheet
    create_sprite_sheet(sprites_folder, sprite_sheet_path, width, height)
    
    messagebox.showinfo("Sucesso", f"Sprite sheet salvo em: {sprite_sheet_path}")

# Função para extrair frames e redimensionar
def extract_frames(gif_path, output_folder, width, height):
    with Image.open(gif_path) as gif:
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.copy().resize((width, height), Image.NEAREST)
            frame_path = os.path.join(output_folder, f"frame_{frame}.png")
            frame_image.save(frame_path, "PNG")

# Função para criar o sprite sheet
def create_sprite_sheet(frames_folder, sprite_sheet_path, frame_width, frame_height):
    frames = [Image.open(os.path.join(frames_folder, f)) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]
    num_frames = len(frames)
    sprite_sheet = Image.new("RGBA", (frame_width * num_frames, frame_height))
    
    for i, frame in enumerate(frames):
        sprite_sheet.paste(frame, (i * frame_width, 0))
    
    sprite_sheet.save(sprite_sheet_path)

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
    import_button.grid(row=0, column=0, padx=10, pady=10)  # Colocado na coluna 0

    # Botão para criar sprite de gif
    create_button = tk.Button(menu_panel, text="Criar Sprite Sheet Por GIF", command=select_files_for_sprite_sheet)
    create_button.grid(row=0, column=1, padx=10, pady=10)  # Colocado na coluna 1

    # Label para exibir a imagem
    image_label = tk.Label(menu_panel)
    image_label.grid(row=1, column=0, columnspan=2, pady=10)  # Fazendo a label ocupar as duas colunas

    # Texto de instrução
    label = tk.Label(menu_panel, text="Ajuste o tamanho do pixel:")
    label.grid(row=2, column=0, columnspan=2, pady=5)  # Ajustado para ocupar as duas colunas

    # Variável para controlar o valor do slider (tamanho do pixel)
    pixel_size_var = tk.IntVar(value=10)

    # Slider para ajustar o tamanho do pixel
    slider = tk.Scale(menu_panel, from_=1, to_=50, orient=tk.HORIZONTAL, label="Tamanho do Pixel", variable=pixel_size_var)
    slider.grid(row=3, column=0, columnspan=2)

    # Função para chamar a atualização da imagem ao clicar
    update_button = tk.Button(menu_panel, text="Atualizar Imagem", command=update_image_display)
    update_button.grid(row=4, column=0, columnspan=2, pady=10)  # Ajuste para ocupar as duas colunas

    # Botão para salvar a imagem pixelada
    save_button = tk.Button(menu_panel, text="Salvar Imagem", command=save_image)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)  # Ajuste para ocupar as duas colunas

    # Ajuste para responsividade
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    menu_panel.grid_rowconfigure(0, weight=1)
    menu_panel.grid_columnconfigure(0, weight=1)

    # Inicia o loop da interface gráfica
    root.mainloop()

# Chama a função para criar a interface
create_gui()