import random
from typing import Optional

import PIL
import click
from PIL import Image
from PIL.Image import Resampling


@click.group()
def main() -> None:
    """Create some colorful images."""
    pass


@main.command()
@click.option("--blocks", "-b", type=int, help="The block size.", default=40)
@click.option("--file-name", "-f", type=str, help="The resulting file name.", default="noise")
@click.option("--primary-chance", "-p", type=int,
              help="The chance of each block independently being the primary color.", default=20)
@click.option("--neighbor-chance", "-n", type=int, help="The chance of each block being the primary color when having "
                                                        "a neighbor of the primary color.", default=33)
@click.option("--open-result", "-o", type=bool, help="Open the result.", default=False)
@click.option("--primary", "-p", type=str, help="The primary color.")
@click.option("--secondary", "-s", type=str, help="The secondary color.")
@click.option("--resize", "-r", type=int, help="Resize the result.")
def noise(blocks: int, file_name: str, primary_chance: int, neighbor_chance: int, open_result: bool,
          primary: Optional[str],
          secondary: Optional[str], resize: Optional[int]):
    """Create a new noisy image."""

    # Generate random colors if colors are not provided.
    random.seed()
    if not primary:
        primary = generate_random_color()
    else:
        primary = hex_to_bytes(primary)
    if not secondary:
        secondary = generate_random_color()
    else:
        secondary = hex_to_bytes(secondary)

    image = PIL.Image.new(mode="RGB", size=(blocks, blocks), color=secondary)
    for x in range(blocks):
        for y in range(blocks):

            # Get the color of the neighboring pixels.
            neighbors = []
            if x > 0:
                left = image.getpixel((x - 1, y))
                neighbors.append(left)
            if x < blocks - 1:
                right = image.getpixel((x + 1, y))
                neighbors.append(right)
            if y > 0:
                down = image.getpixel((x, y - 1))
                neighbors.append(down)
            if y < blocks - 1:
                up = image.getpixel((x, y + 1))
                neighbors.append(up)

                # If any of the neighboring pixels are the primary color, evaluate it using the special neighbor chance.
                # The chance increases with how many neighbors contian the primary color.
                primary_neighbors = list((neighbor == primary for neighbor in neighbors))
                if any(primary_neighbors):
                    if random.randint(0, 100) < neighbor_chance * sum(primary_neighbors):
                        image.putpixel((x, y), primary)
                        continue

            # Otherwise, evaluate it with the normal primary chance.
            if random.randint(0, 100) < primary_chance:
                image.putpixel((x, y), primary)

    # If requests, resize the image using the Nearest Neighbor method.
    if resize:
        image = image.resize((resize, resize), Resampling.NEAREST)

    # Save the image.
    # If desired, show it immediately.
    image.save(f"{file_name}.png")
    if open_result:
        image.show()


def generate_random_color():
    """Generate a random color."""
    return tuple(random.choices(range(256), k=3))


def hex_to_bytes(hex_string: str) -> tuple:
    """
    Get the byte representation of a hex string.
    :param hex_string: The hex string.
    :return: A tuple containing the byte representation.
    """
    red, green, blue = bytes.fromhex(hex_string)
    return red, green, blue


if __name__ == "__main__":
    main()
