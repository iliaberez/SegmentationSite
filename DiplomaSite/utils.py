import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(img):
    plt.switch_backend('AGG')
    plt.figure(figsize=(4,4))
    plt.imshow(img[:,:].T, cmap = 'gray')
    plt.tight_layout()
    chart = get_graph()
    return chart

def get_chart_pred(input):
    img = np.argmax(input, axis=3)[0,:,:]
    img = np.flip(img)
    plt.switch_backend('AGG')
    plt.figure(figsize=(4,4))
    plt.imshow(img, cmap = 'jet')
    plt.tight_layout()
    chart = get_graph()
    return chart