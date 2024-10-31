from tkinter import Tk, filedialog
from PIL import Image
import os

# Função para selecionar o GIF e o diretório de saída
def select_files():
    # Selecionar GIF
    gif_path = filedialog.askopenfilename(title="Selecione o GIF", filetypes=[("GIF Files", "*.gif")])
    if not gif_path:
        return

    # Selecionar diretório de saída
    output_folder = filedialog.askdirectory(title="Selecione o diretório de saída")
    if not output_folder:
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
    extract_frames(gif_path, sprites_folder)
    
    # Criar o sprite sheet
    frame_width, frame_height = get_frame_size(gif_path)
    create_sprite_sheet(sprites_folder, sprite_sheet_path, frame_width, frame_height)
    
    print(f"Sprite sheet salvo em: {sprite_sheet_path}")

# Função para extrair frames
def extract_frames(gif_path, output_folder):
    with Image.open(gif_path) as gif:
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_path = os.path.join(output_folder, f"frame_{frame}.png")
            gif.save(frame_path, "PNG")

# Função para obter o tamanho dos frames
def get_frame_size(gif_path):
    with Image.open(gif_path) as gif:
        gif.seek(0)
        return gif.width, gif.height

# Função para criar o sprite sheet
def create_sprite_sheet(frames_folder, sprite_sheet_path, frame_width, frame_height):
    frames = [Image.open(os.path.join(frames_folder, f)) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]
    num_frames = len(frames)
    sprite_sheet = Image.new("RGBA", (frame_width * num_frames, frame_height))
    
    for i, frame in enumerate(frames):
        sprite_sheet.paste(frame, (i * frame_width, 0))
    
    sprite_sheet.save(sprite_sheet_path)

# Configuração da interface Tkinter
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    select_files()
