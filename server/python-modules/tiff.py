import bioformats
import javabridge
import matplotlib.pyplot as plt
import os
#use python 3.86
# pip install numpy
# pip install python-bioformats
# pip install javabridge
# pip install matplotlib

def initialize_jvm():
    javabridge.start_vm(class_path=bioformats.JARS)




if __name__ == "__main__":
    initialize_jvm()
    # Path to your TIFF file
    tiff_path = 'combined_a.tiff'
    image = bioformats.load_image(tiff_path)  
    

    # omexml = bioformats.get_omexml_metadata(tiff_path)  
    # md = bioformats.OMEXML(omexml)
    # pixels = md.image().Pixels
    # num_channels = pixels.SizeC


    # channel_count = pixels.SizeZ 
    # print(dir(md))
    print(image)
