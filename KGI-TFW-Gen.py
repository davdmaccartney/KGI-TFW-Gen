# python gen_tfw.py <path_to_tiff_directory> [prj]

import osgeo.gdal as gdal
import osgeo.osr as osr
import os
import glob
import sys
import easygui
import fnmatch

dirphoto = easygui.diropenbox(msg=None, title="Selectionez le dossier des GTIFF ou ecrire les TFW", default=None )
list = fnmatch.filter(os.listdir(dirphoto), '*.tif')
total_con=len(list)
D1 = str(total_con)
msg = str(total_con) +" orthos voulez-vous continuer?"
title = "Merci de confirmer"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% ".format( "#"*block + "-"*(barLength-block), int(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


ci=0
cls()
for filename in os.listdir(dirphoto):
    if filename.endswith(".tif"):
        ci  += 1
        src = gdal.Open(dirphoto+'\\'+filename)
        xform = src.GetGeoTransform()

        src_srs = osr.SpatialReference()
        src_srs.ImportFromWkt(src.GetProjection())
        src_srs.MorphToESRI()
        src_wkt = src_srs.ExportToWkt()

        new_prj = os.path.splitext(filename)[0] + '.prj'
        prj = open(dirphoto+'\\'+new_prj, 'wt')
        prj.write(src_wkt)
        prj.close()

        src = None
        edit1=xform[0]+xform[1]/2
        edit2=xform[3]+xform[5]/2

        new_tfw = os.path.splitext(dirphoto+'\\'+filename)[0] + '.tfw'
        tfw = open(new_tfw, 'wt')
        tfw.write("%0.8f\n" % xform[1])
        tfw.write("%0.8f\n" % xform[2])
        tfw.write("%0.8f\n" % xform[4])
        tfw.write("%0.8f\n" % xform[5])
        tfw.write("%0.8f\n" % edit1)
        tfw.write("%0.8f\n" % edit2)
        tfw.close()
        update_progress(ci/total_con)

print('Fin')