# Planar_RZP_Nexafs
Image processing for pump-probe measurements. 
- single image processing includes:
    - background substraction methods (if background provided): no back, constant back, referenced back
    - referenced back: statistics can be saved too, reference roi for this method
    - data integration on given data roi
    
- stack image processing includes:
    - referenced px-shift method for jitter-correction between stack members
    - referenced intensity normalization between stack members
    - avg, shift statistics etc.
    - save avg and statistics
    
    
- two stack processing includes:
    - jitter or px shift correction between avg of two different stack of images (eg. pumped vs no not pumped)
    - normalization intensity between avg of two different stacks
    - nexafs calculation (e.g. -log(pumped/notPumped))
    - save data


In generell the routine is written for 32bit .Tiff pictures size: 2048x2052 px
The routine is using ROIS in order to minimize the necessary calculation.
The routine is robust and does not use many evaluation packages (e.g. the correlation function 
for the jitter correction "px-shift" can be as well done via np.correlate or FFT methods, 
here a simple minimum comparison in a 15px range about a given first guess minimum position
does this - and is comparative much faster then correlating over the whole 2048 px for each
stack member. But! it cannot do sub-px shifts - as it needs a distinct minimum 
and can not be used on spectra that are undecided in that point. NEXAFS usually provides
a sharp absorption edge that fullfills the requirements.)

used packages and versions
python 3.7 / 3.8 compatible
matplotlib
lmfit (Gaussfit otherwise not needed)
numpy

help-scripts for agile use: basic_file_app.py, basic_image_app.py (if you
use different image sizes or image endings like ".tif" e.g., you could change this
here)