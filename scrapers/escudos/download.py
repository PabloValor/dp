import requests
import os.path
from PIL import Image
from StringIO import StringIO

base_url = "http://canchallena.lanacion.com.ar/_ui/desktop/imgs/escudos/{0}.png"

for escudo_id in range(0,2000):
    for tipo in range(1, 3):
        escudo_nombre = '{0}_{1}'.format(escudo_id, tipo)
        image_file = escudo_nombre + '.png'

        if not os.path.isfile(image_file):
          url = base_url.format(escudo_nombre)
          print(url)
          response = requests.get(url)
          if response.status_code == 200:
            print("Guardando")
            i = Image.open(StringIO(response.content))
            i.save(image_file)
            print(escudo_nombre)
