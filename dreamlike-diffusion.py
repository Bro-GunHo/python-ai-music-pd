from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "dreamlike-art/dreamlike-diffusion-1.0",
    torch_dtype=torch.float32
)

# mac os 
pipe = pipe.to("cpu")

prompt = "An astronaut riding a green horse"

image = pipe(prompt).images[0]

image.save("./images/astronaut.png")