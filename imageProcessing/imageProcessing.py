from skimage import io, filters
from skimage.color import rgb2gray
from skimage import img_as_float


def filtre_rouge_then_grey_then_otsu(img_orig):
    red_image = img_as_float(img_orig.copy())  # Make a copy
    # On extrait le canal rouge
    red_image[:, :, 1] = 0
    red_image[:, :, 2] = 0
    # On transforme en niveaux de gris
    im_grey = img_as_float(rgb2gray(red_image))
    # On trouve la valeur après filtrage de otsu
    val_rouge = filters.threshold_otsu(im_grey)
    image_2_rouge = im_grey.copy()
    mask_1_rouge = image_2_rouge > val_rouge
    mask_2_rouge = image_2_rouge < val_rouge
    # On met à blanc les pixels respectant le mask
    image_2_rouge[mask_1_rouge] = 255
    # On met à noir les pixels respectant le mask
    image_2_rouge[mask_2_rouge] = 0
    return image_2_rouge / 255


def filtre_bleu_then_grey_then_otsu(img_orig):
    blue_image = img_orig.copy()  # Make a copy
    blue_image[:, :, 0] = 0
    blue_image[:, :, 1] = 0
    im_grey = rgb2gray(blue_image)
    # On trouve la valeur après filtrage de otsu
    val_bleu = filters.threshold_otsu(im_grey)
    image_2_bleu = im_grey.copy()
    mask_1_bleu = image_2_bleu > val_bleu
    mask_2_bleu = image_2_bleu < val_bleu
    # On met à blanc les pixels respectant le mask
    image_2_bleu[mask_1_bleu] = 255
    # On met à noir les pixels respectant le mask
    image_2_bleu[mask_2_bleu] = 0
    return image_2_bleu / 255


def filtre_vert_then_grey_then_otsu(img_orig):
    green_image = img_orig.copy()  # Make a copy
    green_image[:, :, 0] = 0
    green_image[:, :, 2] = 0
    im_grey = rgb2gray(green_image)
    # On trouve la valeur après filtrage de otsu
    val_vert = filters.threshold_otsu(im_grey)
    image_2_vert = im_grey.copy()
    mask_1_vert = image_2_vert > val_vert
    mask_2_vert = image_2_vert < val_vert
    # On met à blanc les pixels respectant le mask
    image_2_vert[mask_1_vert] = 255
    # On met à noir les pixels respectant le mask
    image_2_vert[mask_2_vert] = 0
    return image_2_vert / 255


import matplotlib.pyplot as plt
from skimage.exposure import histogram


def plot_histo(image, title):
    hist = histogram(image)
    plt.plot(hist[1], hist[0])
    plt.title(title)
    plt.show()
    return


#Changer le chemin pour les images : dépend du pc
image_org = io.imread("../../image_palets_3.jpg")
image_vert = filtre_vert_then_grey_then_otsu(image_org)

image_bleu = filtre_bleu_then_grey_then_otsu(image_org)

image_rouge = filtre_rouge_then_grey_then_otsu(image_org)

io.imshow(image_bleu)

# Le vert donne le rouge
# Le rouge donne le bleu en foncé
# Le bleu donne le bleu en clair
