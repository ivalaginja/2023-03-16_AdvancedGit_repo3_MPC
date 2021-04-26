import matplotlib.pyplot as plt
import numpy as np


def circle_mask(im, xc, yc, rcirc):
    """Create a circular aperture centered on (xc, yc) with radius rcirc."""
    x, y = np.shape(im)
    newy, newx = np.mgrid[:y,:x]
    circ = (newx-xc)**2 + (newy-yc)**2 < rcirc**2
    return circ.astype('float')


def ft2d(func):
    ft = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(func)))
    return ft


def padcplx(c, pad=5):
    """Puts a Complex array in the centre of a zero-filled Complex array.
    pad defines the padding multiplier for the output array."""
    (nx, ny) = c.shape
    bignx = nx * pad + 1
    bigny = ny * pad + 1
    big_c = np.zeros((bignx, bigny), dtype=complex)

    dx = int((nx * (pad - 1)) / 2 + 1)
    dy = int((ny * (pad - 1)) / 2 + 1)

    big_c[dx:dx + nx, dy:dy + ny] = c
    return big_c


def zoom(im, x, y, bb):
    """Cut out a square box from image im centered on (x,y) with half-box size bb."""
    return im[y-bb:y+bb, x-bb:x+bb]


if __name__ == '__main__':

    npix = 512

    lin = np.linspace(-0.5, 0.5, npix)
    xx, yy = np.meshgrid(lin, lin)

    pad = 5  # factor by how much do we pad our images before performing a FT
    npix_pad = npix * pad + 1  # figure out the padded big array sizes after the FT

    # Create a circular aperture
    rad = 0.7 * npix / 2  # radius in pixels of the circular aperture
    circ_ap = circle_mask(xx, int(npix / 2), int(npix / 2), rad)

    # Calculate the Fourier transform, after padding
    circ_ft = ft2d(padcplx(circ_ap))

    # Plot
    zoomfac = 30  # half-size of the zoom box will be 1/zoomfac of total image
    box = int(npix_pad / zoomfac)

    # This is a smaller data array with only our region of interest.
    circ_ft_zoom = zoom(circ_ft, int(npix_pad / 2), int(npix_pad / 2), box)

    # Plot
    fig = plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(circ_ap, cmap='Greys_r', origin='lower')
    plt.colorbar()
    plt.title('Pupil plane')

    plt.subplot(1, 2, 2)
    plt.imshow(np.real(circ_ft_zoom), cmap='inferno', origin='lower')
    plt.colorbar()
    plt.title('Focal plane')

    plt.savefig('fourier_transform_result.pdf')
