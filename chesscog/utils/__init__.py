import numpy as np
import torch

_device = "cuda" if torch.cuda.is_available() else "cpu"


def device(x: torch.Tensor, device: str = _device) -> torch.Tensor:
    return x.to(device)


def sort_corner_points(points: np.ndarray) -> np.ndarray:
    """Permute the board corner coordinates to the order [top left, top right, bottom right, bottom left].

    Args:
        points (np.ndarray): the four corner coordinates

    Returns:
        np.ndarray: the permuted array
    """

    # First, order by y-coordinate
    points = points[points[:, 1].argsort()]
    # Sort top x-coordinates
    points[:2] = points[:2][points[:2, 0].argsort()]
    # Sort bottom x-coordinates (reversed)
    points[2:] = points[2:][points[2:, 0].argsort()[::-1]]

    return points
